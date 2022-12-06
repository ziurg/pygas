from app.domain.model.network import Network, Node, Link


def test_add_node_to_network():
    # Given an empty network
    net = Network()
    # When we add a node by his id
    net.add(Node(id=12))
    # Then the node is included in the network's nodes list
    assert 12 in net.nodes


def test_add_edge_to_network():
    net = Network()
    net.add(Link(id=25, n1=12, n2=35))

    assert 25 in net.links
    assert net.links[25].n1 == 12
    assert net.links[25].n2 == 35


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
