from app.domain.model.link import Link


def test_link_init_without_parameters():
    edge = Link(id=12, n1=3, n2=4)
    assert edge.id == 12
    assert edge.n1 == 3
    assert edge.n2 == 4


def test_link_from_dict():
    init_dict = {
        "id": 12,
        "n1": 5,
        "n2": 4,
        "diameter": 50.6,
        "length": 12.3,
        "material": {},
        "active": True,
    }

    edge = Link(**init_dict)

    assert edge.id == 12
    assert edge.n1 == 5
    assert edge.n2 == 4
    assert edge.diameter == 50.6
    assert edge.length == 12.3
    assert edge.material == {}
    assert edge.active is True
