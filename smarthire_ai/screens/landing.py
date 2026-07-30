"""
SmartHire AI - Landing (Pazarlama) Sayfası
React Landing.jsx referansının native Streamlit karşılığı.

Bu sayfa, oturum açmamış bir ziyaretçinin SmartHire AI'a ilk girişte
gördüğü sayfadır (React videosundaki "Hayalindeki işe AI ile hazırlan"
hero ekranının karşılığı). Giriş/Kayıt sayfasına DOĞRUDAN düşürmek
yerine, önce ürünü tanıtan bir pazarlama sayfası gösterilir.

Hiçbir render_html / unsafe_allow_html / inline HTML/CSS/JS İÇERMEZ.
Sadece st.columns, st.container(border=True), st.metric, st.button,
st.markdown (düz metin) kullanılmıştır.
"""

import streamlit as st
from utils.session import SessionManager


FEATURES = [
    (
        "🧠", "AI Destekli Mülakat",
        "Gerçek zamanlı, pozisyona özel teknik ve davranışsal sorularla "
        "gerçeğine en yakın mülakat deneyimini yaşa."
    ),
    (
        "📄", "CV Analizi",
        "CV'ni yükle, AI iş ilanıyla uyumunu analiz etsin; güçlü ve "
        "eksik yönlerini net biçimde görün."
    ),
    (
        "📊", "Performans Skoru",
        "Hazırlık skorun, güçlü/zayıf yönlerin ve kategori bazlı "
        "ilerlemen tek ekranda."
    ),
]

HOW_IT_WORKS = [
    ("1", "CV'ni Yükle", "PDF CV'ni yükle, hedef pozisyonunu ve iş ilanını ekle."),
    ("2", "Mülakatı Yap", "AI'nin sana özel hazırladığı sorulara süre sınırında cevap ver."),
    ("3", "Gelişim Planını Al", "Skorunu, eksik alanlarını ve kişisel yol haritanı incele."),
]

STATS = [
    ("👥", "12.000+", "Aktif kullanıcı"),
    ("🎯", "%87", "İş bulma başarı oranı"),
    ("💼", "50+", "Desteklenen rol"),
]


def _render_hero():
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.caption("⚡ AI Destekli Mülakat Koçu")
        st.markdown("# Hayalindeki işe\n# AI ile hazırlan")
        st.write(
            "CV'ni analiz et, pozisyona özel mülakat soruları al, anlık "
            "geri bildirimle gelişim planını oluştur. Türkiye'nin ilk AI "
            "mülakat koçuyla rakiplerinden bir adım önde ol."
        )

        cta_col1, cta_col2 = st.columns([2, 1])
        with cta_col1:
            if st.button(
                "🚀 Ücretsiz Dene — kredi kartı gerekmez",
                type="primary",
                use_container_width=True,
                key="landing_hero_cta"
            ):
                SessionManager.navigate_to("register")
        with cta_col2:
            if st.button("Giriş Yap", use_container_width=True, key="landing_hero_login"):
                SessionManager.navigate_to("login")

    with col_right:
        with st.container(border=True):
            st.caption("🟢 Canlı önizleme")
            st.markdown("**Senan Öztürk** — Frontend Developer Adayı")
            st.metric("Hazırlık Skoru", "%72")
            st.progress(0.72)
            st.info("🤖 AI Soru: React'te virtual DOM nasıl çalışır ve performansa katkısı nedir?")
            st.progress(0.88, text="React — %88")
            st.progress(0.45, text="Sistem Tasarımı — %45")
            st.progress(0.67, text="Algoritmalar — %67")


def _render_stats():
    cols = st.columns(len(STATS))
    for col, (icon, value, label) in zip(cols, STATS):
        with col:
            st.metric(f"{icon} {label}", value)


def _render_features():
    st.divider()
    st.caption("Özellikler")
    st.markdown("## Mülakat hazırlığında ihtiyacın olan her şey")
    st.write("CV analizinden kişisel gelişim planına kadar tüm süreç tek platformda.")

    cols = st.columns(3)
    for col, (icon, title, desc) in zip(cols, FEATURES):
        with col:
            with st.container(border=True):
                st.markdown(f"### {icon}")
                st.markdown(f"**{title}**")
                st.caption(desc)


def _render_how_it_works():
    st.divider()
    st.caption("Nasıl Çalışır")
    st.markdown("## 3 adımda mülakata hazır ol")

    cols = st.columns(3)
    for col, (step, title, desc) in zip(cols, HOW_IT_WORKS):
        with col:
            with st.container(border=True):
                st.markdown(f"#### {step}. {title}")
                st.caption(desc)


def _render_final_cta():
    st.divider()
    col_left, col_mid, col_right = st.columns([1, 2, 1])
    with col_mid:
        with st.container(border=True):
            st.markdown("### Hazır mısın?")
            st.write("Hemen ücretsiz dene, kredi kartı bilgisi istemiyoruz.")
            if st.button(
                "Ücretsiz Başla →",
                type="primary",
                use_container_width=True,
                key="landing_final_cta"
            ):
                SessionManager.navigate_to("register")


def render():
    """Landing (pazarlama) sayfası"""

    _render_hero()
    st.divider()
    _render_stats()
    _render_features()
    _render_how_it_works()
    _render_final_cta()
