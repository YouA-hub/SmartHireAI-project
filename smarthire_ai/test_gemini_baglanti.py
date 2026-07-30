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

    print("İstek gönderiliyor...")
    response = client.models.generate_content(
        model=model_name,
        contents="Sadece 'merhaba' kelimesiyle cevap ver."
    )

    print()
    print("✅ BAŞARILI! Gemini'den gelen cevap:")
    print(response.text)

except Exception as e:
    print()
    print("❌ HATA OLUŞTU:")
    print(f"   Tip: {type(e).__name__}")
    print(f"   Mesaj: {e}")
    print()
    print("Olası nedenler:")
    print("  1. API anahtarı geçersiz / yanlış kopyalanmış (boşluk, eksik karakter)")
    print("  2. API anahtarı için Gemini API etkinleştirilmemiş")
    print("  3. Kota (quota) aşılmış veya faturalandırma sorunu var")
    print("  4. Model adı yanlış (gemini-2.5-flash yerine deneyebileceğin: gemini-2.0-flash)")