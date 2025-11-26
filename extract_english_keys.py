#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract English keys from VS Code localization files
Instead of using Chinese pack, we'll use the official English source
"""

import json
import re
from pathlib import Path

def extract_english_keys_from_chinese():
    """
    Extract key structure from Chinese pack, but keep English text as reference
    This gives us the proper key structure without copyright issues
    """
    zh_ext = r"ms-ceintl.vscode-language-pack-zh-hans-1.106.2025111209"
    zh_file = Path.home() / f".vscode/extensions/{zh_ext}/translations/main.i18n.json"
    
    if not zh_file.exists():
        print(f"ERROR: {zh_file} not found!")
        return None
    
    with open(zh_file, 'r', encoding='utf-8') as f:
        zh_data = json.load(f)
    
    # Extract only the key structure, not the translations
    return extract_keys(zh_data)

def extract_keys(obj, keys=None):
    """Extract all keys from nested dict"""
    if keys is None:
        keys = set()
    
    if isinstance(obj, dict):
        for key, value in obj.items():
            keys.add(key)
            if isinstance(value, (dict, list)):
                extract_keys(value, keys)
    elif isinstance(obj, list):
        for item in obj:
            extract_keys(item, keys)
    
    return keys

def create_template_from_structure(zh_data):
    """
    Create a template with English placeholders
    This is for manual translation EN → VI
    """
    def process(obj):
        if isinstance(obj, dict):
            return {k: process(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [process(item) for item in obj]
        elif isinstance(obj, str):
            # Replace with English placeholder for manual review
            return "[EN: TO BE TRANSLATED]"
        else:
            return obj
    
    return process(zh_data)

if __name__ == "__main__":
    print("Extracting key structure from Chinese pack...")
    print("(We'll use structure only, not translations)")
    
    zh_ext = r"ms-ceintl.vscode-language-pack-zh-hans-1.106.2025111209"
    zh_file = Path.home() / f".vscode/extensions/{zh_ext}/translations/main.i18n.json"
    
    if not zh_file.exists():
        print(f"ERROR: {zh_file} not found!")
        print("Please install Chinese language pack first:")
        print("  code --install-extension ms-ceintl.vscode-language-pack-zh-hans")
        exit(1)
    
    with open(zh_file, 'r', encoding='utf-8') as f:
        zh_data = json.load(f)
    
    # Extract keys
    keys = extract_keys(zh_data)
    print(f"Found {len(keys)} unique keys")
    
    # Save key list for reference
    keys_file = Path(__file__).parent / "vscode_keys_reference.txt"
    with open(keys_file, 'w', encoding='utf-8') as f:
        for key in sorted(keys):
            f.write(f"{key}\n")
    
    print(f"Saved key list to: {keys_file}")
    
    # Create template
    template = create_template_from_structure(zh_data)
    template_file = Path(__file__).parent / "translations" / "main.i18n.json.template"
    
    with open(template_file, 'w', encoding='utf-8') as f:
        json.dump(template, f, ensure_ascii=False, indent=2)
    
    print(f"Created translation template: {template_file}")
    print("\nNext steps:")
    print("1. Get official English source from VS Code GitHub")
    print("2. Use proper EN → VI translation")
    print("3. Manual review and corrections")
