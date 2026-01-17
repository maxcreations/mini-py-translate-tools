# mini-py-translate-tools
Mini Py Translate Tools is a lightweight utility for managing translations in multilingual Python projects.

I designed this tool for my PyQt apps to handle translations, so feel free to use it.

## Pluralization Forms and Languages Support
```
Language             Type Ruleset	                  Example (Count: 1, 2, 5)
English/Western      n == 1 vs others	              1 apple, 2 apples, 5 apples
Russian              3-way split (1, 2-4, 5+)	      1 яблоко, 2 яблока, 5 яблок
Polish               Specific 3-way split	          1 utwór, 2 utwory, 5 utworów
French	             n <= 1 vs others	              0 message, 1 message, 2 messages
Asian/Turkic         Always uses the first form       1 件, 2 件, 5 件
```

## Features
**Dynamic Loading:** Loads translation modules on the fly using importlib.

**Smart Pluralization:** Native support for complex plural forms:
3 forms: Russian (RU), Polish (PL).
2 forms: English (EN), French (FR), German, Spanish.
Single form: Chinese (ZH), Japanese (JA), Korean (KO), Turkish (TR).

**Fallback System:** Automatically reverts to English if a translation key is missing in the target language.

**Variable Injection:** Supports dynamic content using Python's .format() syntax.

**Error Highlighting:** Returns visual error indicators (HTML-ready) for missing keys or formatting issues.


## Project Structure
The manager uses dynamic imports, so your project must follow this directory structure:

```
your_project/
│
├── main.py                      # Your application logic
├── _update_translations.py      # (Optional) a tool for auto update all your translation files
└── translations/                # The translation package
    ├── __init__.py              # Required to make it a package
    ├── en.py                    # Default fallback language (Required)
    ├── ru.py                    # Russian translations
    └── fr.py                    # French translations, etc.
```

## Getting Started
### 1. Define Translation Files
Create dictionaries named TRANSLATIONS in your language files. Use lists for keys that require pluralization.
```
translations/en.py

TRANSLATIONS = {
    "welcome": "Hello, {name}!",
    "apples": ["{count} apple", "{count} apples"]
}
```
```
translations/ru.py

TRANSLATIONS = {
    "welcome": "Привет, {name}!",
    "apples": ["{count} яблоко", "{count} яблока", "{count} яблок"]
}
```

### 2. Basic Usage

```
from utils_translator import set_current_language, translate

# 1. Set the language
set_current_language("ru")

# 2. Simple translation
print(translate("welcome", name="Alice")) 
# Output: Привет, Alice!

# 3. Pluralization
print(translate("apples", count=1))  # 1 яблоко
print(translate("apples", count=2))  # 2 яблока
print(translate("apples", count=5))  # 5 яблок
```

## Debugging & Error Handling
To help you find missing translations during development, the translate function returns specific warnings:

**Missing Key:** If a key is not found in either the target or fallback language, it returns:
⚠️key_name⚠️ (wrapped in red HTML span).

**Formatting Error:** If you forget to pass a required variable (e.g., {name}), it returns:
[FMT_ERR] translation_string.

## Auto Update Localization Tool
The project includes an automated script, _update_translations.py, to manage localization keys across the codebase.

### Translation Sync Script
This tool automates the synchronization between your source code and translation files.

**Extraction:** Scans all .py files for translate("string") calls using AST (Abstract Syntax Tree) parsing.

**Synchronization:** Updates files in the translations/ directory, adding new keys and preserving existing ones.

**Organization:** Groups keys in the translation files by the source file they originated from for easier context.

**Safety:** Marks new strings with a # --- New string: --- comment to highlight what needs translation.

### Usage:
Simply run _update_translations.py and it will update all the files in translations folder with new/missing keys.

## License
This project is open-source and available under the MIT License.
