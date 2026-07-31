"""
SmartHire AI - Login Page

Tamamen Streamlit widget'ları kullanılarak oluşturulmuş
giriş ekranı.
"""

import streamlit as st

from utils.session import SessionManager
from utils import user_store
from utils.auth import verify_password
from database.connection import run_db_query
import database.queries as queries
from components.header import render_page_header


def render():
    """Giriş Sayfası"""

    auth_notice = st.session_state.pop("auth_notice", None)
    if auth_notice:
        st.info(auth_notice)

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
            value=st.session_state.pop("login_email", ""),
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

            clean_email = email.strip().lower()

            # 1. DB'den kullanıcıyı çek
            db_user = run_db_query(lambda db: queries.get_user_by_email(db, clean_email))

            if db_user:
                if verify_password(password, db_user.sifre_hash):
                    SessionManager.login_user(
                        email=clean_email,
                        name=db_user.ad_soyad,
                        user_id=db_user.id
                    )
                    st.success("Giriş başarılı.")
                else:
                    st.error("E-posta veya şifre hatalı.")
                return

            # 2. Eğer DB'de yoksa veya DB offline ise fallback kontrolü yap
            saved_store = user_store.load_cv_data(clean_email)
            if saved_store is not None:
                user_name = clean_email.split("@")[0].capitalize()
                SessionManager.login_user(
                    email=clean_email,
                    name=user_name
                )
                st.success("Giriş başarılı.")
                return

            st.error("E-posta veya şifre hatalı.")