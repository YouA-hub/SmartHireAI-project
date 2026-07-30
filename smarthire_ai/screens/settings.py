"""
SmartHire AI - Settings Page

React Settings sayfasının native Streamlit karşılığı.
Bildirim, mülakat zorluğu ve hesap tercihlerini yönetir.

Hiçbir render_html / unsafe_allow_html / inline HTML string İÇERMEZ.
"""

import streamlit as st

from utils.session import SessionManager
from components.header import render_page_header


def _init_settings():
    if "app_settings" not in st.session_state:
        st.session_state.app_settings = {
            "email_notifications": True,
            "reminder_notifications": True,
            "interview_difficulty": "Mid Level (2-5 Yıl)",
            "language": "Türkçe",
        }


def render():
    """Ayarlar Sayfası"""

    _init_settings()
    settings = st.session_state.app_settings

    render_page_header(
        title="Ayarlar ⚙️",
        subtitle="Bildirim, dil ve mülakat tercihlerini buradan yönetebilirsin.",
        badge="Ayarlar",
    )

    with st.form("settings_form"):
        st.subheader("Bildirimler")

        email_notif = st.toggle(
            "E-posta bildirimleri",
            value=settings["email_notifications"],
        )
        reminder_notif = st.toggle(
            "Mülakat hatırlatmaları",
            value=settings["reminder_notifications"],
        )

        st.divider()
        st.subheader("Mülakat Tercihleri")

        difficulty = st.selectbox(
            "Varsayılan Deneyim Seviyesi",
            ["Junior", "Mid Level (2-5 Yıl)", "Senior", "Lead"],
            index=[
                "Junior",
                "Mid Level (2-5 Yıl)",
                "Senior",
                "Lead",
            ].index(settings["interview_difficulty"])
            if settings["interview_difficulty"]
            in ["Junior", "Mid Level (2-5 Yıl)", "Senior", "Lead"]
            else 1,
        )

        st.divider()
        st.subheader("Uygulama Dili")

        language = st.selectbox(
            "Dil",
            ["Türkçe", "English"],
            index=["Türkçe", "English"].index(settings["language"]),
        )

        submitted = st.form_submit_button(
            "💾 Ayarları Kaydet", use_container_width=True, type="primary"
        )

        if submitted:
            settings["email_notifications"] = email_notif
            settings["reminder_notifications"] = reminder_notif
            settings["interview_difficulty"] = difficulty
            settings["language"] = language

            st.success("Ayarların kaydedildi.")

    st.divider()

    st.subheader("Hesap")

    if st.button("🚪 Çıkış Yap", use_container_width=True):
        SessionManager.logout_user()
