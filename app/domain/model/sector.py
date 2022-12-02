from .node import Node
import numpy as np
from scipy.sparse import coo_matrix, spdiags, hstack, vstack
from scipy.sparse.linalg import spsolve
import geojson


class Secteur(object):
    def __init__(self, id=0):
        self.id = id
        self.params = {}
        self.junctions = {}
        self.links = {}
        self.nbJunctions = 0
        self.nbLinks = 0
        self.junc2links = {}
        self.maxP = 0.0
        self.upTanks = {}
        self.downTanks = {}
        self.nbTanks = 0
        self.nbUpTanks = None
        self.nbDownTanks = None
        self.A11 = None
        self.A21 = None
        # Paramètres de l'algorithme
        self._iterMax = 200

    def checkTanks(self):
        """
        On identifie les postes avals pour pouvoir les traiter
        comme des clients, du point de vue de l'équilibrage de
        ce secteur.
        """
        self.nbUpTanks = 0
        self.nbDownTanks = 0
        links_name = [name for name in self.links.keys()]
        for name, t in self.junctions.items():
            if t.aval:
                if t.aval in links_name:
                    # Si le tronçon aval appartient au secteur,
                    # alors c'est un poste d'alimentation de ce secteur
                    self.upTanks[name] = t
                    self.nbUpTanks += 1
                else:
                    self.downTanks[name] = t
                    self.nbDownTanks += 1
        self.nbTanks = self.nbUpTanks + self.nbDownTanks

    def balanceable(self):
        """
        Un réseau peut être équilibré si on connait la
        consommation de tous les postes en aval.
        """
        for t in self.downTanks.values():
            if t.conso == 0:
                return False
        return True

    def _update(self):

        self.nbJunctions = len([j for j in self.junctions])
        self.nbTanks = len([i for i, j in self.junctions.items() if j.isTank])
        self.nbLinks = len([i for i, l in self.links.items() if l.state == "0"])
        # on lie les instances de noeuds aux canalisations
        # TODO : Je ne sais plus pourquoi on fait ça...
        for i, (name, l) in enumerate(self.links.items()):
            l.id = i
            l.id2name[i] = name
            l.j1 = self.junctions[l.n1]
            l.j1.connected = True
            l.j2 = self.junctions[l.n2]
            l.j2.connected = True
        self.nbJunctions = len([i for i, j in self.junctions.items() if j.connected])
        # Répartition de la consommation le long des canalisations aux noeuds.
        links = (c for c in self.links.values() if c.conso != 0.0)
        for link in links:
            # if l.j1.TYPE TODO : Vérifier l'intéret du test
            link.j1.conso += link.conso / 2
            link.j2.conso += link.conso / 2

    def connected_links(self, jname):
        for lName in self.junc2links[jname]:
            try:
                yield self.links[lName]
            except KeyError:
                pass

    def isUpTank(self, j: Node) -> bool:
        if j.isTank and j.name in self.upTanks.keys():
            return True
        else:
            return False

    def _build_a11(self, params):
        temp = float(params["temperature"])
        a11 = np.array([link.A11(temp) for link in self.links.values()])
        self.A11 = spdiags(a11, 0, a11.size, a11.size)

    def _build_a21(self):
        nbJ = int(self.nbJunctions) - int(self.nbUpTanks)
        nbL = int(self.nbLinks)

        # Matrice A21
        #  et récupération du débit aux jonctions pour la matrice dQ
        dQ = []
        jID = 0
        row = []
        col = []
        val = []
        # linksNames = [l.name for l in self.links]
        # log([j.name for j in self.junctions if (not j.isTank and j.connected)])
        for j in self.junctions.values():
            # try:
            if not self.isUpTank(j) and j.connected:
                for link in self.connected_links(j.name):
                    row.append(jID)
                    col.append(link.id)
                    if link.n1 == j.name:
                        val.append(-1)
                    else:
                        val.append(1)
                # dQ.append(j.conso + j.flow)  # Consommation au noeud + débit calculé
                dQ.append(j.conso)  # Consommation au noeud + débit calculé
                # log(j.conso, j.flow, dQ)
                jID += 1
            # except KeyError:
            #     # noeud déconnecté : self.junc2links[j.name]
            #     # TODO : à traiter autrement
            #     dQ.append(j.conso + j.flow)

        self.dQ = np.array(dQ)

        self.A21 = coo_matrix(
            (val, (row, col)),
            shape=(
                nbJ,
                nbL,
            ),
            dtype=np.int16,
        )

    def _build_a_matrix(self, params):
        self._build_a11(params)
        self._build_a21(params)
        A1 = hstack((self.A11, self.A21.transpose()))
        A2 = hstack((self.A21, coo_matrix((self.A21.shape[0], self.A21.shape[0]))))
        A = vstack((A1, A2)).tocsc()
        return A

    def _build_b_matrix(self, params):
        temp = float(params["temperature"])
        # Remplissage de -dE
        dE = np.array([link.dE(temp) for link in self.links.values()])

        # Remplissage de -dQ
        pipeFlow = np.array([link.flow for link in self.links.values()]).transpose()
        dQ = self.dQ - self.A21 * pipeFlow

        B = np.concatenate([dE, dQ]).transpose()
        return B

    def _update_network(self, X):
        # Mise à jour du réseau
        # TODO : extraire les pressions et debits pour
        # permettre une de travailler sur les matrices
        # au cours des itérations. Permet de ne faire la
        # boucle de mise à jour qu'à la fin de la convergence
        for i, (_, l) in enumerate(self.links.items()):
            l.flow += X[i]

        # Mise à jour des pressions aux jonctions
        juncs = (
            j for j in self.junctions.values() if (not self.isUpTank(j) and j.connected)
        )
        for i, j in enumerate(juncs):
            j.pressure += X[i + len(self.links)]

        # Mise à jour des débit aux réservoirs en fonction des débits des canalisations connectées
        for n, t in self.upTanks.items():
            t.conso = 0.0
            for linkName in self.junc2links[t.name]:
                try:
                    t.conso += abs(self.links[linkName].flow)
                except KeyError:
                    # Dans ce cas la canalisation appartient au secteur amont
                    # Il ne faut donc pas prendre en compte son débit.
                    pass
            self.junctions[n].conso = t.conso

    def compute(self, params):

        A = self._build_a_matrix(params)
        B = self._build_b_matrix(params)

        A.astype(np.float32)
        B.astype(np.float32)
        error = B.sum()

        X = spsolve(A, B)

        self._update_network(X)

        return error

    def solve(self, params):
        self._update()
        error = 1
        err_prec = 10
        while (error > 1e-4) and (abs(err_prec - error) > 1):
            err_prec = error
            error = self.compute(params)
            # assert np.isnan(error), "Non convergé"
            if np.isnan(error):
                return 666

        msg = "Secteur %s équilibré.\n" % (self.id)
        for t in self.upTanks.values():
            msg += "\t\t\tRéservoir %s mis à jour. Débit : %0.2e\n" % (t.name, t.conso)
        return 0

    @property
    def length(self):
        """
        Renvoi la longueur cumulée des canalisations
        """
        val = 0.0
        for name, link in self.links.items():
            val += link.length
        return val

    ##############################
    # GRAPHICS METHODS
    ##############################
    @property
    def __geo_interface__(self):
        return {
            "type": "FeatureCollection",
            "features": [o for o in self.obj2export],
        }

    def export_geojson(self, file, obj):

        if isinstance(obj, dict):
            self.obj2export = obj.values()
        else:
            self.obj2export = obj
        with open(file, "w") as filehandle:
            filehandle.write(geojson.dumps(self))

    def __repr__(self):
        if self.maxP >= 1.0:
            level = "%0.1f  bar" % (self.maxP)
        else:
            level = "%0.1f  mbar" % (self.maxP * 1000)
        msg = 'Secteur "%s"\n' % (self.id)
        msg += "\tniveau de pression : %s\n" % (level)
        msg += "\t%i jonctions\n" % (int(self.nbJunctions))
        msg += "\t%i canalisations\n" % (int(self.nbLinks))
        msg += "\t%i réservoirs amonts\n" % (int(self.nbUpTanks))
        msg += "\t%i réservoirs aval\n" % (int(self.nbDownTanks))
        return msg
