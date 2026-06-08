# -*- coding: utf-8 -*-
# Week 2 Day 2 — Dataclasses and type hints

from dataclasses import dataclass, field


# ── 1. Basic @dataclass — no __init__ or __repr__ needed ──
@dataclass
class Bank:
    name: str
    npa: float
    branches: int

hdfc = Bank("HDFC", 1.2, 6800)
sbi  = Bank("SBI", 2.8, 22000)
print(hdfc)               # __repr__ generated for free
print(hdfc.name)
print(hdfc.npa)


# ── 2. Default values ─────────────────────────────────────
@dataclass
class Circular:
    circular_id: str
    tier: str = "low"
    pages: int = 0
    is_active: bool = True

c1 = Circular("RBI/101", "high", 24)
c2 = Circular("RBI/102")            # all defaults used
print(c1)
print(c2)


# ── 3. field() for mutable defaults ──────────────────────
@dataclass
class CircularWithTags:
    circular_id: str
    tags: list[str] = field(default_factory=list)

c1 = CircularWithTags("RBI/101")
c2 = CircularWithTags("RBI/102")
c1.tags.append("kyc")
print(c1.tags)    # ['kyc']
print(c2.tags)    # [] — separate list, not shared


# ── 4. Methods work exactly the same ─────────────────────
@dataclass
class BankWithMethods:
    name: str
    npa: float
    branches: int

    def classify(self) -> str:
        if self.npa > 5.0: return "critical"
        if self.npa > 3.0: return "watch"
        return "healthy"

    def summary(self) -> str:
        return (f"{self.name} | NPA {self.npa}% | "
                f"{self.branches:,} branches | {self.classify()}")

banks = [
    BankWithMethods("HDFC",     1.2, 6800),
    BankWithMethods("Yes Bank", 5.1, 1100),
    BankWithMethods("SBI",      2.8, 22000),
]
for b in banks:
    print(b.summary())


# ── 5. __post_init__ — validation at creation time ────────
@dataclass
class CircularValidated:
    circular_id: str
    pages: int
    tier: str = "low"

    def __post_init__(self):
        if self.pages < 0:
            raise ValueError(f"Pages can't be negative: {self.pages}")
        if self.pages > 20:
            self.tier = "high"    # auto-upgrade

docs = [
    CircularValidated("RBI/101", 36),
    CircularValidated("RBI/102", 8),
    CircularValidated("RBI/103", 24),
]
for d in docs:
    print(f"{d.circular_id}: tier={d.tier}")


# ── 6. frozen=True — immutable config ─────────────────────
@dataclass(frozen=True)
class ModelConfig:
    model: str
    temperature: float
    max_tokens: int

config = ModelConfig("claude-sonnet-4", 0.3, 1024)
print(config)
# config.temperature = 0.9  # uncomment → FrozenInstanceError


# ── 7. Value equality — __eq__ auto-generated ─────────────
@dataclass
class SimpleBank:
    name: str
    npa: float

b1 = SimpleBank("HDFC", 1.2)
b2 = SimpleBank("HDFC", 1.2)
b3 = SimpleBank("SBI",  2.8)
print(f"b1 == b2: {b1 == b2}")   # True  — same values
print(f"b1 == b3: {b1 == b3}")   # False
print(f"b1 is b2: {b1 is b2}")   # False — different objects


# ── 8. Full metadata model — your Week 9 RBI corpus model ─
@dataclass
class CircularMetadata:
    circular_id: str
    section: str
    date: str
    risk_tier: str = "low"
    pages: int = 0
    tags: list[str] = field(default_factory=list)

    def __post_init__(self):
        if self.pages > 20:
            self.risk_tier = "high"

    def classify(self) -> str:
        return "priority" if self.risk_tier == "high" else "standard"

    def summary(self) -> str:
        return (f"[{self.risk_tier.upper()}] {self.circular_id} "
                f"— {self.section} ({self.pages}p) tags={self.tags}")

corpus = [
    CircularMetadata("RBI/101", "KYC",   "2024-01-15",
                     pages=36, tags=["kyc", "compliance"]),
    CircularMetadata("RBI/102", "NBFC",  "2024-02-10", pages=8),
    CircularMetadata("RBI/103", "Fraud", "2024-03-05", pages=24),
]
for doc in corpus:
    print(doc.summary())