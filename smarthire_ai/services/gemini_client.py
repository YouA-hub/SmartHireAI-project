"""
Gemini Client
"""

from google import genai

from config import (
    get_api_key,
    MODEL_NAME
)


_client_cache = {}


def get_client():
    api_key = get_api_key()
    if api_key not in _client_cache:
        _client_cache[api_key] = genai.Client(api_key=api_key)
    return _client_cache[api_key]


class _ClientProxy:
    @property
    def models(self):
        return get_client().models


client = _ClientProxy()


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