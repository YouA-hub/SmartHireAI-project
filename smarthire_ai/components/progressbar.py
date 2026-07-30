"""
SmartHire AI - Progress Bar Component
"""

import streamlit as st


def render_progress_bar(
    value: int,
    label: str | None = None,
    value_label: str | None = None,
    size="thin",
    animated=True
):
    if label:
        c1, c2 = st.columns([5, 1])

        with c1:
            st.caption(label)

        with c2:
            st.caption(value_label or f"{value}%")

    st.progress(int(value))