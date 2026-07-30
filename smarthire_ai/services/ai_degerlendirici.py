"""
SmartHire AI
Gemini AI Evaluation Service

TÜBİTAK 2209-A
"""

from __future__ import annotations

import json
import logging
import time
from typing import Dict, List, Optional

from google.genai import types

from config import MODEL_NAME
from services.gemini_client import client

logger = logging.getLogger(__name__)


# =====================================================
# JSON SCHEMAS
# =====================================================

QUESTION_SCHEMA = {
    "type": "object",
    "properties": {
        "questions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "category": {"type": "string"},
                    "question": {"type": "string"}
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
        "match_rate": {"type": "integer"},
        "matched_skills": {
            "type": "array",
            "items": {"type": "string"}
        },
        "missing_skills": {
            "type": "array",
            "items": {"type": "string"}
        },
        "summary": {"type": "string"}
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
                    "category": {"type": "string"},
                    "content_score": {"type": "integer"},
                    "clarity_score": {"type": "integer"},
                    "relevance_score": {"type": "integer"},
                    "final_score": {"type": "integer"}
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


# =====================================================
# GEMINI HELPERS
# =====================================================

def _clean_json(text: str) -> str:
    """
    Gemini bazen
    ```json
    ...
    ```
    şeklinde cevap verir.
    """
    if not text:
        return ""

    text = text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "", 1)

    if text.startswith("```"):
        text = text.replace("```", "", 1)

    if text.endswith("```"):
        text = text[:-3]

    return text.strip()


def _call_gemini(
    prompt: str,
    schema: dict,
    retries: int = 3
) -> Optional[dict]:

    for attempt in range(retries):
        try:
            print(f"\n====== GEMINI DENEME {attempt+1}/{retries} ======")

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                    response_mime_type="application/json",
                    response_schema=schema
                )
            )

            print("\n====== GEMINI RAW RESPONSE ======")
            print(response.text)
            print("=================================\n")

            text = _clean_json(response.text)
            result = json.loads(text)

            return result

        except Exception as e:
            err_msg = f"{type(e).__name__}: {e}"
            print("\n========== GEMINI ERROR ==========")
            print(err_msg)
            print("==================================\n")
            try:
                import streamlit as st
                st.session_state["last_gemini_error"] = err_msg
            except Exception:
                pass

            time.sleep(2)

    print("❌ Gemini başarısız. Fallback kullanılacak.")
    return None


# =====================================================
# CV - JOB MATCH
# =====================================================

def evaluate_cv_match(
    cv_text: str,
    position: str,
    job_description: str,
    experience_level: str = ""
) -> dict:
    """
    CV ile iş ilanı arasındaki uyumu Gemini ile analiz eder.
    """
    fallback = {
        "match_rate": 70,
        "matched_skills": [],
        "missing_skills": [],
        "summary": "AI değerlendirmesi yapılamadığı için yaklaşık skor gösteriliyor.",
        "used_ai": False
    }

    if not cv_text:
        return fallback

    prompt = f"""
Sen deneyimli bir İnsan Kaynakları uzmanısın.

Görevin aşağıdaki CV ile iş ilanını karşılaştırmaktır.

POZİSYON
{position}

DENEYİM
{experience_level}

İŞ İLANI
{job_description}

CV
{cv_text[:7000]}

Değerlendirmen gereken başlıklar:
• Teknik beceriler
• Programlama dilleri
• Framework bilgisi
• Eğitim
• Projeler
• Deneyim
• İş ilanındaki zorunlu şartlar
• Tercih edilen şartlar

Kurallar
- 0-100 arasında gerçekçi puan ver.
- Eksik teknolojileri yaz.
- Güçlü teknolojileri yaz.
- Türkçe kısa bir özet oluştur.

Sadece JSON döndür.
"""

    result = _call_gemini(prompt, CV_MATCH_SCHEMA)

    if result is None:
        return fallback

    result["used_ai"] = True
    return result


# =====================================================
# INTERVIEW QUESTION GENERATION
# =====================================================

