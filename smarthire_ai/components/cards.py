"""
SmartHire AI - Card Components

React tasarımını referans alan, tamamen Streamlit widgetları ile
oluşturulmuş ortak kart bileşenleri.
"""

import streamlit as st


def render_stat_card(
    title: str,
    value: str,
    icon: str = "📊",
    subtitle: str = ""
):
    """
    Dashboard istatistik kartı
    """
    with st.container(border=True):
        col1, col2 = st.columns([1, 5])

        with col1:
            st.markdown(f"## {icon}")

        with col2:
            st.caption(title)
            st.markdown(f"## {value}")

            if subtitle:
                st.caption(subtitle)


def render_info_card(
    title: str,
    description: str,
    icon: str = "💡",
    badge: str | None = None
):
    """
    Bilgi kartı
    """
    with st.container(border=True):
        top_left, top_right = st.columns([5, 2])

        with top_left:
            st.markdown(f"### {icon} {title}")

        with top_right:
            if badge:
                st.caption(badge)

        st.write(description)


def render_card(
    title: str,
    body: str,
    badge: str | None = None
):
    with st.container(border=True):
        if title:
            col1, col2 = st.columns([5, 1])

            with col1:
                st.subheader(title)

            with col2:
                if badge:
                    st.caption(badge)

        st.write(body)


def render_section_container(
    title: str,
    subtitle: str = ""
):
    st.subheader(title)

    if subtitle:
        st.caption(subtitle)

    st.divider()