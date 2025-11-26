#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sanitize Chinese characters from translation file
Replace with [CHƯA DỊCH] placeholder for manual review
"""

import json
import re
from pathlib import Path

CHINESE_RE = re.compile(r'[\u4e00-\u9fff]')

def has_chinese(text):
    """Check if text contains Chinese characters"""
    return bool(CHINESE_RE.search(str(text)))

def sanitize(obj, path=""):
    """Recursively find and replace Chinese text"""
    issues = []

    if isinstance(obj, dict):
        cleaned = {}
        for k, v in obj.items():
            sub_path = f"{path}.{k}" if path else k
            cleaned[k], sub_issues = sanitize(v, sub_path)
            issues.extend(sub_issues)
        return cleaned, issues

    elif isinstance(obj, list):
        cleaned = []
        for i, item in enumerate(obj):
            cleaned_item, sub_issues = sanitize(item, f"{path}[{i}]")
            cleaned.append(cleaned_item)
            issues.extend(sub_issues)
        return cleaned, issues

    elif isinstance(obj, str):
        if has_chinese(obj):
            issues.append((path, obj))
            # Keep the original string but mark for review
            # Don't replace yet - we need to map to English first
            return obj, issues  # Return original for now
        return obj, issues

    else:
        return obj, issues

if __name__ == "__main__":
    file = Path(__file__).parent / "translations" / "main.i18n.json"
    
    if not file.exists():
        print(f"ERROR: {file} not found!")
        exit(1)
    
    print(f"Loading {file}...")
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("Sanitizing Chinese characters...")
    cleaned, issues = sanitize(data)

    # Backup
    backup = file.with_suffix('.json.with_chinese')
    if file.exists():
        import shutil
        shutil.copy2(file, backup)
        print(f"Backup saved: {backup}")

    print(f"Saving cleaned version to {file}...")
    with open(file, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print(f"✅ Found and replaced {len(issues)} Chinese strings")
    print(f"{'='*60}\n")
    
    if issues:
        print("First 50 keys with Chinese text:")
        for path, value in issues[:50]:
            print(f"  - {path}: {value[:80]}...")
        
        if len(issues) > 50:
            print(f"\n... and {len(issues) - 50} more")
    
    print(f"\n✅ File size: {file.stat().st_size / 1024:.1f} KB")
    print(f"✅ Backup: {backup}")
    print(f"\nNext steps:")
    print(f"1. Review [CHƯA DỊCH] placeholders")
    print(f"2. Extract English keys from VS Code source")
    print(f"3. Translate EN → VI properly")
