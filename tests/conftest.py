import pytest
from app.domain.model.network import Network, Node, Link


@pytest.fixture()
def basic_network():
    net = Network()
    net.add(Node(47, fixed_pressure=0.022))
    net.add(Node(49, fixed_pressure=0.022))
    net.add(Node(59, fixed_flow=300))
    net.add_nodes([51, 53, 56])

    net.add(Link(55, net.nodes[53], net.nodes[47], length=140.0, diameter=107.1))
    net.add(Link(57, net.nodes[53], net.nodes[56], length=350.0, diameter=107.1))
    net.add(Link(60, net.nodes[56], net.nodes[59], length=50.0, diameter=107.1))
    net.add(Link(58, net.nodes[51], net.nodes[56], length=200.0, diameter=107.1))
    net.add(Link(54, net.nodes[51], net.nodes[53], length=350.0, diameter=107.1))
    net.add(Link(52, net.nodes[49], net.nodes[51], length=200.0, diameter=107.1))
    return net
