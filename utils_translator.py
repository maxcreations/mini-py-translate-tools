# Copyright (c) 2026 maxcreations
# Licensed under the MIT License.
# See LICENSE file in the project root for full license information.


import importlib

# --- Global variable for the current language ---
_current_language = "en"
_translation_data = {}
_fallback_translation_data = {}

def load_language_data(lang):
    """Dynamically loads translation data from translations package."""
    global _translation_data, _fallback_translation_data

    if not _fallback_translation_data:
        try:
            fallback_module = importlib.import_module("translations.en")
            _fallback_translation_data = getattr(fallback_module, "TRANSLATIONS", {})
        except ImportError:
            print(
                "FATAL: Could not load fallback translation module 'translations.en'."
            )
            _fallback_translation_data = {}

    if lang == "en":
        _translation_data = _fallback_translation_data
        return

    try:
        module = importlib.import_module(f"translations.{lang}")

        _translation_data = getattr(module, "TRANSLATIONS", {})

    except ImportError:
        print(
            f"Warning: Translation module for '{lang}' not found in 'translations' package. Falling back to default."
        )
        _translation_data = _fallback_translation_data
    except AttributeError:
        print(
            f"Warning: Module 'translations.{lang}' found but 'TRANSLATIONS' dict is missing."
        )
        _translation_data = _fallback_translation_data


def set_current_language(lang):
    """Sets the current language and loads the corresponding translation file."""
    global _current_language
    _current_language = lang
    load_language_data(lang)


def _get_plural_form(lang, n, forms):
    """Selects the correct plural form from a list based on the number."""
    # Convert to integer
    n = int(n) if n is not None else 0

    # Languages with no plural forms (all forms are the same)
    if lang in ["zh", "ja", "ko", "tr"]:  # Chinese, Japanese, Korean, Turkish
        return forms[0] if forms else ""

    if lang == "pl":
        if not forms or len(forms) < 3:
            return forms[0] if forms else ""
        if n == 1:
            return forms[0]  # 1 utwór
        elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
            return forms[1]  # 2, 3, 4 utwory
        else:
            return forms[2]  # 5 utworów, 0 utworów

    # Russian (3 forms)
    if lang == "ru":
        if not forms or len(forms) < 3:
            return forms[0] if forms else ""
        if n % 10 == 1 and n % 100 != 11:
            return forms[0]  # 1, 21, 31...
        elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
            return forms[1]  # 2-4, 22-24, 32-34...
        else:
            return forms[2]  # 0, 5-20, 25-30...

    # French (2 forms, but with a specific rule: 0 uses the plural form)
    if lang == "fr":
        if not forms:
            return ""
        if n <= 1:
            return forms[0]  # 0 or 1
        else:
            return forms[1] if len(forms) > 1 else forms[0]

    # For other languages (English, German, Spanish, Portuguese)
    # Standard logic: 1 = singular, everything else = plural
    if not forms:
        return ""
    if n == 1:
        return forms[0]
    else:
        return forms[1] if len(forms) > 1 else forms[0]


def translate(key, count=None, **kwargs):
    """Translates a key using loaded language data, with a fallback to English."""
    if not isinstance(key, str):
        return str(key)

    lang = _current_language
    string_to_format = _translation_data.get(key)
    is_missing = False

    if string_to_format is None:
        string_to_format = _fallback_translation_data.get(key)
        if string_to_format is None:
            is_missing = True
            string_to_format = key

    if count is not None:
        kwargs["count"] = count
        if isinstance(string_to_format, list):
            string_to_format = _get_plural_form(lang, count, string_to_format)
    try:
        formatted_string = string_to_format.format(**kwargs)
    except (KeyError, IndexError):
        return f"<span style='color: red;'>[FMT_ERR] {string_to_format}</span>"
    if is_missing:
        return f"<span style='color: red;'>⚠️{formatted_string}⚠️</span>"
    else:

        return formatted_string
