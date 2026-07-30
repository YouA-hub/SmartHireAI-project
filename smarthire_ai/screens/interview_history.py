"""
SmartHire AI - Interview History Page

React InterviewHistory sayfasının native Streamlit karşılığı.
Tamamlanan tüm mülakatların listesini gösterir.

Hiçbir render_html / unsafe_allow_html / inline HTML string İÇERMEZ.
"""

import streamlit as st

from utils.session import SessionManager
from components.header import render_page_header
from components.progressbar import render_progress_bar


def render():
    """Eski Mülakatlar Sayfası"""

    col_title, col_back = st.columns([3, 1])

    with col_title:
        render_page_header(
            title="Eski Mülakatlar 📚",
            subtitle="Tamamladığın tüm mülakat simülasyonlarını buradan inceleyebilirsin.",
            badge="Eski Mülakatlar",
        )

    with col_back:
        if st.button("⬅️ Dashboard'a Dön", key="top_back_to_dash", use_container_width=True):
            SessionManager.navigate_to("dashboard")

    history = list(reversed(st.session_state.interview_history))

    if not history:
        st.info(
            "Henüz tamamlanmış bir mülakatın yok. "
            "Dashboard'dan yeni bir mülakat başlatarak buraya kayıt düşebilirsin."
        )

        col_back_empty, col_new_empty = st.columns(2)
        with col_back_empty:
            if st.button(
                "⬅️ Dashboard'a Dön",
                key="empty_back_to_dash",
                use_container_width=True,
            ):
                SessionManager.navigate_to("dashboard")
        with col_new_empty:
            if st.button(
                "🚀 Yeni Mülakat Başlat",
                key="empty_start_new",
                use_container_width=True,
                type="primary",
            ):
                SessionManager.start_new_interview()

        return

    st.caption(f"Toplam {len(history)} mülakat kaydı bulundu.")

    for record in history:
        with st.container(border=True):
            col1, col2 = st.columns([3, 2])

            with col1:
                st.subheader(record.get("position", "Frontend Developer"))
                st.caption(f"📅 {record.get('date', '')} • {record.get('question_count', 5)} soru")

            with col2:
                st.metric("Hazırlık Skoru", f"%{record.get('readiness_score', 0)}")

            col_a, col_b = st.columns(2)

            with col_a:
                st.caption(f"İşe Alınabilirlik: %{record.get('hireability_rate', 0)}")
                render_progress_bar(
                    value=record.get("hireability_rate", 0), size="thin"
                )

            with col_b:
                st.caption(f"CV Uyumu: %{record.get('cv_match_score', 0)}")
                render_progress_bar(
                    value=record.get("cv_match_score", 0), size="thin"
                )

    st.divider()

    col_dash, col_new = st.columns(2)
    with col_dash:
        if st.button("⬅️ Dashboard'a Dön", key="bottom_back_to_dash", use_container_width=True):
            SessionManager.navigate_to("dashboard")
    with col_new:
        if st.button("🚀 Yeni Mülakat Başlat", key="bottom_start_new", use_container_width=True, type="primary"):
            SessionManager.start_new_interview()