def generate_interview_questions(
    cv_text: str,
    position: str,
    job_description: str,
    experience_level: str = ""
) -> dict:
    """
    CV ve iş ilanına göre dinamik mülakat soruları üretir.
    """
    fallback = {
        "questions": [
            {
                "category": "Genel",
                "question": "Kendinizi ve teknik geçmişinizi kısaca tanıtır mısınız?"
            },
            {
                "category": "Teknik Bilgi",
                "question": f"{position} pozisyonu için en güçlü teknik yönünüz nedir?"
            },
            {
                "category": "Problem Çözme",
                "question": "Zorlandığınız bir problemi nasıl çözdünüz?"
            },
            {
                "category": "Takım Çalışması",
                "question": "Takım içerisinde yaşadığınız bir anlaşmazlığı nasıl yönettiniz?"
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

Aşağıdaki aday için gerçek bir teknik mülakat hazırla.

HEDEF POZİSYON
{position}

DENEYİM
{experience_level}

İŞ İLANI
{job_description}

CV
{cv_text[:7000]}

Kurallar:
- Tam olarak 5 soru üret.
- Sorular birbirinden farklı olsun.
- Kolaydan zora doğru ilerlesin.
- CV'de geçen projeleri dikkate al.
- İş ilanındaki teknolojileri dikkate al.
- Ezber soru üretme.
- Teknik odaklı olsun.
- Gerektiğinde adayın projeleri hakkında soru sor.

Her soru için bir kategori yaz.

Sadece JSON döndür.
"""

    result = _call_gemini(prompt, QUESTION_SCHEMA)

    if result is None:
        return fallback

    result["used_ai"] = True
    return result


# =====================================================
# INTERVIEW EVALUATION
# =====================================================

def evaluate_interview_answers(
    questions: List[dict],
    answers: List[str],
    position: str,
    experience_level: str = "",
    cv_text: str = ""
) -> dict:
    """
    Gemini ile gerçek mülakat değerlendirmesi.
    """
    categories = [q["category"] for q in questions]

    fallback = {
        "question_scores": [
            {
                "category": c,
                "content_score": 60,
                "clarity_score": 60,
                "relevance_score": 60,
                "final_score": 60
            }
            for c in categories
        ],
        "strengths": [],
        "improvement_areas": [
            "AI değerlendirmesi yapılamadı."
        ],
        "ai_feedback": "Gemini yanıt vermediği için yaklaşık skor gösteriliyor.",
        "used_ai": False
    }

    if not questions:
        return fallback

    qa = ""
    for i, question in enumerate(questions):
        answer = ""
        if i < len(answers):
            answer = answers[i]

        if not answer.strip():
            answer = "(Boş bırakıldı)"

        qa += f"""
Kategori:
{question["category"]}

Soru:
{question["question"]}

Cevap:
{answer}
"""

    prompt = f"""
Sen Google'da çalışan kıdemli bir teknik mülakat uzmanısın.

Aşağıdaki mülakat cevaplarını değerlendir.

POZİSYON
{position}

DENEYİM
{experience_level}

CV
{cv_text[:5000]}

SORULAR VE CEVAPLAR
{qa}

Kurallar:
Boş cevap: 0-20
Alakasız cevap: 10-35
Anlamsız karakterler (örnek: asdasd, qwerty, drftgyhujkl): 0-15
Çok kısa cevap: 20-40
Yüzeysel cevap: 40-60
Doğru ama eksik: 60-75
İyi teknik cevap: 75-90
Çok güçlü teknik cevap: 90-100

Her soru için şu puanları üret:
content_score
clarity_score
relevance_score
final_score

final_score şu formülle hesaplanmalı:
content*0.50 + clarity*0.30 + relevance*0.20

Daha sonra;
- güçlü yönler
- geliştirilmesi gereken alanlar
- aday hakkında 3-4 cümlelik profesyonel değerlendirme
oluştur.

JSON dışında hiçbir şey yazma.
"""

    result = _call_gemini(prompt, INTERVIEW_SCHEMA)

    if result is None:
        return fallback

    result["used_ai"] = True
    return result


# =====================================================
# SCORE CALCULATIONS
# =====================================================

def calculate_interview_score(question_scores: List[dict]) -> int:
    """Genel mülakat puanı."""
    if not question_scores:
        return 0

    return round(
        sum(q["final_score"] for q in question_scores) / len(question_scores)
    )


def calculate_communication_score(question_scores: List[dict]) -> int:
    """İfade puanı."""
    if not question_scores:
        return 0

    return round(
        sum(q["clarity_score"] for q in question_scores) / len(question_scores)
    )


def calculate_hireability(
    interview_score: int,
    cv_match_score: int
) -> int:
    """
    İşe alınma olasılığı.
    Mülakat %65, CV %35
    """

    if interview_score is None:
        interview_score = 0

    if cv_match_score is None:
        cv_match_score = 70

    score = (interview_score * 0.65) + (cv_match_score * 0.35)

    return round(score)

# =====================================================
# STRENGTHS
# =====================================================

def get_top_strengths(
    question_scores: List[dict],
    top_n: int = 3
) -> List[str]:

    if not question_scores:
        return []

    sorted_scores = sorted(
        question_scores,
        key=lambda x: x["final_score"],
        reverse=True
    )

    result = []
    for item in sorted_scores:
        if item["final_score"] >= 75:
            result.append(item["category"])

    if not result:
        result = [item["category"] for item in sorted_scores[:2]]

    return result[:top_n]


# =====================================================
# IMPROVEMENTS
# =====================================================

def get_improvement_areas(
    question_scores: List[dict],
    top_n: int = 3
) -> List[str]:

    if not question_scores:
        return []

    sorted_scores = sorted(
        question_scores,
        key=lambda x: x["final_score"]
    )

    result = []
    for item in sorted_scores:
        if item["final_score"] < 70:
            result.append(item["category"])

    if not result:
        result = [item["category"] for item in sorted_scores[-2:]]

    return result[:top_n]


# =====================================================
# RESOURCE SUGGESTIONS
# =====================================================

RESOURCE_LIBRARY = {
    "Python": [
        "[https://docs.python.org/3/](https://docs.python.org/3/)",
        "[https://realpython.com/](https://realpython.com/)"
    ],
    "Java": [
        "[https://docs.oracle.com/en/java/](https://docs.oracle.com/en/java/)",
        "[https://www.baeldung.com/](https://www.baeldung.com/)"
    ],
    "SQL": [
        "[https://sqlbolt.com/](https://sqlbolt.com/)",
        "[https://mode.com/sql-tutorial/](https://mode.com/sql-tutorial/)"
    ],
    "React": [
        "[https://react.dev/](https://react.dev/)",
        "[https://scrimba.com/learn-react](https://scrimba.com/learn-react)"
    ],
    "API": [
        "[https://developer.mozilla.org/](https://developer.mozilla.org/)",
        "[https://restfulapi.net/](https://restfulapi.net/)"
    ]
}

def suggest_learning_resources(
    weak_categories: List[str]
) -> Dict[str, List[str]]:

    suggestions = {}

    for category in weak_categories:
        found = False
        for key, value in RESOURCE_LIBRARY.items():
            if key.lower() in category.lower():
                suggestions[category] = value
                found = True
                break

        if not found:
            suggestions[category] = [
                "[https://roadmap.sh](https://roadmap.sh)",
                "[https://www.freecodecamp.org/](https://www.freecodecamp.org/)"
            ]

    return suggestions


# =====================================================
# LANGUAGE ANALYSIS
# =====================================================

def analyze_language_consistency(
    cv_language: Optional[str],
    interview_answers: List[str]
) -> str:

    if not cv_language:
        return "CV'de yabancı dil bilgisi bulunamadı."

    total = 0
    english = 0

    for answer in interview_answers:
        words = answer.split()
        total += len(words)
        english += sum(word.isascii() for word in words)

    if total == 0:
        return "Yeterli veri yok."

    ratio = english / total

    if ratio > 0.70:
        return "Tutarlı"

    if ratio > 0.35:
        return "Kısmen Tutarlı"

    return "Farklılık Gösteriyor"


# =====================================================
# RESULT SUMMARY
# =====================================================

def build_result_summary(
    interview_result: dict,
    cv_match: dict,
    interview_answers: List[str],
    cv_language: Optional[str]
):

    interview_score = calculate_interview_score(interview_result["question_scores"])
    communication_score = calculate_communication_score(interview_result["question_scores"])
    hireability = calculate_hireability(interview_score, cv_match["match_rate"])

    strengths = interview_result.get("strengths")
    if not strengths:
        strengths = get_top_strengths(interview_result["question_scores"])

    improvements = interview_result.get("improvement_areas")
    if not improvements:
        improvements = get_improvement_areas(interview_result["question_scores"])

    resources = suggest_learning_resources(improvements)
    language = analyze_language_consistency(cv_language, interview_answers)

    return {
        "interview_score": interview_score,
        "communication_score": communication_score,
        "cv_match_score": cv_match["match_rate"],
        "hireability": hireability,
        "strengths": strengths,
        "improvement_areas": improvements,
        "resource_suggestions": resources,
        "language_consistency": language,
        "ai_feedback": interview_result["ai_feedback"],
        "question_scores": interview_result["question_scores"]
    }


# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":
    print("SmartHire AI Evaluation Service")