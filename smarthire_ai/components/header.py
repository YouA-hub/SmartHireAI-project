"""
SmartHire AI - Header Components

Tamamen Streamlit widgetları kullanılarak oluşturulmuş ortak sayfa başlığı.
"""

import streamlit as st


def render_page_header(
    title: str,
    subtitle: str = "",
    badge: str | None = None,
    badge_variant: str = "primary"
):
    """
    Ortak Sayfa Başlığı
    """

    if badge:
        st.caption(badge)

    st.title(title)

    if subtitle:
        st.write(subtitle)

    st.divider()