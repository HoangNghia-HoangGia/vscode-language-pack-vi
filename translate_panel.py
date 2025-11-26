import json

EN_TO_VI = {
    # Panel/Sidebar keywords
    "Explorer": "Trình khám phá",
    "Search": "Tìm kiếm",
    "Source Control": "Quản lý mã nguồn",
    "Extensions": "Tiện ích mở rộng",
    "Problems": "Vấn đề",
    "Output": "Đầu ra",
    "Terminal": "Terminal",
    "Debug Console": "Bảng gỡ lỗi",
    "Timeline": "Dòng thời gian",
    "Git": "Git",
    "Changes": "Thay đổi",
    "Staged Changes": "Thay đổi đã stage",
    "Open Editors": "Tệp đang mở",
    "Outline": "Dàn bài",
    "No Folder Opened": "Chưa mở thư mục",
    
    # Emmet commands - EXTENDED
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

def ai_translate(text):
    return text  # placeholder cho AI nơi Copilot sẽ mở rộng

def translate_string(text):
    text = text.replace("[EN] ", "")

    if text in EN_TO_VI:
        return f"[DICT] {EN_TO_VI[text]}"

    ai_result = ai_translate(text)
    if ai_result != text:
        return f"[AI] {ai_result}"

    return f"[TODO] {text}"

with open("translations/panel.json", "r", encoding="utf-8") as f:
    data = json.load(f)

translated = {}
dict_count, ai_count, todo_count = 0, 0, 0

for k, v in data.items():
    if isinstance(v, str):
        result = translate_string(v)

        if result.startswith("[DICT]"):
            dict_count += 1
        elif result.startswith("[AI]"):
            ai_count += 1
        else:
            todo_count += 1

        translated[k] = result
    else:
        translated[k] = v

with open("translations/panel_translated.json", "w", encoding="utf-8") as f:
    json.dump(translated, f, ensure_ascii=False, indent=2)

print("✅ Panel Translation Done")
print("DICT:", dict_count)
print("AI:", ai_count)
print("TODO:", todo_count)
