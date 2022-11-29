from dataclasses import dataclass, field


@dataclass
class Edge:
    """Edge object

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

    id: int
    n1: int
    n2: int
    params: field(default_factory=dict) = None

    def __getattr__(self, attribute):
        return self.params[attribute]
