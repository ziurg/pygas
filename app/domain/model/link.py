from dataclasses import dataclass


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

    def __init__(self, id: int, n1: int, n2: int, **kwargs):
        self.id = id
        self.n1 = n1
        self.n2 = n2
        self.params = {}
        for k, v in kwargs.items():
            self.params[k] = v

    def __getattr__(self, attribute):
        return self.params[attribute]
