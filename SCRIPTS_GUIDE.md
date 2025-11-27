# Vietnamese Language Pack - Development & Release Scripts

Hệ thống 2 scripts tối ưu cho phát triển và phát hành extension.

---

## 🔧 DEV-UPDATE.PS1 - Phát triển nhanh

**Mục đích:** Test thay đổi ngay lập tức trên máy local

**Khi nào dùng:**
- Đang sửa file dịch `translations/main.i18n.json`
- Cần test UI tiếng Việt ngay
- Chưa sẵn sàng release cho users

**Cách dùng:**
```powershell
.\dev-update.ps1
```

**Quy trình tự động:**
1. ✅ Đóng VS Code
2. ✅ Tăng version patch (3.2.1 → 3.2.2)
3. ✅ Build VSIX
4. ✅ Gỡ extension cũ
5. ✅ Cài extension mới
6. ✅ Set locale = vi
7. ✅ Mở lại VS Code với UI tiếng Việt

**Thời gian:** ~8-12 giây

---

## 🌐 QUICK-PUBLISH.PS1 - Phát hành Production

**Mục đích:** Release lên Marketplace cho toàn bộ users

**Khi nào dùng:**
- Đã test kỹ với dev-update
- Sẵn sàng release phiên bản chính thức
- Muốn users tự động nhận update

**Cách dùng:**
```powershell
# Bump patch (3.2.1 → 3.2.2)
.\quick-publish.ps1

# Bump minor (3.2.1 → 3.3.0)
.\quick-publish.ps1 -BumpType minor

# Bump major (3.2.1 → 4.0.0)
.\quick-publish.ps1 -BumpType major

# Với commit message tùy chỉnh
.\quick-publish.ps1 -Message "Fix hotkey conflicts"
```

**Quy trình tự động:**
1. ✅ Check vsce
2. ✅ Đọc version hiện tại
3. ✅ Bump version theo loại
4. ✅ Update package.json
5. ✅ Build VSIX
6. ✅ Publish lên Marketplace
7. ✅ Git commit + tag + push

**Thời gian:** ~30-60 giây

**Kết quả:**
- Extension lên Marketplace
- Users nhận auto-update notification
- Git tag tự động tạo
- Release sẵn sàng

---

## 📊 So sánh

| Feature | dev-update.ps1 | quick-publish.ps1 |
|---------|----------------|-------------------|
| **Tốc độ** | ⚡ 8-12s | ⏱ 30-60s |
| **Phạm vi** | Chỉ máy bạn | Toàn bộ users |
| **Git commit** | ❌ Không | ✅ Tự động |
| **Marketplace** | ❌ Không | ✅ Có |
| **Auto-update users** | ❌ Không | ✅ Có |
| **Khi nào dùng** | Dev/Test | Production Release |

---

## 🎯 Workflow đề xuất

```
[Sửa translations] → dev-update.ps1 → Test → Sửa tiếp → dev-update.ps1 → Test
                                                              ↓
                                                    [Đã ổn định]
                                                              ↓
                                                  quick-publish.ps1
                                                              ↓
                                            [Users tự động nhận update]
```

---

## ⚙️ Yêu cầu

### Cho dev-update.ps1:
- ✅ vsce đã cài: `npm install -g @vscode/vsce`

### Cho quick-publish.ps1:
- ✅ vsce đã cài
- ✅ Đã login: `vsce login HoangNghia-HoangGia`
- ✅ Git repository đã config

---

## 🔐 Setup Marketplace (Chỉ làm 1 lần)

1. **Tạo Publisher** (2 phút):
   - Vào: https://marketplace.visualstudio.com/manage
   - Tạo Publisher ID: `HoangNghia-HoangGia`

2. **Tạo PAT Token** (2 phút):
   - Vào: https://dev.azure.com/{YOUR_ORG}/_usersSettings/tokens
   - Scopes: **Marketplace > Manage**
   - Copy token

3. **Login vsce** (1 phút):
   ```powershell
   vsce login HoangNghia-HoangGia
   # Paste token when prompted
   ```

**Lưu ý:** Setup này chỉ làm 1 lần duy nhất. Sau đó `quick-publish.ps1` tự động hoàn toàn.

---

## 💡 Tips

- Dùng `dev-update.ps1` nhiều lần khi đang dev
- Chỉ dùng `quick-publish.ps1` khi đã test kỹ
- Extension ID: `HoangNghia-HoangGia.vscode-language-pack-vi`
- Marketplace: https://marketplace.visualstudio.com/items?itemName=HoangNghia-HoangGia.vscode-language-pack-vi

---

## 🆘 Troubleshooting

**dev-update.ps1 báo lỗi build:**
- Check file `translations/main.i18n.json` có lỗi syntax không

**quick-publish.ps1 báo "Not authenticated":**
- Chạy: `vsce login HoangNghia-HoangGia`

**VS Code không đổi sang tiếng Việt:**
- Ctrl+Shift+P → "Configure Display Language" → Chọn "vi"
- Restart VS Code

---

✨ **Hoàn toàn MIỄN PHÍ cho mọi người dùng!**
