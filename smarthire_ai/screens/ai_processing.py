"""
SmartHire AI - AI Processing Page

React AIProcessing sayfasının (koyu tema, dairesel adım göstergesi, %)
native Streamlit karşılığı.

st.status() bileşeni, React'teki "CV analiz ediliyor / kişiselleştirme
tamamlanıyor" adım adım süreç göstergesini kayıpsız karşılar:
genişletilebilir bir kutu içinde adım adım log + spinner/tik ikonu.

Hiçbir render_html / unsafe_allow_html / inline HTML string İÇERMEZ.
"""

import time

import streamlit as st

from utils.session import SessionManager
from database.connection import run_db_query
import database.queries as queries
from components.header import render_page_header
from services.ai_degerlendirici import evaluate_cv_match


PROCESSING_STEPS = [
    ("CV içeriği taranıyor", 0.6),
    ("Beceriler ve deneyim çıkarılıyor", 0.7),
    ("Son kontroller yapılıyor", 0.4),
]


def render():
    """AI İşleniyor / Analiz Ekranı"""

    render_page_header(
        title="CV Analiz Ediliyor 🤖",
        subtitle="CV'n ve ilan bilgilerin yapay zeka tarafından işleniyor.",
        badge="Adım 3 / 4",
    )

    already_done = st.session_state.get("ai_processing_done", False)

    if already_done:
        st.success("Analiz tamamlandı.")
        if st.button(
            "✅ CV Onay Sayfasına Devam Et",
            use_container_width=True,
            type="primary",
        ):
            SessionManager.navigate_to("cv_confirm")
        return

    progress_bar = st.progress(0, text="Başlatılıyor...")

    with st.status("CV analiz ediliyor...", expanded=True) as status:
        total = len(PROCESSING_STEPS) + 1  # +1: gerçek AI değerlendirme adımı

        for index, (label, duration) in enumerate(PROCESSING_STEPS, start=1):
            st.write(f"• {label}")
            time.sleep(duration)

            progress_bar.progress(
                index / total,
                text=f"{label} ({index}/{total})",
            )

        # ---- Gerçek AI değerlendirmesi (sahte sleep değil, gerçek API çağrısı) ----
        st.write("• Pozisyon eşleşmesi hesaplanıyor")

        cv_data = st.session_state.cv_data

        match_result = evaluate_cv_match(
            cv_text=cv_data.get("clean_text", ""),
            position=cv_data.get("position", ""),
            job_description=cv_data.get("job_description", ""),
            experience_level=cv_data.get("experience_level", ""),
        )

        cv_data["match_rate"] = match_result["match_rate"]
        cv_data["matched_skills"] = match_result["matched_skills"]
        cv_data["missing_skills"] = match_result["missing_skills"]
        cv_data["ai_cv_summary"] = match_result["summary"]
        user_id = st.session_state.user.get("id")
        if user_id:
            run_db_query(lambda db: queries.update_cv_analysis(
                db,
                user_id=user_id,
                uyum_orani=match_result["match_rate"],
                eslesen_beceriler=match_result["matched_skills"],
                eksik_beceriler=match_result["missing_skills"],
                ai_cv_ozeti=match_result["summary"],
                cv_uyum_ai_ile_mi=match_result["used_ai"],
            ))
        SessionManager.persist_cv_data()

        progress_bar.progress(
            (len(PROCESSING_STEPS) + 1) / total,
            text=f"Pozisyon eşleşmesi hesaplanıyor ({total}/{total})",
        )

        status.update(
            label="Analiz tamamlandı ✅",
            state="complete",
            expanded=False,
        )

    st.session_state.ai_processing_done = True
    st.rerun()