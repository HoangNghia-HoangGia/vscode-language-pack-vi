#!/usr/bin/env python3
# length_check.py
# Flags items where Vietnamese translation length >> English length
# Outputs: reports/length_issues.json

import json
from pathlib import Path

ROOT = Path(".")
EN = ROOT / "translations" / "main.i18n.locked.json"
TR = ROOT / "translations" / "main.i18n.json"
OUT = ROOT / "reports" / "length_issues.json"

RATIO_THRESHOLD = 1.5  # tune: percent of longer allowed; 1.5 means 50% longer

def main():
    en = json.loads(EN.read_text(encoding="utf-8")) if EN.exists() else {}
    tr = json.loads(TR.read_text(encoding="utf-8")) if TR.exists() else {}
    issues = []
    for key, eng in en.items():
        trans = tr.get(key, "")
        if not isinstance(eng, str) or not isinstance(trans, str):
            continue
        e = len(eng.strip())
        t = len(trans.strip())
        if e == 0:
            continue
        ratio = t / e
        if ratio > RATIO_THRESHOLD:
            issues.append({
                "key": key,
                "english": eng,
                "translated": trans,
                "en_len": e,
                "tr_len": t,
                "ratio": round(ratio, 2)
            })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(issues, ensure_ascii=False, indent=2), encoding="utf-8")
    print("✅ Length check done. Issues:", len(issues), "->", OUT)
    if issues:
        print("Sample:", issues[0])

if __name__ == "__main__":
    main()
