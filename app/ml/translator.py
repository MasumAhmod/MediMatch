import re

from deep_translator import GoogleTranslator


# =========================================================
# DETECT BENGALI TEXT
# =========================================================

def contains_bengali(text: str) -> bool:
    """
    Returns True if the text contains Bengali characters.
    """

    if not text:
        return False

    return bool(
        re.search(
            r"[\u0980-\u09FF]",
            text
        )
    )


# =========================================================
# TRANSLATE TEXT TO ENGLISH
# =========================================================

def translate_to_english(text: str) -> str:
    """
    Translates Bengali text into English.

    English text is returned unchanged.

    If translation fails, the original text is returned
    so that the application does not crash.
    """

    if not text:
        return ""

    # -----------------------------------------------------
    # English text
    # -----------------------------------------------------

    if not contains_bengali(text):
        return text

    # -----------------------------------------------------
    # Bengali → English
    # -----------------------------------------------------

    try:

        translated_text = GoogleTranslator(
            source="auto",
            target="en"
        ).translate(text)

        if translated_text:

            print(
                "Bengali translation:",
                translated_text
            )

            return translated_text

        return text

    except Exception as error:

        print(
            "Translation failed:",
            error
        )

        return text

