"""
SmartHire AI - Profile Page

React Profile sayfasının native Streamlit karşılığı.
Kullanıcı bilgilerini görüntüler ve düzenlemesine izin verir.

Hiçbir render_html / unsafe_allow_html / inline HTML string İÇERMEZ.
"""

import streamlit as st

from components.header import render_page_header
from components.cards import render_stat_card


def render():
    """Profil Sayfası"""

    render_page_header(
        title="Profilim 👤",
        subtitle="Kişisel bilgilerini ve CV özetini buradan yönetebilirsin.",
        badge="Profil",
    )

    user = st.session_state.user
    cv_data = st.session_state.cv_data

    col_avatar, col_info = st.columns([1, 3])

    with col_avatar:
        with st.container(border=True):
            st.markdown(f"## {user.get('avatar_initials', 'U')}")
            st.caption("Profil Rozeti")

    with col_info:
        st.subheader(user.get("name", "Kullanıcı"))
        st.caption(cv_data.get("position", "Pozisyon belirtilmedi"))
        st.write(user.get("email", ""))

    st.divider()

    st.subheader("Bilgileri Güncelle")

    with st.form("profile_form"):
        col1, col2 = st.columns(2)

        with col1:
            new_name = st.text_input("Ad Soyad", value=user.get("name", ""))

        with col2:
            new_email = st.text_input("E-posta", value=user.get("email", ""))
            new_position = st.text_input(
                "Hedef Pozisyon",
                value=cv_data.get("position", ""),
            )

        submitted = st.form_submit_button(
            "💾 Bilgileri Kaydet", use_container_width=True, type="primary"
        )

        if submitted:
            user["name"] = new_name
            user["email"] = new_email
            user["avatar_initials"] = "".join(
                part[0].upper() for part in new_name.split()[:2]
            ) or user.get("avatar_initials", "U")

            cv_data["position"] = new_position

            st.success("Profil bilgilerin güncellendi.")

    st.divider()

    st.subheader("CV Özeti")

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        render_stat_card(
            "CV Uyum Oranı",
            f"%{cv_data.get('match_rate', 0)}",
            "🎯",
        )

    with col_b:
        render_stat_card(
            "Deneyim Seviyesi",
            cv_data.get("experience_level", "-"),
            "📈",
        )

    with col_c:
        render_stat_card(
            "Yüklü CV",
            cv_data.get("file_name", "-"),
            "📄",
        )

    if cv_data.get("skills"):
        st.write("**Beceriler:**")
        st.caption(", ".join(cv_data["skills"]))