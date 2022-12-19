import numpy as np
from scipy.sparse import coo_matrix, spdiags, hstack, vstack
from scipy.sparse.linalg import spsolve
from app.domain.model.link import Link


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

    def _link_kc(self, link: Link):
        if link.pressure > 2:
            return 156720 * 10**-6
        else:
            return 75927 * 10**-6

    def _link_res(self, link: Link):
        kelvin_temp = float(self.temperature) + 273.15
        density = float(self.gas_density)
        length = float(link.length)
        diameter = float(link.diameter)
        kc = self._link_kc(link)
        return length * kc * diameter**-4.82 * density * kelvin_temp

    def _link_coeff(self, link: Link) -> float:
        """A11 matrix coefficient used for Hardy Cross method"""
        n = self.headloss_coeff
        val = n * self._link_res(link) * abs(link.flow) ** (n - 1)
        return val

    def _link_dE(self, link: Link) -> float:
        """Headloss correction for Hardy Cross method

        Parameters
        ----------
        link : Link
            Link instance used to compute correction

        Returns
        -------
        float
            correction value used in matrix dE
        """
        n = self.headloss_coeff
        p0 = self.p0
        val = np.sign(link.flow) * self._link_res(link) * abs(link.flow) ** n
        if link.pressure > 2:
            val += (link.n2.pressure + p0) ** 2 - (link.n1.pressure + p0) ** 2
        else:
            val += link.n2.pressure - link.n1.pressure
        return -val

    def _build_a11(self):
        a11 = np.array([self._link_coeff(link) for link in self.net.links.values()])
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
        # Remplissage de -dE
        dE = np.array([self._link_dE(link) for link in self.net.links.values()])

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
