"""
Audit Filter - Extract High-Risk Translations
Identifies translations that need manual review based on keywords and patterns.
"""

import json
from pathlib import Path

INPUT_LOG = "logs/full_ai_log.json"
OUTPUT_AUDIT = "translations/audit_priority.json"

# Keywords that indicate critical UI elements requiring careful review
HIGH_RISK_KEYWORDS = [
    # File operations
    "file", "folder", "directory", "path", "workspace",
    
    # Core functions
    "debug", "debugger", "breakpoint", "watch",
    "terminal", "console", "output",
    
    # Error handling
    "error", "warning", "exception", "failed", "fail",
    
    # Git operations
    "commit", "push", "pull", "merge", "branch", "repository",
    
    # Editor core
    "editor", "edit", "save", "open", "close",
    "search", "find", "replace",
    
    # Settings
    "settings", "preferences", "configuration", "configure",
    
    # Extensions
    "extension", "install", "uninstall", "enable", "disable",
]

def calculate_risk_score(item):
    """
    Calculate risk score for a translation.
    Higher score = higher priority for manual review.
    """
    score = 0
    text_lower = item["translated"].lower()
    source_lower = item["source"].lower()
    
    # Check for high-risk keywords
    keyword_matches = sum(1 for kw in HIGH_RISK_KEYWORDS if kw in text_lower)
    score += keyword_matches * 10
    
    # Check for placeholders (critical to preserve)
    placeholder_count = len(item.get("placeholders", []))
    score += placeholder_count * 15
    
    # Check translation length difference (possible mistranslation)
    source_len = len(item["source"])
    translated_len = len(item["translated"])
    length_ratio = translated_len / max(source_len, 1)
    if length_ratio > 2 or length_ratio < 0.5:
        score += 20
    
    # Check for command keys
    if any(key in item["key"] for key in ["command", "title", "menu"]):
        score += 25
    
    return score


def main():
    print("🔍 Starting Audit Filter...")
    print(f"📂 Input: {INPUT_LOG}")
    
    if not Path(INPUT_LOG).exists():
        print(f"❌ Error: {INPUT_LOG} not found!")
        print("   Run full_ai_translate.py first.")
        return
    
    with open(INPUT_LOG, "r", encoding="utf-8") as f:
        logs = json.load(f)

    audit_list = []
    
    print(f"📊 Analyzing {len(logs)} translations...\n")

    for item in logs:
        score = calculate_risk_score(item)
        
        if score > 0:  # Any risk detected
            audit_item = {
                "key": item["key"],
                "source": item["source"],
                "translated": item["translated"],
                "risk_score": score,
                "placeholders": item.get("placeholders", []),
                "status": "pending_review"
            }
            audit_list.append(audit_item)

    # Sort by risk score (highest first)
    audit_list.sort(key=lambda x: x["risk_score"], reverse=True)

    # Save audit priority list
    with open(OUTPUT_AUDIT, "w", encoding="utf-8") as f:
        json.dump(audit_list, f, ensure_ascii=False, indent=2)

    print("✅ Audit priority list generated")
    print(f"📁 Output: {OUTPUT_AUDIT}")
    print(f"\n📊 Statistics:")
    print(f"  Total translations: {len(logs)}")
    print(f"  High-risk items: {len(audit_list)} ({len(audit_list)/len(logs)*100:.1f}%)")
    
    # Show top 10 highest risk
    if audit_list:
        print(f"\n🔴 Top 10 Highest Risk Translations:")
        for i, item in enumerate(audit_list[:10], 1):
            print(f"  {i}. [{item['risk_score']}] {item['key']}")
            print(f"     EN: {item['source']}")
            print(f"     VI: {item['translated']}")
            print()


if __name__ == "__main__":
    main()
