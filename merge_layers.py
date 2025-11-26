#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Merge Priority Layers → Final main.i18n.json
Architecture: Core + UI + Misc → Production-ready language pack
"""

import json
from pathlib import Path

def clean_tag(text):
    """
    Remove quality tags: [DICT], [AI], [TODO] → clean Vietnamese
    Keep original English if [TODO]
    """
    if not isinstance(text, str):
        if isinstance(text, list):
            return [clean_tag(item) for item in text]
        return text
    
    # Remove tags
    for tag in ["[DICT] ", "[AI] ", "[TODO] "]:
        if text.startswith(tag):
            return text[len(tag):]
    
    return text

def merge_layers(core_file, ui_file, misc_file, output_file):
    """
    Merge 3 priority layers into final language pack
    Priority: Core > UI > Misc (in case of conflicts)
    """
    print("="*70)
    print("🔗 MERGE PRIORITY LAYERS")
    print("="*70)
    
    # Load all layers
    print("\n📂 Loading layers...")
    with open(core_file, 'r', encoding='utf-8') as f:
        core = json.load(f)
        print(f"  ✅ Core: {len(core)} keys")
    
    with open(ui_file, 'r', encoding='utf-8') as f:
        ui = json.load(f)
        print(f"  ✅ UI:   {len(ui)} keys")
    
    with open(misc_file, 'r', encoding='utf-8') as f:
        misc = json.load(f)
        print(f"  ✅ Misc: {len(misc)} keys")
    
    # Merge (Core overrides UI overrides Misc)
    print("\n🔄 Merging...")
    merged = {}
    
    # Start with Misc
    for key, value in misc.items():
        merged[key] = clean_tag(value)
    
    # Overlay UI
    for key, value in ui.items():
        merged[key] = clean_tag(value)
    
    # Overlay Core (highest priority)
    for key, value in core.items():
        merged[key] = clean_tag(value)
    
    # Count quality
    dict_count = 0
    ai_count = 0
    todo_count = 0
    
    for key, value in merged.items():
        if key == "":
            continue  # Skip copyright header
        
        if isinstance(value, str):
            if "[DICT]" in str(core.get(key, "") or ui.get(key, "") or misc.get(key, "")):
                dict_count += 1
            elif "[AI]" in str(core.get(key, "") or ui.get(key, "") or misc.get(key, "")):
                ai_count += 1
            else:
                todo_count += 1
    
    # Save
    print(f"\n💾 Saving to: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)
    
    total = len(merged) - 1  # Exclude copyright header
    print(f"\n✅ MERGE COMPLETE!")
    print(f"  📊 Từ điển:    {dict_count:4d} strings ({dict_count/total*100:.1f}%)")
    print(f"  🤖 AI:         {ai_count:4d} strings ({ai_count/total*100:.1f}%)")
    print(f"  ⚠️  English:    {todo_count:4d} strings ({todo_count/total*100:.1f}%)")
    print(f"  📦 Total:      {total} strings")
    print(f"\n📁 Output: {output_file}")
    print("="*70)
    
    return dict_count, ai_count, todo_count

if __name__ == "__main__":
    base_dir = Path(__file__).parent / "translations"
    
    merge_layers(
        core_file=base_dir / "core_translated.json",
        ui_file=base_dir / "ui_translated.json",
        misc_file=base_dir / "misc_translated.json",
        output_file=base_dir / "main.i18n.json"
    )
    
    print("\n💡 Tiếp theo:")
    print("  1. Review main.i18n.json")
    print("  2. Package extension: vsce package")
    print("  3. Test: code --install-extension *.vsix --force")
    print("  4. Launch: code --locale=vi")
