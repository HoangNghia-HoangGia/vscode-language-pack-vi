import json
import time
from pathlib import Path

# ============ CONFIG ============
INPUT_FILE = "translations/panel.json"
OUTPUT_FILE = "translations/panel_ai_translated.json"
LOG_FILE = "logs/ai_translate_log.json"
RATE_LIMIT = 0.4  # tránh spam AI API
# ================================

# Từ điển an toàn (ưu tiên hơn AI)
SAFE_DICT = {
    "Explorer": "Trình khám phá",
    "Search": "Tìm kiếm",
    "Extensions": "Tiện ích mở rộng",
    "Source Control": "Quản lý mã nguồn",
    "Terminal": "Terminal",
    "Problems": "Vấn đề",
    "Output": "Đầu ra",
    "Debug Console": "Bảng gỡ lỗi",
    "Timeline": "Dòng thời gian",
    "Git": "Git",
    "Changes": "Thay đổi",
    "Staged Changes": "Thay đổi đã stage",
    "Open Editors": "Tệp đang mở",
    "Outline": "Dàn bài",
    "No Folder Opened": "Chưa mở thư mục",
    
    # Emmet commands
    "Wrap with Abbreviation": "Bọc với viết tắt",
    "Remove Tag": "Xóa thẻ",
    "Update Tag": "Cập nhật thẻ",
    "Go to Matching Pair": "Đi tới cặp khớp",
    "Balance (inward)": "Cân bằng (vào trong)",
    "Balance (outward)": "Cân bằng (ra ngoài)",
    "Go to Previous Edit Point": "Đi tới điểm sửa trước",
    "Go to Next Edit Point": "Đi tới điểm sửa tiếp",
    "Merge Lines": "Gộp dòng",
    "Select Previous Item": "Chọn mục trước",
    "Select Next Item": "Chọn mục tiếp",
    "Split/Join Tag": "Tách/Gộp thẻ",
    "Toggle Comment": "Bật/Tắt ghi chú",
    "Evaluate Math Expression": "Tính biểu thức toán",
    "Update Image Size": "Cập nhật kích thước ảnh",
    "Reflect CSS Value": "Phản ánh giá trị CSS",
    "Increment by 1": "Tăng 1",
    "Decrement by 1": "Giảm 1",
    "Increment by 0.1": "Tăng 0.1",
    "Decrement by 0.1": "Giảm 0.1",
    "Increment by 10": "Tăng 10",
    "Decrement by 10": "Giảm 10",
    "Show Emmet Commands": "Hiện lệnh Emmet",
    
    # Jupyter Notebook
    "New Jupyter Notebook": "Jupyter Notebook mới",
    "Jupyter Notebook": "Jupyter Notebook",
    "Clean Invalid Image Attachment Reference": "Xóa tham chiếu ảnh không hợp lệ",
    "Copy Cell Output": "Sao chép đầu ra ô",
    "Add Cell Output to Chat": "Thêm đầu ra ô vào chat",
    "Open Cell Output in Text Editor": "Mở đầu ra ô trong trình soạn",
}

# Giả lập AI – Copilot sẽ thay bằng API thật
def ai_translate(text):
    """
    PLACEHOLDER: Replace with real AI API
    Options:
    - Google Translate API
    - DeepL API
    - OpenAI GPT-4 API
    - Azure Translator
    """
    # Remove [EN] prefix if exists
    text = text.replace("[EN] ", "")
    
    # Simple rule-based translation for demo
    # In production, call real AI API here
    return f"{text} (AI dịch)"


def translate_string(text):
    """
    Translation priority:
    1. SAFE_DICT (manual dictionary)
    2. AI translation
    """
    # Remove [EN] prefix
    clean_text = text.replace("[EN] ", "")
    
    if clean_text in SAFE_DICT:
        return f"[DICT] {SAFE_DICT[clean_text]}"

    ai_result = ai_translate(clean_text)
    return f"[AI] {ai_result}"


def main():
    print("🚀 Starting AI Translation Engine...")
    print(f"📂 Input: {INPUT_FILE}")
    
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    output = {}
    logs = []
    
    dict_count = 0
    ai_count = 0
    
    total = len(data)
    processed = 0

    for key, value in data.items():
        if isinstance(value, str):
            result = translate_string(value)
            
            if result.startswith("[DICT]"):
                dict_count += 1
            elif result.startswith("[AI]"):
                ai_count += 1

            logs.append({
                "key": key,
                "english": value,
                "translated": result,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "unix_time": time.time()
            })

            output[key] = result
            
            processed += 1
            if processed % 10 == 0:
                print(f"⏳ Progress: {processed}/{total} ({processed/total*100:.1f}%)")
            
            time.sleep(RATE_LIMIT)
        else:
            output[key] = value

    # Create logs directory
    Path("logs").mkdir(exist_ok=True)

    # Save translated output
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    # Save audit log
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)

    print("\n✅ AI translation complete")
    print(f"📁 Output: {OUTPUT_FILE}")
    print(f"🧾 Log: {LOG_FILE}")
    print(f"🔍 Total strings: {len(output)}")
    print(f"📖 DICT: {dict_count} ({dict_count/total*100:.1f}%)")
    print(f"🤖 AI: {ai_count} ({ai_count/total*100:.1f}%)")


if __name__ == "__main__":
    main()
