import json

EN_TO_VI = {
    "File": "Tập tin",
    "Edit": "Chỉnh sửa",
    "View": "Xem",
    "Debug": "Gỡ lỗi",
    "Run": "Chạy",
    "Open": "Mở",
    "Save": "Lưu",
    "Close": "Đóng",
    "Settings": "Cài đặt",
    "Search": "Tìm kiếm",
    "Replace": "Thay thế",
    "Find": "Tìm",
    "Terminal": "Terminal",
    "Problems": "Vấn đề",
    "Extensions": "Tiện ích mở rộng",
    "New": "Mới",
    "Copy": "Sao chép",
    "Paste": "Dán",
    "Cut": "Cắt",
    "Undo": "Hoàn tác",
    "Redo": "Làm lại",
    "Delete": "Xóa",
    "Select": "Chọn",
    "Go": "Đi tới",
    "Help": "Trợ giúp",
}

def ai_translate(text):
    # Copilot sẽ thay bằng API AI nếu muốn
    return text  # fallback an toàn

def translate_string(text):
    text = text.replace("[EN] ", "")

    if text in EN_TO_VI:
        return f"[DICT] {EN_TO_VI[text]}"

    ai_result = ai_translate(text)

    if ai_result and ai_result != text:
        return f"[AI] {ai_result}"

    return f"[TODO] {text}"

print("Loading core.json...")

with open("translations/core.json", "r", encoding="utf-8") as f:
    data = json.load(f)

translated = {}
dict_count = 0
ai_count = 0
todo_count = 0

for key, value in data.items():
    if isinstance(value, str):
        result = translate_string(value)

        if result.startswith("[DICT]"):
            dict_count += 1
        elif result.startswith("[AI]"):
            ai_count += 1
        else:
            todo_count += 1

        translated[key] = result
    elif isinstance(value, list):
        # Handle array values
        translated[key] = value
    else:
        translated[key] = value

with open("translations/core_translated.json", "w", encoding="utf-8") as f:
    json.dump(translated, f, ensure_ascii=False, indent=2)

print("✅ Translation complete!")
print("DICT:", dict_count)
print("AI:", ai_count)
print("TODO:", todo_count)
print(f"Coverage: {dict_count/(dict_count+ai_count+todo_count)*100:.1f}%")
