#!/usr/bin/env python3
"""
Vietnamese Language Pack Translation Generator
Generates full Vietnamese translations from Chinese language pack template
"""

import json
import os
import sys
from pathlib import Path

# Translation mapping: Chinese -> Vietnamese for common terms
TRANSLATION_MAP = {
    # File menu
    "文件": "Tập tin",
    "新建": "Mới",
    "打开": "Mở",
    "保存": "Lưu",
    "另存为": "Lưu thành",
    "关闭": "Đóng",
    "退出": "Thoát",
    
    # Edit menu
    "编辑": "Chỉnh sửa",
    "撤消": "Hoàn tác",
    "重做": "Làm lại",
    "剪切": "Cắt",
    "复制": "Sao chép",
    "粘贴": "Dán",
    "查找": "Tìm kiếm",
    "替换": "Thay thế",
    
    # View menu
    "查看": "Xem",
    "视图": "Xem",
    "命令面板": "Bảng lệnh",
    "打开视图": "Mở khung nhìn",
    "外观": "Giao diện",
    "编辑器布局": "Bố cục trình soạn thảo",
    
    # Common terms
    "是": "Có",
    "否": "Không",
    "确定": "OK",
    "取消": "Hủy",
    "应用": "Áp dụng",
    "重置": "Đặt lại",
    "删除": "Xóa",
    "添加": "Thêm",
    "移除": "Loại bỏ",
    "启用": "Bật",
    "禁用": "Tắt",
    "设置": "Cài đặt",
    "首选项": "Tùy chọn",
    "扩展": "Tiện ích mở rộng",
    "主题": "Chủ đề",
    "语言": "Ngôn ngữ",
    "键盘快捷方式": "Phím tắt",
    "用户": "Người dùng",
    "工作区": "Không gian làm việc",
    "文件夹": "Thư mục",
    "搜索": "Tìm kiếm",
    "调试": "Gỡ lỗi",
    "运行": "Chạy",
    "终端": "Terminal",
    "帮助": "Trợ giúp",
    "关于": "Giới thiệu",
    "更新": "Cập nhật",
    "错误": "Lỗi",
    "警告": "Cảnh báo",
    "信息": "Thông tin",
    "成功": "Thành công",
    "失败": "Thất bại",
    "加载": "Đang tải",
    "正在": "Đang",
    "完成": "Hoàn thành",
    "请": "Vui lòng",
    "选择": "Chọn",
    "输入": "Nhập",
    "输出": "Đầu ra",
    "配置": "Cấu hình",
    "路径": "Đường dẫn",
    "名称": "Tên",
    "类型": "Loại",
    "值": "Giá trị",
    "描述": "Mô tả",
    "版本": "Phiên bản",
    "作者": "Tác giả",
    "许可证": "Giấy phép",
    "详细信息": "Chi tiết",
    "选项": "Tùy chọn",
    "高级": "Nâng cao",
    "默认": "Mặc định",
    "自定义": "Tùy chỉnh",
    "导入": "Nhập",
    "导出": "Xuất",
    "上传": "Tải lên",
    "下载": "Tải xuống",
    "刷新": "Làm mới",
    "重新加载": "Tải lại",
    "重启": "Khởi động lại",
    "安装": "Cài đặt",
    "卸载": "Gỡ cài đặt",
    "权限": "Quyền",
    "安全": "Bảo mật",
    "隐私": "Riêng tư",
    "网络": "Mạng",
    "代理": "Proxy",
    "性能": "Hiệu suất",
    "问题": "Vấn đề",
    "建议": "Đề xuất",
    "反馈": "Phản hồi",
    "报告": "Báo cáo",
    "文档": "Tài liệu",
    "示例": "Ví dụ",
    "教程": "Hướng dẫn",
    "快速入门": "Bắt đầu nhanh",
}

def translate_text(chinese_text):
    """Translate Chinese text to Vietnamese using mapping"""
    if not chinese_text or not isinstance(chinese_text, str):
        return chinese_text
    
    # Try direct mapping first
    if chinese_text in TRANSLATION_MAP:
        return TRANSLATION_MAP[chinese_text]
    
    # Try partial translation
    result = chinese_text
    for zh, vi in TRANSLATION_MAP.items():
        result = result.replace(zh, vi)
    
    # If no translation found, keep original but mark it
    if result == chinese_text and any('\u4e00' <= c <= '\u9fff' for c in chinese_text):
        # Contains Chinese characters - mark for manual translation
        return f"[TODO] {chinese_text}"
    
    return result

def process_translations(data):
    """Recursively process translation data"""
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            if isinstance(value, str):
                result[key] = translate_text(value)
            elif isinstance(value, (dict, list)):
                result[key] = process_translations(value)
            else:
                result[key] = value
        return result
    elif isinstance(data, list):
        return [translate_text(item) if isinstance(item, str) else process_translations(item) for item in data]
    else:
        return data

def main():
    # Paths
    user_profile = os.environ.get('USERPROFILE', '')
    zh_pack_pattern = os.path.join(user_profile, '.vscode', 'extensions', 'ms-ceintl.vscode-language-pack-zh-hans-*', 'translations', 'main.i18n.json')
    
    # Find Chinese language pack
    import glob
    zh_files = glob.glob(zh_pack_pattern)
    
    if not zh_files:
        print("ERROR: Chinese language pack not found!")
        print(f"Expected path: {zh_pack_pattern}")
        sys.exit(1)
    
    zh_file = zh_files[0]
    print(f"Found Chinese pack: {zh_file}")
    
    # Load Chinese translations
    print("Loading Chinese translations...")
    with open(zh_file, 'r', encoding='utf-8') as f:
        zh_data = json.load(f)
    
    print(f"Loaded {len(zh_data)} root keys")
    
    # Generate Vietnamese translations
    print("Generating Vietnamese translations...")
    vi_data = process_translations(zh_data)
    
    # Output file
    output_dir = Path(__file__).parent.parent / 'translations'
    output_file = output_dir / 'main.i18n.json.generated'
    
    print(f"Saving to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(vi_data, f, ensure_ascii=False, indent=2)
    
    # Count TODO items
    output_str = json.dumps(vi_data, ensure_ascii=False)
    todo_count = output_str.count('[TODO]')
    total_strings = output_str.count('"')
    
    print("\n" + "="*60)
    print("GENERATION COMPLETE!")
    print("="*60)
    print(f"Output file: {output_file}")
    print(f"File size: {output_file.stat().st_size / 1024:.2f} KB")
    print(f"Translations needing review: {todo_count}")
    print(f"Auto-translated: {total_strings - todo_count}")
    print(f"Coverage: {((total_strings - todo_count) / total_strings * 100):.1f}%")
    print("\nNext steps:")
    print("1. Review and edit [TODO] items in the generated file")
    print("2. Copy to translations/main.i18n.json when ready")
    print("3. Rebuild VSIX package")

if __name__ == '__main__':
    main()
