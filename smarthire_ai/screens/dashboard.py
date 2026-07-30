"""
SmartHire AI - Dashboard Ekranı
React Dashboard.jsx bileşeni referans alınarak yerel Streamlit widget'ları ve cards.py / progressbar.py bileşenleri ile yeniden oluşturulmuştur.
Hiçbir ham HTML string'i, inline CSS veya unsafe_allow_html İÇERMEZ.
"""

import streamlit as st
from utils.session import SessionManager
from components.header import render_page_header
from components.cards import render_stat_card, render_info_card
from components.progressbar import render_progress_bar

def render():
    """Dashboard Görünümünü çizer."""
    
    user = st.session_state.user
    user_name = user.get("name", "Senan").split()[0]
    
    # 1. Welcome Header & CTA
    col_h1, col_h2 = st.columns([3, 1], gap="medium")
    with col_h1:
        render_page_header(
            title=f"Merhaba, {user_name} 👋",
            subtitle="Hazırlık skorun %78 — hedefi geçmek için mülakat simülasyonuna başla.",
            badge="⚡ SmartHire AI Dashboard",
            badge_variant="primary"
        )
    with col_h2:
        if st.button("🚀 Yeni Mülakat Başlat", key="dash_start_btn", use_container_width=True, type="primary"):
            SessionManager.start_new_interview()

    # 2. Metrik Kartları (3 Kolon)
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        render_stat_card("Hazırlık Skoru", "%78", "📈", "3 mülakat verisi • Güncel")
        render_progress_bar(value=78, size="thin", animated=True)
        
    with col2:
        render_stat_card("Son Mülakat Skoru", "%68", "🎯", "Frontend Developer — 24 Temmuz")
        render_progress_bar(value=68, size="thin", animated=True)
        
    with col3:
        render_stat_card("CV Uyum Oranı", "%88", "📄", "React Developer pozisyonu ile")
        render_progress_bar(value=88, size="thin", animated=True)

    st.divider()
    
    # 3. Gelişim Önerileri ve Hızlı İşlemler
    col_left, col_right = st.columns([1, 1], gap="large")
    
    with col_left:
        st.markdown("### 💡 Gelişim Önerileri")
        
        render_info_card(
            title="Sistem tasarımı konusunu güçlendir",
            description="Son mülakatta sistem tasarımı sorularında %45 puan aldın.",
            icon="⚠️",
            badge="Yüksek Öncelik"
        )
        
        render_info_card(
            title="Veri yapıları pratik yap",
            description="LeetCode ile günde 2 soru çözümü öneriliyor.",
            icon="📚",
            badge="Orta Öncelik"
        )
        
        render_info_card(
            title="React bilgin güçlü — devam et",
            description="Hooks ve performans optimizasyonu konularında %88 aldın.",
            icon="✅",
            badge="Güçlü Alan"
        )
        
        render_info_card(
            title="İletişim becerilerini geliştir",
            description="Cevaplarında daha net yapılandırma (STAR metodu) önerilir.",
            icon="🎯",
            badge="Orta Öncelik"
        )
        
    with col_right:
        st.markdown("### ⚡ Hızlı İşlemler")
        
        with st.container(border=True):
            st.caption("🚀 Yeni Mülakat Başlat — AI ile pratik yap")
            if st.button("Mülakat Simülasyonuna Git ➡️", key="qa_new_int", use_container_width=True, type="primary"):
                SessionManager.start_new_interview()
                
        with st.container(border=True):
            st.caption("🗺️ Gelişim Yol Haritası — Kişisel öğrenme planın")
            if st.button("Yol Haritasını İncele ➡️", key="qa_dev_plan", use_container_width=True, type="secondary"):
                SessionManager.navigate_to("dev_plan")
                
        with st.container(border=True):
            st.caption("📄 CV'ni Güncelle — Yeni pozisyon analizi yap")
            if st.button("CV Yükleme Ekranına Git ➡️", key="qa_update_cv", use_container_width=True, type="secondary"):
                SessionManager.navigate_to("upload_cv")
                
        with st.container(border=True):
            st.caption("📈 Sonuç Raporunu Gör — Detaylı performans analizi")
            if st.button("Sonuç Raporunu Aç ➡️", key="qa_view_results", use_container_width=True, type="secondary"):
                SessionManager.navigate_to("result")
