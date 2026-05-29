# -*- coding: utf-8 -*-
# Week 1 Day 3 — Control flow: if/else, for, while, range, break, continue

# ── 1. if / elif / else ───────────────────────────────
npa = 3.8
if npa>5.0:
    print("Critical — RBI intervention likely")
elif npa>3.0:
    print("Watch list — review required")
else:
    print("Healthy — within RBI threshold")

tier = "high"
is_active = True

if tier == "high" and is_active:
    print("Priority review needed")
elif tier=="low" and not is_active:
    print("Can defer")
# ── 2. for loop over a list ───────────────────────────

banks=["HDFC", "ICICI", "SBI", "Axis"]

for bank in banks:
    print(f"Processing: {bank}")
# ── 3. for loop over a list of dicts ─────────────────
circulars = [
    {"id": "RBI/101", "tier": "high",  "pages": 24},
    {"id": "RBI/102", "tier": "low",   "pages": 8},
    {"id": "RBI/103", "tier": "high",  "pages": 36},
]

total = 0
for c in circulars:
    if c["tier"]=="high":
        total += c["pages"]
        print(f"  Priority: {c['id']} ({c['pages']} pages)")
print(f"Total high-tier pages: {total}")

# ── 4. range() ────────────────────────────────────────

for i in range(5):
    print(i)
for i in range(1, 6):
    print(i)
for i in range(0, 10, 2):
    print(i)
# ── 5. enumerate() ────────────────────────────────────
for i, bank in enumerate(banks, start=1):
    print(f"  {i}. {bank}")
# ── 6. while loop ─────────────────────────────────────
balance = 10000
withdrawal = 2500
count = 0
while balance >= withdrawal:
    balance -= withdrawal
    count += 1
    print(f"Withdrawal {count}: balance ₹{balance:,}")

print(f"Insufficient funds after {count} withdrawals")

# ── 7. break ──────────────────────────────────────────
for c in circulars:
    if c["tier"] == "high":
        print(f"First high-tier circular: {c['id']}")
        break

# ── 8. continue ───────────────────────────────────────
banks_with_data = [
    {"name": "HDFC",     "npa": 1.2},
    {"name": None,       "npa": None},
    {"name": "SBI",      "npa": 2.8},
    {"name": None,       "npa": None},
    {"name": "Yes Bank", "npa": 5.1},
    {"name": "Kotak",    "npa": 0.9},
]

for b in banks_with_data:
    if b["name"] is None:
        continue
    if b["npa"] > 5.0:
        print(f"Critical: {b['name']} NPA={b['npa']}%")
        break
    print(f"OK: {b['name']}")
