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
    """Geçmiş Mülakatlar Sayfası"""

    render_page_header(
        title="Geçmiş Mülakatlar 📚",
        subtitle="Tamamladığın tüm mülakat simülasyonlarını buradan inceleyebilirsin.",
        badge="Geçmiş",
    )

    history = list(reversed(st.session_state.interview_history))

    if not history:
        st.info(
            "Henüz tamamlanmış bir mülakatın yok. "
            "Dashboard'dan yeni bir mülakat başlatarak buraya kayıt düşebilirsin."
        )

        if st.button(
            "🚀 Yeni Mülakat Başlat",
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
                st.subheader(record["position"])
                st.caption(f"📅 {record['date']} • {record['question_count']} soru")

            with col2:
                st.metric("Hazırlık Skoru", f"%{record['readiness_score']}")

            col_a, col_b = st.columns(2)

            with col_a:
                st.caption(f"İşe Alınabilirlik: %{record['hireability_rate']}")
                render_progress_bar(
                    value=record["hireability_rate"], size="thin"
                )

            with col_b:
                st.caption(f"CV Uyumu: %{record['cv_match_score']}")
                render_progress_bar(
                    value=record["cv_match_score"], size="thin"
                )
