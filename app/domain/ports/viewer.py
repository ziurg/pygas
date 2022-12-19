import abc

from app.domain.model.network import Network


class ViewerInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def show(self, net: Network) -> None:
        raise NotImplementedError
