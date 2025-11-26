#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FIX REVIEW ENTRIES
==================
Fix các entries bị flag TOO_LONG hoặc REVIEW
"""

import json
import re
from pathlib import Path

# Manual fixes cho các entries có vấn đề
MANUAL_FIXES = {
    "extensions/css-language-features.css.lint.unknownAtRules.desc": 
        "At-rule không xác định",
    
    "extensions/css-language-features.css.lint.unknownProperties.desc": 
        "Thuộc tính không xác định",
    
    "extensions/css-language-features.css.validate.desc": 
        "Bật/tắt kiểm tra tính hợp lệ",
    
    "extensions/css-language-features.css.lint.unknownVendorSpecificProperties.desc":
        "Thuộc tính vendor không xác định",
    
    "extensions/css-language-features.less.lint.unknownAtRules.desc":
        "At-rule không xác định",
    
    "extensions/css-language-features.less.lint.unknownProperties.desc":
        "Thuộc tính không xác định",
    
    "extensions/css-language-features.less.lint.unknownVendorSpecificProperties.desc":
        "Thuộc tính vendor không xác định",
    
    "extensions/css-language-features.less.validate.desc":
        "Bật/tắt kiểm tra tính hợp lệ",
    
    "extensions/css-language-features.scss.lint.unknownAtRules.desc":
        "At-rule không xác định",
    
    "extensions/css-language-features.scss.lint.unknownProperties.desc":
        "Thuộc tính không xác định",
    
    "extensions/css-language-features.scss.lint.unknownVendorSpecificProperties.desc":
        "Thuộc tính vendor không xác định",
    
    "extensions/css-language-features.scss.validate.desc":
        "Bật/tắt kiểm tra tính hợp lệ",
}

# Các pattern dịch ngắn gọn hơn
SHORT_PATTERNS = {
    "Enables or disables": "Bật/tắt",
    "Enable or disable": "Bật/tắt",
    "Enable/disable": "Bật/tắt",
    "all validations": "kiểm tra tính hợp lệ",
    "Unknown ": "",  # Bỏ "Unknown" để ngắn hơn
    "not validated": "không kiểm tra",
}

def fix_review_entries():
    """Fix các entries cần review"""
    
    review_file = Path(__file__).parent / 'translation_balanced' / '02_NEEDS_REVIEW.json'
    
    with open(review_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    fixed_count = 0
    still_need_review = []
    
    for entry in data['entries']:
        key = entry['key']
        original = entry['original']
        translated = entry['translated']
        
        # Check if có manual fix
        if key in MANUAL_FIXES:
            entry['translated'] = MANUAL_FIXES[key]
            entry['fixed'] = True
            fixed_count += 1
            continue
        
        # Remove flags
        translated_clean = re.sub(r'^\[(TOO_LONG|REVIEW|MISSING_TERM:[^\]]+)\]\s*', '', translated)
        
        # Nếu là REVIEW do có backticks/technical → giữ nguyên tiếng Anh
        if '[REVIEW]' in translated and ('`' in original or '{' in original):
            entry['translated'] = original.replace('[EN] ', '')
            entry['note'] = 'Keep English (technical content)'
            entry['fixed'] = True
            fixed_count += 1
            continue
        
        # Áp dụng short patterns
        for en, vi in SHORT_PATTERNS.items():
            translated_clean = translated_clean.replace(en, vi)
        
        # Check length lại
        original_len = len(original.replace('[EN] ', ''))
        new_len = len(translated_clean)
        
        if new_len <= original_len * 1.35:  # OK nếu chỉ dài hơn 35%
            entry['translated'] = translated_clean
            entry['fixed'] = True
            fixed_count += 1
        else:
            # Vẫn còn quá dài → giữ tiếng Anh
            entry['translated'] = original.replace('[EN] ', '')
            entry['note'] = 'Keep English (too long when translated)'
            entry['fixed'] = True
            fixed_count += 1
    
    # Save fixed entries
    fixed_file = Path(__file__).parent / 'translation_balanced' / '02_NEEDS_REVIEW_FIXED.json'
    
    with open(fixed_file, 'w', encoding='utf-8') as f:
        json.dump({
            '_count': len(data['entries']),
            '_fixed': fixed_count,
            '_instructions': 'Các entries đã được fix. Review và apply.',
            'entries': data['entries']
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Fixed {fixed_count}/{len(data['entries'])} entries")
    print(f"📁 Output: {fixed_file}")
    print(f"\n🎯 Next: Review file trên và run: python balanced_translate.py apply_all")

def apply_all_translations():
    """Apply tất cả translations (safe + fixed)"""
    
    # Load main.i18n.json
    main_file = Path(__file__).parent / 'translations' / 'main.i18n.json'
    
    with open(main_file, 'r', encoding='utf-8') as f:
        main_data = json.load(f)
    
    total_applied = 0
    
    # 1. Apply AUTO_SAFE
    safe_file = Path(__file__).parent / 'translation_balanced' / '01_AUTO_SAFE.json'
    
    with open(safe_file, 'r', encoding='utf-8') as f:
        safe_data = json.load(f)
    
    for entry in safe_data['entries']:
        key = entry['key']
        translated = re.sub(r'^\[.*?\]\s*', '', entry['translated'])
        main_data[key] = translated
        total_applied += 1
    
    print(f"✅ Applied {len(safe_data['entries'])} AUTO_SAFE entries")
    
    # 2. Apply FIXED
    fixed_file = Path(__file__).parent / 'translation_balanced' / '02_NEEDS_REVIEW_FIXED.json'
    
    if fixed_file.exists():
        with open(fixed_file, 'r', encoding='utf-8') as f:
            fixed_data = json.load(f)
        
        for entry in fixed_data['entries']:
            if entry.get('fixed', False):
                key = entry['key']
                translated = re.sub(r'^\[.*?\]\s*', '', entry['translated'])
                main_data[key] = translated
                total_applied += 1
        
        print(f"✅ Applied {fixed_data['_fixed']} FIXED entries")
    
    # Save updated main.i18n.json
    with open(main_file, 'w', encoding='utf-8') as f:
        json.dump(main_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n🎉 TOTAL: Applied {total_applied} translations to main.i18n.json")
    
    # Check how many left
    remaining = sum(1 for v in main_data.values() if isinstance(v, str) and v.startswith('[EN]'))
    print(f"📊 Remaining [EN] entries: {remaining}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python fix_review.py fix       - Fix review entries")
        print("  python fix_review.py apply_all - Apply all translations")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'fix':
        fix_review_entries()
    elif command == 'apply_all':
        apply_all_translations()
    else:
        print(f"Unknown command: {command}")
