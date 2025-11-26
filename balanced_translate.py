#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BALANCED TRANSLATION ENGINE
===========================
Kết hợp:
1. Dictionary terms
2. Simple AI assistance (không phải deep pipeline)
3. Human review checkpoints

KHÔNG dùng AI translation model phức tạp
CHỈ dùng pattern matching + rules
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

# =====================================================================
# TRANSLATION DICTIONARY (đã verify thủ công)
# =====================================================================

TERM_DICT = {
    # Verbs - Actions
    "provides": "cung cấp",
    "enables": "cho phép",
    "disables": "vô hiệu hóa",
    "controls": "điều khiển",
    "configures": "cấu hình",
    "specifies": "chỉ định",
    "defines": "định nghĩa",
    "determines": "xác định",
    "allows": "cho phép",
    "prevents": "ngăn chặn",
    "validates": "kiểm tra tính hợp lệ",
    "checks": "kiểm tra",
    "ensures": "đảm bảo",
    "triggers": "kích hoạt",
    "inserts": "chèn",
    "removes": "xóa",
    "shows": "hiển thị",
    "hides": "ẩn",
    "opens": "mở",
    "closes": "đóng",
    "toggles": "bật/tắt",
    
    # Nouns - UI Elements
    "syntax highlighting": "làm nổi cú pháp",
    "bracket matching": "khớp ngoặc",
    "folding": "gập code",
    "completion": "hoàn thành",
    "validation": "kiểm tra tính hợp lệ",
    "formatting": "định dạng",
    "linting": "kiểm tra lỗi",
    "hover": "đỗ chuột",
    "tooltip": "chú giải công cụ",
    "notification": "thông báo",
    "warning": "cảnh báo",
    "error": "lỗi",
    "message": "thông điệp",
    "prompt": "nhắc nhở",
    "dialog": "hộp thoại",
    "panel": "bảng điều khiển",
    "sidebar": "thanh bên",
    "status bar": "thanh trạng thái",
    "menu": "menu",
    "context menu": "menu ngữ cảnh",
    "command": "lệnh",
    "shortcut": "phím tắt",
    "keybinding": "liên kết phím",
    "setting": "cài đặt",
    "configuration": "cấu hình",
    "preference": "tùy chọn",
    "option": "tùy chọn",
    "property": "thuộc tính",
    "value": "giá trị",
    "parameter": "tham số",
    "argument": "đối số",
    
    # Adjectives
    "default": "mặc định",
    "custom": "tùy chỉnh",
    "automatic": "tự động",
    "manual": "thủ công",
    "enabled": "đã bật",
    "disabled": "đã tắt",
    "required": "bắt buộc",
    "optional": "tùy chọn",
    "valid": "hợp lệ",
    "invalid": "không hợp lệ",
    "unknown": "không xác định",
    "deprecated": "đã lỗi thời",
    "experimental": "thử nghiệm",
    
    # Common phrases
    " and ": " và ",
    " or ": " hoặc ",
    " when ": " khi ",
    " if ": " nếu ",
    " with ": " với ",
    " for ": " cho ",
    " in ": " trong ",
    " on ": " trên ",
    " at ": " tại ",
    " from ": " từ ",
    " to ": " đến ",
    " by ": " bởi ",
    
    # Numbers and lists
    " a list of ": " danh sách ",
    " number of ": " số lượng ",
    " maximum ": " tối đa ",
    " minimum ": " tối thiểu ",
    
    # File related
    " files": " files",
    " file": " file",
    " folder": " folder",
    " directory": " thư mục",
    " path": " đường dẫn",
    " extension": " extension",
}

# Thuật ngữ KHÔNG DỊCH (giữ nguyên)
KEEP_ENGLISH = {
    # Dev terms
    "commit", "push", "pull", "fetch", "merge", "rebase", "branch",
    "debug", "debugger", "breakpoint", "watch",
    "workspace", "repository", "repo",
    "IntelliSense", "snippet", "snippets",
    
    # Technology names
    "Git", "GitHub", "GitLab",
    "CSS", "LESS", "SCSS", "HTML", "JSON", "XML", "YAML",
    "TypeScript", "JavaScript", "Python", "Java", "C#", "C++",
    "Node.js", "npm", "Docker",
    
    # File extensions
    ".js", ".ts", ".py", ".java", ".cpp", ".cs",
    ".html", ".css", ".json", ".xml", ".yaml",
    
    # Placeholders
    "{", "}", "${", "`",
    
    # URLs
    "http://", "https://", "www.",
}

# =====================================================================
# TRANSLATION ENGINE
# =====================================================================

def is_technical_sentence(text: str) -> bool:
    """Kiểm tra xem câu có phải là technical description phức tạp không"""
    
    # Indicators of technical sentence
    indicators = [
        '{', '}',  # Has placeholders
        '`',       # Has code markers
        '(',       # Has parentheses with technical terms
        'http',    # Has URLs
        '  ',      # Multiple spaces (might be code)
    ]
    
    count = sum(1 for ind in indicators if ind in text)
    
    # Also check length
    if len(text) > 200:
        count += 1
    
    return count >= 2

