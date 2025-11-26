#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vietnamese Translation Generator for VS Code Language Pack
Enhanced version with comprehensive Chinese to Vietnamese translation
"""

import json
import re
import sys
from pathlib import Path

# Comprehensive Vietnamese translation dictionary (Chinese -> Vietnamese)
TRANSLATIONS = {
    # Common UI terms
    "文件": "Tập tin", "编辑": "Chỉnh sửa", "查看": "Xem", "转到": "Đi tới",
    "运行": "Chạy", "终端": "Terminal", "帮助": "Trợ giúp", "窗口": "Cửa sổ",
    
    # Actions
    "打开": "Mở", "关闭": "Đóng", "保存": "Lưu", "另存为": "Lưu thành",
    "新建": "Tạo mới", "删除": "Xóa", "重命名": "Đổi tên", "复制": "Sao chép",
    "粘贴": "Dán", "剪切": "Cắt", "撤消": "Hoàn tác", "重做": "Làm lại",
    "搜索": "Tìm kiếm", "替换": "Thay thế", "查找": "Tìm", "全部": "Tất cả",
    "选择": "Chọn", "取消": "Hủy", "确定": "OK", "应用": "Áp dụng",
    "刷新": "Làm mới", "重新加载": "Tải lại", "重启": "Khởi động lại",
    "继续": "Tiếp tục", "停止": "Dừng", "暂停": "Tạm dừng", "开始": "Bắt đầu",
    
    # Extended terms
    "操作": "thao tác", "对话框": "hộp thoại", "保留": "Giữ nguyên",
    "大小写": "chữ hoa/thường", "辅助": "hỗ trợ", "模式": "chế độ",
    "检查": "kiểm tra", "用": "dùng", "中": "trong", "此项": "mục này",
    "更多": "Thêm", "切换": "Chuyển đổi", "视图": "Chế độ xem",
    "结束": "Kết thúc",
    "下一个": "Tiếp theo",
    "上一个": "Trước đó",
    "导航": "Điều hướng",
    "返回": "Quay lại",
    "前进": "Tiến",
    
    # File operations
    "文件夹": "Thư mục",
    "目录": "Thư mục",
    "路径": "Đường dẫn",
    "位置": "Vị trí",
    "扩展名": "Phần mở rộng",
    "类型": "Loại",
    "大小": "Kích thước",
    "日期": "Ngày",
    "时间": "Thời gian",
    "修改": "Sửa đổi",
    "创建": "Tạo",
    "访问": "Truy cập",
    
    # Editor
    "编辑器": "Trình soạn thảo",
    "代码": "Mã",
    "行": "Dòng",
    "列": "Cột",
    "字符": "Ký tự",
    "字": "Từ",
    "选中": "Đã chọn",
    "光标": "Con trỏ",
    "插入": "Chèn",
    "覆盖": "Ghi đè",
    "缩进": "Thụt lề",
    "注释": "Chú thích",
    "格式化": "Định dạng",
    "语法": "Cú pháp",
    "突出显示": "Đánh dấu",
    "折叠": "Thu gọn",
    "展开": "Mở rộng",
    
    # Debugging
    "调试": "Gỡ lỗi",
    "断点": "Điểm dừng",
    "监视": "Theo dõi",
    "变量": "Biến",
    "堆栈": "Ngăn xếp",
    "调用": "Gọi",
    "异常": "Ngoại lệ",
    "错误": "Lỗi",
    "警告": "Cảnh báo",
    "信息": "Thông tin",
    "诊断": "Chẩn đoán",
    
    # Extensions
    "扩展": "Tiện ích mở rộng",
    "插件": "Plugin",
    "安装": "Cài đặt",
    "卸载": "Gỡ cài đặt",
    "启用": "Bật",
    "禁用": "Tắt",
    "更新": "Cập nhật",
    "版本": "Phiên bản",
    "市场": "Cửa hàng",
    
    # Settings
    "设置": "Cài đặt",
    "配置": "Cấu hình",
    "首选项": "Tùy chọn",
    "选项": "Tùy chọn",
    "默认": "Mặc định",
    "用户": "Người dùng",
    "工作区": "Không gian làm việc",
    "工作区文件夹": "Thư mục làm việc",
    
    # Source control
    "源代码管理": "Quản lý mã nguồn",
    "提交": "Commit",
    "推送": "Push",
    "拉取": "Pull",
    "分支": "Nhánh",
    "合并": "Merge",
    "克隆": "Clone",
    "暂存": "Stage",
    "更改": "Thay đổi",
    "差异": "Khác biệt",
    "历史": "Lịch sử",
    "存储库": "Repository",
    
    # Terminal
    "新终端": "Terminal mới",
    "拆分终端": "Chia terminal",
    "清除": "Xóa",
    "命令": "Lệnh",
    "输出": "Đầu ra",
    "输入": "Đầu vào",
    "执行": "Thực thi",
    
    # Views
    "视图": "Chế độ xem",
    "面板": "Bảng điều khiển",
    "侧边栏": "Thanh bên",
    "活动栏": "Thanh hoạt động",
    "状态栏": "Thanh trạng thái",
    "标题栏": "Thanh tiêu đề",
    "菜单": "Menu",
    "工具栏": "Thanh công cụ",
    "选项卡": "Tab",
    "窗口": "Cửa sổ",
    "布局": "Bố cục",
    
    # Search
    "搜索结果": "Kết quả tìm kiếm",
    "匹配": "Khớp",
    "区分大小写": "Phân biệt chữ hoa chữ thường",
    "全字匹配": "Khớp toàn bộ từ",
    "正则表达式": "Biểu thức chính quy",
    "包含": "Bao gồm",
    "排除": "Loại trừ",
    "文件中": "Trong tệp",
    
    # Problems
    "问题": "Vấn đề",
    "诊断信息": "Chẩn đoán",
    "筛选器": "Bộ lọc",
    "严重性": "Mức độ nghiêm trọng",
    
    # Common words
    "和": "và",
    "或": "hoặc",
    "的": "",
    "是": "là",
    "否": "Không",
    "是": "Có",
    "无": "Không có",
    "有": "Có",
    "请": "Vui lòng",
    "正在": "Đang",
    "已": "Đã",
    "将": "Sẽ",
    "可": "Có thể",
    "不": "Không",
    "未": "Chưa",
    "从": "Từ",
    "到": "Đến",
    "在": "Ở",
    "为": "Cho",
    "与": "Với",
    "但": "Nhưng",
    "因为": "Vì",
    "所以": "Nên",
    "如果": "Nếu",
    "则": "Thì",
    "当": "Khi",
    "使用": "Sử dụng",
    "需要": "Cần",
    "必须": "Phải",
    "可以": "Có thể",
    "应该": "Nên",
    "可能": "Có thể",
    "无法": "Không thể",
    "失败": "Thất bại",
    "成功": "Thành công",
    "完成": "Hoàn thành",
    "正在进行": "Đang tiến hành",
    "等待": "Đang chờ",
    "加载": "Đang tải",
    "处理": "Xử lý",
    "显示": "Hiển thị",
    "隐藏": "Ẩn",
    "详细信息": "Chi tiết",
    "更多": "Thêm",
    "少": "Ít hơn",
    "全部": "Tất cả",
    "部分": "Một phần",
    "当前": "Hiện tại",
    "最近": "Gần đây",
    "新": "Mới",
    "旧": "Cũ",
}

def translate_text(text):
    """Translate Chinese text to Vietnamese"""
    if not isinstance(text, str):
        return text
    
    result = text
    # Sort by length (longest first) to avoid partial matches
    for zh, vi in sorted(TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True):
        result = result.replace(zh, vi)
    
    return result

def translate_json_recursive(obj):
    """Recursively translate all strings in JSON object"""
    if isinstance(obj, dict):
        return {k: translate_json_recursive(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [translate_json_recursive(item) for item in obj]
    elif isinstance(obj, str):
        return translate_text(obj)
    else:
        return obj

def main():
    # Read Chinese translation file
    zh_file = r"C:\Users\Admin\.vscode\extensions\ms-ceintl.vscode-language-pack-zh-hans-1.106.2025111209\translations\main.i18n.json"
    output_file = r"translations\main.i18n.json.new"
    
    print(f"Reading Chinese translations from: {zh_file}")
    with open(zh_file, 'r', encoding='utf-8') as f:
        zh_data = json.load(f)
    
    print(f"Translating {len(zh_data)} root keys...")
    vi_data = translate_json_recursive(zh_data)
    
    print(f"Writing Vietnamese translations to: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(vi_data, f, ensure_ascii=False, indent=2)
    
    # Statistics
    zh_str = json.dumps(zh_data, ensure_ascii=False)
    vi_str = json.dumps(vi_data, ensure_ascii=False)
    
    print(f"\n=== Translation Statistics ===")
    print(f"Original size: {len(zh_str):,} bytes")
    print(f"Translated size: {len(vi_str):,} bytes")
    print(f"Root keys: {len(zh_data)}")
    print(f"Dictionary size: {len(TRANSLATIONS)} terms")
    
    # Calculate coverage
    translated_count = sum(1 for zh in TRANSLATIONS.keys() if zh in zh_str)
    print(f"Coverage: {translated_count}/{len(TRANSLATIONS)} ({translated_count/len(TRANSLATIONS)*100:.1f}%)")
    print(f"\nTranslation complete! File saved to: {output_file}")

if __name__ == "__main__":
    main()
