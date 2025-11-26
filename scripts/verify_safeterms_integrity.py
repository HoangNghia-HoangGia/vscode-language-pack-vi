#!/usr/bin/env python3
# verify_safeterms_integrity.py
# Scans translations for safe term violations.
# If any safe term found translated (heuristic: translated form contains common vietnamese words replacing safe term),
# the script flags them. Conservative approach: ensure safe term appears verbatim in translation when it existed in English.

import json, re
from pathlib import Path

ROOT = Path(".")
EN = ROOT / "translations" / "main.i18n.locked.json"
TR = ROOT / "translations" / "main.i18n.json"
SAFE_FILE = ROOT / "translations" / "safe_terms.json"
OUT = ROOT / "reports" / "safeterm_violations.json"

# Default safe terms if file doesn't exist
DEFAULT_SAFE_TERMS = {
    "VS Code": "VS Code",
    "Git": "Git",
    "GitHub": "GitHub",
    "JSON": "JSON",
    "HTML": "HTML",
    "CSS": "CSS",
    "JavaScript": "JavaScript",
    "TypeScript": "TypeScript",
    "Python": "Python",
    "Terminal": "Terminal",
    "Node.js": "Node.js",
    "npm": "npm"
}

def load(p):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}

def main():
    en = load(EN)
    tr = load(TR)
    safe = load(SAFE_FILE) if SAFE_FILE.exists() else DEFAULT_SAFE_TERMS
    violations = []
    for key, eng in en.items():
        trans = tr.get(key, "")
        if not isinstance(eng, str) or not isinstance(trans, str):
            continue
        for sk in safe.keys():
            if sk.lower() in eng.lower():
                # Expect sk to appear verbatim in trans (case-sensitive check)
                if sk not in trans:
                    violations.append({
                        "key": key,
                        "english": eng,
                        "translated": trans,
                        "missing_safe_term": sk
                    })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(violations, ensure_ascii=False, indent=2), encoding="utf-8")
    print("✅ Safe term integrity check done. Violations:", len(violations), "->", OUT)
    if violations:
        print("-> First violation sample:", violations[0])

if __name__ == "__main__":
    main()
