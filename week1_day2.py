# Week 1 Day 2 — Python core syntax practice
# Topic: variables, strings, f-strings, lists, dicts, comprehensions

# ── 1. Variables ──────────────────────────────────────

bank_name="RBI"
repo_rate=6.5
is_scheduled = True

print(bank_name)
print(repo_rate)
print(is_scheduled)

# ── 2. Strings ────────────────────────────────────────

circular_title = "master circular on kyc norms"

print(circular_title.upper())
print(circular_title.title())
print(circular_title.replace("kyc","KYC"))
print(len(circular_title))

# ── 3. f-strings ──────────────────────────────────────

npa_ratio = 0.0213
total_assets = 4850000

print(f"bank name:{bank_name}")
print(f"Repo rate: {repo_rate}%")
print(f"NPA ratio: {npa_ratio:.2%}")
print(f"Total assets: ₹{total_assets:,}")

# ── 4. Lists ──────────────────────────────────────────

banks = ["HDFC", "ICICI", "SBI", "Axis", "Kotak"]

print(banks[0])
print(banks[-1])
print(banks[1:3])
banks.append("Yes Bank")
banks.sort()
print(banks)

# ── 5. Dicts ──────────────────────────────────────────

circular = {
    "id": "RBI/2024/101",
    "topic": "KYC Guidelines",
    "risk_tier": "high",
    "pages": 24
}

print(circular["topic"])

print(circular.get("missing_key", "N/A"))
circular["status"] = "active"
for key,value in circular.items():
    print(f"  {key}: {value}")

# ── 6. List comprehensions ────────────────────────────

all_banks = [
    {"name": "HDFC",     "npa": 1.2},
    {"name": "Yes Bank", "npa": 4.8},
    {"name": "SBI",      "npa": 2.1},
    {"name": "Kotak",    "npa": 0.9},
]

low_npa_banks= [b["name"] for b in all_banks if b["npa"]<2.5]
print(low_npa_banks)

