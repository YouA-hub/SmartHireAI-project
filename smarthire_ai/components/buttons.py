"""
SmartHire AI - Button Component Library
React Button.jsx ve Button.css tasarımı ile birebir uyumlu buton bileşenleri.
"""

import streamlit as st

def render_button(
    label: str,
    key: str,
    variant: str = "primary",
    use_container_width: bool = True,
    disabled: bool = False,
    on_click=None
) -> bool:
    """
    Streamlit için özel stilli buton bileşeni.
    
    Args:
        label: Buton üzerindeki yazı
        key: Streamlit benzersiz anahtarı
        variant: 'primary', 'secondary', 'gradient', 'danger', 'ghost'
        use_container_width: Tam genişlikte mi gösterilsin
        disabled: Pasif durumda mı
        on_click: Tıklama callback fonksiyonu
        
    Returns:
        bool: Butona tıklandı mı
    """
    # Streamlit button type mapping
    btn_type = "primary" if variant in ["primary", "gradient"] else "secondary"
    
    clicked = st.button(
        label=label,
        key=key,
        type=btn_type,
        use_container_width=use_container_width,
        disabled=disabled,
        on_click=on_click
    )
    return clicked
