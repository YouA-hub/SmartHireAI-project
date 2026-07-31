"""
SmartHire AI - Interview History Page

React InterviewHistory sayfasının native Streamlit karşılığı.
Tamamlanan tüm mülakatların listesini gösterir.

Hiçbir render_html / unsafe_allow_html / inline HTML string İÇERMEZ.
"""

import streamlit as st

from utils.session import SessionManager
from database.connection import run_db_query
import database.queries as queries
from components.header import render_page_header
from components.progressbar import render_progress_bar


def _get_history_records():
    """Önce DB'den mülakat geçmişini çeker, bulunamazsa session_state'e döner."""
    user_id = st.session_state.user.get("id")
    if user_id:
        sessions = run_db_query(lambda db: queries.get_user_sessions(db, user_id)) or []
        if sessions:
            history = []
            for s in sessions:
                res = run_db_query(lambda db, sid=s.id: queries.get_result_by_session(db, sid))
                date_str = s.baslangic_tarihi.strftime("%d.%m.%Y") if s.baslangic_tarihi else ""
                history.append({
                    "session_id": s.oturum_kodu,
                    "date": date_str,
                    "position": s.pozisyon or "Frontend Developer",
                    "readiness_score": res.hazirlik_skoru if (res and res.hazirlik_skoru is not None) else 0,
                    "hireability_rate": float(res.ise_alim_orani) if (res and res.ise_alim_orani is not None) else 0,
                    "cv_match_score": res.cv_uyum_skoru if (res and res.cv_uyum_skoru is not None) else 0,
                    "question_count": s.toplam_soru_sayisi or 0,
                })
            return history

    return list(reversed(st.session_state.interview_history))


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

    history = _get_history_records()


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
