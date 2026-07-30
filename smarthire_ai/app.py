"""
SmartHire AI - Main Application Entry Point & Router
TÜBİTAK 2209-A kapsamında geliştirilmiştir.
Streamlit Ana Uygulaması ve Sayfa Yönlendirici.
"""

import os
import sys
import streamlit as st

# Sayfa Yapılandırması (En üstte çağrılır)
st.set_page_config(
    page_title="SmartHire AI — Mülakat Simülasyon Platformu",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modül Yollarını Ekleme
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from utils.session import SessionManager
from components.navbar import render_navbar
from components.footer import render_footer

# 1. Custom CSS Yükleme
def load_css():
    css_path = os.path.join(BASE_DIR, "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 2. Oturum Durumunu Başlatma
SessionManager.init_session()

# 3. CSS Uygulama
load_css()

# 4. Üst Navigasyon Çubuğunu Çizme
render_navbar()

# 5. Dinamik Sayfa Yönlendirme (Router)
current_page = SessionManager.get_current_page()

if current_page == "landing":
    from screens.landing import render
    render()
elif current_page == "login":
    from screens.login import render
    render()
elif current_page == "register":
    from screens.register import render
    render()
elif current_page == "dashboard":
    from screens.dashboard import render
    render()
elif current_page == "upload_cv":
    from screens.upload_cv import render
    render()
elif current_page == "ai_processing":
    from screens.ai_processing import render
    render()
elif current_page == "cv_confirm":
    from screens.cv_confirm import render
    render()
elif current_page == "ready":
    from screens.ready import render
    render()
elif current_page == "interview":
    from screens.interview import render
    render()
elif current_page == "result":
    from screens.result import render
    render()
elif current_page == "dev_plan":
    from screens.dev_plan import render
    render()
elif current_page == "interview_history":
    from screens.interview_history import render
    render()
elif current_page == "profile":
    from screens.profile import render
    render()
elif current_page == "settings":
    from screens.settings import render
    render()
else:
    st.error("Sayfa bulunamadı.")

# 6. Alt Bilgi (Footer)
render_footer()