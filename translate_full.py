#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Full Chinese to Vietnamese Translator for VS Code Language Pack
Uses character-by-character replacement with comprehensive mapping
"""

import json
import re
from pathlib import Path

# Load Chinese translation file
zh_file = Path(__file__).parent / r".vscode\extensions\ms-ceintl.vscode-language-pack-zh-hans-1.106.2025111209\translations\main.i18n.json"
vi_output = Path(__file__).parent / "translations" / "main.i18n.json"

# Comprehensive Chinese to Vietnamese phrase mapping
PHRASE_MAP = {
    # Complete UI translations
    "操作": "thao tác",
    "对话框": "hộp thoại", 
    "保留大小写": "Giữ nguyên chữ hoa/thường",
    "辅助": "hỗ trợ",
    "模式": "chế độ",
    "检查": "kiểm tra",
    "用": "dùng",
    "中": "trong",
    "此项": "mục này",
    "更多": "Thêm",
    "切换": "Chuyển đổi",
    "视图": "Chế độ xem",
    "文件": "Tập tin",
    "编辑": "Chỉnh sửa",
    "查看": "Xem",
    "转到": "Đi tới",
    "运行": "Chạy",
    "终端": "Terminal",
    "帮助": "Trợ giúp",
    "打开": "Mở",
    "关闭": "Đóng",
    "保存": "Lưu",
    "另存为": "Lưu thành",
    "全部保存": "Lưu tất cả",
}

def translate_chinese_to_vietnamese(text):
    """Translate Chinese text to Vietnamese using phrase mapping"""
    if not isinstance(text, str):
        return text
    
    # First try exact phrase matches
    for zh, vi in sorted(PHRASE_MAP.items(), key=lambda x: len(x[0]), reverse=True):
        text = text.replace(zh, vi)
    
    # If still contains Chinese characters, keep as is (will be manually reviewed)
    return text

def has_chinese(text):
    """Check if text contains Chinese characters"""
    if not isinstance(text, str):
        return False
    return bool(re.search(r'[\u4e00-\u9fff]', text))

def process_translations(data, parent_key=""):
    """Recursively translate all Chinese text to Vietnamese"""
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            result[key] = process_translations(value, f"{parent_key}.{key}" if parent_key else key)
        return result
    elif isinstance(data, list):
        return [process_translations(item, f"{parent_key}[{i}]") for i, item in enumerate(data)]
    elif isinstance(data, str):
        translated = translate_chinese_to_vietnamese(data)
        return translated
    else:
        return data

# Check if Chinese language pack exists
if not zh_file.exists():
    # Try to find it in user profile
    import os
    user_profile = os.path.expanduser("~")
    zh_file = Path(user_profile) / r".vscode\extensions\ms-ceintl.vscode-language-pack-zh-hans-1.106.2025111209\translations\main.i18n.json"
    
    if not zh_file.exists():
        print(f"ERROR: Chinese language pack not found at: {zh_file}")
        print("Please install Chinese Language Pack first: code --install-extension MS-CEINTL.vscode-language-pack-zh-hans")
        exit(1)

print(f"Loading Chinese translations from: {zh_file}")
with open(zh_file, 'r', encoding='utf-8') as f:
    zh_data = json.load(f)

print("Translating Chinese to Vietnamese...")
vi_data = process_translations(zh_data)

# Count translations
total_keys = 0
chinese_remaining = 0

def count_keys(data):
    global total_keys, chinese_remaining
    if isinstance(data, dict):
        for value in data.values():
            count_keys(value)
    elif isinstance(data, list):
        for item in data:
            count_keys(item)
    elif isinstance(data, str):
        total_keys += 1
        if has_chinese(data):
            chinese_remaining += 1

count_keys(vi_data)

print(f"\nTranslation Statistics:")
print(f"  Total strings: {total_keys}")
print(f"  Chinese remaining: {chinese_remaining}")
print(f"  Vietnamese coverage: {((total_keys - chinese_remaining) / total_keys * 100):.1f}%")

# Backup original
if vi_output.exists():
    backup = vi_output.with_suffix('.json.backup2')
    print(f"\nBacking up original to: {backup}")
    vi_output.rename(backup)

# Save Vietnamese translations
print(f"Saving Vietnamese translations to: {vi_output}")
vi_output.parent.mkdir(parents=True, exist_ok=True)
with open(vi_output, 'w', encoding='utf-8') as f:
    json.dump(vi_data, f, ensure_ascii=False, indent=2)

file_size = vi_output.stat().st_size
print(f"\nSuccess! Generated {file_size / 1024:.0f}KB Vietnamese translation file")
print(f"\nNext steps:")
print(f"  1. Review translations with Chinese characters")
print(f"  2. Run: vsce package")
print(f"  3. Install: code --install-extension vscode-language-pack-vi-*.vsix --force")
