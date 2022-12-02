from .node import Node


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

    def __sub__(self, other):
        linksSelf = [name for name in self.links.keys()]
        linksOther = [name for name in other.links.keys()]
        nodesSelf = [name for name in self.junctions.keys()]
        nodesOther = [name for name in other.junctions.keys()]

        if len(linksSelf) >= len(linksOther):
            linksDiff = list(set(linksSelf) - set(linksOther))
        else:
            linksDiff = list(set(linksOther) - set(linksSelf))
        if len(nodesSelf) >= len(nodesOther):
            nodesDiff = list(set(nodesSelf) - set(nodesOther))
        else:
            nodesDiff = list(set(nodesOther) - set(nodesSelf))

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
            # if self.id == 2:
            #     logger.debug("####### %s")
            if t.conso == 0:
                logger.debug(
                    "Le secteur %s ne peut pas encore être équilibré, la consommation du poste %s étant nulle."
                    % (self.id, t.name)
                )
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
        for l in links:
            # if l.j1.TYPE TODO : Vérifier l'intéret du test
            l.j1.conso += l.conso / 2
            l.j2.conso += l.conso / 2

    def connected_links(self, jname):
        for lName in self.junc2links[jname]:
            try:
                yield self.links[lName]
            except:
                pass

    def isUpTank(self, j: Node) -> Boolean:
        if j.isTank and j.name in self.upTanks.keys():
            return True
        else:
            return False

    def compute(self, params):
        nbJ = int(self.nbJunctions) - int(self.nbUpTanks)
        nbL = int(self.nbLinks)
        # log(nbJ, nbL)
        temp = float(params["temperature"])

        a11 = np.array([l.A11(temp) for l in self.links.values()])
        self.A11 = spdiags(a11, 0, a11.size, a11.size)

        # Matrice A21
        #  et récupération du débit aux jonctions pour la matrice dQ
        dQ = []
        jID = 0
        row = []
        col = []
        val = []
        # linksNames = [l.name for l in self.links]
        # log([j.name for j in self.junctions if (not j.isTank and j.connected)])
        logger.debug("....Construction A21")
        for j in self.junctions.values():
            # try:
            if not self.isUpTank(j) and j.connected:
                log(j.name)
                for l in self.connected_links(j.name):
                    row.append(jID)
                    col.append(l.id)
                    if l.n1 == j.name:
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

        self.A21 = coo_matrix(
            (val, (row, col)),
            shape=(
                nbJ,
                nbL,
            ),
            dtype=np.int16,
        )

        logger.debug("....Assemblage A11 & A21")
        A1 = hstack((self.A11, self.A21.transpose()))
        A2 = hstack((self.A21, coo_matrix((self.A21.shape[0], self.A21.shape[0]))))
        A = vstack((A1, A2)).tocsc()
        # log(np.round(A.todense(),3))

        logger.debug("....Construction dQ & dE")
        # Remplissage de -dE
        dE = np.array([l.dE(temp) for l in self.links.values()])
        log("dE", dE)
        error = dE.sum()

        # Remplissage de -dQ
        pipeFlow = np.array([l.flow for l in self.links.values()]).transpose()
        log("Q", pipeFlow)
        log("dQ", np.array(dQ))
        log("A21", self.A21.todense())
        dQ = np.array(dQ) - self.A21 * pipeFlow
        log("B2", dQ)
        error += dQ.sum()
        log("error", error)

        B = np.concatenate([dE, dQ]).transpose()

        logger.debug("start resolution")
        A.astype(np.float32)
        B.astype(np.float32)
        # log(A.getnnz())

        # B.astype(np.dtype("float32"))
        X = spsolve(A, B)

        logger.debug("....Updating values")
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
            # logger.debug('Réservoir %s mis à jour. Débit : %0.2f'%(t.name,t.flow))

        return error

    @timeit
    def solve(self, params):
        logger.debug("Equilibrage du secteur %s" % (self.id))
        self._update()
        error = 1
        err_prec = 10
        while (error > 1e-4) and (abs(err_prec - error) > 1):
            err_prec = error
            error = self.compute(params)
            # assert np.isnan(error), "Non convergé"
            if np.isnan(error):
                logger.error("NON CONVERGE !!!")
                return 666

        msg = "Secteur %s équilibré.\n" % (self.id)
        for t in self.upTanks.values():
            msg += "\t\t\tRéservoir %s mis à jour. Débit : %0.2e\n" % (t.name, t.conso)
        logger.debug(msg)
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

    @timeit
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
