#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clean AI tags
"""

import json
import re
from pathlib import Path

main_file = Path(__file__).parent / 'translations' / 'main.i18n.json'

with open(main_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

cleaned = 0

for key, value in data.items():
    if isinstance(value, str):
        # Remove [AI] and [AI dịch] tags
        if '[AI]' in value:
            data[key] = re.sub(r'\s*\[AI\].*?\)', '', value).strip()
            data[key] = re.sub(r'\s*\(AI dịch\)', '', data[key]).strip()
            cleaned += 1

with open(main_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ Cleaned {cleaned} [AI] tags")
