import json

with open("translations/ui.json", "r", encoding="utf-8") as f:
    data = json.load(f)

panel = {}

keywords = [
    "explorer",
    "search",
    "scm",
    "source",
    "git",
    "extensions",
    "problems",
    "output",
    "terminal",
    "debug",
    "timeline"
]

for k, v in data.items():
    kl = k.lower()
    if any(word in kl for word in keywords):
        panel[k] = v

with open("translations/panel.json", "w", encoding="utf-8") as f:
    json.dump(panel, f, ensure_ascii=False, indent=2)

print("✅ Extracted Panel + Sidebar layer")
print("Total:", len(panel))
