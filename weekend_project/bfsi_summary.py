# -*- coding: utf-8 -*-
"""
Week 1 Weekend Project — BFSI Compliance Summary Generator
Reads a JSON config of banks, flags those above the NPA threshold,
prints a formatted report, and writes a summary JSON.
"""

import json
from pathlib import Path

def load_config(path: str) -> dict:
    """Read the JSON config. Fall back to defaults if missing."""
    config_path = Path(path)
    if not config_path.exists():
        print(f"⚠ Config not found at {config_path} — using defaults")
        return {"report_title": "Default Report", "npa_threshold": 3.0, "banks": []}
    with open(config_path, "r") as f:
        return json.load(f)


def classify(npa: float, threshold: float) -> str:
    """Classify a bank's NPA against the threshold."""
    if npa > threshold + 1.5:
        return "CRITICAL"
    if npa > threshold:
        return "FLAG"
    return "OK"


def build_summary(config: dict) -> dict:
    """Process banks and return a summary dict."""
    threshold = config["npa_threshold"]
    flagged = []
    total_branches = 0

    print(f"\n=== {config['report_title']} ===")
    print(f"NPA threshold: {threshold}%\n")

    for bank in config["banks"]:
        status = classify(bank["npa"], threshold)
        total_branches += bank["branches"]
        print(f"  [{status:>8}]  {bank['name']:<14} "
              f"NPA {bank['npa']:>4}%  ({bank['branches']:,} branches)")
        if status != "OK":
            flagged.append(bank["name"])

    return {
        "report_title": config["report_title"],
        "banks_reviewed": len(config["banks"]),
        "flagged_count": len(flagged),
        "flagged_banks": flagged,
        "total_branches": total_branches,
    }


def save_summary(summary: dict, path: str) -> None:
    """Write the summary to a JSON file."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\n✓ Summary written to {output_path}")


def main() -> None:
    config = load_config("config.json")
    summary = build_summary(config)
    print(f"\nFlagged {summary['flagged_count']} of "
          f"{summary['banks_reviewed']} banks: {summary['flagged_banks']}")
    save_summary(summary, "output/summary.json")


if __name__ == "__main__":
    main()