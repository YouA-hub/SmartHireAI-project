"""
SmartHire AI - Sidebar Navigation Component
React Sidebar.jsx + AppLayout.jsx mimarisinin native Streamlit karşılığı.

Mimari kararı (React ile paralel):
- Oturum açılmamışsa (login/register): sidebar YOK, sadece üstte küçük bir
  marka logosu gösterilir. React'teki FullscreenLayout'un karşılığıdır.
- Oturum açıksa: kalıcı st.sidebar ile Dashboard / CV Yükle / CV Onay /
  Hazırlık / Mülakat / Sonuçlar / Yol Haritası navigasyonu + en altta
  kullanıcı bilgisi + çıkış butonu gösterilir. React'teki AppLayout'un
  (Sidebar + Navbar + Content) karşılığıdır.

Hiçbir render_html / unsafe_allow_html / inline HTML string İÇERMEZ.
Sadece st.sidebar, st.button, st.container(border=True), st.columns,
st.caption, st.markdown (düz metin) kullanılmıştır.
"""

import streamlit as st
from utils.session import SessionManager

# (etiket, sayfa anahtarı, ikon) — eski sidebar yapısı
NAV_ITEMS = [
    ("Dashboard", "dashboard", "📊"),
    ("CV Yükle", "upload_cv", "📄"),
    ("Mülakat", "interview", "🎤"),
    ("Mülakat Sonucu", "result", "📈"),
    ("Eski Mülakatlar", "interview_history", "📚"),
    ("Gelişim Planı", "dev_plan", "🗺️"),
    ("Profil", "profile", "👤"),
    ("Ayarlar", "settings", "⚙️"),
]


def _render_brand(container=st):
    """Marka logosu — hem sidebar'da hem fullscreen üst kısımda kullanılır."""
    container.markdown("### ⚡ SmartHire AI")


def render_navbar():
    """
    Ana giriş noktası. app.py bu fonksiyonu her sayfa yüklemesinde çağırır.
    """
    _render_sidebar()
    _render_leave_interview_dialog()


def _render_sidebar():
    """Kalıcı sol navigasyon."""
    current_page = SessionManager.get_current_page()
    user = st.session_state.get("user", {})

    with st.sidebar:
        _render_brand()
        st.divider()

        # --- Ana navigasyon ---
        for label, page_key, icon in NAV_ITEMS:
            is_active = current_page == page_key
            if st.button(
                f"{icon}  {label}",
                key=f"sidebar_nav_{page_key}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state.is_authenticated = True
                SessionManager.request_navigation(page_key)

        st.divider()

        # --- Kullanıcı kartı ---
        with st.container(border=True):
            col_avatar, col_info = st.columns([1, 3])
            with col_avatar:
                st.markdown(f"**{user.get('avatar_initials', 'U')}**")
            with col_info:
                st.caption(f"**{user.get('name', 'Kullanıcı')}**")
                st.caption(user.get("role", "Aday"))

        if st.button("🚪 Çıkış Yap", key="sidebar_logout", use_container_width=True):
            SessionManager.request_logout()


def _render_leave_interview_dialog():
    """
    Kullanıcı devam eden (tamamlanmamış) bir mülakattayken sidebar'dan
    başka bir sayfaya geçmeye ya da çıkış yapmaya çalıştığında açılan
    onay diyaloğu.

    st.session_state.pending_nav_target set edildiğinde tetiklenir
    (bkz. SessionManager.request_navigation / request_logout).
    """

    target = st.session_state.get("pending_nav_target")
    if not target:
        return

    target_label = (
        "çıkış yapmak"
        if target == "__logout__"
        else f"**{SessionManager.PAGES.get(target, target)}** sayfasına gitmek"
    )

    @st.dialog("⚠️ Mülakattan Ayrılmak Üzeresin")
    def _dialog():
        st.write(
            f"Devam eden bir mülakatın var. Şu an {target_label} istiyorsun. "
            "Ayrılırsan bu mülakat **erken sonlandırılmış** sayılır ve "
            "kaldığın yerden devam edemezsin — sadece yeni bir mülakat "
            "başlatabilirsin."
        )
        st.caption(
            "Devam etmek istiyorsan 'Mülakata Devam Et' seçeneğine, "
            "yine de ayrılmak istiyorsan diğer seçeneğe tıkla."
        )

        col_stay, col_leave = st.columns(2)
        with col_stay:
            if st.button(
                "↩️ Mülakata Devam Et",
                use_container_width=True,
                type="primary",
            ):
                SessionManager.cancel_pending_navigation()
        with col_leave:
            if st.button(
                "🚪 Mülakatı Sonlandır ve Ayrıl",
                use_container_width=True,
            ):
                SessionManager.confirm_pending_navigation()

    _dialog()