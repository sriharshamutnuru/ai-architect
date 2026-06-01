# -*- coding: utf-8 -*-
# Week 1 Day 5 — Files & JSON: open, read/write, json, pathlib
import json
from pathlib import Path
# ── 1. Writing a file ─────────────────────────────────
banks = ["HDFC", "ICICI", "SBI", "Axis"]

with open("banks.txt", "w") as f:
    for bank in banks:
        f.write(bank + "\n") # write() never adds \n for you
print("Wrote banks.txt")

# ── 2. Reading a file line by line ────────────────────
with open("banks.txt", "r") as f:
    for i, line in enumerate(f, start=1):
        print(f"  {i}. {line.strip()}")   # strip removes trailing \n
# ── 3. Appending to a file ────────────────────────────
with open("banks.txt", "a") as f:
    f.write("Kotak\n")              # 'a' keeps existing content

with open("banks.txt", "r") as f:
    print(f"Total lines now: {len(f.readlines())}")

# ── 4. json.loads — string to Python ──────────────────
raw = '{"id": "RBI/101", "tier": "high", "pages": 24}'
data = json.loads(raw)
print(data["id"], "—", data["pages"], "pages")
print(type(data))                   # <class 'dict'>

# ── 5. json.dumps — Python to string ──────────────────
circular = {"id": "RBI/101", "tier": "high", "pages": 24}
print(json.dumps(circular, indent=2))

# ── 6. Writing JSON to a file ─────────────────────────
report = {
    "quarter": "Q3-2024",
    "banks": [
        {"name": "HDFC", "npa": 1.2},
        {"name": "SBI",  "npa": 2.8},
    ],
    "reviewed": True,
}

with open("report.json", "w") as f:
    json.dump(report, f, indent=2)  # dump (no s) writes to file

print("Wrote report.json")

# ── 7. Reading JSON from a file ───────────────────────
with open("report.json", "r") as f:
    loaded = json.load(f)           # load (no s) reads from file

print(f"Quarter: {loaded['quarter']}")
print(f"Banks tracked: {len(loaded['banks'])}")

# ── 8. pathlib basics ─────────────────────────────────
p = Path("data") / "circulars" / "rbi_master_101.json"
print(f"Full path: {p}")
print(f"Filename:  {p.name}")
print(f"Extension: {p.suffix}")
print(f"Stem:      {p.stem}")
print(f"Parent:    {p.parent}")

# ── 9. pathlib — check and create ─────────────────────
if Path("report.json").exists():
    print("report.json exists ✓")

Path("output/reports").mkdir(parents=True, exist_ok=True)
print("Created output/reports/")