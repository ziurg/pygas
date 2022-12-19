from pyvis.network import Network as PyVisNet
from app.domain.model.network import Network

from app.domain.ports.viewer import ViewerInterface


class VisNetwork(PyVisNet):
    nbLinks = 0

    def __init__(self, net: Network):
        super().__init__()
        self.load(net)

    def load(self, net: Network):
        for node in net.nodes.values():
            id = node.id
            if node.is_tank:
                self.add_node(id, label=str(id), title="T", pressure=node.pressure)
            elif node.is_customer:
                self.add_node(id, label=str(id), title="G", flow=node.flow)
            else:
                self.add_node(id, label=str(id))
        for link in net.links.values():
            id = link.id
            n1 = link.n1.id
            n2 = link.n2.id
            self.add_edge(id, n1, n2, longueur=link.length, diametre=link.diameter)

    def get_edge(self, label):
        return [e for e in self.get_edges() if str(e["label"]) == str(label)][0]

    def get_node(self, label):
        return super().get_node(int(label))

    def reverse_edge(self, label):
        e = self.get_edge(label)
        if e["arrows"] == "to":
            e["arrows"] = "from"
        else:
            e["arrows"] = "to"

    def add_node(self, *args, **kwargs):
        try:
            title = kwargs["title"]
            if title.upper() in ["U", "T", "S"]:
                kwargs["color"] = "#E53E18"
                kwargs["size"] = 9
                kwargs["shape"] = "triangle"
                kwargs["flow"] = 0.0
            elif title.upper() == "B":
                kwargs["color"] = "green"
                kwargs["size"] = 9
                kwargs["shape"] = "triangle"
                kwargs["pressure"] = 0.001
            elif title.upper() == "G":
                kwargs["color"] = "#5188C2"
                kwargs["size"] = 5
                kwargs["pressure"] = 0.001
            else:
                raise KeyError
        except KeyError:
            kwargs["title"] = "0"
            kwargs["color"] = "#000000"
            kwargs["size"] = 1
            kwargs["pressure"] = 0.001

        try:
            _ = kwargs["flow"]
        except KeyError:
            kwargs["flow"] = 0.0

        kwargs["num"] = len(self.get_nodes()) + 1
        super().add_node(*args, **kwargs)

    def add_edge(self, *args, **kwargs):
        if len(args) > 2:
            kwargs["label"] = str(args[0])
            args = args[1:]
        kwargs["color"] = "gray"
        kwargs["flow"] = 0.01
        self.nbLinks += 1
        kwargs["num"] = self.nbLinks
        super().add_edge(*args, **kwargs)

    def viz(self, name):
        for e in self.get_edges():
            if float(e["flow"]) < 0.0:
                e["flow"] = -e["flow"]
                self.reverse_edge(
                    e["label"]
                )  # orientation automatique en fonction du débit
            e["label"] += "\n(%.1f Nm3/h)" % abs(e["flow"])
        for j in (self.get_node(j) for j in self.get_nodes()):
            if float(j["pressure"]) < 1.0:
                j["label"] += "\n(%.1f mPa)" % (j["pressure"] * 1000.0)
            else:
                j["label"] += "\n(%.1f Pa)" % j["pressure"]

        self.toggle_physics(False)
        self.show(name, local=False)


class PyvisWiewer(ViewerInterface):
    model: VisNetwork = None

    def __init__(self, name: str = "net.html"):
        super().__init__()
        self.name = name

    def show(self, net: Network) -> None:
        self.model = VisNetwork(net)
        self.model.viz(self.name)
