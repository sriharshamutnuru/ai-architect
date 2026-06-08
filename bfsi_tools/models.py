# -*- coding: utf-8 -*-
# bfsi_tools/models.py — data models for BFSI objects

from dataclasses import dataclass, field
from .exceptions import InvalidTierError

VALID_TIERS = ["high", "medium", "low"]


@dataclass
class Circular:
    circular_id: str
    tier: str
    pages: int = 0
    tags: list[str] = field(default_factory=list)

    def __post_init__(self):
        if self.tier not in VALID_TIERS:
            raise InvalidTierError(
                f"'{self.tier}' is not valid. Use: {VALID_TIERS}"
            )
        if self.pages > 20 and self.tier == "low":
            self.tier = "medium"   # auto-upgrade short circulars

    def classify(self) -> str:
        return "priority" if self.tier == "high" else "standard"

    def summary(self) -> str:
        return (f"[{self.tier.upper()}] {self.circular_id} "
                f"({self.pages}p) → {self.classify()}")


@dataclass
class Bank:
    name: str
    npa: float
    branches: int = 0

    def classify(self) -> str:
        if self.npa > 5.0: return "critical"
        if self.npa > 3.0: return "watch"
        return "healthy"

    def summary(self) -> str:
        return (f"{self.name} | NPA {self.npa}% | "
                f"{self.branches:,} branches | {self.classify()}")