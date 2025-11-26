#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MANUAL TRANSLATION HELPER
=========================
Tool để hỗ trợ dịch thủ công các CRITICAL entries
Có thể dùng AI để GỢI Ý nhưng cần REVIEW và CHỈNH SỬA
"""

import json
from pathlib import Path
from typing import Dict, List

# =====================================================================
# PRE-DEFINED TRANSLATIONS (Đã được verify)
# =====================================================================

VERIFIED_TRANSLATIONS = {
    # Common patterns
    "Provides syntax highlighting": "Làm nổi cú pháp",
    "Provides snippets": "Cung cấp snippets",
    "bracket matching": "khớp ngoặc",
    "and folding": "và gập code",
    "Language Basics": "Ngôn ngữ cơ bản",
    "Language Features": "Tính năng ngôn ngữ",
    
    # UI terms
    "Controls": "Điều khiển",
    "Enable/disable": "Bật/tắt",
    "validation": "kiểm tra tính hợp lệ",
    "problem severities": "mức độ vấn đề",
    
    # Không dịch
    "CSS": "CSS",
    "LESS": "LESS",
    "SCSS": "SCSS",
    "IntelliSense": "IntelliSense",
    "auto-fixing": "auto-fixing",
    "files": "files",
}

# =====================================================================
# SMART TRANSLATION với PATTERN MATCHING
# =====================================================================

def smart_translate(text: str) -> str:
    """
    Áp dụng các pattern đã verify
    """
    result = text.replace('[EN] ', '')
    
    # Áp dụng verified translations
    for en, vi in VERIFIED_TRANSLATIONS.items():
        result = result.replace(en, vi)
    
    return result

def translate_extension_description(desc: str, lang_name: str) -> str:
    """
    Pattern đặc biệt cho extension descriptions
    
    Pattern: "Provides X, Y and Z in <Lang> files"
    → "Cung cấp X, Y và Z cho files <Lang>"
    """
    desc = desc.replace('[EN] ', '')
    
    # Pattern 1: "Provides X and Y in <Lang> files"
    if desc.startswith("Provides"):
        desc = desc.replace("Provides", "Cung cấp")
        desc = desc.replace(" in ", " cho ")
        desc = desc.replace(" for ", " cho ")
        desc = desc.replace("files.", "files")
    
    # Giữ nguyên các thuật ngữ
    desc = desc.replace("syntax highlighting", "làm nổi cú pháp")
    desc = desc.replace("bracket matching", "khớp ngoặc")
    desc = desc.replace("folding", "gập code")
    desc = desc.replace("snippets", "snippets")
    desc = desc.replace(" and ", " và ")
    desc = desc.replace(" & ", " & ")
    
    # Các pattern phức tạp → giữ nguyên tiếng Anh
    if "debug" in desc.lower() and len(desc) > 100:
        return "[EN] " + desc  # Keep complex debug descriptions in English
    
    return desc

# =====================================================================
# BATCH TRANSLATE với HUMAN REVIEW
# =====================================================================

def translate_critical_batch():
    """Dịch batch CRITICAL entries"""
    
    input_file = Path(__file__).parent / 'translation_workflow' / '01_CRITICAL_manual_translation.json'
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    entries = data['entries']
    
    print(f"\n{'='*70}")
    print(f"TRANSLATING {len(entries)} CRITICAL ENTRIES")
    print(f"{'='*70}\n")
    
    translated_count = 0
    
    # Group by pattern
    extension_descs = []
    
    for entry in entries:
        key = entry['key']
        original = entry['original']
        
        # Extension descriptions
        if '.description' in key and 'extensions/' in key:
            extension_descs.append(entry)
    
    print(f"📦 Extension Descriptions: {len(extension_descs)} entries")
    
    # Translate extension descriptions
    print("\n" + "="*70)
    print("TRANSLATING EXTENSION DESCRIPTIONS")
    print("="*70 + "\n")
    
    for entry in extension_descs[:20]:  # First 20 for demo
        key = entry['key']
        original = entry['original']
        
        # Extract language name from key
        lang_key = key.split('/')[1].split('.')[0]
        
        # Smart translate
        translated = translate_extension_description(original, lang_key)
        
        entry['translated'] = translated
        translated_count += 1
        
        print(f"Key: {key}")
        print(f"EN:  {original}")
        print(f"VI:  {translated}")
        print(f"✓ [OK to use]" if len(translated) < len(original) * 1.4 else "⚠ [TOO LONG - review needed]")
        print("-" * 70 + "\n")
    
    # Save progress
    output_file = Path(__file__).parent / 'translation_workflow' / '01_CRITICAL_TRANSLATED.json'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            '_note': 'Translated entries - REVIEW BEFORE APPLYING',
            '_translated_count': translated_count,
            'entries': entries
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Translated {translated_count} entries")
    print(f"📁 Saved to: {output_file}")
    print(f"\n🎯 Next: REVIEW các translations trong file trên")

# =====================================================================
# APPLY TRANSLATIONS BACK TO main.i18n.json
# =====================================================================

def apply_translations():
    """Áp dụng các translations đã review vào main.i18n.json"""
    
    # Load translated entries
    translated_file = Path(__file__).parent / 'translation_workflow' / '01_CRITICAL_TRANSLATED.json'
    
    if not translated_file.exists():
        print("❌ File 01_CRITICAL_TRANSLATED.json not found. Run translate first.")
        return
    
    with open(translated_file, 'r', encoding='utf-8') as f:
        translated_data = json.load(f)
    
    # Load main.i18n.json
    main_file = Path(__file__).parent / 'translations' / 'main.i18n.json'
    
    with open(main_file, 'r', encoding='utf-8') as f:
        main_data = json.load(f)
    
    # Apply translations
    applied_count = 0
    
    for entry in translated_data['entries']:
        key = entry['key']
        translated = entry.get('translated', '')
        
        if translated and translated != '':
            # Remove [EN] tag
            if not translated.startswith('[EN]'):
                main_data[key] = translated
                applied_count += 1
    
    # Save updated main.i18n.json
    with open(main_file, 'w', encoding='utf-8') as f:
        json.dump(main_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Applied {applied_count} translations to main.i18n.json")
    print(f"📁 Updated: {main_file}")

# =====================================================================
# CLI
# =====================================================================

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python manual_translate_helper.py translate  - Translate critical batch")
        print("  python manual_translate_helper.py apply      - Apply to main.i18n.json")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'translate':
        translate_critical_batch()
    elif command == 'apply':
        apply_translations()
    else:
        print(f"Unknown command: {command}")
