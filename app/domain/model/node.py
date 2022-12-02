# -*- coding: utf-8 -*-
from dataclasses import dataclass


@dataclass
class Node:
    """Node object

    Note
    ----
    Other attributes used for network are :
    label: str
        name of the node
    x: float
        x coordinate of the node
    y: float
        y coordinate of the node
    z: float
        z coordinate of the node
    flow: float
        flow consumption at the node
    pressure: float
        nodal pressure
    active: bool
        can be inactive in case of special nodes (customer or valve)
    """

    def __init__(self, id, **kwargs):
        self.id = id
        self.params = {}
        for k, v in kwargs.items():
            self.params[k] = v

    def __getattr__(self, attribute):
        return self.params[attribute]
