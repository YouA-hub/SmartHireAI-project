"""
SmartHire AI
Gemini AI Evaluation Service

Bu modül;

- CV ile iş ilanı eşleştirmesi
- Dinamik mülakat sorusu üretimi
- Mülakat değerlendirmesi
- Tahmini işe alınma olasılığı
- Kaynak önerileri
- Dil tutarlılığı analizi

işlemlerini Google Gemini API kullanarak gerçekleştirir.

TÜBİTAK 2209-A
"""

from __future__ import annotations

import json
import logging
import os
from typing import Dict, List, Optional


from config import GEMINI_API_KEY

logger = logging.getLogger(__name__)

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
logger.info("Gemini API anahtarı yüklendi.")




_client = None

# ----------------------------------------------------
# Gemini Client
# ----------------------------------------------------

def _get_client():
    """
    Gemini istemcisini yalnızca ilk kullanımda oluşturur.
    """
    global _client

    if _client is not None:
        return _client

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        logger.warning("Gemini API Key bulunamadı.")
        return None

    try:
        from google import genai
        
        _client = genai.Client(
            api_key=api_key
        )
        
        logger.info("Gemini bağlantısı kuruldu.")
        return _client

    except Exception as e:
        logger.exception(e)
        return None


# ----------------------------------------------------
# JSON Şemaları
# ----------------------------------------------------

QUESTION_SCHEMA = {
    "type": "object",
    "properties": {
        "questions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string"
                    },
                    "question": {
                        "type": "string"
                    }
                },
                "required": [
                    "category",
                    "question"
                ]
            }
        }
    },
    "required": [
        "questions"
    ]
}

CV_MATCH_SCHEMA = {
    "type": "object",
    "properties": {
        "match_rate": {
            "type": "integer"
        },
        "matched_skills": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "missing_skills": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "summary": {
            "type": "string"
        }
    },
    "required": [
        "match_rate",
        "matched_skills",
        "missing_skills",
        "summary"
    ]
}

INTERVIEW_SCHEMA = {
    "type": "object",
    "properties": {
        "question_scores": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string"
                    },
                    "content_score": {
                        "type": "integer"
                    },
                    "clarity_score": {
                        "type": "integer"
                    },
                    "relevance_score": {
                        "type": "integer"
                    },
                    "final_score": {
                        "type": "integer"
                    }
                },
                "required": [
                    "category",
                    "content_score",
                    "clarity_score",
                    "relevance_score",
                    "final_score"
                ]
            }
        },
        "strengths": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "improvement_areas": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "ai_feedback": {
            "type": "string"
        }
    },
    "required": [
        "question_scores",
        "strengths",
        "improvement_areas",
        "ai_feedback"
    ]
}


# ----------------------------------------------------
# Gemini Ortak Çağrısı
# ----------------------------------------------------

def _call_gemini(prompt: str, schema: dict) -> Optional[dict]:
    client = _get_client()

    if client is None:
        return None

    try:
        from google.genai import types

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=schema,
                temperature=0.2
            )
        )
        return json.loads(response.text)

    except Exception as e:
        logger.exception(e)
        return None


# ----------------------------------------------------
# Dinamik Mülakat Sorusu Üretme
# ----------------------------------------------------

def generate_interview_questions(
    cv_text: str,
    position: str,
    job_description: str,
    experience_level: str = ""
) -> dict:
    """
    CV ve iş ilanını analiz ederek
    pozisyona özel 5 mülakat sorusu üretir.
    """
    fallback = {
        "questions": [
            {
                "category": "Genel Yazılım Bilgisi",
                "question": "Kendinizi ve teknik geçmişinizi kısaca anlatır mısınız?"
            },
            {
                "category": "Problem Çözme",
                "question": "Zorlandığınız bir projeyi ve nasıl çözdüğünüzü anlatın."
            },
            {
                "category": "Teknik Bilgi",
                "question": "Bu pozisyon için en güçlü teknik yönünüz nedir?"
            },
            {
                "category": "Takım Çalışması",
                "question": "Takım içinde yaşadığınız bir problemi nasıl çözdünüz?"
            },
            {
                "category": "Motivasyon",
                "question": "Neden bu pozisyonda çalışmak istiyorsunuz?"
            }
        ],
        "used_ai": False
    }

    if not cv_text:
        return fallback

    prompt = f"""
Sen kıdemli bir teknik mülakat uzmanısın.

Aşağıdaki CV'yi ve iş ilanını analiz et.

HEDEF POZİSYON:
{position}

DENEYİM SEVİYESİ:
{experience_level}

İŞ İLANI:
{job_description}

CV:
{cv_text[:7000]}

Görevin:
- Tam olarak 5 soru üret.
- Her soru farklı bir kategoriye ait olsun.
- Kategorileri kendin belirle.
- Sorular teknik olsun.
- CV'deki projeleri dikkate al.
- İş ilanındaki teknolojileri dikkate al.
- Sorular kolaydan zora doğru ilerlesin.

Sadece JSON döndür.
"""

    result = _call_gemini(prompt, QUESTION_SCHEMA)

    if result is None:
        return fallback

    result["used_ai"] = True
    return result


