"""
Placeholder Protection Module
Prevents translation engines from breaking runtime variables like {name}, ${var}, %1$s

Critical for:
- VS Code i18n format strings
- String interpolation
- Printf-style formatting
- Template literals
"""

import re

# Regex patterns for common placeholder formats
PLACEHOLDER_PATTERNS = [
    r"\{[^}]+\}",      # {name}, {count}, {0}
    r"\$\{[^}]+\}",    # ${variable}, ${expression}
    r"%\d*\$?[sdfox]", # %s, %1$s, %2$d, %f, %o, %x
    r"\[\[.+?\]\]",    # [[link]]
    r"<[^>]+>",        # <html>, <tag>
]

PLACEHOLDER_RE = re.compile("|".join(PLACEHOLDER_PATTERNS))

def protect_placeholders(text):
    """
    Replace placeholders with tokens so translation won't break them.
    
    Args:
        text: String that may contain placeholders
        
    Returns:
        tuple: (protected_text, list_of_placeholders)
        
    Example:
        >>> protect_placeholders("Hello {name}, you have {count} items")
        ("Hello <<PH_0>>, you have <<PH_1>> items", ["{name}", "{count}"])
    """
    if not isinstance(text, str):
        return text, []

    placeholders = PLACEHOLDER_RE.findall(text)
    protected = text

    for i, ph in enumerate(placeholders):
        token = f"<<PH_{i}>>"
        protected = protected.replace(ph, token, 1)

    return protected, placeholders


def restore_placeholders(text, placeholders):
    """
    Restore placeholders back after translation.
    
    Args:
        text: Translated text with tokens
        placeholders: List of original placeholders
        
    Returns:
        str: Text with placeholders restored
        
    Example:
        >>> restore_placeholders("Xin chào <<PH_0>>, bạn có <<PH_1>> mục", ["{name}", "{count}"])
        "Xin chào {name}, bạn có {count} mục"
    """
    restored = text
    for i, ph in enumerate(placeholders):
        token = f"<<PH_{i}>>"
        restored = restored.replace(token, ph)

    return restored


def validate_placeholders(original, translated):
    """
    Verify that translation preserved all placeholders.
    
    Args:
        original: Original English text
        translated: Translated Vietnamese text
        
    Returns:
        tuple: (is_valid, missing_placeholders)
        
    Example:
        >>> validate_placeholders("Hello {name}", "Xin chào")
        (False, ["{name}"])
    """
    original_phs = set(PLACEHOLDER_RE.findall(original))
    translated_phs = set(PLACEHOLDER_RE.findall(translated))
    
    missing = original_phs - translated_phs
    
    return len(missing) == 0, list(missing)


# Test function
if __name__ == "__main__":
    test_cases = [
        "Hello {name}, you have {count} items",
        "File: ${file} at line %d",
        "Error: %1$s in %2$s",
        "Open [[link]] to continue",
        "<html> tags should be preserved",
    ]
    
    print("🧪 Testing Placeholder Protection\n")
    
    for test in test_cases:
        protected, phs = protect_placeholders(test)
        restored = restore_placeholders(protected, phs)
        valid, missing = validate_placeholders(test, restored)
        
        print(f"Original:  {test}")
        print(f"Protected: {protected}")
        print(f"Restored:  {restored}")
        print(f"Valid:     {'✅' if valid else '❌'} {missing if not valid else ''}")
        print()
