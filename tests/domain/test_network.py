from app.domain.model.network import Network
from app.domain.model.node import Node
from app.domain.model.edge import Edge


def test_network_init_without_any_parameter():
    Network()


def test_network_init():
    net = Network(name="BigNet")
    assert net.name == "BigNet"


def test_network_add_node():
    net = Network()
    node = Node(12)
    net.add(node)
    assert node in net


def test_network_add_edge():
    net = Network()
    edge = Edge(12, 101, 102)
    net.add(edge)
    assert edge in net


def test_add_edges_from_list():
    net = Network()
    edges = [[1, 2], [3, 4], [5, 6]]
    for i, [n1, n2] in enumerate(edges):
        net.add(Edge(i, n1, n2))

    for i, edge in enumerate(net.edges.values()):
        assert edge.n1 == edges[i][0]
        assert edge.n2 == edges[i][1]


def test_network_contain_node():
    net = Network()
    nids = [i for i in range(100)]
    for nid in nids:
        n = Node(nid)
        net.add(n)
        assert n in net


def test_network_contain_edge():
    net = Network()
    nids = [i for i in range(100)]
    for id in nids:
        e = Edge(id, id, id * 100)
        net.add(e)
        assert e in net
