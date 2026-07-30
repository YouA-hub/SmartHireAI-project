"""
SmartHire AI - Live Interview Screen

Canli mulakat ekrani: AI tarafindan uretilen sorular tek tek sorulur,
her soru icin 90 saniyelik gorsel sayac gosterilir, cevaplar toplanir
ve son soru cevaplandiginda evaluate_interview_answers() ile Gemini
uzerinden degerlendirilip sonuc utils.session.interview_state icine
yazilir (bkz. screens/result.py).
"""

import os

import streamlit as st
import streamlit.components.v1 as components

from utils.session import SessionManager
from components.header import render_page_header
from components.timer import render_interview_timer
from services.ai_degerlendirici import (
    generate_interview_questions,
    evaluate_interview_answers,
    build_result_summary,
)

# --- Sekme/Pencere/Site Değişikliği Algılayıcı (çift yönlü bileşen) -------
#
# ÖNEMLİ: Eski yaklaşım (components.html + window.parent.location.href ile
# sayfayı ?left_interview=1 parametresiyle yeniden yükleme) ÇALIŞMIYORDU,
# çünkü Streamlit'in components.html iframe'i "sandbox"lı olup üst pencereyi
# (top-level) yönlendirme izni (allow-top-navigation) içermiyor; tarayıcı bu
# yönlendirmeyi sessizce engelliyordu.
#
# Bunun yerine burada Streamlit'in resmi çift-yönlü bileşen protokolünü
# (postMessage tabanlı — sandbox tarafından ASLA engellenmez) kendimiz,
# harici bir pip paketine ihtiyaç duymadan uyguluyoruz. Frontend kodu:
# components/tab_switch_frontend/index.html
_TAB_SWITCH_FRONTEND_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "components",
    "tab_switch_frontend",
)

_tab_switch_component = components.declare_component(
    "smarthire_tab_switch_detector",
    path=_TAB_SWITCH_FRONTEND_DIR,
)


def _detect_tab_switch() -> bool:
    """
    Gömülü bileşeni render eder ve kullanıcının mülakat sırasında başka
    bir sekmeye/pencereye/siteye geçip geçmediğini döndürür.

    Tarayıcı tarafında visibilitychange/blur/pagehide event'lerinden biri
    tetiklendiğinde, bileşen bunu postMessage ile ANINDA Python'a
    (bu fonksiyonun dönüş değeri olarak) bildirir — bu da normal bir
    widget değeri değişikliği gibi otomatik olarak bir Streamlit
    rerun'ı tetikler.
    """

    left = _tab_switch_component(key="tab_switch_detector", default=False)
    return bool(left)


def _terminate_interview_due_to_tab_switch():
    """Sekme/pencere/site değişikliği tespit edildiğinde mülakatı erken ve
    kalıcı biçimde sonlandırır; kullanıcı geri dönüp devam edemez."""

    SessionManager._terminate_abandoned_interview(reason="tab_switch")

    # is_completed artik True oldugu icin navigate_to("interview")
    # otomatik olarak "result" sayfasina yonlendirir.
    SessionManager.navigate_to("interview")


def _ensure_questions_generated():
    """Ilk girişte (veya sorular herhangi bir sebeple kayipsa) AI sorularini
    uretir ve session_state'e yazar. Ayni oturum icinde tekrar tekrar
    Gemini'ye istek atmamak icin bir kere uretilir."""

    if st.session_state.get("interview_questions"):
        return

    cv_data = st.session_state.get("cv_data", {})

    result = generate_interview_questions(
        cv_text=cv_data.get("clean_text", ""),
        position=cv_data.get("position", ""),
        job_description=cv_data.get("job_description", ""),
        experience_level=cv_data.get("experience_level", ""),
    )

    questions = result["questions"]

    st.session_state.interview_questions = questions
    st.session_state.interview_questions_used_ai = result.get("used_ai", False)

    st.session_state.interview_state["total_questions"] = len(questions)


def _finish_interview():
    """Son cevap da alindiktan sonra tum mulakati Gemini ile degerlendirir,
    sonuclari interview_state icine yazar ve sonuc sayfasina yonlendirir."""

    cv_data = st.session_state.cv_data
    interview_state = st.session_state.interview_state
    questions = st.session_state.interview_questions
    answers = interview_state["answers"]

    interview_result = evaluate_interview_answers(
        questions=questions,
        answers=answers,
        position=cv_data.get("position", ""),
        experience_level=cv_data.get("experience_level", ""),
        cv_text=cv_data.get("clean_text", ""),
    )

    cv_match = {
        "match_rate": cv_data.get("match_rate", 70),
    }

    summary = build_result_summary(
        interview_result=interview_result,
        cv_match=cv_match,
        interview_answers=answers,
        cv_language=cv_data.get("english_level"),
    )

    interview_state["readiness_score"] = summary["interview_score"]
    interview_state["hireability_rate"] = summary["hireability"]
    interview_state["cv_match_score"] = summary["cv_match_score"]
    interview_state["category_scores"] = [
        {"category": q["category"], "score": q["final_score"]}
        for q in summary["question_scores"]
    ]
    interview_state["strengths"] = summary["strengths"]
    interview_state["improvement_areas"] = summary["improvement_areas"]
    interview_state["ai_feedback"] = summary["ai_feedback"]
    interview_state["evaluated_by_ai"] = interview_result.get("used_ai", False)

    SessionManager.complete_current_interview()

    # is_completed artik True oldugu icin navigate_to("interview")
    # otomatik olarak "result" sayfasina yonlendirir.
    SessionManager.navigate_to("interview")


def render():
    """Canli Mulakat Sayfasi"""

    _ensure_questions_generated()

    questions = st.session_state.interview_questions
    interview_state = st.session_state.interview_state

    index = interview_state["current_question_index"]
    total = interview_state["total_questions"]

    current_question = questions[index]

    render_page_header(
        title="Mülakat 🎙️",
        subtitle=f"Soru {index + 1} / {total} — {current_question['category']}",
        badge="Canlı Oturum",
    )

    # Sekme/pencere/site değişikliği tespit edildiyse mülakatı hemen
    # sonlandır ve sonuç sayfasına yönlendir; sorunun geri kalanını render
    # etmeye devam etme.
    if _detect_tab_switch():
        _terminate_interview_due_to_tab_switch()
        return

    render_interview_timer(
        seconds_left=90,
        session_id=f"{interview_state['session_id']}_{index}",
    )

    st.subheader(current_question["question"])

    with st.expander("💡 İpucu"):
        st.write(
            "Cevabını somut bir örnekle destekle: ne yaptığını, "
            "neden o şekilde yaptığını ve sonucunu kısaca anlat."
        )

    answer_key = f"answer_input_{interview_state['session_id']}_{index}"

    answer = st.text_area(
        "Cevabın",
        key=answer_key,
        height=180,
        placeholder="Cevabını buraya yaz...",
    )

    is_last_question = index == total - 1
    button_label = "✅ Mülakatı Bitir" if is_last_question else "➡️ Sonraki Soru"

    st.caption("📌 Sorular arasında geri dönüş yapılamaz.")

    if st.button(button_label, use_container_width=True, type="primary"):

        interview_state["answers"].append(answer)

        if is_last_question:
            with st.spinner("Cevapların değerlendiriliyor..."):
                _finish_interview()
        else:
            interview_state["current_question_index"] += 1
            st.rerun()