"""
SmartHire AI - Interview Ready Page

Tamamen Streamlit widget'ları kullanılarak oluşturulmuş
mülakat hazırlık ekranı.
"""

import streamlit as st

from utils.session import SessionManager
from components.header import render_page_header
from components.cards import (
    render_stat_card,
    render_info_card,
)


def render():
    """Hazırlık Sayfası"""

    cv_data = st.session_state.get("cv_data", {})

    position = cv_data.get(
        "position",
        "Frontend Developer"
    )

    experience = cv_data.get(
        "experience_level",
        "Mid"
    )

    render_page_header(
        title="Mülakata Hazır mısın? 🚀",
        subtitle=f"{position} • {experience}",
        badge="Hazırlık Tamamlandı"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        render_stat_card(
            "CV Uyum Skoru",
            "%88",
            "🎯",
            "Yüksek Uyum"
        )

    with col2:
        render_stat_card(
            "Toplam Soru",
            "6",
            "❓",
            "4 Teknik + 2 Genel"
        )

    with col3:
        render_stat_card(
            "Tahmini Süre",
            "10 dk",
            "⏱️",
            "90 sn / soru"
        )

    st.divider()

    st.subheader("Mülakat Kuralları")

    col_left, col_right = st.columns(2)

    with col_left:

        render_info_card(
            title="Süre",
            description="Her soru için 90 saniye süren bulunuyor.",
            icon="⏱️",
            badge="90 sn"
        )

        render_info_card(
            title="Tek Oturum",
            description="Sorular arasında geri dönüş yapılamaz.",
            icon="📌",
            badge="Kural"
        )

    with col_right:

        render_info_card(
            title="İngilizce Sorusu",
            description="Son soru İngilizce iletişim becerini ölçer.",
            icon="🇬🇧",
            badge="English"
        )

        render_info_card(
            title="İpucu",
            description="İstersen soru altında bulunan ipuçlarını kullanabilirsin.",
            icon="💡",
            badge="Destek"
        )

    st.divider()

    if st.button(
        "🚀 Mülakatı Başlat",
        use_container_width=True,
        type="primary"
    ):
        SessionManager.navigate_to("interview")