from ...domain.repository import NetworkRepository
from ...domain.model.network import Network


class CarpatheRepository(NetworkRepository):
    def get(networkName: str) -> Network:
        """TODO
        - Chercher les fichiers .noe et .can contenant le nom
        - Contruire un réseau avec les infos issus des fichiers
        """
        pass

    def save(model: Network) -> None:
        """TODO
        Exporter au format noe can
        """
        pass
