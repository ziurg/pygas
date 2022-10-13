from ...domain.repository import NetworkRepository
from ...domain.model.network import Network


class JsonRepository(NetworkRepository):
    def get(networkName: str) -> Network:
        """TODO
        - chercher le fichier avec le nom
        - Contruire un réseau avec les infos contenus dans le(s) json(s)
        """

        pass

    def save(model: Network) -> None:
        pass
