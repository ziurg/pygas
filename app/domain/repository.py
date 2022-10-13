import abc
from model.network import Network
from model.node import Node
from model.edge import Edge


class NetworkRepository:
    @abc.abstractmethod
    def get(networkName: str) -> Network:
        pass

    @abc.abstractmethod
    def save(model: Network) -> None:
        pass

    @abc.abstractmethod
    def find_node(n_id: int) -> Node:
        pass

    @abc.abstractmethod
    def find_edge(e_id: int) -> Edge:
        pass
