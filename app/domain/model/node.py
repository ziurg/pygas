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
    pressure: float
        nodal pressure
    flow: float
        flow consumption at the node
    active: bool
        can be inactive in case of special nodes (customer or valve)
    """

    def __init__(self, id, **kwargs):
        self.id = id
        self.pressure = 0.0
        self.flow = 0.0
        self.is_tank = False
        self.is_customer = False
        self.params = {}
        for k, v in kwargs.items():
            try:
                self.__dict__[k] = v
            except KeyError:
                self.params[k] = v

    def __getattr__(self, attribute):
        return self.params[attribute]

    def __eq__(self, other: int):
        return self.id == other
