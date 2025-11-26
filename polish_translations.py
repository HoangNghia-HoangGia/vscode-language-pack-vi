#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
POLISH TRANSLATIONS
===================
Sửa các vấn đề grammar và style nhỏ
"""

import json
import re
from pathlib import Path

def polish_sentence(text: str) -> str:
    """Polish một câu"""
    
    if not text or len(text) < 2:
        return text
    
    # 1. Capitalize đầu câu (chỉ với chữ tiếng Việt)
    if text[0].islower() and text[0].isalpha():
        text = text[0].upper() + text[1:]
    
    # 2. Fix spacing
    text = re.sub(r'\s+', ' ', text)  # Multiple spaces -> single
    text = re.sub(r'\s+\.', '.', text)  # Space before period
    text = re.sub(r'\s+,', ',', text)  # Space before comma
    
    # 3. Fix common Vietnamese grammar
    text = text.replace(' trong trong ', ' trong ')
    text = text.replace(' cho cho ', ' cho ')
    text = text.replace(' và và ', ' và ')
    
    # 4. Fix "cài đặts" -> "cài đặt" (bỏ s thừa)
    text = re.sub(r'cài đặts\b', 'cài đặt', text)
    text = re.sub(r'properties\b', 'thuộc tính', text)
    text = re.sub(r'property\b', 'thuộc tính', text)
    
    # 5. Fix "hợp lệs" -> "hợp lệ"
    text = re.sub(r'hợp lệs\b', 'hợp lệ', text)
    
    # 6. Fix "Inhợp lệ" -> "Không hợp lệ"
    text = text.replace('Inhợp lệ', 'Không hợp lệ')
    text = text.replace('inhợp lệ', 'không hợp lệ')
    
    return text

def polish_all():
    """Polish tất cả translations"""
    
    main_file = Path(__file__).parent / 'translations' / 'main.i18n.json'
    
    with open(main_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    polished = 0
    
    for key, value in data.items():
        if isinstance(value, str) and len(value) > 0:
            original = value
            polished_text = polish_sentence(value)
            
            if polished_text != original:
                data[key] = polished_text
                polished += 1
    
    # Save
    with open(main_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Polished {polished} entries")

if __name__ == '__main__':
    polish_all()
