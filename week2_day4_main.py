# -*- coding: utf-8 -*-
# week2_day4_main.py — uses bfsi_tools package

import logging
from bfsi_tools import parse_circular, parse_bank

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)-8s %(message)s"
)

# ── Circular parsing ──────────────────────────────────────
circular_payloads = [
    '{"id": "RBI/101", "tier": "high",  "pages": 36, "tags": ["kyc"]}',
    '{"id": "RBI/102", "tier": "low",   "pages": 8}',
    '{"id": "RBI/103", "pages": 24}',          # missing tier — uses default
    'not json at all',
    '{"tier": "high", "pages": 12}',            # missing id
    '{"id": "RBI/104", "tier": "extreme"}',     # invalid tier
]

print("── Circulars ──")
for p in circular_payloads:
    c = parse_circular(p)
    if c:
        print(f"  {c.summary()}")

# ── Bank parsing ──────────────────────────────────────────
bank_payloads = [
    '{"name": "HDFC",     "npa": 1.2, "branches": 6800}',
    '{"name": "Yes Bank", "npa": 5.1, "branches": 1100}',
    '{"name": "SBI",      "npa": 2.8}',
    '{"npa": 3.5}',                             # missing name
]

print("\n── Banks ──")
for p in bank_payloads:
    b = parse_bank(p)
    if b:
        print(f"  {b.summary()}")