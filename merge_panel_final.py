import json
from pathlib import Path

# Load locked base
with open("translations/main.i18n.locked.json", "r", encoding="utf-8") as f:
    base = json.load(f)

# Load human-reviewed panel translations
panel_file = Path("translations/panel_human_reviewed.json")

if panel_file.exists():
    print("✅ Using human-reviewed panel translations")
    with open(panel_file, "r", encoding="utf-8") as f:
        panel = json.load(f)
else:
    print("⚠️ Human review not complete, using AI-translated version")
    with open("translations/panel_ai_translated.json", "r", encoding="utf-8") as f:
        panel = json.load(f)

# Merge override
base.update(panel)

# Save final main.i18n.json
with open("translations/main.i18n.json", "w", encoding="utf-8") as f:
    json.dump(base, f, ensure_ascii=False, indent=2)

# Generate statistics
dict_count = sum(1 for v in base.values() if isinstance(v, str) and "[DICT]" in v)
ai_count = sum(1 for v in base.values() if isinstance(v, str) and "[AI]" in v)
human_count = sum(1 for v in base.values() if isinstance(v, str) and "[HUMAN]" in v)
todo_count = sum(1 for v in base.values() if isinstance(v, str) and "[TODO]" in v)
en_count = sum(1 for v in base.values() if isinstance(v, str) and "[EN]" in v)

total_translated = dict_count + ai_count + human_count

print("\n✅ Main pack updated with Panel translations")
print(f"\n📊 Translation Statistics:")
print(f"  [DICT] Manual Dictionary: {dict_count}")
print(f"  [AI] AI Generated: {ai_count}")
print(f"  [HUMAN] Human Reviewed: {human_count}")
print(f"  [TODO] Pending: {todo_count}")
print(f"  [EN] Untranslated: {en_count}")
print(f"\n  Total Translated: {total_translated}/{len(base)} ({total_translated/len(base)*100:.1f}%)")
