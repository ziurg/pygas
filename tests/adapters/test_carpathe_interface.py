from app.adapters.spi.carpathe_repo import CarpatheRepository
from app.domain.model.network import Network


def test_carpathe_load():
    # Given an empty Network and Carpathe files (.noe and .can)
    model = Network()
    rootname = "pygas/tests/data/example"
    # When files are loaded
    interface = CarpatheRepository()
    model.load(interface, rootname)
    # Then the network is filled with corresponding informations.
    assert model.nodes[47].x == 359932.940000
    assert model.nodes[47].y == 304077.320000
    assert model.nodes[47].z == 0.000000
    assert model.nodes[47].sector == "secteur BP"
    assert model.nodes[47].is_tank is True
    assert model.nodes[47].setpoint == 0.022000
    assert model.nodes[49].x == 360571.770000
    assert model.nodes[49].y == 303979.040000
    assert model.nodes[49].z == 0.000000
    assert model.nodes[49].is_tank is True
    assert model.nodes[49].setpoint == 0.022000
    assert model.nodes[59].x == 360473.490000
    assert model.nodes[59].y == 304081.420000
    assert model.nodes[59].z == 0.000000
    assert model.nodes[59].is_customer is True
    assert model.nodes[59].conso_risk_2pct == 150.0
    assert model.nodes[59].conso_risk_50pct == 100.0
    assert len(model.nodes) == 6
    assert len(model.links) == 6
    # os.remove(rootname + ".noe")
    # os.remove(rootname + ".can")


# def test_carpathe_load_2():
#     # Given an empty Network and Carpathe files (.noe and .can)
#     model = Network()
#     rootname = "tests/data/RGE_29_11_2022"
#     # When files are loaded
#     interface = CarpatheRepository()
#     model.load(interface, rootname)
#     assert len(model.nodes) == 403164
#     assert len(model.links) == 403990
