"""
SmartHire AI - Footer Component

Tamamen Streamlit bileşenleri ile oluşturulmuş ortak footer.
"""

import streamlit as st


def render_footer():
    """Uygulamanın alt bilgi alanını oluşturur."""

    st.divider()

    col1, col2 = st.columns([3, 1])

    with col1:
        st.caption(
            "SmartHire AI • TÜBİTAK 2209-A Yapay Zeka Destekli Mülakat Simülasyon Platformu"
        )

    with col2:
        st.caption("© 2026")