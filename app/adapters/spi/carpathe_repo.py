from app.domain.repository import NetworkRepository
from app.domain.model.network import Network, Node, Link


class CarpatheRepository(NetworkRepository):
    """Carpathe interface"""

    def __init__(self):
        self.network = None

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
        self.network = model
        self._load_noe(rootname + ".noe")
        self._load_can(rootname + ".can")
        self._sanity_check()
        return self.network

    def write(self, rootname: str) -> None:
        """Generate network files in Carpathe format

        Parameters
        ----------
        model : Network
             Network instance with all informations
        rootname : str
            name used for .noe and .can files.
        """
        self._write_noe(rootname + ".noe")
        self._write_can(rootname + ".can")
        self._write_rnoe(rootname + ".rnoe")
        self._write_rcan(rootname + ".rcan")

    def _sanity_check(self):
        # TODO :
        # Check if null lengths or diameters are used
        # ... ?
        pass

    def _parse_node(self, line: str) -> Node:
        """Create Node instance from Carpathe line.

        Parameters
        ----------
        line : str
            line from .noe file (Carpathe)

        Returns
        -------
        Node
            Node instance filled with line informations
        """
        sline = line.strip().split("\t")
        [id, x, y, z, cat, *_] = sline
        node = Node(int(id))
        node.x = float(x)
        node.y = float(y)
        node.z = float(z)
        node.params["type"] = cat
        if cat.upper() in ["T", "S", "U"]:  # Tank node
            node.params["status"] = int(sline[5])
            node.params["name"] = sline[6]
            node.params["post_id"] = sline[7]
            node.params["downstream_pipe"] = int(sline[8])
            node.params["nb_lines"] = int(sline[9])
            node.params["active_line"] = int(sline[10])
            node.params["setpoint"] = float(sline[12])
            node.params["design_flow"] = float(sline[14])
            node.params["design_pressure"] = float(sline[15])
            node.is_tank = True
        elif cat.upper() == "R":  # Valve
            node.params["status"] = int(sline[5])
            node.params["name"] = sline[6]
        elif cat.upper() == "G":  # Customer
            node.params["status"] = int(sline[5])
            node.params["name"] = sline[6]
            node.params["customer_id"] = sline[7]
            node.params["unloading_sensitivity"] = int(sline[8])
            node.params["conso_risk_2pct"] = float(sline[9])
            node.params["conso_risk_50pct"] = float(sline[10])
            node.params["pressure"] = float(sline[12])
            node.params["usage"] = sline[14]
            node.is_customer = True
            #
            node.params["flow"] = node.params["conso_risk_2pct"]
        return node

    def _parse_link(self, line: str) -> Link:
        """Create Link instance from Carpathe line.

        Parameters
        ----------
        line : str
            line from .can file (Carpathe)

        Returns
        -------
        Link
            Link instance filled with line informations
        """
        values = line.strip().split("\t")
        keys = [
            "id",
            "n1",
            "n2",
            "pressure_index",
            "length",
            "diameter",
            "year",
            "function",
            "headloss_formula",
            "status",
            "2pct_consumption",
            "50pct_consumption",
            "threshold_consumption",
        ]
        params = {k: v for k, v in zip(keys, values)}
        link = Link(**params)
        # Replace node id by Node instance
        link.n1 = self.network.nodes[int(link.n1)]
        link.n2 = self.network.nodes[int(link.n2)]

        return link

    def _load_noe(self, file: str) -> None:
        with open(file, "r") as f:
            # Ignoring empty lines and deleting \n
            lines = (line.strip() for line in f if line.strip())
            #
            #############################################
            # HEADER READING
            #############################################
            noeParamsLoc = {
                "5": "nb_nodes",
                "6": "nb_tanks",
                "7": "nb_links",
                "8": "altitude_ref",  # Altitude de référence
                "9": "altitude_min",  # Altitude minimum
                "10": "altitude_max",  # Altitude maximum
                "11": "max_slope",  # Pente maximum
                "12": "gas_density",  # Densité du gaz
                "13": "heat_of_combustion",  # Pouvoir calorifique supérieur [kWh/m3]
                "14": "gas_temperature",  # Température du gaz [°C]
                "15": "pressure_drop",  # Delta pression [bar]
                "16": "2pct_temperature",  # Température du risque 2%
                "17": "50pct_temperature",  # Température du risque 50%
                "18": "threshold_temperature",  # Température du seuil de chauffage
                "19": "summer_temperature",  # Température été
                "20": "nb_degree_day",  # Nombre de degrés-jours annuel
            }
            for i, line in enumerate(lines):
                try:
                    paramName = noeParamsLoc[str(i + 1)]
                    self.network.params[paramName] = float(line)
                except KeyError:  # Not relevant parameter
                    pass
                if i == 19:
                    break

            #############################################
            # SECTOR BLOCKS READING
            #############################################
            sector = ""
            for i, line in enumerate(lines):
                try:
                    node = self._parse_node(line)
                    node.params["sector"] = sector
                    self.network.add(node)
                except (ValueError, IndexError):
                    sector = line

    def _load_can(self, file: str) -> None:
        with open(file, "r") as f:
            # Ignoring empty lines and deleting \n
            lines = (line.strip() for line in f if line.strip())
            #
            #############################################
            # HEADER READING
            #############################################
            for i, line in enumerate(lines):
                # Skipping (no relevant informations)
                if i == 7:
                    break
            #############################################
            # SECTOR BLOCKS READING
            #############################################
            sector = ""
            for i, line in enumerate(lines):
                try:
                    link = self._parse_link(line)
                    link.params["sector"] = sector
                    self.network.add(link)
                except (TypeError):
                    sector = line

    def _write_noe(self, rootname: str) -> None:
        pass

    def _write_can(self, rootname: str) -> None:
        pass

    def _write_rnoe(self, rootname: str) -> None:
        pass

    def _write_rcan(self, rootname: str) -> None:
        pass
