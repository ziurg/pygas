from pyvis.network import Network as PyVisNet
from app.domain.model.network import Network

from app.domain.ports.viewer import ViewerInterface


class VisNetwork(PyVisNet):
    nbLinks = 0

    def __init__(self, net: Network):
        super().__init__(directed=True)
        self.load(net)

    def load(self, net: Network):
        for node in net.nodes.values():
            id = node.id
            press = node.pressure
            flow = node.flow
            if node.is_tank:
                self.add_node(id, label=str(id), title="T", pressure=press, flow=flow)
            elif node.is_customer:
                self.add_node(id, label=str(id), title="G", pressure=press, flow=flow)
            else:
                self.add_node(id, label=str(id), pressure=press, flow=flow)
        for link in net.links.values():
            id = link.id
            n1 = link.n1.id
            n2 = link.n2.id
            press = link.pressure
            flow = link.flow
            self.add_edge(
                id,
                n1,
                n2,
                length=link.length,
                diameter=link.diameter,
                pressure=press,
                flow=flow,
            )

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
            elif title.upper() == "B":
                kwargs["color"] = "green"
                kwargs["size"] = 9
                kwargs["shape"] = "triangle"
            elif title.upper() == "G":
                kwargs["color"] = "#5188C2"
                kwargs["size"] = 5
            else:
                raise KeyError
        except KeyError:
            kwargs["title"] = "0"
            kwargs["color"] = "#000000"
            kwargs["size"] = 1

        kwargs["num"] = len(self.get_nodes()) + 1
        super().add_node(*args, **kwargs)

    def add_edge(self, *args, **kwargs):
        if len(args) > 2:
            kwargs["label"] = str(args[0])
            args = args[1:]
        kwargs["color"] = "gray"
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