# ----------------------------------------------------
# CV - İş İlanı Uyum Analizi
# ----------------------------------------------------

def evaluate_cv_match(
    cv_text: str,
    position: str,
    job_description: str,
    experience_level: str = ""
) -> dict:
    """
    CV ile iş ilanı arasındaki uyumu analiz eder.
    """
    fallback = {
        "match_rate": 70,
        "matched_skills": [],
        "missing_skills": [],
        "summary": "Gemini kullanılamadığı için yaklaşık skor gösteriliyor.",
        "used_ai": False
    }

    if not cv_text or not job_description:
        return fallback

    prompt = f"""
Sen deneyimli bir İnsan Kaynakları uzmanısın.

CV ile iş ilanını karşılaştır.

Pozisyon:
{position}

Deneyim:
{experience_level}

İş ilanı:
{job_description}

CV:
{cv_text[:7000]}

Şunları değerlendir:
- Eğitim
- Teknik beceriler
- Programlama dilleri
- Framework bilgisi
- Sertifikalar
- Projeler
- Deneyim
- İş ilanındaki zorunlu yetkinlikler
- Tercih edilen yetkinlikler

0-100 arasında uyum puanı ver.

Sadece JSON döndür.
"""

    result = _call_gemini(prompt, CV_MATCH_SCHEMA)

    if result is None:
        return fallback

    result["used_ai"] = True
    return result


# ----------------------------------------------------
# Mülakat Değerlendirmesi
# ----------------------------------------------------

def evaluate_interview_answers(
    questions: List[dict],
    answers: List[str],
    position: str,
    experience_level: str = "",
    cv_text: str = "",
) -> dict:
    """
    Mülakat cevaplarını değerlendirir.

    Her soru;
    - İçerik Doğruluğu (%50)
    - Açıklık ve İfade (%30)
    - İlgi Düzeyi (%20)
    kriterlerine göre puanlanır.
    """
    categories = [q["category"] for q in questions]

    fallback = {
        "question_scores": [
            {
                "category": cat,
                "content_score": 65,
                "clarity_score": 65,
                "relevance_score": 65,
                "final_score": 65
            }
            for cat in categories
        ],
        "strengths": [
            "Sorular düzenli cevaplandı."
        ],
        "improvement_areas": [
            "Gemini kullanılamadığı için ayrıntılı analiz yapılamadı."
        ],
        "ai_feedback": "Yaklaşık değerlendirme gösteriliyor.",
        "used_ai": False
    }

    if not questions:
        return fallback

    qa_text = ""
    for i, soru in enumerate(questions):
        cevap = ""
        if i < len(answers):
            cevap = answers[i]

        if not cevap.strip():
            cevap = "(Boş bırakıldı)"

        qa_text += f"""
Kategori:
{soru["category"]}

Soru:
{soru["question"]}

Cevap:
{cevap}
"""

    prompt = f"""
Sen deneyimli bir teknik mülakat uzmanısın.

Aşağıdaki mülakatı değerlendir.

HEDEF POZİSYON
{position}

DENEYİM
{experience_level}

CV
{cv_text[:4000]}

SORULAR VE CEVAPLAR
{qa_text}

Her soru için;
1) İçerik Doğruluğu (0-100)
2) Açıklık ve İfade Yeteneği (0-100)
3) İlgi Düzeyi (0-100)
puanı ver.

Daha sonra;
Final Puanını
(Content × 0.50) + (Clarity × 0.30) + (Relevance × 0.20)
formülü ile hesapla.

Kurallar:
- Boş cevap çok düşük puan almalı.
- Konu dışı cevap düşük puan almalı.
- Yanlış teknik bilgi düşük puan almalı.
- Ezber cevap orta puan almalı.
- Doğru, açıklayıcı ve teknik cevap yüksek puan almalı.

Daha sonra;
- Güçlü yönleri yaz.
- Geliştirilmesi gereken alanları yaz.
- 2-3 cümlelik Türkçe AI geri bildirimi oluştur.

Sadece JSON döndür.
"""

    result = _call_gemini(prompt, INTERVIEW_SCHEMA)

    if result is None:
        return fallback

    result["used_ai"] = True
    return result


