"""
SmartHire AI - Development Plan & Resource Recommendations (Gelişim Yol Haritası)
React DevelopmentPlan.jsx kopyası.
Eksik alanlar için Video, Teknik Makale/Dokümantasyon ve İnteraktif Platform kaynak önerilerini
tamamen native Streamlit componentleri ile (render_html / HTML kullanmadan) çizer.
"""

import streamlit as st
from utils.session import SessionManager

PRIORITY_CARDS = [
    {
        "id": 1,
        "title": "1. Sistem & API Tasarımı Mimarisi",
        "score": 45,
        "badge": "Yüksek Öncelik",
        "badge_kind": "danger",  # kırmızı ton
        "goal": "Büyük ölçekli sistemlerin temel bileşenlerini (load balancer, CDN, caching, RESTful API tasarımı) açıklayabilmek.",
        "resources": [
            {"title": "ByteByteGo — System Design 101", "url": "https://blog.bytebytego.com", "type": "🎥 Video Course"},
            {"title": "System Design Primer (donnemartin)", "url": "https://github.com/donnemartin/system-design-primer", "type": "📰 Teknik Makale / Dokümantasyon"},
            {"title": "roadmap.sh — System Design Path", "url": "https://roadmap.sh/system-design", "type": "💻 İnteraktif Platform"}
        ],
        "estimate": "3–4 Hafta"
    },
    {
        "id": 2,
        "title": "2. Veritabanı & İlişkisel Mimari",
        "score": 58,
        "badge": "Yüksek Öncelik",
        "badge_kind": "danger",
        "goal": "İlişkisel veritabanlarında indeksleme, transaction ACID kuralları ve sorgu optimizasyonunu uygulamak.",
        "resources": [
            {"title": "PostgreSQL Documentation", "url": "https://www.postgresql.org/docs/", "type": "📰 Dokümantasyon"},
            {"title": "SQLBolt — Interactive SQL Lessons", "url": "https://sqlbolt.com/", "type": "💻 İnteraktif Platform"},
            {"title": "Mode Analytics SQL Tutorial", "url": "https://mode.com/sql-tutorial/", "type": "📰 Teknik Makale"}
        ],
        "estimate": "2–3 Hafta"
    },
    {
        "id": 3,
        "title": "3. Algoritma & Veri Yapıları",
        "score": 62,
        "badge": "Orta Öncelik",
        "badge_kind": "warning",  # turuncu ton
        "goal": "LeetCode Medium seviye soruları 20 dakikada optimum karmaşıklıkla çözebilmek.",
        "resources": [
            {"title": "CS50x — Harvard Algorithm Series", "url": "https://youtube.com", "type": "🎥 Video"},
            {"title": "roadmap.sh — Data Structures", "url": "https://roadmap.sh", "type": "📰 Dokümantasyon"},
            {"title": "NeetCode 150 Practice", "url": "https://neetcode.io", "type": "💻 İnteraktif Platform"}
        ],
        "estimate": "4–6 Hafta"
    }
]


def render():
    """Gelişim Yol Haritası Ekranını native Streamlit componentleri ile çizer."""

    st.markdown("## Gelişim Yol Haritası & Öğrenme Kaynakları 🗺️")
    st.caption(
        "Son mülakat verilerine göre kişiselleştirildi • "
        "Zayıf noktalarınızı güçlendirmek için önerilen kaliteli kaynaklar"
    )

    st.write("")  # dikey boşluk

    for card in PRIORITY_CARDS:
        with st.container(border=True):
            # --- Başlık + Rozet (badge) satırı ---
            title_col, badge_col = st.columns([4, 1])
            with title_col:
                st.markdown(f"#### {card['title']}")
            with badge_col:
                if card["badge_kind"] == "danger":
                    st.error(card["badge"], icon="🔥")
                else:
                    st.warning(card["badge"], icon="⚠️")

            # --- Skor & Süre metrikleri ---
            m1, m2 = st.columns(2)
            with m1:
                st.metric("Mevcut Skor", f"%{card['score']}")
            with m2:
                st.metric("Tahmini Çalışma Süresi", card["estimate"])

            # --- Hedef bilgisi ---
            st.info(f"🎯 **Hedef:** {card['goal']}")

            # --- Önerilen kaynaklar ---
            st.markdown("**📚 Önerilen Öğrenme Kaynakları:**")
            for res in card["resources"]:
                res_col, type_col, link_col = st.columns([3, 2, 1])
                with res_col:
                    st.markdown(f"**{res['title']}**")
                with type_col:
                    st.caption(res["type"])
                with link_col:
                    st.link_button("Kaynağa Git", res["url"], use_container_width=True)

        st.write("")  # kartlar arası boşluk

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Yeni Mülakat Yap & Skorunu Güncelle", use_container_width=True, type="primary"):
            SessionManager.start_new_interview()
    with col2:
        if st.button("📊 Dashboard'a Dön", use_container_width=True, type="secondary"):
            SessionManager.navigate_to("dashboard")