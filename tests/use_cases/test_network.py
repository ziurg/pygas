from app.domain.model.network import Network
from app.adapters.spi.carpathe_repo import CarpatheRepository


def test_balance_basic_network():
    # Given a network defined in Carpathe format
    net = Network()
    rootname = "pygas/tests/data/example"
    interface = CarpatheRepository()
    net.load(interface, rootname)
    # When we ask to balance network
    net.solve()
    # Then we get correct pressures and flows
    assert 12 in net.nodes


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
