"""
SmartHire AI - Badge Components

Tamamen Streamlit widget'ları ile oluşturulmuş rozet bileşenleri.
"""

import streamlit as st


def render_badge(text: str, variant: str = "primary"):
    """
    Ekrana küçük bir rozet gösterir.
    """

    colors = {
        "primary": "🔵",
        "success": "🟢",
        "warning": "🟡",
        "danger": "🔴",
        "accent": "🟣",
        "neutral": "⚪"
    }

    icon = colors.get(variant, "🔵")

    st.caption(f"{icon} {text}")


def get_badge_html(*args, **kwargs):
    """
    Eski kodlarla uyumluluk için bırakıldı.
    HTML döndürmez.
    """
    return ""