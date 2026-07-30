"""
SmartHire AI - Login Page

Tamamen Streamlit widget'ları kullanılarak oluşturulmuş
giriş ekranı.
"""

import streamlit as st

from utils.session import SessionManager
from components.header import render_page_header


def render():
    """Giriş Sayfası"""

    render_page_header(
        title="Tekrar Hoş Geldin 👋",
        subtitle="Hesabına giriş yap ve mülakat simülasyonuna devam et.",
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

        email = st.text_input(
            "E-posta",
            placeholder="sen@ornek.com",
            key="login_email"
        )

        password = st.text_input(
            "Şifre",
            type="default" if st.session_state.get("login_show_password") else "password",
            key="login_password_input"
        )

        show_password = st.checkbox(
            "Şifreyi Göster",
            key="login_show_password"
        )

        submitted = st.button(
            "🚀 Giriş Yap",
            use_container_width=True,
            type="primary",
            key="login_submit"
        )

        if st.button(
            "🔑 Şifremi Unuttum",
            use_container_width=True
        ):
            st.info("Şifre sıfırlama özelliği yakında eklenecek.")

        st.divider()

        st.button(
            "🌐 Google ile Giriş Yap",
            use_container_width=True
        )

        st.divider()

        st.write("Hesabın yok mu?")

        if st.button(
            "📝 Kayıt Ol",
            use_container_width=True
        ):
            SessionManager.navigate_to("register")

        if submitted:

            if not email:
                st.error("E-posta boş bırakılamaz.")
                return

            if "@" not in email:
                st.error("Geçerli bir e-posta giriniz.")
                return

            if not password:
                st.error("Şifre boş bırakılamaz.")
                return

            user_name = email.split("@")[0].capitalize()

            SessionManager.login_user(
                email=email,
                name=user_name
            )

            st.success("Giriş başarılı.")