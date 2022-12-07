from app.domain.model.network import Network
from app.domain.model.node import Node
from app.domain.model.link import Link


def test_node_init_without_parameters():
    node = Node(id=12)
    assert node.id == 12


def test_node_init_with_params():

    params = {
        "x": -0.09998975,
        "y": 51.75436525,
        "z": 101.0,
        "flow": 12.0e3,
        "pressure": 543.2,
    }
    node = Node(id=12, **params)
    assert node.id == 12
    assert node.x == -0.09998975
    assert node.y == 51.75436525
    assert node.z == 101.0
    assert node.flow == 12.0e3
    assert node.pressure == 543.2


def test_link_init_without_parameters():
    edge = Link(id=12, n1=Node(id=3), n2=Node(id=4))
    assert edge.id == 12
    assert edge.n1 == 3
    assert edge.n2 == 4


def test_link_from_dict():
    init_dict = {
        "id": 12,
        "diameter": 50.6,
        "length": 12.3,
        "material": {},
        "active": True,
    }

    edge = Link(n1=Node(id=5), n2=Node(id=4), **init_dict)

    assert edge.id == 12
    assert edge.n1 == 5
    assert edge.n2 == 4
    assert edge.diameter == 50.6
    assert edge.length == 12.3
    assert edge.material == {}
    assert edge.active is True


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
    edge = Link(12, 101, 102)
    net.add(edge)
    assert edge in net


def test_add_edges_from_list():
    net = Network()
    edges = [[1, 2], [3, 4], [5, 6]]
    for i, [n1, n2] in enumerate(edges):
        net.add(Link(i, n1, n2))

    for i, edge in enumerate(net.links.values()):
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
        e = Link(id, id, id * 100)
        net.add(e)
        assert e in net


def test_node_in_link():
    net = Network()

    node1 = Node(id=1)
    node2 = Node(id=2)
    node3 = Node(id=3)
    edge1 = Link(id=1, n1=node1, n2=node2)
    edge2 = Link(id=2, n1=node2, n2=node3)

    net.add(node1)
    net.add(node2)
    net.add(node3)
    net.add(edge1)
    net.add(edge2)

    assert node1 in edge1
    assert 1 in edge1


def test_connected_links():
    net = Network()

    node1 = Node(id=1)
    node2 = Node(id=2)
    node3 = Node(id=3)
    edge1 = Link(id=12, n1=node1, n2=node2)
    edge2 = Link(id=23, n1=node2, n2=node3)

    net.add(node1)
    net.add(node2)
    net.add(node3)
    net.add(edge1)
    net.add(edge2)

    node1_links = [link.id for link in net.connected_links(node1)]
    node2_links = [link.id for link in net.connected_links(node2)]
    node3_links = [link.id for link in net.connected_links(node3)]
    assert sorted(node1_links) == [12]
    assert sorted(node2_links) == [12, 23]
    assert sorted(node3_links) == [23]
