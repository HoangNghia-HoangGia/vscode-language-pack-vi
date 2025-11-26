#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto-translate Chinese to Vietnamese using Google Translate
Requires: pip install deep-translator
"""

import json
import re
from pathlib import Path
from deep_translator import GoogleTranslator

# Paths
zh_ext = r"ms-ceintl.vscode-language-pack-zh-hans-1.106.2025111209"
zh_file = Path.home() / f".vscode/extensions/{zh_ext}/translations/main.i18n.json"
vi_output = Path(__file__).parent / "translations" / "main.i18n.json"

def has_chinese(text):
    """Check if text contains Chinese characters"""
    return bool(re.search(r'[\u4e00-\u9fff]', str(text)))

def translate_text(text):
    """Translate Chinese to Vietnamese"""
    if not isinstance(text, str) or not has_chinese(text):
        return text
    
    try:
        # Translate Chinese to Vietnamese
        translator = GoogleTranslator(source='zh-CN', target='vi')
        result = translator.translate(text)
        return result
    except Exception as e:
        print(f"Translation error: {text[:50]}... => {e}")
        return text

def process_translations(data, depth=0):
    """Recursively translate all strings"""
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            result[key] = process_translations(value, depth+1)
        return result
    elif isinstance(data, list):
        return [process_translations(item, depth+1) for item in data]
    elif isinstance(data, str):
        return translate_text(data)
    else:
        return data

if __name__ == "__main__":
    if not zh_file.exists():
        print(f"ERROR: {zh_file} not found!")
        exit(1)
    
    print("Loading Chinese translations...")
    with open(zh_file, 'r', encoding='utf-8') as f:
        zh_data = json.load(f)
    
    print("Translating to Vietnamese (this may take a while)...")
    vi_data = process_translations(zh_data)
    
    # Backup
    if vi_output.exists():
        vi_output.rename(vi_output.with_suffix('.json.backup3'))
    
    # Save
    print(f"Saving to {vi_output}...")
    with open(vi_output, 'w', encoding='utf-8') as f:
        json.dump(vi_data, f, ensure_ascii=False, indent=2)
    
    print(f"Done! {vi_output.stat().st_size/1024:.0f}KB")
