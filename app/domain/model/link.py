from dataclasses import dataclass
from .node import Node
from functools import singledispatchmethod


@dataclass
class Link:
    """Link object

    Note
    ----
    Other attributes used for network are :
    length: float
        pipe length in meters
    diameter:float
        pipe diameter in millimeters
    material: Material
        pipe's material
    active: bool
        can be inactive if pipe is disconneted
    """

    def __init__(self, id: int, n1: Node, n2: Node, **kwargs):
        self.id = id
        self.n1 = n1
        self.n2 = n2
        self.flow = 0.0
        self.params = {}
        for k, v in kwargs.items():
            try:
                self.__dict__[k] = v
            except KeyError:
                self.params[k] = v

    def __getattr__(self, attribute):
        try:
            return self.params[attribute]
        except KeyError:
            return self.__dict__[attribute]

    @singledispatchmethod
    def __contains__(self, _) -> bool:
        raise NotImplementedError("This object type is not valid for this method.")

    @__contains__.register(Node)
    def _(self, node: Node) -> bool:
        if self.n1.id == node.id:
            return True
        elif self.n2.id == node.id:
            return True
        else:
            return False

    @__contains__.register(int)
    def _(self, node_id: int) -> bool:
        if self.n1.id == node_id:
            return True
        elif self.n2.id == node_id:
            return True
        else:
            return False

    def up(self) -> int:
        """Return upstream node id

        Returns
        -------
        int
            Node id
        """
        if self.flow >= 0:
            return self.n1
        else:
            return self.n2

    def down(self) -> int:
        """Return downstream node id

        Returns
        -------
        int
            Node id
        """
        if self.flow < 0:
            return self.n1
        else:
            return self.n2

    def get_pressure(self):
        avg_pressure = (self.n1.pressure + self.n2.pressure) / 2.0
        return avg_pressure

    def _kc(self):
        if self.get_pressure() > 2:
            return 156720 * 10**-6
        else:
            return 75927 * 10**-6

    def _res(self, **params):
        kelvin_temp = float(params["temperature"]) + 273.15
        density = float(params["gas_density"])
        length = float(self.length)
        diameter = float(self.diameter)
        return length * self._kc() * diameter**-4.82 * density * kelvin_temp

    def coeff(self, **params) -> float:
        """A11 matrix coefficient used for Hardy Cross method"""
        n = params["headloss_coeff"]
        val = n * self._res(**params) * abs(self.flow) ** (n - 1)
        return val

    def _link_coef(self, link):
        n = self.headloss_coeff
        kelvin_temp = self.temperature + 273.15
        density = self.gas_density
        res = link.length * link.kc * link.diameter**-4.82 * density * kelvin_temp
        coeff = n * res * abs(link.flow) ** (n - 1)
        return coeff
