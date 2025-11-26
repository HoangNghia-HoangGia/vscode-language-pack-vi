#!/usr/bin/env python3
# compute_coverage.py
# Outputs: reports/coverage_breakdown.json

import json
from pathlib import Path
import re

ROOT = Path(".")
TRANSLATED = ROOT / "translations" / "main.i18n.json"
REPORT = ROOT / "reports" / "coverage_breakdown.json"

def load(p):
    if not p.exists():
        print(f"[ERROR] Missing {p}")
        return {}
    return json.loads(p.read_text(encoding="utf-8"))

def classify(val):
    if not isinstance(val, str):
        return "non_string"
    v = val.strip()
    if v.startswith("[DICT]"):
        return "dict"
    if v.startswith("[AI]"):
        return "ai"
    if v.startswith("[HUMAN]"):
        return "human"
    if v.startswith("[CHỜ_DỊCH]") or v.startswith("[CHO_DICH]"):
        return "waiting"
    if v.startswith("[SAFE]"):
        return "safe"
    if v.startswith("[EN]"):
        return "untranslated"
    if v.startswith("[TODO]"):
        return "todo"
    # fallback: consider it 'translated_unlabeled'
    return "translated_unlabeled"

def main():
    data = load(TRANSLATED)
    total = len(data)
    counts = {}
    sample = {}
    for k,v in data.items():
        c = classify(v)
        counts[c] = counts.get(c, 0) + 1
        if c not in sample and len(sample) < 10:
            sample[c] = {"key": k, "value": v}
    report = {
        "total_keys": total,
        "counts": counts,
        "samples": sample
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("✅ Coverage computed. See", REPORT)
    print("Summary:", report["counts"])

if __name__ == "__main__":
    main()
