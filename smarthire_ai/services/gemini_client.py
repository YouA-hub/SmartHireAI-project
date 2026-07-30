"""
Gemini Client
"""

from google import genai

from config import (
    GEMINI_API_KEY,
    MODEL_NAME
)

client = genai.Client(
    api_key=GEMINI_API_KEY
)


def generate(prompt: str) -> str:
    """
    Gemini'den metin üretir.
    """

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        text = response.text.strip()

        print("\n========== GEMINI ==========")
        print(text)
        print("============================\n")

        return text

    except Exception as e:

        print("\n========== GEMINI ERROR ==========")
        print(type(e).__name__)
        print(e)
        print("==================================\n")

        raise