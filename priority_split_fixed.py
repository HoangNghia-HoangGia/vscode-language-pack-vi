import json

with open("translations/main.i18n.locked.json", "r", encoding="utf-8") as f:
    data = json.load(f)

core, ui, misc = {}, {}, {}

for k, v in data.items():
    key_lower = k.lower()
    
    # Core: extensions quan trọng (editor, debugger, git, language features)
    if any(x in key_lower for x in ["editor", "debug", "git", "language-features", "typescript", "javascript", "python", "markdown"]):
        core[k] = v
    # UI: menu, views, panels, commands
    elif any(x in key_lower for x in ["menu", "view", "panel", "command", "sidebar", "status", "toolbar", "title", "button", "icon"]):
        ui[k] = v
    # Misc: còn lại
    else:
        misc[k] = v

def save(name, obj):
    with open(f"translations/{name}", "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

save("core.json", core)
save("ui.json", ui)
save("misc.json", misc)

print("✅ Split complete!")
print("Core:", len(core))
print("UI:", len(ui))
print("Misc:", len(misc))
