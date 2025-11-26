#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
INTERACTIVE TRANSLATION TOOL
=============================
Dịch từng entry một với HUMAN CONTROL HOÀN TOÀN
"""

import json
from pathlib import Path

def create_translation_template():
    """
    Tạo file Excel-like để dễ dàng dịch thủ công
    """
    
    input_file = Path(__file__).parent / 'translation_workflow' / '01_CRITICAL_manual_translation.json'
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    entries = data['entries']
    
    # Tạo CSV để import vào Excel/Google Sheets
    output_csv = Path(__file__).parent / 'translation_workflow' / 'CRITICAL_TRANSLATE_ME.csv'
    
    with open(output_csv, 'w', encoding='utf-8-sig') as f:  # utf-8-sig for Excel
        # Header
        f.write("Key,English,Vietnamese (EDIT HERE),Notes\n")
        
        for entry in entries:
            key = entry['key']
            original = entry['original'].replace('[EN] ', '')
            
            # Escape quotes and commas for CSV
            key_esc = key.replace('"', '""')
            orig_esc = original.replace('"', '""').replace('\n', ' ')
            
            f.write(f'"{key_esc}","{orig_esc}","",""\n')
    
    print(f"✅ Created CSV template: {output_csv}")
    print(f"\n📝 How to use:")
    print(f"  1. Open file in Excel/Google Sheets")
    print(f"  2. Fill column 'Vietnamese (EDIT HERE)'")
    print(f"  3. Add notes nếu cần")
    print(f"  4. Save as CSV (UTF-8)")
    print(f"  5. Run: python interactive_translate.py import")

def import_translations_from_csv():
    """
    Import translations từ CSV đã edit
    """
    
    csv_file = Path(__file__).parent / 'translation_workflow' / 'CRITICAL_TRANSLATE_ME.csv'
    
    if not csv_file.exists():
        print("❌ CSV file not found. Run 'create' first.")
        return
    
    import csv
    
    translations = {}
    
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = row['Key']
            vietnamese = row['Vietnamese (EDIT HERE)'].strip()
            
            if vietnamese:  # Only import non-empty translations
                translations[key] = vietnamese
    
    # Load main.i18n.json
    main_file = Path(__file__).parent / 'translations' / 'main.i18n.json'
    
    with open(main_file, 'r', encoding='utf-8') as f:
        main_data = json.load(f)
    
    # Apply translations
    applied = 0
    
    for key, translation in translations.items():
        if key in main_data:
            main_data[key] = translation
            applied += 1
    
    # Save
    with open(main_file, 'w', encoding='utf-8') as f:
        json.dump(main_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Imported {applied} translations into main.i18n.json")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python interactive_translate.py create  - Tạo CSV template")
        print("  python interactive_translate.py import  - Import từ CSV")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'create':
        create_translation_template()
    elif command == 'import':
        import_translations_from_csv()
    else:
        print(f"Unknown command: {command}")
