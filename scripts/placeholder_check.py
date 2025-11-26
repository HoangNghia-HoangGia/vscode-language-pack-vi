#!/usr/bin/env python3
# placeholder_check.py
# Focus: ensure placeholders in english are preserved in translated strings.
# Patterns checked: {name}, {0}, %s, %d, $(command), ${var}

import json, re
from pathlib import Path

ROOT = Path(".")
EN = ROOT / "translations" / "main.i18n.locked.json"
TR = ROOT / "translations" / "main.i18n.json"
OUT = ROOT / "reports" / "placeholder_issues.json"

PATS = [
    r"\{[0-9a-zA-Z_]+\}",
    r"%[sd]",
    r"\$\([^)]+\)",
    r"\$\{[^}]+\}"
]

def find_all(s):
    out = []
    for p in PATS:
        out += re.findall(p, s or "")
    return out

def main():
    en = json.loads(EN.read_text(encoding="utf-8")) if EN.exists() else {}
    tr = json.loads(TR.read_text(encoding="utf-8")) if TR.exists() else {}
    issues = []
    for key, eng in en.items():
        trans = tr.get(key, "")
        if not isinstance(eng, str) or not isinstance(trans, str):
            continue
        ph_en = find_all(eng)
        ph_tr = find_all(trans)
        # Compare sets
        set_en = set(ph_en)
        set_tr = set(ph_tr)
        if set_en != set_tr:
            issues.append({
                "key": key,
                "english_placeholders": list(set_en),
                "translated_placeholders": list(set_tr),
                "english": eng,
                "translated": trans
            })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(issues, ensure_ascii=False, indent=2), encoding="utf-8")
    print("✅ Placeholder check done. Issues:", len(issues), "->", OUT)
    if issues:
        print("Sample:", issues[0])

if __name__ == "__main__":
    main()
