# -*- coding: utf-8 -*-
# Week 2 Day 1 — Classes: __init__, self, methods, __repr__

# ── 1. Basic class + __init__ ─────────────────────────


class Bank:
    def __init__(self, name: str, npa: float):
        self.name = name
        self.npa = npa

    def classify(self) -> str:
        if self.npa > 5.0:
            return "critical"
        elif self.npa > 3.0:
            return "watch"
        return "healthy"

    def __repr__(self) -> str:
        return f"Bank(name='{self.name}', npa={self.npa})"

hdfc = Bank("HDFC", 1.2)
sbi  = Bank("SBI", 2.8)
yes  = Bank("Yes Bank", 5.1)

print(hdfc)
print(hdfc.classify())
print(yes.classify())

banks = [hdfc, sbi, yes]
print(banks)

# ── 2. Loop + method together ─────────────────────────
for bank in banks:
    print(f"  {bank.name}: {bank.classify()}")

# ── 3. Class with multiple methods ────────────────────
class Circular:
    def __init__(self, circular_id: str, tier: str, pages: int):
        self.circular_id = circular_id
        self.tier = tier
        self.pages = pages

    def is_long(self) -> bool:
        return self.pages > 20

    def describe(self) -> str:
        size = "long" if self.is_long() else "short"
        return f"{self.circular_id} is a {size} circular ({self.pages} pages)"

    def __repr__(self) -> str:
        return f"Circular(id='{self.circular_id}', tier='{self.tier}', pages={self.pages})"

docs = [
    Circular("RBI/101", "high", 24),
    Circular("RBI/102", "low",  8),
    Circular("RBI/103", "high", 36),
]

for doc in docs:
    print(doc.describe())

# ── 4. Object state — tracking across method calls ────
class LoanAccount:
    def __init__(self, holder: str, principal: float, rate: float):
        self.holder = holder
        self.principal = principal
        self.rate = rate

    def annual_interest(self) -> float:
        return self.principal * self.rate / 100

    def monthly_interest(self) -> float:
        return self.annual_interest() / 12

    def summary(self) -> str:
        return (f"{self.holder}: ₹{self.principal:,} @ {self.rate}% "
                f"= ₹{self.annual_interest():,.0f}/yr "
                f"(₹{self.monthly_interest():,.0f}/mo)")

    def __repr__(self) -> str:
        return f"LoanAccount(holder='{self.holder}', principal={self.principal})"

loan = LoanAccount("Arjun", 500000, 8.5)
print(loan.summary())
print(loan.monthly_interest())

# ── 5. APIClient — the shape you'll use in Week 5 ─────
class APIClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.call_count = 0

    def get(self, endpoint: str) -> dict:
        self.call_count += 1
        return {
            "endpoint": endpoint,
            "status": 200,
            "call_num": self.call_count
        }

    def reset(self) -> None:
        self.call_count = 0

    def __repr__(self) -> str:
        return f"APIClient(url='{self.base_url}', calls={self.call_count})"

client = APIClient("https://api.rbi.gov.in", "secret-key")
print(client.get("/circulars"))
print(client.get("/notifications"))
print(client.get("/master-directions"))
print(client)
client.reset()
print(f"After reset: {client}")