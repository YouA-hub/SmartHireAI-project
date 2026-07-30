"""
SmartHire AI - CV Confirmation Page

Tamamen Streamlit widget'ları kullanılarak oluşturulmuş
CV onay ekranı.
"""

import streamlit as st

from utils.session import SessionManager
from components.header import render_page_header
from components.cards import (
    render_card,
    render_info_card,
)


def render():
    """CV Onay Sayfası"""

    cv_data = st.session_state.get("cv_data", {})

    user = st.session_state.get("user", {})
    user_name = user.get("name", "Kullanıcı")

    render_page_header(
        title="CV Özeti ✅",
        subtitle="CV analiz edildi. Bilgileri kontrol ederek devam edebilirsin.",
        badge="Adım 2 / 2"
    )

    render_card(
        title="Aday Bilgileri",
        body=(
            f"**Ad Soyad:** {user_name}\n\n"
            f"**Dosya:** {cv_data.get('file_name','CV.pdf')}\n\n"
            f"**Pozisyon:** {cv_data.get('position','Frontend Developer')}\n\n"
            f"**Deneyim:** {cv_data.get('experience_level','Mid')}"
        )
    )

    st.divider()

    st.subheader("🎯 CV — İlan Uyum Analizi")

    match_rate = cv_data.get("match_rate")

    if match_rate is not None:

        if not cv_data.get("cv_match_evaluated_by_ai", False):
            st.caption(
                "⚠️ Bu skor yapay zeka tarafından hesaplanamadı, "
                "yaklaşık bir değer gösteriliyor."
            )

        col1, col2 = st.columns([1, 2])

        with col1:
            st.metric("Uyum Oranı", f"%{match_rate}")

        with col2:
            st.progress(match_rate / 100)

        if cv_data.get("ai_cv_summary"):
            st.write(cv_data["ai_cv_summary"])

        col_a, col_b = st.columns(2)

        with col_a:
            st.write("**✅ Eşleşen Beceriler**")
            for skill in cv_data.get("matched_skills", []):
                st.success(skill)

        with col_b:
            st.write("**⚠️ Eksik Beceriler**")
            missing = cv_data.get("missing_skills", [])
            if missing:
                for skill in missing:
                    st.warning(skill)
            else:
                st.caption("Belirgin bir eksik bulunamadı.")

    else:
        st.info(
            "Uyum analizi için iş ilanı metni girilmedi — "
            "CV Yükle sayfasından iş ilanı ekleyerek tekrar deneyebilirsin."
        )

    st.divider()

    st.subheader("🛠️ Tespit Edilen Beceriler")

    skills = cv_data.get("skills", [])

    if skills:

        cols = st.columns(2)

        for index, skill in enumerate(skills):

            with cols[index % 2]:
                st.success(skill)

    else:

        st.info("CV içerisinde beceri bulunamadı.")

    st.divider()

    render_info_card(
        title="Mülakat Soruları Hazır",
        description=(
            "CV analiz edildi ve hedef pozisyona uygun "
            "kişiselleştirilmiş sorular oluşturuldu."
        ),
        icon="🤖",
        badge="AI Hazır"
    )

    st.divider()

    if st.button(
        "🚀 Mülakat Hazırlığına Geç",
        use_container_width=True,
        type="primary"
    ):
        SessionManager.navigate_to("ready")