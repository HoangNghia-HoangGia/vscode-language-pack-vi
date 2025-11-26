#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Dịch main.i18n.json CÓ KIỂM SOÁT
========================================
Tuân thủ 3 nguyên tắc:
1. Không dịch sai thuật ngữ dev
2. Không phá layout UI
3. Không dịch bằng AI mà không review

Workflow:
- Phân loại entries: Critical | Medium | Simple
- Critical: Yêu cầu dịch thủ công (export ra file riêng)
- Medium: AI dịch + Flag để human review
- Simple: AI dịch với validation tự động
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Set
from collections import defaultdict

# =====================================================================
# 1. LOAD DEV TERMS DICTIONARY
# =====================================================================

def load_dev_terms() -> Dict:
    """Load danh sách thuật ngữ không được dịch"""
    dict_path = Path(__file__).parent / "dev_terms_dictionary.json"
    with open(dict_path, 'r', encoding='utf-8') as f:
        return json.load(f)

DEV_DICT = load_dev_terms()

# Tạo set tất cả terms cần bảo vệ (lowercase để check case-insensitive)
PROTECTED_TERMS = set()
for category in ['git_terms', 'debug_terms', 'vscode_core_terms', 
                  'programming_terms', 'file_system_terms', 'ui_action_terms']:
    PROTECTED_TERMS.update(term.lower() for term in DEV_DICT.get(category, []))

for term in DEV_DICT.get('compound_terms_do_not_split', []):
    PROTECTED_TERMS.add(term.lower())

for acronym in DEV_DICT.get('acronyms_keep_uppercase', []):
    PROTECTED_TERMS.add(acronym.lower())

# =====================================================================
# 2. CLASSIFICATION LOGIC
# =====================================================================

CRITICAL_PATTERNS = [
    # UI Core elements
    r'extensions/(git|github|markdown|typescript|javascript|python|cpp|java|csharp|php|ruby|go|rust)/',
    # Commands và menus
    r'\.(command|menu|title|category|description)$',
    # Error và warning messages
    r'\.(error|warning|info|notification)\.',
    # Keybindings
    r'keyboard\.',
    r'keybinding\.',
    # Settings quan trọng
    r'workbench\.action\.',
    r'editor\.(action|command)\.',
]

SIMPLE_PATTERNS = [
    # Display names đơn giản
    r'extensions/[^/]+\.displayName$',
    # Descriptions đơn giản không có placeholder
    r'extensions/[^/]+\.description$',
    # Language basics
    r'Language Basics$',
    r'syntax highlighting$',
]

def classify_entry(key: str, value) -> str:
    """
    Phân loại entry thành: critical | medium | simple
    """
    # Skip non-string values (như header list)
    if not isinstance(value, str):
        return 'skip'
    
    # Skip đã dịch
    if not value.startswith('[EN]'):
        return 'translated'
    
    # Critical: Cần dịch thủ công
    for pattern in CRITICAL_PATTERNS:
        if re.search(pattern, key):
            return 'critical'
    
    # Simple: Không có placeholder, không có dev terms phức tạp
    has_placeholder = '{' in value or '`' in value
    has_markdown = '[' in value and '](' in value
    has_complex_punctuation = '|' in value or '...' in value
    
    if not has_placeholder and not has_markdown and not has_complex_punctuation:
        for pattern in SIMPLE_PATTERNS:
            if re.search(pattern, key):
                return 'simple'
    
    # Còn lại: Medium (cần AI + review)
    return 'medium'

# =====================================================================
# 3. VALIDATION FUNCTIONS
# =====================================================================

def check_dev_terms_violation(original: str, translated: str) -> List[str]:
    """Kiểm tra xem có dịch sai thuật ngữ dev không"""
    violations = []
    
    # Extract terms from original (case-insensitive)
    original_lower = original.lower()
    
    for term in PROTECTED_TERMS:
        # Nếu term xuất hiện trong original
        if term in original_lower:
            # Kiểm tra xem translated có GIỮ NGUYÊN term không
            if term not in translated.lower():
                violations.append(f"Term '{term}' bị mất hoặc dịch sai")
    
    return violations

