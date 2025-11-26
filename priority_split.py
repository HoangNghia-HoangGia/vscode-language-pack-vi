#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Priority-based Translation Split System
Architecture: Core → UI → Misc
Strategy: Translate by priority, not by random
"""

import json
from pathlib import Path

def split_by_priority(base_file):
    """
    Split language pack into 3 priority layers:
    - Core: workbench, editor, debug (CRITICAL)
    - UI: menu, view, panel, commands (HIGH)
    - Misc: everything else (NORMAL)
    """
    print(f"📖 Loading base file: {base_file}")
    with open(base_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    core = {}
    ui = {}
    misc = {}
    
    for key, value in data.items():
        if key == "":
            # Copyright header goes to all
            core[key] = value
            ui[key] = value
            misc[key] = value
            continue
        
        key_lower = key.lower()
        
        # Core components (CRITICAL) - Essential UI strings
        # These are from package.nls.json files, not workbench prefixed
        if any(term in key_lower for term in [
            "displayname", "description", "command.", "title",
            "editor", "debug", "search", "terminal"
        ]):
            core[key] = value
        
        # UI components (HIGH priority)
        elif any(term in key_lower for term in [
            "menu", "view", "panel", "sidebar", "statusbar",
            "category", "group", "action"
        ]):
            ui[key] = value
        
        # Everything else (NORMAL priority)
        else:
            misc[key] = value
    
    return core, ui, misc

def save_layer(name, data, output_dir):
    """Save layer to JSON file"""
    output_file = output_dir / name
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return output_file

if __name__ == "__main__":
    print("="*70)
    print("🎯 PRIORITY-BASED TRANSLATION SYSTEM")
    print("="*70)
    print()
    print("📋 Strategy:")
    print("  1. Core (workbench, editor, debug) → CRITICAL")
    print("  2. UI (menu, view, panel) → HIGH")
    print("  3. Misc (everything else) → NORMAL")
    print()
    
    base_file = Path(__file__).parent / "translations" / "main.i18n.base.json"
    output_dir = Path(__file__).parent / "translations"
    
    if not base_file.exists():
        print(f"❌ Base file not found: {base_file}")
        exit(1)
    
    # Split
    print("🔪 Splitting into layers...")
    core, ui, misc = split_by_priority(base_file)
    
    # Save each layer
    core_file = save_layer("core.json", core, output_dir)
    ui_file = save_layer("ui.json", ui, output_dir)
    misc_file = save_layer("misc.json", misc, output_dir)
    
    print()
    print("✅ Split complete!")
    print()
    print("📊 Statistics:")
    print(f"  ├─ Core (CRITICAL): {len(core)-1} strings → {core_file}")
    print(f"  ├─ UI (HIGH):       {len(ui)-1} strings → {ui_file}")
    print(f"  └─ Misc (NORMAL):   {len(misc)-1} strings → {misc_file}")
    print(f"  📦 Total: {len(core) + len(ui) + len(misc) - 3} strings")
    print()
    print("🎯 Next steps:")
    print("  1. Translate core.json FIRST (most critical)")
    print("  2. Then ui.json (high priority)")
    print("  3. Finally misc.json (normal priority)")
    print()
    print("✅ Ready for AI-assisted translation!")
