# Vietnamese Language Pack - Auto Update Guide
# Hướng dẫn sử dụng hệ thống tự động cập nhật

## 📋 Tổng quan (V2.0)

Phiên bản V2.0 của hệ thống Auto Update Vietnamese Language Pack đã được harden:
- ✅ Smart VS Code detection (PATH + cài đặt mặc định)
- ✅ Optional SHA256 integrity verification (Verify-FileIntegrity)
- ✅ Log chuyển vào `%APPDATA%/VSCodeVietnameseLangPack/update-history.log`
- ✅ Separation of Concerns (Core Engine vs Setup Script)
- ✅ Scheduled Task chỉ cấu hình bởi `setup-auto-update.ps1`
- ✅ Hỗ trợ tham số `-ExpectedSha256`
- ✅ Ghi log chi tiết cho việc theo dõi
### Bước 2: Cấu hình GitHub Repository (BẮT BUỘC)
Repository đã được cấu hình mặc định:

```powershell
# Repo mặc định: HoangNghia-HoangGia/vscode-language-pack-vi
.\setup-auto-update.ps1

# Hoặc tùy chỉnh repo khác:
.\setup-auto-update.ps1 -GitHubRepo "your-org/vscode-language-pack-vi"
```
2. VS Code đã được cài đặt và có thể chạy từ command line
### Chạy cập nhật ngay lập tức (Manual)
```powershell
# Sử dụng repo mặc định
.\vietnamese-langpack-auto-update.ps1

# Hoặc chỉ định repo cụ thể
.\vietnamese-langpack-auto-update.ps1 -GitHubRepo "HoangNghia-HoangGia/vscode-language-pack-vi"
```

### Force update (bỏ qua kiểm tra phiên bản)
```powershell
.\vietnamese-langpack-auto-update.ps1 -ForceUpdate
```

