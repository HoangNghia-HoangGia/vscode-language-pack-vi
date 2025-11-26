#!/usr/bin/env python3
# export_high_risk.py
# Criteria for high-risk:
# - contains indicators of command/cli/placeholder changes
# - contains safe-term violations (non-preserved)
# - placeholders missing or altered (simple check)
# - length ratio > threshold (config)
# Outputs: reports/high_risk_items.json

import json, re
from pathlib import Path

ROOT = Path(".")
EN = ROOT / "translations" / "main.i18n.locked.json"
TR = ROOT / "translations" / "main.i18n.json"
SAFE_FILE = ROOT / "translations" / "safe_terms.json"
OUT = ROOT / "reports" / "high_risk_items.json"

LENGTH_RATIO_THRESHOLD = 1.6  # tuneable
PLACEHOLDER_PATTERNS = [
    r"\{[0-9a-zA-Z_]+\}",
    r"%\w",
    r"\$\([^)]+\)",
    r"\$\{[^}]+\}"
]

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

def find_placeholders(s):
    ph = []
    for pat in PLACEHOLDER_PATTERNS:
        ph += re.findall(pat, s)
    return ph

def contains_safe_vi(s, safe_keys):
    # If any safe_key lowercase appears in translated string in vietnamese-like form (heuristic),
    # we check for presence of known translations (unlikely). We'll just check that safe keys exist verbatim.
    for k in safe_keys:
        if k.lower() in s.lower():
            return True
    return False

def main():
    en = load(EN)
    tr = load(TR)
    safe = load(SAFE_FILE) if SAFE_FILE.exists() else DEFAULT_SAFE_TERMS
    safe_keys = list(safe.keys())
    items = []
    for key, eng in en.items():
        trans = tr.get(key, "")
        reason = []
        # 1) placeholder check: placeholders in eng but missing in trans or changed count
        ph_en = find_placeholders(eng if isinstance(eng, str) else "")
        ph_tr = find_placeholders(trans if isinstance(trans, str) else "")
        if ph_en and (len(ph_en) != len(ph_tr) or any(p not in trans for p in ph_en)):
            reason.append("placeholder_mismatch")
        # 2) safe-term presence in eng but maybe altered: here, eng contains safe term, trans does not contain it verbatim
        for sk in safe_keys:
            eng_str = eng if isinstance(eng, str) else ""
            trans_str = trans if isinstance(trans, str) else ""
            if sk.lower() in eng_str.lower():
                if sk not in trans_str:  # safe-term not preserved verbatim
                    reason.append("safe_term_not_preserved:" + sk)
        # 3) length ratio
        eng_str = eng if isinstance(eng, str) else ""
        trans_str = trans if isinstance(trans, str) else ""
        if eng_str.strip():
            en_len = len(eng_str)
            tr_len = len(trans_str)
            if en_len > 0 and (tr_len / en_len) > LENGTH_RATIO_THRESHOLD:
                reason.append("length_ratio_high:%.2f" % (tr_len/en_len))
        # 4) suspicious tokens (commands, cli)
        trans_str = trans if isinstance(trans, str) else ""
        low = trans_str.lower()
        cmd_indicators = ["command", "run", "execute", "restart", "terminal", "git", "push", "commit", "checkout"]
        if any(ci in low for ci in cmd_indicators) and trans_str.strip().startswith("[CHỜ_DỊCH]"):
            reason.append("command_needs_review")
        if reason:
            items.append({
                "key": key,
                "english": eng,
                "translated": trans,
                "reasons": list(dict.fromkeys(reason))
            })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    print("✅ Exported high-risk items:", len(items), "->", OUT)

if __name__ == "__main__":
    main()
