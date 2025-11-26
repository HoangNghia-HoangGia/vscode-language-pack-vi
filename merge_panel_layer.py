import json

# Load base locked file
with open("translations/main.i18n.locked.json", "r", encoding="utf-8") as f:
    base = json.load(f)

# Load translated panel
with open("translations/panel_translated.json", "r", encoding="utf-8") as f:
    panel = json.load(f)

# Merge override
base.update(panel)

with open("translations/main.i18n.json", "w", encoding="utf-8") as f:
    json.dump(base, f, ensure_ascii=False, indent=2)

print("✅ Main pack updated with Panel + Sidebar translations")