### Chạy im lặng (cho scheduled task / CI)
```powershell
.\vietnamese-langpack-auto-update.ps1 -Silent
```
1. Mở PowerShell với quyền Administrator
- **Vị trí mới (V2.0):** `%APPDATA%\VSCodeVietnameseLangPack\update-history.log`
```powershell
### Thay đổi tần suất cập nhật (Task V2.0)
1. Mở Task Scheduler (`taskschd.msc`)
2. Task name: `VSCode_Vietnamese_AutoUpdate`
3. Sửa Trigger (mặc định: Chủ Nhật 09:00 AM)
- ✅ Kiểm tra VS Code
- **Auto-update script logs:** `%APPDATA%\VSCodeVietnameseLangPack\update-history.log`
- ✅ Tạo shortcut trên desktop
### Cho Người dùng
- ✅ Luôn có phiên bản mới nhất
- ✅ Không cần theo dõi cập nhật thủ công
- ✅ Tự động cài đặt (với tuỳ chọn xác thực SHA256)
- ✅ Log sạch – không chiếm Desktop
### Tự động (Scheduled Task)
### Cho Nhà phát triển
- ✅ Phân phối cập nhật qua GitHub Releases
- ✅ Hỗ trợ hash integrity trong pipeline
- ✅ Giảm support cho vấn đề phiên bản cũ
- ✅ Dễ refactor (Separation of Concerns)

### Thủ công (Manual)
- **Cách chạy:** Double-click shortcut trên desktop hoặc chạy script trực tiếp
- **Chế độ:** Hiển thị tiến trình và kết quả
- **Tùy chọn:** Có thể force update bất kể phiên bản

## 🔧 Sử dụng thủ công

### Chạy cập nhật ngay lập tức
```powershell
.\vietnamese-langpack-auto-update.ps1
```

### Force update (bỏ qua kiểm tra phiên bản)
```powershell
.\vietnamese-langpack-auto-update.ps1 -ForceUpdate
```

### Chạy im lặng (cho scheduled task)
```powershell
.\vietnamese-langpack-auto-update.ps1 -Silent
```

## 📊 Theo dõi và Log

### File Log
- **Vị trí:** `%USERPROFILE%\Desktop\vietnamese-langpack-update.log`
- **Nội dung:** Tất cả hoạt động của hệ thống cập nhật
- **Định dạng:** Timestamp + Level + Message

### Xem log gần đây
```powershell
Get-Content "$env:USERPROFILE\Desktop\vietnamese-langpack-update.log" -Tail 20
```

### Xóa log cũ
```powershell
# Xóa log cũ hơn 30 ngày
$logFile = "$env:USERPROFILE\Desktop\vietnamese-langpack-update.log"
$oldEntries = Get-Content $logFile | Where-Object {
    $dateString = $_ -match '\[(\d{4}-\d{2}-\d{2})' | ForEach-Object { $matches[1] }
    if ($dateString) {
        $logDate = [DateTime]::Parse($dateString)
        ($logDate -lt (Get-Date).AddDays(-30))
    }
}
# ... (có thể thêm logic xóa)
```

## ⚙️ Cấu hình nâng cao

### Thay đổi tần suất cập nhật
Để thay đổi lịch chạy scheduled task:

1. Mở Task Scheduler (taskschd.msc)
2. Tìm task "Vietnamese Language Pack Auto Update"
3. Sửa trigger theo ý muốn

### Thay đổi repository
Nếu repository GitHub thay đổi:

1. Sửa biến `$GitHubRepo` trong cả 2 script
2. Chạy lại setup để cập nhật scheduled task

## 🔍 Xử lý sự cố

### Lỗi: "VS Code not found"
- Đảm bảo VS Code được cài đặt
- Thêm VS Code vào PATH environment variable
- Khởi động lại PowerShell

### Lỗi: "Access denied" khi tạo task
- Chạy PowerShell với quyền Administrator
- Kiểm tra chính sách execution: `Get-ExecutionPolicy`

### Lỗi: "Cannot connect to GitHub"
- Kiểm tra kết nối internet
- Kiểm tra firewall/antivirus
- Verify repository URL đúng

### Update không hoạt động
- Kiểm tra file log để xem lỗi cụ thể
- Chạy thủ công để debug
- Verify repository có releases với file .vsix

## 📞 Hỗ trợ

### Kiểm tra trạng thái
```powershell
# Xem trạng thái scheduled task
Get-ScheduledTask -TaskName "Vietnamese Language Pack Auto Update"

# Xem lịch sử chạy gần đây
Get-ScheduledTask -TaskName "Vietnamese Language Pack Auto Update" | Get-ScheduledTaskInfo
```

### Tắt auto update
```powershell
# Tắt scheduled task
Disable-ScheduledTask -TaskName "Vietnamese Language Pack Auto Update"

# Xóa hoàn toàn
Unregister-ScheduledTask -TaskName "Vietnamese Language Pack Auto Update" -Confirm:$false
```

### Bật lại auto update
```powershell
Enable-ScheduledTask -TaskName "Vietnamese Language Pack Auto Update"
```

## 🎯 Lợi ích

### Cho Người dùng
- ✅ Luôn có phiên bản mới nhất
- ✅ Không cần theo dõi cập nhật thủ công
- ✅ Tự động cài đặt an toàn
- ✅ Ghi log đầy đủ để debug

### Cho Nhà phát triển
- ✅ Phân phối cập nhật dễ dàng qua GitHub
- ✅ Người dùng tự động nhận update
- ✅ Giảm support cho vấn đề phiên bản cũ
- ✅ Tăng adoption rate

## 📈 Thống kê và Metrics

Script sẽ log các thông tin sau:
- Số lần kiểm tra cập nhật
- Số lần có update mới
- Thời gian download và cài đặt
- Lỗi gặp phải (nếu có)

---

**🇻🇳 Vietnamese Language Pack Auto Update System**
**🚀 Keeping your Vietnamese localization always current**
**💎 Production Ready - Community Focused**