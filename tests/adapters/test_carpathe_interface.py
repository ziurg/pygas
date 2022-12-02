from app.adapters.spi.carpathe_repo import CarpatheRepository
from app.domain.model.network import Network


def test_carpathe_load():
    # Given an empty Network and Carpathe files (.noe and .can)
    model = Network()
    rootname = "tests/data/example"
    # When files are loaded
    interface = CarpatheRepository()
    model.load(interface, rootname)
    # Then the network is filled with corresponding informations.
    assert model.nodes[47].x == 359932.940000
    assert model.nodes[47].y == 304077.320000
    assert model.nodes[47].z == 0.000000
    assert model.nodes[47].sector == "secteur BP"
    # assert model.nodes[47].is_tank() == True
    # assert model.nodes[47].pressure == 0.022000
    # assert model.nodes[49].x == 360571.770000
    # assert model.nodes[49].y == 303979.040000
    # assert model.nodes[49].z == 0.000000
    # assert model.nodes[49].is_tank() == True
    # assert model.nodes[49].pressure == 0.022000
    # assert model.nodes[59].x == 360473.490000
    # assert model.nodes[59].y == 304081.420000
    # assert model.nodes[59].z == 0.000000
    # assert model.nodes[59].is_tank() == False
    # assert model.nodes[59].flow == 100.0
    # os.remove(rootname + ".noe")
    # os.remove(rootname + ".can")
