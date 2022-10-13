# -*- coding: utf-8 -*-
from dataclasses import dataclass, asdict


@dataclass
class Gas:

    name: str
    density: float
    temperature: float

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    def to_dict(self):
        return asdict(self)
