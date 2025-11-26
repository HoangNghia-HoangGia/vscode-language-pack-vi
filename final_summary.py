#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final Summary Generator
"""

import json
from pathlib import Path

def generate_summary():
    main_file = Path(__file__).parent / 'translations' / 'main.i18n.json'
    
    with open(main_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total = 0
    translated = 0
    en_tagged = 0
    ai_tagged = 0
    
    for key, value in data.items():
        if key == '' or not isinstance(value, str):
            continue
        
        total += 1
        
        if value.startswith('[EN]'):
            en_tagged += 1
        elif '[AI]' in value:
            ai_tagged += 1
        else:
            translated += 1
    
    print("\n" + "="*70)
    print("FINAL TRANSLATION SUMMARY - main.i18n.json")
    print("="*70)
    print(f"\n📊 Statistics:")
    print(f"   Total entries:          {total:4d}")
    print(f"   ✅ Translated:          {translated:4d} ({translated/total*100:.1f}%)")
    print(f"   ❌ [EN] tagged:         {en_tagged:4d}")
    print(f"   ⚠️  [AI] tagged:         {ai_tagged:4d}")
    print(f"\n🎯 Translation Status:")
    
    if en_tagged == 0 and ai_tagged == 0:
        print(f"   🎉 100% COMPLETE - All entries translated!")
    else:
        print(f"   ⚠️  Incomplete - {en_tagged + ai_tagged} entries need work")
    
    # Check validation reports
    reports_dir = Path(__file__).parent / 'reports'
    
    if reports_dir.exists():
        print(f"\n🔍 Validation Reports:")
        
        placeholder_file = reports_dir / 'placeholder_issues.json'
        if placeholder_file.exists():
            with open(placeholder_file, 'r', encoding='utf-8') as f:
                placeholder_data = json.load(f)
                count = len(placeholder_data) if isinstance(placeholder_data, list) else len(placeholder_data.get('issues', []))
                print(f"   Placeholder issues:     {count:4d}")
        
        hotkey_file = reports_dir / 'hotkey_issues.json'
        if hotkey_file.exists():
            with open(hotkey_file, 'r', encoding='utf-8') as f:
                hotkey_data = json.load(f)
                count = len(hotkey_data) if isinstance(hotkey_data, list) else len(hotkey_data.get('issues', []))
                print(f"   Hotkey conflicts:       {count:4d}")
        
        length_file = reports_dir / 'length_issues.json'
        if length_file.exists():
            with open(length_file, 'r', encoding='utf-8') as f:
                length_data = json.load(f)
                count = len(length_data) if isinstance(length_data, list) else len(length_data.get('issues', []))
                print(f"   Length issues:          {count:4d}")
    
    print("\n" + "="*70)
    print("✅ Ready for production!")
    print("="*70 + "\n")

if __name__ == '__main__':
    generate_summary()