def check_ui_length(original: str, translated: str, context_key: str) -> List[str]:
    """Kiểm tra độ dài UI"""
    issues = []
    
    # Xác định loại UI element từ key
    max_length = 200  # default
    
    if '.title' in context_key or '.menu' in context_key:
        max_length = 40
    elif '.command' in context_key:
        max_length = 50
    elif '.label' in context_key:
        max_length = 30
    
    # Tiếng Việt thường dài hơn tiếng Anh 20-30%
    expected_max = len(original) * 1.3
    
    if len(translated) > max(max_length, expected_max):
        issues.append(f"Quá dài: {len(translated)} chars (max ~{int(expected_max)})")
    
    return issues

def check_placeholder_integrity(original: str, translated: str) -> List[str]:
    """Kiểm tra placeholder {0}, {1}, {variable} không bị sửa"""
    issues = []
    
    # Extract placeholders from original
    original_placeholders = set(re.findall(r'\{[^\}]+\}', original))
    translated_placeholders = set(re.findall(r'\{[^\}]+\}', translated))
    
    missing = original_placeholders - translated_placeholders
    extra = translated_placeholders - original_placeholders
    
    if missing:
        issues.append(f"Thiếu placeholder: {missing}")
    if extra:
        issues.append(f"Placeholder thừa: {extra}")
    
    return issues

def validate_translation(key: str, original: str, translated: str) -> Tuple[bool, List[str]]:
    """
    Validate toàn bộ translation
    Returns: (is_valid, list_of_issues)
    """
    issues = []
    
    # Check 1: Dev terms
    dev_violations = check_dev_terms_violation(original, translated)
    issues.extend(dev_violations)
    
    # Check 2: UI length
    length_issues = check_ui_length(original, translated, key)
    issues.extend(length_issues)
    
    # Check 3: Placeholders
    placeholder_issues = check_placeholder_integrity(original, translated)
    issues.extend(placeholder_issues)
    
    is_valid = len(issues) == 0
    return is_valid, issues

# =====================================================================
# 4. MAIN PROCESSING
# =====================================================================

