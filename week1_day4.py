# -*- coding: utf-8 -*-
# Week 1 Day 4 — Functions: def, return, args, defaults, *args, **kwargs, type hints

from typing import Optional

# ── 1. Basic function with return ─────────────────────

def classify_npa(npa:float)->str:
    if npa>5.0:
        return "Criical"
    elif npa > 3.0:
        return "Watch"
    else:
        return "healthy"
print(classify_npa(3.8))   # watch
print(classify_npa(6.1))   # critical
print(classify_npa(1.2))   # healthy

# ── 2. Default arguments ──────────────────────────────

def circular_summary(circular_id:str,tier:str="low",pages:int=0)->str:
    return f"ID: {circular_id} | Tier: {tier} | Pages: {pages}"
print(circular_summary("RBI/103"))
print(circular_summary("RBI/104", "high", 36))
print(circular_summary("RBI/105", pages=12))

# ── 3. Loop + function together ───────────────────────

banks = [("HDFC", 1.2), ("Yes Bank", 5.1), ("SBI", 2.8), ("Kotak", 0.9)]

for name,npa in banks:
    status = classify_npa(npa)
    print(f"  {name}: {status}")

# ── 4. Multiple return values ─────────────────────────

def page_stats(pages:list[int])->tuple[float, int, int]:
     avg = sum(pages) / len(pages)
     return avg, max(pages), min(pages)
avg, hi, lo = page_stats([24, 8, 36, 12])
print(f"avg={avg:.1f}  hi={hi}  lo={lo}")

# ── 5. Early return — guard clause ────────────────────
def safe_average(values: list[float]) -> float | None:
    if not values:
        return None
    return sum(values) / len(values)

print(safe_average([1.2, 2.4, 3.6]))   # 2.4
print(safe_average([]))                 # None

# ── 6. *args ──────────────────────────────────────────
def total_exposure(*amounts: float) -> float:
    return sum(amounts)

print(total_exposure(500000, 250000, 750000))   # 1500000.0

# ── 7. **kwargs ───────────────────────────────────────
def log_circular(**metadata) -> None:
    print("Logging circular:")
    for key, val in metadata.items():
        print(f"  {key}: {val}")

log_circular(id="RBI/101", tier="high", pages=24)

# ── 8. *args + **kwargs together ──────────────────────
def summarise(*banks: str, **config) -> None:
    print(f"Banks: {banks}")
    print(f"Config: {config}")
    for bank in banks:
        print(f"  Processing {bank} — limit={config.get('limit', 100)}")

summarise("HDFC", "SBI", "Axis", limit=50, region="West")

# ── 9. Optional return type ───────────────────────────
def find_circular(circulars: list[dict], target_id: str) -> Optional[dict]:
    for c in circulars:
        if c["id"] == target_id:
            return c
    return None
docs = [
    {"id": "RBI/101", "tier": "high",  "pages": 24},
    {"id": "RBI/102", "tier": "low",   "pages": 8},
]

result = find_circular(docs, "RBI/101")
if result:
    print(f"Found: {result['id']} — {result['pages']} pages")

missing = find_circular(docs, "RBI/999")
print(f"Missing: {missing}")

# ── 10. Loan eligibility — putting it all together ────
def loan_eligibility(
    salary: float,
    score: int = 700,
    existing_loans: int = 0
) -> str:
    if score < 650:
        return "rejected — low score"
    if existing_loans > 2:
        return "rejected — too many loans"
    if salary < 30000:
        return "rejected — low salary"
    return "approved"

print(loan_eligibility(50000))
print(loan_eligibility(50000, score=600))
print(loan_eligibility(50000, existing_loans=3))
print(loan_eligibility(25000))