# -*- coding: utf-8 -*-
# Week 2 Day 5 — pip, venv, requirements.txt, .gitignore

import sys
import os
import importlib

# ── 1. Check your environment ─────────────────────────────
print(f"Python: {sys.version[:6]}")
print(f"Executable: {sys.executable}")

in_venv = "venv" in sys.executable
print(f"In venv: {in_venv}")
print()

# ── 2. Check installed packages ───────────────────────────
standard_lib = ["json", "pathlib", "dataclasses", "logging", "os"]
third_party  = ["pydantic", "dotenv", "rich", "pytest", "httpx"]

print("── Standard library ──")
for pkg in standard_lib:
    try:
        importlib.import_module(pkg)
        print(f"  ✓ {pkg}")
    except ImportError:
        print(f"  ✗ {pkg}")

print("\n── Third-party ──")
for pkg in third_party:
    try:
        importlib.import_module(pkg)
        print(f"  ✓ {pkg}")
    except ImportError:
        print(f"  ✗ {pkg} — run: pip install {pkg}")

# ── 3. os.getenv — reading config from environment ────────
os.environ["MODEL_NAME"]   = "claude-sonnet-4"
os.environ["MAX_TOKENS"]   = "1024"
os.environ["TEMPERATURE"]  = "0.3"

model    = os.getenv("MODEL_NAME",  "claude-haiku")
max_tok  = int(os.getenv("MAX_TOKENS", "512"))
temp     = float(os.getenv("TEMPERATURE", "0.7"))
missing  = os.getenv("MISSING_KEY", "default-value")

print(f"\n── Environment config ──")
print(f"  Model:      {model}")
print(f"  Max tokens: {max_tok}")
print(f"  Temp:       {temp}")
print(f"  Missing:    {missing}")

# ── 4. What your Week 5 requirements.txt will look like ───
week5_deps = [
    ("anthropic",      "0.25.0"),
    ("httpx",          "0.27.0"),
    ("pydantic",       "2.6.4"),
    ("python-dotenv",  "1.0.1"),
    ("litellm",        "1.30.0"),
    ("langfuse",       "2.7.3"),
]

print("\n── Week 5 requirements.txt preview ──")
for pkg, ver in week5_deps:
    print(f"  {pkg:<22}=={ver}")

# ── 5. Using bfsi_tools package from Day 4 ───────────────
print("\n── bfsi_tools package test ──")
try:
    from bfsi_tools import parse_circular, Bank, Circular
    c = parse_circular('{"id": "RBI/101", "tier": "high", "pages": 36}')
    if c:
        print(f"  Circular: {c.summary()}")
    b = Bank("HDFC", 1.2, 6800)
    print(f"  Bank: {b.summary()}")
    print("  ✓ bfsi_tools package working correctly")
except ImportError as e:
    print(f"  ✗ Import failed: {e}")
    print("  Make sure bfsi_tools/ folder exists with __init__.py")