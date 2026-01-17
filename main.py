# Copyright (c) 2024 maxcreations
# Licensed under the MIT License.
# See LICENSE file in the project root for full license information.

import importlib
from utils_translator import translate, set_current_language

if __name__ == "__main__":
    # 1. Set Russian language
    set_current_language("ru")

    print("--- РУССКИЙ ЯЗЫК ---")
    # Simple variable replacement
    print(translate("welcome", name = "Ихтиандр"))

    # Plural forms (3 forms in RU)
    print(translate("apples", count = 1))  # 1 apple
    print(translate("apples", count = 3))  # 3 apples
    print(translate("apples", count = 10))  # 10 apples

    # 2. Switch to English
    set_current_language("en")

    print("\n--- ENGLISH LANGUAGE ---")
    print(translate("welcome", name = "Aquaman"))

    # Plural forms (2 forms in EN)
    print(translate("apples", count = 1))  # 1 apple
    print(translate("apples", count = 5))  # 5 apples

    # 3. Test missing key (Fallback)
    print("\n--- FALLBACK & ERRORS ---")
    # Key not present in any file
    print(translate("missing_key"))

    # Formatting error (argument {error} not provided)
    print(translate("error_msg"))