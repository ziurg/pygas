# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Dict, Union
from functools import singledispatchmethod

if TYPE_CHECKING:
    from app.domain.repository import NetworkRepository

# from pygas.domain.model.node import Node
from .node import Node
from .edge import Edge


@dataclass
class Network:
    name: Optional[str] = ""
    nodes: Optional[Dict[int, Node]] = None
    edges: Optional[Dict[int, Edge]] = None
    params: Optional[Dict] = None

    def __post_init__(self):
        self.nodes = {}
        self.edges = {}
        self.params = {"spatial_system": "EPSG:4326"}

    @singledispatchmethod
    def add(self, _: Union[Node, Edge]) -> None:
        raise NotImplementedError("This object type can't be added to the model.")

    @add.register(Node)
    def _(self, n: Node) -> None:
        self.nodes[n.id] = n

    @add.register(Edge)
    def _(self, e: Edge) -> None:
        self.edges[e.id] = e

    @singledispatchmethod
    def __contains__(self, _) -> bool:
        raise NotImplementedError("This object type is not valid for this method.")

    @__contains__.register(Node)
    def _(self, n: Node) -> bool:
        return n.id in self.nodes

    @__contains__.register(Edge)
    def _(self, e: Edge) -> bool:
        return e.id in self.edges

    def load(self, interface: "NetworkRepository", file: str):
        return interface.load(self, file)

    def write(self, interface: "NetworkRepository", file: str):
        return interface.write(self, file)
