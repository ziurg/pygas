from app.domain.model.edge import Edge
from app.domain.model.pipe_material import Material


def test_edge_init_without_parameters():
    edge = Edge(id=12, n1=3, n2=4)
    assert edge.id == 12
    assert edge.n1 == 3
    assert edge.n2 == 4


def test_edge_from_dict():
    init_dict = {
        "id": 12,
        "n1": 5,
        "n2": 4,
    }

    edge = Edge.from_dict(init_dict)

    assert edge.id == 12
    assert edge.n1 == 5
    assert edge.n2 == 4


def test_edge_to_dict():
    init_dict = {
        "id": 12,
        "n1": 5,
        "n2": 4,
        "diameter": 50.6,
        "length": 12.3,
        "material": {},
        "active": True,
    }

    edge = Edge.from_dict(init_dict)

    assert edge.to_dict() == init_dict
