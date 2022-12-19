from app.adapters.api.pyvis_visu import PyvisWiewer
from app.adapters.api.pyvis_visu import VisNetwork


def test_pyvis_init(basic_network):
    net = basic_network
    pyvisnet = VisNetwork(net)
    pyvisnet.viz("network.html")


def test_basic_network_show(basic_network):
    net = basic_network
    viewer = PyvisWiewer()
    net.solve()
    net.show(viewer)
