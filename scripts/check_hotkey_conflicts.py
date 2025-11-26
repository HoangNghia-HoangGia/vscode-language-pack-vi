#!/usr/bin/env python3
# check_hotkey_conflicts.py
# Basic accelerator / hotkey checks:
# - Look for patterns like "&File" or "Alt+X" changed (heuristic)
# - Ensure translations didn't remove ampersand accelerators (if used)
# Outputs: reports/hotkey_issues.json

import json, re
from pathlib import Path

ROOT = Path(".")
EN = ROOT / "translations" / "main.i18n.locked.json"
TR = ROOT / "translations" / "main.i18n.json"
OUT = ROOT / "reports" / "hotkey_issues.json"

AMP_PATTERN = re.compile(r"&\w")  # e.g., &F

def main():
    en = json.loads(EN.read_text(encoding="utf-8")) if EN.exists() else {}
    tr = json.loads(TR.read_text(encoding="utf-8")) if TR.exists() else {}
    issues = []
    for key, eng in en.items():
        trans = tr.get(key, "")
        if not isinstance(eng, str) or not isinstance(trans, str):
            continue
        amp_en = AMP_PATTERN.findall(eng)
        amp_tr = AMP_PATTERN.findall(trans)
        if amp_en and not amp_tr:
            issues.append({
                "key": key,
                "english": eng,
                "translated": trans,
                "issue": "ampersand_accelerator_removed"
            })
        # Check for Alt+ patterns presence mismatch
        alt_en = "alt+" in eng.lower()
        alt_tr = "alt+" in trans.lower()
        if alt_en != alt_tr:
            issues.append({
                "key": key,
                "english": eng,
                "translated": trans,
                "issue": "alt_shortcut_mismatch"
            })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(issues, ensure_ascii=False, indent=2), encoding="utf-8")
    print("✅ Hotkey check done. Issues:", len(issues), "->", OUT)
    if issues:
        print("Sample:", issues[0])

if __name__ == "__main__":
    main()
