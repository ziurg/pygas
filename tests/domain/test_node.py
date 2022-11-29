from app.domain.model.node import Node


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
    node = Node(id=12, params=params)
    assert node.id == 12
    assert node.x == -0.09998975
    assert node.y == 51.75436525
    assert node.z == 101.0
    assert node.flow == 12.0e3
    assert node.pressure == 543.2
