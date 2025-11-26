#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LEGAL APPROACH: Extract English strings from VS Code Official Source
Source: https://github.com/microsoft/vscode
NO Chinese pack dependency!
"""

import json
import subprocess
from pathlib import Path

def clone_vscode_source():
    """Clone VS Code official repository"""
    vscode_dir = Path(__file__).parent / "vscode-source"
    
    if vscode_dir.exists():
        print(f"✅ VS Code source already exists at {vscode_dir}")
        return vscode_dir
    
    print("📦 Cloning VS Code official repository...")
    print("⏳ This will take a few minutes...")
    
    try:
        subprocess.run([
            "git", "clone", 
            "--depth", "1",  # Shallow clone for speed
            "https://github.com/microsoft/vscode.git",
            str(vscode_dir)
        ], check=True)
        print("✅ Clone successful!")
        return vscode_dir
    except Exception as e:
        print(f"❌ Failed to clone: {e}")
        return None

def extract_nls_files(vscode_dir):
    """
    Extract all NLS (National Language Support) files from VS Code source
    These contain the English strings we need
    """
    nls_files = []
    
    # VS Code stores strings in .nls.json files
    for nls_file in vscode_dir.rglob("*.nls.json"):
        nls_files.append(nls_file)
    
    print(f"Found {len(nls_files)} NLS files")
    return nls_files

def build_english_base(nls_files):
    """
    Build comprehensive English base from NLS files
    This is the LEGAL source for translation
    """
    english_base = {}
    
    for nls_file in nls_files:
        try:
            with open(nls_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Get relative path as key prefix
            rel_path = nls_file.relative_to(nls_file.parents[2])
            prefix = str(rel_path).replace('\\', '/').replace('.nls.json', '')
            
            # Add to base
            if isinstance(data, dict):
                for key, value in data.items():
                    full_key = f"{prefix}/{key}"
                    english_base[full_key] = value
        except Exception as e:
            print(f"Warning: Could not process {nls_file}: {e}")
    
    return english_base

if __name__ == "__main__":
    print("="*70)
    print("🇻🇳 VIETNAMESE LANGUAGE PACK - LEGAL APPROACH")
    print("="*70)
    print()
    print("📖 Source: VS Code Official Repository (English)")
    print("🚫 NO Chinese pack dependency")
    print("✅ 100% Legal & Proper")
    print()
    
    # Step 1: Clone VS Code
    vscode_dir = clone_vscode_source()
    
    if not vscode_dir:
        print("❌ Cannot proceed without VS Code source")
        exit(1)
    
    # Step 2: Extract NLS files
    nls_files = extract_nls_files(vscode_dir)
    
    if not nls_files:
        print("❌ No NLS files found")
        exit(1)
    
    # Step 3: Build English base
    print(f"📝 Processing {len(nls_files)} NLS files...")
    english_base = build_english_base(nls_files)
    
    print(f"✅ Extracted {len(english_base)} English strings")
    
    # Step 4: Save English base
    output = Path(__file__).parent / "english_base.json"
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(english_base, f, ensure_ascii=False, indent=2)
    
    print(f"💾 Saved to: {output}")
    print()
    print("🎯 Next steps:")
    print("1. Review english_base.json")
    print("2. Translate EN → VI (using AI or manual)")
    print("3. Build final main.i18n.json")
    print()
    print("✅ All legal! No copyright issues!")
