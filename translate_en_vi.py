#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI-Assisted Translation System with Quality Tags
Architecture: Dictionary-first, AI-assisted, Human-reviewable
Tags: [DICT] for dictionary, [AI] for AI-generated
"""

import json
import re
from pathlib import Path

# Translation dictionary (will expand this)
EN_TO_VI = {
    # Common UI terms
    "File": "Tập tin",
    "Edit": "Chỉnh sửa", 
    "View": "Xem",
    "Go": "Đi tới",
    "Run": "Chạy",
    "Terminal": "Terminal",
    "Help": "Trợ giúp",
    "Open": "Mở",
    "Save": "Lưu",
    "Close": "Đóng",
    "New": "Mới",
    "Settings": "Cài đặt",
    "Extensions": "Tiện ích mở rộng",
    "Search": "Tìm kiếm",
    "Replace": "Thay thế",
    "Find": "Tìm",
    "Debug": "Gỡ lỗi",
    "Source Control": "Kiểm soát mã nguồn",
    "Problems": "Vấn đề",
    "Output": "Đầu ra",
    "Preferences": "Tùy chọn",
    "Keyboard Shortcuts": "Phím tắt",
    "User": "Người dùng",
    "Workspace": "Không gian làm việc",
    "Folder": "Thư mục",
    "Explorer": "Trình khám phá",
    "Language": "Ngôn ngữ",
    
    # Actions
    "Open File": "Mở tập tin",
    "Save As": "Lưu thành",
    "Save All": "Lưu tất cả",
    "Close All": "Đóng tất cả",
    "New File": "Tập tin mới",
    "New Folder": "Thư mục mới",
    "Copy": "Sao chép",
    "Paste": "Dán",
    "Cut": "Cắt",
    "Undo": "Hoàn tác",
    "Redo": "Làm lại",
    
    # Status
    "Loading": "Đang tải",
    "Saving": "Đang lưu",
    "Error": "Lỗi",
    "Warning": "Cảnh báo",
    "Success": "Thành công",
    "Failed": "Thất bại",
    "Completed": "Hoàn thành",
    
    # Extended - Programming languages
    "Provides snippets, syntax highlighting, bracket matching and folding": "Cung cấp đoạn mã, tô sáng cú pháp, khớp ngoặc và gấp mã",
    "Language Basics": "Ngôn ngữ cơ bản",
}

def ai_translate(text):
    """
    Placeholder for AI translation
    In production: call OpenAI/Anthropic API
    For now: return marked placeholder
    """
    # TODO: Integrate with AI API
    # Example: openai.ChatCompletion.create(...)
    return f"[NEEDS_AI] {text}"

def translate_string(text, use_ai=False):
    """
    Translate English string to Vietnamese
    Strategy:
    1. Try dictionary first → [DICT] tag
    2. If not found and use_ai=True → AI translate → [AI] tag
    3. Otherwise → [TODO] tag
    """
    if not isinstance(text, str):
        # Handle lists and other types
        if isinstance(text, list):
            return [translate_string(item, use_ai) for item in text]
        return text
    
    # Remove [EN] marker
    original = text.replace("[EN] ", "")
    
    # Try exact match first
    if original in EN_TO_VI:
        return f"[DICT] {EN_TO_VI[original]}"
    
    # Try case-insensitive match
    for en, vi in EN_TO_VI.items():
        if original.lower() == en.lower():
            return f"[DICT] {vi}"
    
    # AI translation if enabled
    if use_ai:
        vi_text = ai_translate(original)
        return f"[AI] {vi_text}"
    
    # Mark for manual review
    return f"[TODO] {original}"

def translate_layer(input_file, output_file, use_ai=False):
    """
    Translate a priority layer
    Tags output with [DICT], [AI], or [TODO]
    """
    print(f"\n{'='*70}")
    print(f"📖 DỊCH: {Path(input_file).name}")
    print(f"{'='*70}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total = len(data)
    dict_count = 0
    ai_count = 0
    todo_count = 0
    
    results = {}
    
    for i, (key, value) in enumerate(data.items(), 1):
        translated = translate_string(value, use_ai)
        results[key] = translated
        
        # Count by tag (check if string for lists)
        if isinstance(translated, str):
            if translated.startswith("[DICT]"):
                dict_count += 1
            elif translated.startswith("[AI]"):
                ai_count += 1
            elif translated.startswith("[TODO]"):
                todo_count += 1
        elif isinstance(translated, list):
            # Count list items
            for item in translated:
                if isinstance(item, str):
                    if item.startswith("[DICT]"):
                        dict_count += 1
                    elif item.startswith("[AI]"):
                        ai_count += 1
                    elif item.startswith("[TODO]"):
                        todo_count += 1
        
        # Progress
        if i % 50 == 0:
            print(f"  ⏳ {i}/{total} strings...")
    
    # Save results
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ HOÀN THÀNH: {Path(output_file).name}")
    print(f"  📊 Từ điển:    {dict_count:4d} matches ({dict_count/total*100:.1f}%)")
    print(f"  🤖 AI:         {ai_count:4d} matches ({ai_count/total*100:.1f}%)")
    print(f"  ⚠️  Cần dịch:   {todo_count:4d} strings ({todo_count/total*100:.1f}%)")
    print(f"  📦 Total:      {total} keys")

if __name__ == "__main__":
    print("="*70)
    print("🌐 HỆ THỐNG DỊCH THÔNG MINH - VIETNAMESE LANGUAGE PACK")
    print("="*70)
    print("📋 Chiến lược: Dictionary-first → AI-assisted → Human review")
    print("🏷️  Tags: [DICT] = Từ điển | [AI] = AI | [TODO] = Cần dịch thủ công")
    print(f"📚 Từ điển hiện tại: {len(EN_TO_VI)} thuật ngữ")
    
    base_dir = Path(__file__).parent / "translations"
    
    # Phase 1: Core (CRITICAL)
    translate_layer(
        base_dir / "core.json",
        base_dir / "core_translated.json",
        use_ai=False  # Set True when AI ready
    )
    
    # Phase 2: UI (HIGH)
    translate_layer(
        base_dir / "ui.json", 
        base_dir / "ui_translated.json",
        use_ai=False
    )
    
    # Phase 3: Misc (NORMAL)
    translate_layer(
        base_dir / "misc.json",
        base_dir / "misc_translated.json",
        use_ai=False
    )
    
    print("\n" + "="*70)
    print("🎯 KẾT QUẢ: Đã tạo 3 layers đã dịch")
    print("="*70)
    print("  📁 core_translated.json - CRITICAL priority")
    print("  📁 ui_translated.json   - HIGH priority")
    print("  📁 misc_translated.json - NORMAL priority")
    print("\n💡 Tiếp theo: Review các [TODO] tags, sau đó chạy merge_layers.py")
    print("="*70)
