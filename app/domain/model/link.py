from dataclasses import dataclass
from .node import Node


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
            self.params[k] = v

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

    @property
    def pressure(self):
        avg_pressure = (self.n1.pressure + self.n2.pressure) / 2.0
        return avg_pressure

    @property
    def _kc(self):
        if self.pressure > 2:
            return 156720 * 10**-6
        else:
            return 75927 * 10**-6

    def _res(self, **params):
        kelvin_temp = params["temperature"] + 273.15
        density = params["gas_density"]
        return self.length * self._kc * self.diameter**-4.82 * density * kelvin_temp

    def coeff(self, **params) -> float:
        """A11 matrix coefficient used for Hardy Cross method"""
        n = params["headloss_coeff"]
        val = n * self._res(params) * abs(self.flow) ** (n - 1)
        return val

    def _link_coef(self, link):
        n = self.headloss_coeff
        kelvin_temp = self.temperature + 273.15
        density = self.gas_density
        res = link.length * link.kc * link.diameter**-4.82 * density * kelvin_temp
        coeff = n * res * abs(link.flow) ** (n - 1)
        return coeff

    def __getattr__(self, attribute):
        return self.params[attribute]
