from app.domain.model.edge import Edge


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

    edge = Edge(**init_dict)

    assert edge.id == 12
    assert edge.n1 == 5
    assert edge.n2 == 4


def test_edge_with_other_arguments():
    init_dict = {
        "id": 12,
        "n1": 5,
        "n2": 4
    }
    other_arg = {
        "diameter": 50.6,
        "length": 12.3,
        "material": {},
        "active": True,
    }

    edge = Edge(**init_dict, params=other_arg)

    assert edge.id == 12
    assert edge.n1 == 5
    assert edge.n2 == 4
    assert edge.diameter == 50.6
    assert edge.length == 12.3
    assert edge.material == {}
    assert edge.active is True
