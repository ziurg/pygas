import abc
from app.domain.model.network import Network


class NetworkRepository:
    @abc.abstractmethod
    def load(self, model: Network, file: str) -> Network:
        raise NotImplementedError

    @abc.abstractmethod
    def write(self, model: Network, file: str) -> None:
        raise NotImplementedError
