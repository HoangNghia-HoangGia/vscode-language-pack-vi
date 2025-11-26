#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PROPER SOLUTION: Get English strings from VS Code official source
Then translate EN → VI properly, not CN → VI
"""

import json
import re
from pathlib import Path
import urllib.request

def download_official_english():
    """
    Download official English language files from VS Code repo
    This is the CORRECT way - no copyright issues
    """
    # VS Code uses English as default, we need to get it from their repo
    url = "https://raw.githubusercontent.com/microsoft/vscode/main/i18n/vscode-language-pack-en/translations/main.i18n.json"
    
    try:
        print(f"Downloading official English keys from VS Code repo...")
        with urllib.request.urlopen(url) as response:
            data = response.read()
            return json.loads(data)
    except Exception as e:
        print(f"Failed to download: {e}")
        return None

def create_vietnamese_from_english(en_data):
    """
    Create Vietnamese translation template from English
    This needs manual translation or AI assistance (EN → VI)
    """
    def translate_en_to_vi(text):
        # TODO: Implement proper EN → VI translation
        # For now, mark for manual translation
        return f"[VI_TODO: {text}]"
    
    def process(obj):
        if isinstance(obj, dict):
            return {k: process(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [process(item) for item in obj]
        elif isinstance(obj, str):
            return translate_en_to_vi(obj)
        else:
            return obj
    
    return process(en_data)

if __name__ == "__main__":
    print("="*60)
    print("PROPER VIETNAMESE LANGUAGE PACK GENERATION")
    print("Source: Official VS Code English → Vietnamese")
    print("="*60)
    print()
    
    # Try to download official English
    en_data = download_official_english()
    
    if en_data:
        print("✅ Got official English keys!")
        
        # Create Vietnamese template
        vi_template = create_vietnamese_from_english(en_data)
        
        # Save
        output = Path(__file__).parent / "translations" / "main.i18n.json.en_template"
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(vi_template, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Saved to: {output}")
        print()
        print("Next steps:")
        print("1. Use AI or professional translator for EN → VI")
        print("2. Review and correct translations")
        print("3. No copyright issues!")
    else:
        print("❌ Could not get official English source")
        print()
        print("Alternative approach:")
        print("1. Use Chinese pack structure only (for keys)")
        print("2. Look up English text from VS Code docs")
        print("3. Translate EN → VI manually")
        print()
        print("Current file has mixed Chinese - needs cleanup!")
