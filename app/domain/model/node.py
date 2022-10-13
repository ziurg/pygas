# -*- coding: utf-8 -*-
from typing import Optional
from dataclasses import dataclass, asdict


@dataclass
class Node:
    id: int
    label: Optional[str] = ""
    x: Optional[float] = None
    y: Optional[float] = None
    z: Optional[float] = None
    flow: Optional[float] = 0.0
    pressure: Optional[float] = 0.0
    active: Optional[bool] = True

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    def to_dict(self) -> dict:
        return asdict(self)
