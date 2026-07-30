"""
SmartHire AI - Gemini Bağlantı Testi
"""

import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

print("-" * 50)
print("GEMINI BAĞLANTI TESTİ")
print("-" * 50)

if not api_key:
    print("❌ HATA: .env dosyasında GEMINI_API_KEY bulunamadı.")
    print("   Kontrol et: .env dosyası app.py ile AYNI klasörde mi?")
    raise SystemExit(1)

print(f"✅ API Key bulundu (ilk 6 karakter): {api_key[:6]}...")
print(f"✅ Model: {model_name}")
print()

try:
    from google import genai

    client = genai.Client(api_key=api_key)

    models = [
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
        "gemini-3.5-flash",
        "gemini-3.5-flash-lite",
    ]

    for model in models:

        print("\n" + "-" * 50)
        print(f"Model deneniyor: {model}")

        try:
            response = client.models.generate_content(
                model=model,
                contents="Sadece 'OK' yaz."
            )

            print("✅ ÇALIŞTI")
            print(response.text)

        except Exception as err:
            print("❌ Çalışmadı")
            print(err)

except Exception as e:
    print()
    print("❌ HATA OLUŞTU:")
    print(f"Tip: {type(e).__name__}")
    print(f"Mesaj: {e}")