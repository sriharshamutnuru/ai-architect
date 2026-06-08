# -*- coding: utf-8 -*-
# Week 2 Day 3 — Error handling and logging

import json
import logging
from dataclasses import dataclass

# ── 0. Configure logging once at the top ─────────────────
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)-8s %(message)s"
)

# ── 1. Basic try/except ───────────────────────────────────
raw_good = '{"id": "RBI/101", "pages": 24}'
raw_bad  = "not valid json"

for raw in [raw_good, raw_bad]:
    try:
        data = json.loads(raw)
        print(f"Parsed: {data['id']}")
    except json.JSONDecodeError as e:
        print(f"Bad JSON: {e}")

print("Program continues normally\n")

# ── 2. Multiple except blocks ─────────────────────────────
def parse_circular(raw: str) -> dict:
    try:
        data = json.loads(raw)
        return {"id": data["id"], "pages": int(data["pages"])}
    except json.JSONDecodeError:
        logging.error("Not valid JSON")
    except KeyError as e:
        logging.error(f"Missing field: {e}")
    except ValueError as e:
        logging.error(f"Bad value: {e}")
    return {}

tests = [
    '{"id": "RBI/101", "pages": 24}',
    "not json",
    '{"pages": 8}',
    '{"id": "RBI/103", "pages": "many"}',
]
for t in tests:
    result = parse_circular(t)
    if result:
        print(f"  OK: {result}")

# ── 3. else and finally ───────────────────────────────────
def safe_parse(raw: str) -> dict | None:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        logging.error(f"Parse failed: {e}")
        return None
    else:
        logging.info(f"Parsed OK: {data.get('id', 'no-id')}")
        return data
    finally:
        logging.debug("Attempt complete")   # always runs

safe_parse('{"id": "RBI/101"}')
safe_parse("bad json")

# ── 4. Custom exceptions ──────────────────────────────────
class CircularParseError(Exception):
    pass

class InvalidTierError(Exception):
    pass

def validate_circular(data: dict) -> dict:
    if "id" not in data:
        raise CircularParseError("Missing required field: id")
    if data.get("tier") not in ["high", "low", "medium"]:
        raise InvalidTierError(f"Invalid tier: {data.get('tier')}")
    return data

cases = [
    {"id": "RBI/101", "tier": "high"},
    {"tier": "high"},
    {"id": "RBI/103", "tier": "critical"},
]
for case in cases:
    try:
        result = validate_circular(case)
        print(f"  Valid: {result['id']}")
    except CircularParseError as e:
        print(f"  ParseError: {e}")
    except InvalidTierError as e:
        print(f"  TierError: {e}")

# ── 5. Logging levels ─────────────────────────────────────
logging.debug("Debug — only in development")
logging.info("Info — normal operations")
logging.warning("Warning — unusual but recoverable")
logging.error("Error — something failed")

# ── 6. Full robust parser — everything combined ───────────
@dataclass
class Circular:
    circular_id: str
    tier: str
    pages: int

    def classify(self) -> str:
        return "priority" if self.pages > 20 else "standard"

def parse_full(raw: str) -> Circular | None:
    try:
        data = json.loads(raw)
        if "id" not in data:
            raise CircularParseError("Missing required field: id")
        tier = data.get("tier", "low")
        if tier not in ["high", "low", "medium"]:
            raise InvalidTierError(f"Invalid tier: {tier}")
        return Circular(data["id"], tier, data.get("pages", 0))
    except json.JSONDecodeError as e:
        logging.error(f"Bad JSON: {e}")
    except CircularParseError as e:
        logging.error(f"Parse error: {e}")
    except InvalidTierError as e:
        logging.error(f"Tier error: {e}")
    else:
        logging.info("Parse successful")
    finally:
        logging.debug("Parse attempt done")
    return None

payloads = [
    '{"id": "RBI/101", "tier": "high", "pages": 36}',
    "not valid json",
    '{"tier": "high", "pages": 8}',
    '{"id": "RBI/103", "tier": "critical", "pages": 12}',
]

print("\n── Full parser results ──")
for p in payloads:
    result = parse_full(p)
    if result:
        print(f"  {result.circular_id}: {result.classify()}")