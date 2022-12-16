import numpy as np
from scipy.sparse import coo_matrix, spdiags, hstack, vstack
from scipy.sparse.linalg import spsolve


class Solver:
    def __init__(self, net, **kwargs):
        self.net = net  # ? .copy()
        self.p0 = 1.013e-3
        self.precision = 1e-4
        self.temperature = 25.0
        self.headloss_coeff = 1.82
        self.gas_density = 0.61
        self.convergence = []
        self.params = {}
        for key, value in kwargs.items():
            try:
                self.__dict__[key] = value
            except KeyError:
                self.params[key] = value

    def __getattr__(self, attribute):
        return self.params[attribute]

    def _init_values(self):
        """
        Initialize values to non zeros,
        and add index to links
        """
        for node in self.net.nodes.values():
            node.pressure = 0.001
        for i, link in enumerate(self.net.links.values()):
            link.flow = 0.001
            link.index = i

    def _build_a11(self):
        params = {**self.__dict__, **self.params}
        a11 = np.array([link.coeff(**params) for link in self.net.links.values()])
        self.A11 = spdiags(a11, 0, a11.size, a11.size)

    def _build_a21(self):
        nb_rows = self.net.nb_nodes - self.net.nb_tanks
        nb_columns = self.net.nb_links

        # Matrice A21
        #  et récupération du débit aux jonctions pour la matrice dQ
        dQ = []
        node_row = 0
        row = []
        col = []
        val = []
        nodes = (node for node in self.net.nodes.values() if not node.is_tank)
        for node_row, node in enumerate(nodes):
            for link in self.net.connected_links(node):
                row.append(node_row)
                col.append(link.index)
                if link.n1 == node:
                    val.append(-1)
                else:
                    val.append(1)
            dQ.append(node.flow)  # Consommation au noeud + débit calculé
            node_row += 1

        self.dQ = np.array(dQ)

        self.A21 = coo_matrix(
            (val, (row, col)),
            shape=(
                nb_rows,
                nb_columns,
            ),
            dtype=np.int16,
        )

    def _build_a_matrix(self):
        self._build_a11()
        self._build_a21()
        A1 = hstack((self.A11, self.A21.transpose()))
        A2 = hstack((self.A21, coo_matrix((self.A21.shape[0], self.A21.shape[0]))))
        A = vstack((A1, A2)).tocsc()
        return A

    def _build_b_matrix(self):
        params = {**self.__dict__, **self.params}
        # Remplissage de -dE
        dE = np.array([link.dE(**params) for link in self.net.links.values()])

        # Remplissage de -dQ
        pipeFlow = np.array([link.flow for link in self.net.links.values()]).transpose()
        dQ = self.dQ - self.A21 * pipeFlow

        B = np.concatenate([dE, dQ]).transpose()
        return B

    def _update_network(self, X):
        """Update network values

        Apply Hardy Cross corrections on pressures
        and flows.

        Parameters
        ----------
        X : ndarray or sparse matrix
            Correction matrix (Hardy Cross method)
        """
        # Update link's flows
        for i, (_, link) in enumerate(self.net.links.items()):
            link.flow += X[i]

        # Update nodes' pressures
        nodes = (node for node in self.net.nodes.values() if not node.is_tank)
        for i, node in enumerate(nodes):
            node.pressure += X[i + len(self.net.links)]

    def solve(self):

        self._init_values()
        A = self._build_a_matrix()
        B = self._build_b_matrix()

        A.astype(np.float32)
        B.astype(np.float32)
        error = B.sum()

        X = spsolve(A, B)

        self._update_network(X)

        return error

    def run(self):
        """Network balancing

        Use Hardy Cross method to iteratively solve for
        flow and pressure drop.

        Parameters
        ----------
        net : Network
            Network with links and junctions
        config : Dict[str, Any]
            dictionnary with necessary parameters, like temperature.

        Returns
        -------
        Network
            Return Network instance with updated flow and pressure values.
        """
        error = 1
        err_prec = 10
        while (error > self.precision) and (abs(err_prec - error) > 1):
            err_prec = error
            error = self.solve()
            self.convergence.append(error)
            if np.isnan(error):
                raise Exception("Sorry, something's wrong !")
        return 0
