# Vietnamese Language Pack - Status & Action Plan

## 📊 Current Status

- ✅ Extension structure: Complete
- ✅ Package.json: Updated to VS Code ^1.90.0
- ⚠️ Translations: Mixed Chinese/Vietnamese (~13,091 Chinese strings)
- ✅ Backup: main.i18n.json.with_chinese (870KB)

## 🔧 Tools Created

1. **sanitize_chinese.py** - Identifies Chinese characters
2. **extract_english_keys.py** - Extracts key structure  
3. **proper_translation.py** - Attempts official English source
4. **auto_translate.py** - CN → VI translator (problematic)

## ⚠️ Current Issues

### Major Problems:
1. **Copyright Risk**: Using Chinese pack translations
2. **Quality**: CN → VI loses context vs EN → VI
3. **Mixed Language**: 13,091 strings contain Chinese
4. **Marketplace Rejection Risk**: Invalid source data

## ✅ Proper Solution

### Phase 1: Clean Current File
```bash
# Keep only pure Vietnamese translations
# Flag Chinese strings for replacement
python sanitize_and_flag.py
```

### Phase 2: Get English Source
Since VS Code doesn't publish English pack (it's default), we need to:

**Option A**: Extract from VS Code Source Code
```bash
git clone https://github.com/microsoft/vscode
# Extract English strings from src/**/*.ts files
python extract_from_source.py
```

**Option B**: Use English Language Pack from Chinese as Reference
```bash
# Get key → English mapping
# Then translate EN → VI properly
python map_english_keys.py
```

### Phase 3: Translate EN → VI
```bash
# Use proper AI translation or human translation
# Source: English → Vietnamese
# NOT: Chinese → Vietnamese
python translate_en_vi.py
```

## 📝 Recommended Actions NOW

### Immediate (Today):
1. **Don't publish current version** - has copyright issues
2. **Document current progress** - save all work
3. **Create clean baseline** - remove all Chinese

### Short Term (This Week):
1. Extract English keys from VS Code source
2. Build EN → VI translation pipeline
3. Review first 100 keys manually

### Long Term (Next Month):
1. Complete all translations (EN → VI)
2. Community review
3. Professional proofreading
4. Official marketplace submission

## 🎯 Success Criteria

- [ ] 0 Chinese characters in final file
- [ ] All keys mapped to English first
- [ ] Manual review of critical UI strings
- [ ] File size ~1-1.5MB (similar to other packs)
- [ ] VS Code compatibility: ^1.90.0
- [ ] No copyright violations

## 🚀 Next Steps

1. Run comprehensive audit:
   ```bash
   python final_audit.py
   ```

2. Create clean EN → VI pipeline:
   ```bash
   python create_en_vi_pipeline.py
   ```

3. Generate status report:
   ```bash
   python generate_report.py
   ```

## 📧 Contact

- Repository: github.com/HoangNghia-HoangGia/vscode-language-pack-vi
- Email: boos@duhochoanggia.com

---

**Status**: 🟡 Work in Progress  
**Quality**: 🔴 Not Production Ready  
**Action**: 🔧 Needs Proper EN → VI Translation
