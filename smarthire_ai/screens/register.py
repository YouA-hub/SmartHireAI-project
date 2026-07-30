"""
SmartHire AI - Register Page

Tamamen Streamlit widget'ları kullanılarak oluşturulmuş
kayıt ekranı.
"""

import streamlit as st

from utils.session import SessionManager
from components.header import render_page_header


def render():
    """Kayıt Sayfası"""

    render_page_header(
        title="Hesap Oluştur ✨",
        subtitle="Ücretsiz kaydol ve AI mülakat simülasyonuna başla.",
        badge="SmartHire AI"
    )

    col_left, col_mid, col_right = st.columns([1, 2, 1])

    with col_mid:

        # NOT: "Şifreyi Göster" checkbox'ı bilerek st.form(...) DIŞINDA
        # tutuluyor. Streamlit formlarındaki widget'lar sadece submit
        # butonuna basılınca script'i yeniden çalıştırır; checkbox form
        # içindeyken tıklanınca sayfa hemen güncellenmediği için şifre
        # gizli/açık geçişi çalışmıyormuş gibi görünüyordu. Formun
        # dışına alınca her tıklamada anında rerun tetikleniyor.

        full_name = st.text_input(
            "Ad Soyad",
            placeholder="Senan Öztürk",
            key="register_full_name"
        )

        email = st.text_input(
            "E-posta",
            placeholder="sen@ornek.com",
            key="register_email"
        )

        password = st.text_input(
            "Şifre",
            type="default" if st.session_state.get("register_show_password") else "password",
            key="register_password_input"
        )

        show_password = st.checkbox(
            "Şifreyi Göster",
            key="register_show_password"
        )

        role = st.selectbox(
            "Hedef Pozisyon",
            [
                "Frontend Developer",
                "Backend Developer",
                "Full Stack Developer",
                "Data Scientist",
                "AI Engineer",
                "Diğer"
            ],
            key="register_role"
        )

        custom_role = ""
        if role == "Diğer":
            custom_role = st.text_input(
                "Hedef pozisyonunu yaz",
                placeholder="Örn. Mobil Uygulama Geliştirici",
                key="register_custom_role"
            )

        accept_terms = st.checkbox(
            "Kullanım koşullarını kabul ediyorum.",
            key="register_accept_terms"
        )

        submitted = st.button(
            "🚀 Hesap Oluştur",
            use_container_width=True,
            type="primary",
            key="register_submit"
        )

        st.divider()

        if st.button(
            "🔑 Zaten hesabım var",
            use_container_width=True
        ):
            SessionManager.navigate_to("login")

        if submitted:

            if not full_name.strip():
                st.error("Ad Soyad boş bırakılamaz.")
                return

            if not email or "@" not in email:
                st.error("Geçerli bir e-posta giriniz.")
                return

            if len(password) < 8:
                st.error("Şifre en az 8 karakter olmalıdır.")
                return

            if not accept_terms:
                st.error("Devam etmek için kullanım koşullarını kabul etmelisiniz.")
                return

            if role == "Diğer" and not custom_role.strip():
                st.error("Lütfen hedef pozisyonunu yazın.")
                return

            target_position = custom_role.strip() if role == "Diğer" else role

            # Kayıt sırasında seçilen/yazılan hedef pozisyon, CV Yükle
            # sayfasında ön dolgu olarak kullanılsın. NOT: bu satır
            # login_user()'dan ÖNCE çalışmalı — login_user() içeride
            # navigate_to() -> st.rerun() çağırdığı için ondan sonraki
            # hiçbir kod çalışmıyordu.
            st.session_state.cv_data["position"] = target_position

            SessionManager.login_user(
                email=email,
                name=full_name
            )