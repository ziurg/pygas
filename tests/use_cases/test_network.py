from app.domain.model.network import Network
from app.domain.model.solver import Solver
from app.adapters.spi.carpathe_repo import CarpatheRepository


def test_create_basic_network(basic_network):
    net = basic_network

    assert 47 in net.nodes
    assert net.nodes[49].is_tank == True
    assert net.links[60].length == 50
    assert net.nb_tanks == 2
    assert net.nb_nodes == 6
    assert net.nb_links == 6


def test_create_a11_matrix(basic_network):
    net = basic_network
    net.solve()
    # assert net.nodes[47].flow == 4
    # assert net.nodes[49].flow == 4
    assert net.nodes[51].pressure == 4
    assert net.nodes[53].pressure == 4
    assert net.nodes[56].pressure == 4
    assert net.nodes[59].pressure == 4
    assert net.links[55].flow == 4
    assert net.links[57].flow == 4
    assert net.links[60].flow == 4
    assert net.links[58].flow == 4
    assert net.links[54].flow == 4
    assert net.links[52].flow == 4

def test_balance_basic_network():
    # Given a basic network (only pipes and junctions)
    net = Network()
    rootname = "pygas/tests/data/example"
    interface = CarpatheRepository()
    net.load(interface, rootname)
    # When we ask to balance network
    # net.solve()
    # Then we get correct pressures and flows
    # assert False  # TODO


# def test_balance_complex_network():
# # Given a complex network (with valves, sub-networks, ...)
# net = Network()
# rootname = "pygas/tests/data/complex_example"
# interface = CarpatheRepository()
# net.load(interface, rootname)
# # When we ask to balance network
# net.solve()
# # Then we get correct pressures and flows
# assert False  # TODO

# Construire un réseau depuis un fichier json

# Construire un réseau depuis des fichiers noe et can (Carpathe)

# Equilibrer le reseau

# Calculer les proportions de chaque gaz (réseau avec 2 gaz)

# Récupérer les valeurs de pression aux noeuds

# Récupérer les valeurs de débit dans une canalisation

# Récupérer les valeur en un noeud précis

# Fermer une vanne

# Ouvrir une vanne

# Switcher etat vanne
