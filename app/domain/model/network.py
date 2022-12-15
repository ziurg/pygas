# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Dict, List, Union, Generator
from functools import singledispatchmethod

if TYPE_CHECKING:
    from app.domain.repository import NetworkRepository

# from pygas.domain.model.node import Node
from .node import Node
from .link import Link
from .solver import Solver


@dataclass
class Network:
    name: Optional[str] = ""
    nodes: Optional[Dict[int, Node]] = None
    links: Optional[Dict[int, Link]] = None
    params: Optional[Dict] = None

    def __post_init__(self):
        self.nodes = {}
        self.links = {}
        self.params = {"spatial_system": "EPSG:4326"}

    @singledispatchmethod
    def add(self, _: Union[Node, Link]) -> None:
        raise NotImplementedError("This object type can't be added to the model.")

    @add.register(Node)
    def _(self, n: Node) -> None:
        self.nodes[n.id] = n

    @add.register(Link)
    def _(self, e: Link) -> None:
        self.links[e.id] = e

    @singledispatchmethod
    def __contains__(self, _) -> bool:
        raise NotImplementedError("This object type is not valid for this method.")

    @__contains__.register(Node)
    def _(self, n: Node) -> bool:
        return n.id in self.nodes

    @__contains__.register(Link)
    def _(self, e: Link) -> bool:
        return e.id in self.links

    def add_nodes(self, nodes: List[int]) -> None:
        for node_id in nodes:
            if not node_id in self.nodes:
                self.nodes[node_id] = Node(node_id)

    @property
    def nb_nodes(self):
        return len(self.nodes)

    @property
    def nb_links(self):
        return len(self.links)

    @property
    def nb_tanks(self):
        return len([node for node in self.nodes.values() if node.is_tank])

    def connected_links(self, node: Node) -> Generator[Link, None, None]:
        """Get all links connected to the given node.

        Parameters
        ----------
        node : Node
            node instance

        Yields
        ------
        Generator[Link, None, None]
            Link instances connected to the node
        """
        for link in self.links.values():
            if node in link:
                yield link

    def load(self, interface: "NetworkRepository", file: str):
        return interface.load(self, file)

    def write(self, interface: "NetworkRepository", file: str):
        return interface.write(self, file)

    def solve(self):
        solver = Solver(self)
        solver.run()


class ComplexNetwork(Network):
    """Réseau contenant des postes de détente.

    Ce type de réseau doit être traité comme un
    assemblage de sous réseaux.
    """

    pass
