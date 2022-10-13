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


def test_network_add_edge():
    net = Network()
    edge = Edge(12, 101, 102)
    net.add(edge)


def test_add_edges_from_list():
    net = Network()
    edges = [[1, 2], [3, 4], [5, 6]]
    for i, [n1, n2] in enumerate(edges):
        net.add(Edge(i, n1, n2))

    for i, edge in enumerate(net.edges.values()):
        assert edge.n1 == edges[i][0]
        assert edge.n2 == edges[i][1]