def analyze_main_i18n(input_file: str):
    """Phân tích main.i18n.json và phân loại các entries"""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Statistics
    stats = defaultdict(int)
    categorized = {
        'critical': [],
        'medium': [],
        'simple': [],
        'translated': []
    }
    
    for key, value in data.items():
        if key == '':  # Skip header
            continue
        
        category = classify_entry(key, value)
        
        if category == 'skip':  # Skip non-string values
            continue
        
        stats[category] += 1
        
        categorized[category].append({
            'key': key,
            'original': value,
            'translated': '',
            'needs_review': False,
            'validation_issues': []
        })
    
    # Export kết quả
    output_dir = Path(__file__).parent / 'translation_workflow'
    output_dir.mkdir(exist_ok=True)
    
    # 1. Critical entries - Cần dịch thủ công
    critical_file = output_dir / '01_CRITICAL_manual_translation.json'
    with open(critical_file, 'w', encoding='utf-8') as f:
        json.dump({
            '_instructions': 'Dịch thủ công các entries này. Đây là phần QUAN TRỌNG nhất.',
            '_count': len(categorized['critical']),
            'entries': categorized['critical']
        }, f, ensure_ascii=False, indent=2)
    
    # 2. Medium entries - AI + review
    medium_file = output_dir / '02_MEDIUM_ai_with_review.json'
    with open(medium_file, 'w', encoding='utf-8') as f:
        json.dump({
            '_instructions': 'AI dịch nhưng CẦN REVIEW. Check kỹ dev terms và UI length.',
            '_count': len(categorized['medium']),
            'entries': categorized['medium']
        }, f, ensure_ascii=False, indent=2)
    
    # 3. Simple entries - AI tự động
    simple_file = output_dir / '03_SIMPLE_ai_auto.json'
    with open(simple_file, 'w', encoding='utf-8') as f:
        json.dump({
            '_instructions': 'AI dịch tự động với validation. Vẫn nên spot-check.',
            '_count': len(categorized['simple']),
            'entries': categorized['simple']
        }, f, ensure_ascii=False, indent=2)
    
    # 4. Summary report
    summary_file = output_dir / '00_SUMMARY.txt'
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("MAIN.I18N.JSON TRANSLATION WORKFLOW SUMMARY\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Total entries to translate: {sum(stats[k] for k in ['critical', 'medium', 'simple'])}\n\n")
        f.write(f"CRITICAL (manual translation):  {stats['critical']:4d} entries\n")
        f.write(f"MEDIUM (AI + review):           {stats['medium']:4d} entries\n")
        f.write(f"SIMPLE (AI auto):               {stats['simple']:4d} entries\n")
        f.write(f"Already translated:             {stats['translated']:4d} entries\n")
        f.write("\n" + "=" * 70 + "\n")
        f.write("WORKFLOW:\n")
        f.write("=" * 70 + "\n")
        f.write("1. Start với 01_CRITICAL_manual_translation.json\n")
        f.write("   → Dịch thủ công từng entry\n")
        f.write("   → Đảm bảo dev terms chính xác\n")
        f.write("   → Đảm bảo UI không bị vỡ layout\n\n")
        f.write("2. Process 02_MEDIUM_ai_with_review.json\n")
        f.write("   → Có thể dùng AI hỗ trợ\n")
        f.write("   → NHƯNG phải review từng entry\n")
        f.write("   → Flag các entry nghi ngờ\n\n")
        f.write("3. Process 03_SIMPLE_ai_auto.json\n")
        f.write("   → AI dịch với validation tự động\n")
        f.write("   → Spot-check 10-20% để đảm bảo\n\n")
        f.write("4. Merge results back to main.i18n.json\n")
        f.write("   → Run validation script\n")
        f.write("   → Fix all issues\n")
        f.write("   → Test trong VS Code\n")
    
    print(f"\n✅ Phân tích hoàn tất!")
    print(f"📁 Output directory: {output_dir}")
    print(f"\n📊 Statistics:")
    print(f"   Critical: {stats['critical']} entries (cần dịch thủ công)")
    print(f"   Medium:   {stats['medium']} entries (AI + review)")
    print(f"   Simple:   {stats['simple']} entries (AI auto)")
    print(f"   Done:     {stats['translated']} entries (đã dịch)")
    print(f"\n🎯 Next step: Bắt đầu với file 01_CRITICAL_manual_translation.json")

# =====================================================================
# 5. HELPER: SIMPLE AI TRANSLATOR (với validation)
# =====================================================================

def simple_translate_with_validation(entries: List[Dict]) -> List[Dict]:
    """
    Dịch simple entries bằng quy tắc đơn giản (không dùng AI phức tạp)
    Chỉ dịch những pattern an toàn
    """
    
    # Simple translation rules
    simple_rules = {
        'Language Basics': 'Ngôn ngữ cơ bản',
        'Provides syntax highlighting': 'Cung cấp làm nổi cú pháp',
        'Provides snippets': 'Cung cấp snippets',
        'bracket matching': 'khớp ngoặc',
        'and folding': 'và gập code',
        'in files': 'trong files',
    }
    
    results = []
    for entry in entries:
        original = entry['original'].replace('[EN] ', '')
        translated = original
        
        # Áp dụng simple rules
        for en, vi in simple_rules.items():
            translated = translated.replace(en, vi)
        
        # Validate
        is_valid, issues = validate_translation(entry['key'], original, translated)
        
        entry['translated'] = translated
        entry['needs_review'] = not is_valid
        entry['validation_issues'] = issues
        
        results.append(entry)
    
    return results

# =====================================================================
# 6. CLI
# =====================================================================

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python translate_controlled.py <command>")
        print("Commands:")
        print("  analyze - Phân tích và phân loại entries")
        print("  validate <file> - Validate một translation file")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'analyze':
        input_file = Path(__file__).parent / 'translations' / 'main.i18n.json'
        analyze_main_i18n(str(input_file))
    
    elif command == 'validate':
        if len(sys.argv) < 3:
            print("Usage: python translate_controlled.py validate <translation_file>")
            sys.exit(1)
        
        # TODO: Implement validation của translation file
        print("Validation feature - Coming soon")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
