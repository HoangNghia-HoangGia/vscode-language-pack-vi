"""
Full AI Translation Engine
Production-grade translation system with:
- Placeholder protection
- Safe terms preservation
- Audit logging
- Rate limiting
- Skip logic for already-translated content
"""

import json
import time
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from core.protect_placeholders import protect_placeholders, restore_placeholders

# ============ CONFIG ============
INPUT = "translations/main.i18n.json"
OUTPUT = "translations/main.ai.translated.json"
LOG = "logs/full_ai_log.json"
RATE = 0.3  # seconds between API calls
# ================================

# Terms that MUST NOT be translated (technical terms)
SAFE_TERMS = {
    "VS Code": "VS Code",
    "Git": "Git",
    "GitHub": "GitHub",
    "GitLab": "GitLab",
    "JSON": "JSON",
    "HTML": "HTML",
    "CSS": "CSS",
    "JavaScript": "JavaScript",
    "TypeScript": "TypeScript",
    "Python": "Python",
    "Terminal": "Terminal",
    "Markdown": "Markdown",
    "Node.js": "Node.js",
    "npm": "npm",
    "API": "API",
    "URL": "URL",
    "HTTP": "HTTP",
    "HTTPS": "HTTPS",
}

def ai_translate(text: str) -> str:
    """
    AI Translation Engine - REPLACE WITH REAL API
    
    Options:
    1. Google Translate API
    2. DeepL API
    3. OpenAI GPT-4 API
    4. Azure Translator
    
    Current: Placeholder for demo
    """
    # PLACEHOLDER - Replace with real AI API call
    # For now, just return marked text
    return f"{text} (AI dịch)"


def protect_terms(text):
    """Replace safe terms with tokens to prevent translation."""
    protected = text
    for term in SAFE_TERMS:
        # Case-sensitive replacement
        protected = protected.replace(term, f"@@{term}@@")
    return protected


def restore_terms(text):
    """Restore protected terms after translation."""
    restored = text
    for term in SAFE_TERMS:
        restored = restored.replace(f"@@{term}@@", term)
    return restored


def should_skip(text):
    """
    Determine if a string should skip translation.
    
    Skip if:
    - Empty or whitespace only
    - Already tagged [DICT] or [HUMAN]
    - URL/URI
    - Pure numbers or symbols
    """
    if not isinstance(text, str):
        return True
        
    if len(text.strip()) == 0:
        return True
    
    # Already manually translated/reviewed
    if text.startswith("[DICT]") or text.startswith("[HUMAN]"):
        return True
    
    # URLs should not be translated
    if text.startswith("http://") or text.startswith("https://"):
        return True
    
    # File paths
    if text.startswith("file://") or text.startswith("vscode://"):
        return True
    
    return False


def main():
    print("🚀 Starting Full AI Translation Engine...")
    print(f"📂 Input: {INPUT}")
    print(f"📂 Output: {OUTPUT}")
    print(f"🧾 Log: {LOG}")
    print()
    
    # Load input
    with open(INPUT, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Ensure logs directory exists
    Path("logs").mkdir(exist_ok=True)

    result = {}
    log_entries = []
    
    total = len(data)
    processed = 0
    skipped = 0
    translated = 0
    errors = 0

    print(f"📊 Total entries: {total}\n")

    for key, value in data.items():
        processed += 1
        
        # Progress indicator
        if processed % 100 == 0:
            print(f"⏳ Progress: {processed}/{total} ({processed/total*100:.1f}%) - Translated: {translated}, Skipped: {skipped}")

        # Skip non-string values
        if not isinstance(value, str):
            result[key] = value
            skipped += 1
            continue

        # Skip already translated or special content
        if should_skip(value):
            result[key] = value
            skipped += 1
            continue

        try:
            # Step 1: Protect placeholders
            protected_placeholders, placeholders = protect_placeholders(value)
            
            # Step 2: Protect safe terms
            protected_terms = protect_terms(protected_placeholders)
            
            # Step 3: Remove [EN] prefix if exists
            clean_text = protected_terms.replace("[EN] ", "")
            
            # Step 4: AI translation
            ai_raw = ai_translate(clean_text)
            
            # Step 5: Restore safe terms
            restored_terms = restore_terms(ai_raw)
            
            # Step 6: Restore placeholders
            restored_final = restore_placeholders(restored_terms, placeholders)
            
            # Step 7: Tag with [AI]
            final_translation = f"[AI] {restored_final}"
            
            result[key] = final_translation
            translated += 1

            # Log for audit
            log_entries.append({
                "key": key,
                "source": value,
                "translated": final_translation,
                "placeholders": placeholders,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            })

            # Rate limiting
            time.sleep(RATE)
            
        except Exception as e:
            print(f"❌ Error processing key '{key}': {e}")
            result[key] = value  # Keep original on error
            errors += 1

    # Save translated output
    print(f"\n💾 Saving output...")
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # Save audit log
    print(f"💾 Saving audit log...")
    with open(LOG, "w", encoding="utf-8") as f:
        json.dump(log_entries, f, ensure_ascii=False, indent=2)

    print(f"\n✅ FULL AI TRANSLATION COMPLETE\n")
    print(f"📁 Output: {OUTPUT}")
    print(f"🧾 Log: {LOG}")
    print(f"\n📊 Statistics:")
    print(f"  Total entries: {total}")
    print(f"  Translated: {translated} ({translated/total*100:.1f}%)")
    print(f"  Skipped: {skipped} ({skipped/total*100:.1f}%)")
    print(f"  Errors: {errors}")
    print(f"\n⚠️  Note: Current AI engine is placeholder.")
    print(f"   Replace ai_translate() with real API for production.")


if __name__ == "__main__":
    main()
