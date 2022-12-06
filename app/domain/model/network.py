# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Dict, Union
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

    def load(self, interface: "NetworkRepository", file: str):
        return interface.load(self, file)

    def write(self, interface: "NetworkRepository", file: str):
        return interface.write(self, file)

    def balance(self):
        solver = Solver(self)
        solver.run()
        # TODO
        # Vérifier si les mathodes ci-dessous sont nécessaires
        # ou si les valeurs sont mises à jour directement.
        self.nodes = solver.get_nodes_results()
        self.nodes = solver.get_links_results()


class ComplexNetwork(Network):
    """Réseau contenant des postes de détente.

    Ce type de réseau doit être traité comme un
    assemblage de sous réseaux.
    """

    pass
