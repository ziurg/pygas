from app.domain.repository import NetworkRepository
from app.domain.model.network import Network, Node


class CarpatheRepository(NetworkRepository):
    def load(self, model: Network, rootname: str) -> Network:
        """Read files in Carpathe format
        - Chercher les fichiers .noe et .can contenant le nom
        - Contruire un réseau avec les infos issus des fichiers
        Args:
            model : Network
                Network instance to complete with noe and can informations
            rootname : str
                name used for .noe and .can files (have to be similar).
            rootname : Optional[str]
                Spatial coordinate system used in files

        Returns:
            FEM: Finite Element Model
        """
        network = model
        network = self._load_noe(network, rootname + ".noe")
        network = self._load_can(network, rootname + ".can")
        return network

    def write(self, model: Network, rootname: str) -> None:
        """Generate network files in Carpathe format

        Parameters
        ----------
        model : Network
             Network instance with all informations
        rootname : str
            name used for .noe and .can files.
        """
        self._write_noe(model, "rootname" + ".noe")
        self._write_can(model, "rootname" + ".can")
        self._write_rnoe(model, "rootname" + ".rnoe")
        self._write_rcan(model, "rootname" + ".rcan")

    def _parse_node(self, line: str) -> Node:
        sline = line.strip().split("\t")
        [name, x, y, z, kind, *_] = sline
        node = Node(int(name))
        node.x = float(x)
        node.y = float(y)
        node.z = float(z)
        # self.Type = self.Type.replace("0.0", "0")
        # if self.Type == "0":  # no relevant node : nothing to do
        #     return
        # self.state = int(sline[5])
        # if self.Type.lower() in ["t","s","u"]:  # Tank node
        #     if self.state == 0:  # active state
        #         self.pressure = float(sline[12])
        #         self.aval = sline[8]
        #     else:  # alike any other node
        #         self.Type = "0"
        #         self.state = 0
        # elif self.Type == "g":  # Customer
        #     self.customer_name = sline[6]
        #     if self.state == 0:  # customer is connected
        #         self.flow += float(sline[9])
        return node

    def _load_noe(self, model: Network, file: str) -> Network:
        with open(file, "r") as f:
            # Mise en forme et suppression lignes vides
            lines = (line.lower() for line in f.readlines() if line.strip())
            #
            #############################################
            # HEADER READING
            #############################################
            noeParamsLoc = {
                "5": "nbNodes",
                "6": "nbTanks",
                "7": "nbLinks",
                "8": "altRef",  # Altitude de référence
                "9": "altMin",  # Altitude minimum
                "10": "altMax",  # Altitude maximum
                "11": "penteMax",  # Pente maximum
                "12": "densite",  # Densité du gaz
                "13": "pc",  # Povoir calorifique supérieur [kWh/m3]
                "14": "temp",  # Température du gaz [°C]
                "15": "deltaP",  # Delta pression [bar]
                "16": "temp2pct",  # Température du risque 2%
                "17": "temp50pct",  # Température du risque 50%
                "18": "tempSeuil",  # Température du seuil de chauffage
                "19": "tempEte",  # Température été
                "20": "nbDegJ",  # Nombre de degrés-jours annuel
            }
            for i, line in enumerate(lines):
                try:
                    paramName = noeParamsLoc[str(i + 1)]
                    model.params[paramName] = float(line)
                except KeyError:
                    pass
                if i == 19:
                    break

            #############################################
            # SECTOR BLOCKS READING
            #############################################
            for i, line in enumerate(lines):
                try:
                    node = self._parse_node(line)
                    model.add(node)
                except (ValueError, IndexError):
                    # On est sur un nom de secteur
                    pass

    def _load_can(self, model: Network, rootname: str) -> Network:
        pass

    def _write_noe(self, model: Network, rootname: str) -> None:
        pass

    def _write_can(self, model: Network, rootname: str) -> None:
        pass

    def _write_rnoe(self, model: Network, rootname: str) -> None:
        pass

    def _write_rcan(self, model: Network, rootname: str) -> None:
        pass
