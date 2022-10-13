# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Optional, Dict, Union
from functools import singledispatchmethod


# from pygas.domain.model.node import Node
from .node import Node
from .edge import Edge


@dataclass
class Network:
    name: Optional[str] = ""
    nodes: Optional[Dict[int, Node]] = None
    edges: Optional[Dict[int, Edge]] = None

    def __post_init__(self):
        self.nodes = {}
        self.edges = {}

    @singledispatchmethod
    def add(self, _: Union[Node, Edge]) -> None:
        raise NotImplementedError("This object type can't be added to the model.")

    @add.register(Node)
    def _(self, n: Node) -> None:
        self.nodes[n.id] = n

    @add.register(Edge)
    def _(self, e: Edge) -> None:
        self.edges[e.id] = e
