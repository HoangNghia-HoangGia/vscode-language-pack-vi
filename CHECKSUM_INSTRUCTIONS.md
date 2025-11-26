# Vietnamese Language Pack - Checksum & Integrity Guide (V2.0)

## 🎯 Mục tiêu
Bảo vệ chuỗi cung ứng (Supply Chain) bằng cách xác thực tính toàn vẹn file `.vsix` trước khi cài đặt.

## 🔐 Tại sao cần SHA256?
- Phát hiện chỉnh sửa trái phép.
- Ngăn MITM (Man-in-the-Middle) thay nội dung.
- Tăng độ tin cậy khi phân phối qua GitHub Releases.

## 🧪 Quy trình tạo SHA256 cho file VSIX
Giả sử file build: `vscode-language-pack-vi-2.2.0.vsix`

```powershell
# PowerShell (Windows)
Get-FileHash -Path .\vscode-language-pack-vi-2.2.0.vsix -Algorithm SHA256 | Select-Object -ExpandProperty Hash
```

```bash
# macOS / Linux (Terminal)
shasum -a 256 vscode-language-pack-vi-2.2.0.vsix | awk '{print $1}'
```

Kết quả ví dụ:
```
D9A6F4B3E7A8C2F1AA5579C39E2B4E8B22A1C4F6D1234567890ABCDEF1122334
```

## 📄 Tạo file checksum (checksums.txt)
Tạo file tại root của Release hoặc đính kèm làm asset:
```
# checksums.txt
vscode-language-pack-vi-2.2.0.vsix SHA256=D9A6F4B3E7A8C2F1AA5579C39E2B4E8B22A1C4F6D1234567890ABCDEF1122334
```

## 🚀 Publish trên GitHub Releases
1. Build VSIX
2. Tạo `checksums.txt`
3. Tạo Release mới (tag v2.2.0)
4. Upload cả 2 files:
   - `vscode-language-pack-vi-2.2.0.vsix`
   - `checksums.txt`
5. Ghi rõ phần "Integrity Verified" trong Release Notes.

## 🛠️ Sử dụng trong script cập nhật
Chạy script cập nhật với tham số `-ExpectedSha256`:
```powershell
# Ví dụ (thay giá trị hash thật)
./vietnamese-langpack-auto-update.ps1 -GitHubRepo "nguyenvana/vscode-language-pack-vi" -ExpectedSha256 "D9A6F4B3E7A8C2F1AA5579C39E2B4E8B22A1C4F6D1234567890ABCDEF1122334"
```

## 🔍 Tự động lấy hash (Advanced Pipeline)
Bạn có thể tự động parse hash từ body Release nếu ghi rõ:
```
SHA256: D9A6F4B3E7A8C2F1AA5579C39E2B4E8B22A1C4F6D1234567890ABCDEF1122334
```
Hoặc lưu hash trong asset riêng: `vscode-language-pack-vi-2.2.0.vsix.sha256`

Ví dụ parse asset hash tự động:
```powershell
$release = Invoke-RestMethod "https://api.github.com/repos/nguyenvana/vscode-language-pack-vi/releases/latest"
$hashAsset = $release.assets | Where-Object { $_.name -match "\.sha256$" }
$expectedHash = Invoke-WebRequest -Uri $hashAsset.browser_download_url -UseBasicParsing | Select-String -Pattern "[A-F0-9]{64}" | ForEach-Object { $_.Matches[0].Value }
```

## 🛡️ Kiểm tra sau khi cài đặt
Sau khi script chạy, mở log: `%APPDATA%\VSCodeVietnameseLangPack\update-history.log`

Tìm dòng:
```
Integrity check passed (SHA256 matches).
```
Nếu thấy:
```
SHA256 mismatch. Expected: ... | Actual: ...
```
=> DỪNG NGAY việc phân phối và điều tra nguồn file.

## 🚫 Các lỗi thường gặp
| Vấn đề | Nguyên nhân | Cách xử lý |
|--------|-------------|------------|
| Hash mismatch | File bị thay đổi sau khi tính hash | Rebuild và tạo hash mới |
| Empty hash | Quên truyền tham số | Thêm -ExpectedSha256 vào lệnh |
| Không tìm thấy asset .sha256 | Release thiếu file hash | Upload lại asset |

## ✅ Checklist Trước Khi Release
- [ ] Build VSIX thành công
- [ ] Tạo hash SHA256
- [ ] Ghi hash vào `checksums.txt`
- [ ] Upload VSIX + checksums.txt lên GitHub
- [ ] Cập nhật Release Notes có mục "SHA256 Verified"
- [ ] Test auto-update với tham số -ExpectedSha256

---
**Security Assurance:** Khi bật xác thực SHA256, nguy cơ Supply Chain Attack giảm đáng kể.
**Phiên bản tài liệu:** 2.0