def smart_translate(text: str, context_key: str = "") -> Tuple[str, bool]:
    """
    Dịch thông minh với dictionary
    
    Returns: (translated_text, needs_review)
    """
    
    original = text
    text = text.replace('[EN] ', '')
    
    # Check if too technical → flag for review
    if is_technical_sentence(text):
        return f"[REVIEW] {text}", True
    
    # Apply dictionary translations
    translated = text
    
    for en, vi in TERM_DICT.items():
        # Case-insensitive replacement
        pattern = re.compile(re.escape(en), re.IGNORECASE)
        translated = pattern.sub(vi, translated)
    
    # Check length (tiếng Việt không nên dài hơn 40% tiếng Anh)
    length_ratio = len(translated) / len(text) if len(text) > 0 else 1
    
    needs_review = False
    
    if length_ratio > 1.4:
        needs_review = True
        translated = f"[TOO_LONG] {translated}"
    
    # Check if có dev terms bị dịch nhầm
    for keep_term in KEEP_ENGLISH:
        if keep_term.lower() in text.lower():
            if keep_term.lower() not in translated.lower():
                needs_review = True
                translated = f"[MISSING_TERM:{keep_term}] {translated}"
    
    return translated, needs_review

# =====================================================================
# BATCH PROCESSING với CATEGORIZATION
# =====================================================================

def process_all_entries():
    """
    Process tất cả entries:
    - Auto-translate với dictionary
    - Flag những cái cần review
    - Export ra các file theo priority
    """
    
    main_file = Path(__file__).parent / 'translations' / 'main.i18n.json'
    
    with open(main_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    results = {
        'auto_safe': [],      # Dịch tự động, safe
        'needs_review': [],   # Cần human review
        'keep_english': [],   # Giữ nguyên tiếng Anh
        'already_done': []    # Đã dịch rồi
    }
    
    for key, value in data.items():
        if key == '' or not isinstance(value, str):
            continue
        
        if not value.startswith('[EN]'):
            results['already_done'].append({
                'key': key,
                'translation': value
            })
            continue
        
        # Translate
        translated, needs_review = smart_translate(value, key)
        
        entry = {
            'key': key,
            'original': value,
            'translated': translated,
            'length_en': len(value),
            'length_vi': len(translated)
        }
        
        if needs_review:
            results['needs_review'].append(entry)
        else:
            results['auto_safe'].append(entry)
    
    # Export results
    output_dir = Path(__file__).parent / 'translation_balanced'
    output_dir.mkdir(exist_ok=True)
    
    # 1. Auto-safe (có thể apply ngay)
    with open(output_dir / '01_AUTO_SAFE.json', 'w', encoding='utf-8') as f:
        json.dump({
            '_count': len(results['auto_safe']),
            '_instructions': 'Những translations này SAFE để apply ngay. Đã kiểm tra dictionary.',
            'entries': results['auto_safe']
        }, f, ensure_ascii=False, indent=2)
    
    # 2. Needs review (phải check thủ công)
    with open(output_dir / '02_NEEDS_REVIEW.json', 'w', encoding='utf-8') as f:
        json.dump({
            '_count': len(results['needs_review']),
            '_instructions': 'CẦN REVIEW. Có issue về length hoặc dev terms.',
            'entries': results['needs_review']
        }, f, ensure_ascii=False, indent=2)
    
    # Summary
    print(f"\n{'='*70}")
    print(f"BALANCED TRANSLATION RESULTS")
    print(f"{'='*70}\n")
    print(f"✅ Auto-safe:      {len(results['auto_safe']):4d} entries (ready to apply)")
    print(f"⚠️  Needs review:  {len(results['needs_review']):4d} entries (manual check)")
    print(f"✓  Already done:  {len(results['already_done']):4d} entries")
    print(f"\n📁 Output: {output_dir}")
    print(f"\n🎯 Next steps:")
    print(f"  1. Review entries in 02_NEEDS_REVIEW.json")
    print(f"  2. Fix issues manually")
    print(f"  3. Run: python balanced_translate.py apply")

def apply_safe_translations():
    """Apply các translations đã verify"""
    
    safe_file = Path(__file__).parent / 'translation_balanced' / '01_AUTO_SAFE.json'
    
    if not safe_file.exists():
        print("❌ Run 'process' first")
        return
    
    with open(safe_file, 'r', encoding='utf-8') as f:
        safe_data = json.load(f)
    
    # Load main.i18n.json
    main_file = Path(__file__).parent / 'translations' / 'main.i18n.json'
    
    with open(main_file, 'r', encoding='utf-8') as f:
        main_data = json.load(f)
    
    # Apply
    applied = 0
    
    for entry in safe_data['entries']:
        key = entry['key']
        translated = entry['translated']
        
        # Remove flags if any
        translated = re.sub(r'^\[.*?\]\s*', '', translated)
        
        main_data[key] = translated
        applied += 1
    
    # Save
    with open(main_file, 'w', encoding='utf-8') as f:
        json.dump(main_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Applied {applied} safe translations to main.i18n.json")

# =====================================================================
# CLI
# =====================================================================

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python balanced_translate.py process - Process all entries")
        print("  python balanced_translate.py apply   - Apply safe translations")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'process':
        process_all_entries()
    elif command == 'apply':
        apply_safe_translations()
    else:
        print(f"Unknown command: {command}")
