from dataclasses import dataclass, asdict
from app.domain.model.pipe_material import Material
from typing import Optional


@dataclass
class Edge:
    id: int
    n1: int
    n2: int
    length: Optional[float] = 0.0
    diameter: Optional[float] = 0.0
    material: Optional[Material] = None
    active: Optional[bool] = True

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    def to_dict(self) -> dict:
        return asdict(self)