# ----------------------------------------------------
# Genel Mülakat Skoru
# ----------------------------------------------------

def calculate_interview_score(question_scores: List[dict]) -> int:
    """
    Beş sorunun ortalamasını alır.
    """
    if not question_scores:
        return 0

    ortalama = sum(
        q["final_score"] for q in question_scores
    ) / len(question_scores)

    return round(ortalama)


# ----------------------------------------------------
# İletişim Skoru
# ----------------------------------------------------

def calculate_communication_score(question_scores: List[dict]) -> int:
    """
    Açıklık ve İfade puanlarının ortalaması.
    """
    if not question_scores:
        return 0

    ortalama = sum(
        q["clarity_score"] for q in question_scores
    ) / len(question_scores)

    return round(ortalama)


# ----------------------------------------------------
# Tahmini İşe Alınma Olasılığı
# ----------------------------------------------------

def calculate_hireability(
    interview_score: int,
    cv_match_score: int
) -> int:
    """
    Hireability = Mülakat × 0.65 + CV × 0.35
    """
    skor = (interview_score * 0.65) + (cv_match_score * 0.35)
    return round(skor)


# ----------------------------------------------------
# Güçlü Yönleri Belirleme
# ----------------------------------------------------

def get_top_strengths(question_scores: List[dict], top_n: int = 3) -> List[str]:
    """
    En yüksek puanlı kategorileri döndürür.

    NOT: top_n, mevcut soru sayısının yarısını geçemez. Aksi halde
    (örn. 5 soru + top_n=3 ile) en yüksek 3 ve en düşük 3 kategori
    ortadaki soruyu paylaşır ve sonuç ekranında "Güçlü Yönler" ile
    "Gelişim Alanları" aynı kategoriyi gösterir — bu bir çakışma
    hatasıydı.
    """
    if not question_scores:
        return []

    max_n = max(1, len(question_scores) // 2)
    effective_n = min(top_n, max_n)

    sirali = sorted(
        question_scores,
        key=lambda x: x["final_score"],
        reverse=True
    )
    return [item["category"] for item in sirali[:effective_n]]


# ----------------------------------------------------
# Gelişim Alanlarını Belirleme
# ----------------------------------------------------

def get_improvement_areas(question_scores: List[dict], top_n: int = 3) -> List[str]:
    """
    En düşük puanlı kategorileri döndürür.

    NOT: get_top_strengths ile aynı sebepten top_n, soru sayısının
    yarısıyla sınırlandırılıyor — bkz. get_top_strengths docstring'i.
    """
    if not question_scores:
        return []

    max_n = max(1, len(question_scores) // 2)
    effective_n = min(top_n, max_n)

    sirali = sorted(
        question_scores,
        key=lambda x: x["final_score"]
    )
    return [item["category"] for item in sirali[:effective_n]]


# ----------------------------------------------------
# Kaynak Önerileri
# ----------------------------------------------------

RESOURCE_LIBRARY = {
    "Python": [
        "https://docs.python.org/3/",
        "https://realpython.com/",
        "https://www.freecodecamp.org/"
    ],
    "Java": [
        "https://docs.oracle.com/en/java/",
        "https://www.baeldung.com/",
        "https://www.geeksforgeeks.org/java/"
    ],
    "React": [
        "https://react.dev/",
        "https://scrimba.com/learn-react",
        "https://frontendmasters.com/"
    ],
    "SQL": [
        "https://www.sqlbolt.com/",
        "https://mode.com/sql-tutorial/",
        "https://www.w3schools.com/sql/"
    ],
    "API": [
        "https://restfulapi.net/",
        "https://developer.mozilla.org/",
        "https://swagger.io/"
    ]
}

def suggest_learning_resources(
    weak_categories: List[str]
) -> Dict[str, List[str]]:
    """
    Zayıf kategorilere göre kaynak önerir.
    """
    suggestions = {}

    for category in weak_categories:
        bulundu = False
        for key in RESOURCE_LIBRARY:
            if key.lower() in category.lower():
                suggestions[category] = RESOURCE_LIBRARY[key]
                bulundu = True
                break
        
        if not bulundu:
            suggestions[category] = [
                "https://roadmap.sh",
                "https://www.freecodecamp.org/",
                "https://developer.mozilla.org/"
            ]

    return suggestions


# ----------------------------------------------------
# Dil Tutarlılığı Analizi
# ----------------------------------------------------

def analyze_language_consistency(
    cv_language: Optional[str],
    interview_answers: List[str]
) -> str:
    """
    CV'deki yabancı dil seviyesi ile
    İngilizce cevapların tutarlılığını analiz eder.
    """
    if not cv_language:
        return "CV'de yabancı dil bilgisi bulunamadı."

    english_words = 0
    total_words = 0

    for answer in interview_answers:
        words = answer.split()
        total_words += len(words)
        
        for word in words:
            if word.isascii():
                english_words += 1

    if total_words == 0:
        return "İngilizce cevap bulunamadı."

    ratio = english_words / total_words

    if ratio > 0.70:
        return "Tutarlı"
    elif ratio > 0.35:
        return "Kısmen Tutarlı"
    
    return "Farklılık Gösteriyor"


# ----------------------------------------------------
# Sonuç Ekranı Verisi
# ----------------------------------------------------

def build_result_summary(
    interview_result: dict,
    cv_match: dict,
    interview_answers: List[str],
    cv_language: Optional[str]
) -> dict:
    """
    Sonuç ekranının ihtiyaç duyduğu
    bütün verileri tek sözlükte toplar.
    """
    interview_score = calculate_interview_score(
        interview_result["question_scores"]
    )

    communication_score = calculate_communication_score(
        interview_result["question_scores"]
    )

    hireability = calculate_hireability(
        interview_score,
        cv_match["match_rate"]
    )

    strengths = get_top_strengths(
        interview_result["question_scores"]
    )

    improvements = get_improvement_areas(
        interview_result["question_scores"]
    )

    resources = suggest_learning_resources(
        improvements
    )

    language_analysis = analyze_language_consistency(
        cv_language,
        interview_answers
    )

    return {
        "interview_score": interview_score,
        "communication_score": communication_score,
        "cv_match_score": cv_match["match_rate"],
        "hireability": hireability,
        "strengths": strengths,
        "improvement_areas": improvements,
        "resource_suggestions": resources,
        "language_consistency": language_analysis,
        "ai_feedback": interview_result["ai_feedback"],
        "question_scores": interview_result["question_scores"]
    }
    # ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    print("AI Değerlendirici Testi")

    cv = """
Bilgisayar Mühendisliği öğrencisi.
Python, Java, SQL biliyor.
2 adet yapay zeka projesi geliştirdi.
"""

    ilan = """
Junior Python Developer

Aranan Özellikler:
- Python
- SQL
- Git
- REST API
"""

    sonuc = evaluate_cv_match(
        cv_text=cv,
        position="Junior Python Developer",
        job_description=ilan,
        experience_level="Junior"
    )

    print("\nCV Sonucu\n")
    print(json.dumps(sonuc, indent=2, ensure_ascii=False))

    sorular = [
        {
            "question": "Python'da list ile tuple farkı nedir?",
            "category": "Python"
        },
        {
            "question": "REST API nedir?",
            "category": "Backend"
        }
    ]

    cevaplar = [
        "Tuple değiştirilemez, list değiştirilebilir.",
        "REST API HTTP üzerinden çalışan servis mimarisidir."
    ]

    sonuc2 = evaluate_interview_answers(
        questions=sorular,
        answers=cevaplar,
        position="Junior Python Developer",
        experience_level="Junior",
        cv_text=cv
    )

    print("\nMülakat Sonucu\n")
    print(json.dumps(sonuc2, indent=2, ensure_ascii=False))