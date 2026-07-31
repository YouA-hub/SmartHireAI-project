import os

import streamlit as st
import streamlit.components.v1 as components

from utils.session import SessionManager
from database.connection import run_db_query
import database.queries as queries
from components.header import render_page_header
from components.timer import render_interview_timer
from services.ai_degerlendirici import (
    generate_interview_questions,
    evaluate_interview_answers,
    build_result_summary,
)

# --- Sekme/Pencere/Site Değişikliği Algılayıcı (çift yönlü bileşen) -------
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
    left = _tab_switch_component(key="tab_switch_detector", default=False)
    return bool(left)


def _terminate_interview_due_to_tab_switch():
    SessionManager._terminate_abandoned_interview(reason="tab_switch")
    SessionManager.navigate_to("interview")


def _ensure_questions_generated():
    """Ilk girişte AI sorularini uretir, session_state ve DB'ye yazar."""

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

    interview_state = st.session_state.interview_state
    interview_state["total_questions"] = len(questions)

    # DB'ye mülakat oturumunu ve sorularını kaydet
    user_id = st.session_state.user.get("id")
    session_code = interview_state["session_id"]
    if user_id:
        db_oturum = run_db_query(lambda db: queries.create_interview_session(
            db,
            user_id=user_id,
            oturum_kodu=session_code,
            pozisyon=cv_data.get("position"),
            deneyim_seviyesi=cv_data.get("experience_level"),
            toplam_soru_sayisi=len(questions),
        ))
        if db_oturum:
            interview_state["db_session_id"] = db_oturum.id
            for i, q in enumerate(questions):
                db_q = run_db_query(lambda db, idx=i, q_dict=q: queries.save_question(
                    db,
                    user_id=user_id,
                    oturum_id=db_oturum.id,
                    soru_metni=q_dict.get("question", ""),
                    kategori=q_dict.get("category"),
                    soru_sirasi=idx + 1,
                ))
                if db_q:
                    q["db_question_id"] = db_q.id


def _finish_interview():
    """Son cevap da alindiktan sonra tum mulakati Gemini ile degerlendirir,
    sonuclari interview_state ve DB'ye yazar."""

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
        "match_rate": cv_data.get("match_rate") or 70,
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

    # DB işlemleri: Soruların puan/geri bildirimlerini ve nihai sonuç özetini kaydet
    user_id = st.session_state.user.get("id")
    session_code = interview_state.get("session_id")

    for i, q_score in enumerate(summary.get("question_scores", [])):
        if i < len(questions):
            q_id = questions[i].get("db_question_id")
            if q_id:
                run_db_query(lambda db, qid=q_id, qs=q_score, ans=answers[i] if i < len(answers) else "": queries.save_answer_and_score(
                    db,
                    question_id=qid,
                    cevap=ans,
                    puan=qs.get("final_score"),
                    geri_bildirim=qs.get("feedback"),
                    icerik_puani=qs.get("content_score"),
                    aciklik_puani=qs.get("clarity_score"),
                    iliskililik_puani=qs.get("relevance_score"),
                ))

    db_oturum = run_db_query(lambda db: queries.complete_interview_session(db, oturum_kodu=session_code))
    oturum_id = db_oturum.id if db_oturum else interview_state.get("db_session_id")

    if user_id and oturum_id:
        run_db_query(lambda db: queries.save_result(
            db,
            user_id=user_id,
            oturum_id=oturum_id,
            ise_alim_orani=summary.get("hireability"),
            hazirlik_skoru=summary.get("interview_score"),
            cv_uyum_skoru=summary.get("cv_match_score"),
            iletisim_skoru=summary.get("communication_score"),
            kategori_skorlari=interview_state.get("category_scores"),
            guclu_yonler=summary.get("strengths"),
            gelisim_alanlari=summary.get("improvement_areas"),
            dil_tutarliligi=summary.get("language_consistency"),
            ai_geri_bildirimi=summary.get("ai_feedback"),
            ai_ile_degerlendirildi_mi=interview_result.get("used_ai", False),
        ))

    SessionManager.complete_current_interview()
    SessionManager.record_completed_interview()

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

        # DB'ye o anki sorunun cevabını kaydet
        q_id = current_question.get("db_question_id")
        if q_id:
            run_db_query(lambda db, qid=q_id, ans=answer: queries.save_answer_and_score(
                db,
                question_id=qid,
                cevap=ans
            ))

        if is_last_question:
            with st.spinner("Cevapların değerlendiriliyor..."):
                _finish_interview()
        else:
            interview_state["current_question_index"] += 1
            st.rerun()