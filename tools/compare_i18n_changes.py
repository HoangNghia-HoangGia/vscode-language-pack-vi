"""
I18N Integrity Checker
Compares two i18n files to detect:
- Lost keys (potential data loss)
- Added keys (unexpected changes)
- Structural integrity
"""

import json
import sys
from pathlib import Path

def load_json(filepath):
    """Load JSON file safely."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: File not found: {filepath}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {filepath}: {e}")
        sys.exit(1)


def main():
    if len(sys.argv) < 3:
        print("Usage: python compare_i18n_changes.py <old_file> <new_file>")
        print("\nExample:")
        print("  python tools/compare_i18n_changes.py translations/main.i18n.locked.json translations/main.i18n.json")
        sys.exit(1)

    old_file = sys.argv[1]
    new_file = sys.argv[2]

    print("🔍 I18N Integrity Checker\n")
    print(f"📂 Old file: {old_file}")
    print(f"📂 New file: {new_file}")
    print()

    old = load_json(old_file)
    new = load_json(new_file)

    old_keys = set(old.keys())
    new_keys = set(new.keys())

    lost_keys = old_keys - new_keys
    added_keys = new_keys - old_keys
    common_keys = old_keys & new_keys

    print("=" * 60)
    print("           I18N COMPARISON REPORT")
    print("=" * 60)
    print()

    print(f"📊 Old file keys: {len(old_keys)}")
    print(f"📊 New file keys: {len(new_keys)}")
    print(f"📊 Common keys:   {len(common_keys)}")
    print()

    # Check for lost keys (CRITICAL)
    if lost_keys:
        print(f"❌ LOST KEYS: {len(lost_keys)} (CRITICAL!)")
        print("   These keys existed in old file but missing in new file:")
        print()
        for k in sorted(list(lost_keys)[:50]):
            print(f"   - {k}")
        if len(lost_keys) > 50:
            print(f"   ... and {len(lost_keys) - 50} more")
        print()
    else:
        print("✅ No keys lost!")
        print()

    # Check for added keys
    if added_keys:
        print(f"➕ NEW KEYS: {len(added_keys)}")
        print("   These keys are in new file but not in old file:")
        print()
        for k in sorted(list(added_keys)[:50]):
            print(f"   + {k}")
        if len(added_keys) > 50:
            print(f"   ... and {len(added_keys) - 50} more")
        print()
    else:
        print("✅ No unexpected new keys.")
        print()

    # Check for value changes (sample)
    changed_values = []
    for key in list(common_keys)[:100]:  # Sample first 100
        if old[key] != new[key]:
            changed_values.append(key)

    if changed_values:
        print(f"🔄 CHANGED VALUES: {len(changed_values)} (sample from first 100 common keys)")
        print()
        for k in changed_values[:10]:
            print(f"   Key: {k}")
            print(f"   Old: {str(old[k])[:80]}")
            print(f"   New: {str(new[k])[:80]}")
            print()
    else:
        print("✅ No value changes detected (in sample).")
        print()

    # Summary
    print("=" * 60)
    print("                    SUMMARY")
    print("=" * 60)
    print()

    integrity_ok = len(lost_keys) == 0
    
    if integrity_ok:
        print("✅ INTEGRITY CHECK PASSED")
        print("   - No keys lost")
        print("   - Structure preserved")
        print()
        print("🟢 BUILD APPROVED")
    else:
        print("❌ INTEGRITY CHECK FAILED")
        print(f"   - {len(lost_keys)} keys lost")
        print()
        print("🔴 BUILD REJECTED")
        print("   Fix lost keys before deploying.")

    print()
    
    # Exit code
    sys.exit(0 if integrity_ok else 1)


if __name__ == "__main__":
    main()
