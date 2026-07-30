"""
SmartHire AI - Configuration
"""

import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# API KEY
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    try:
        GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GEMINI", {}).get("GEMINI_API_KEY")
    except Exception:
        pass

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY .env veya Streamlit Secrets dosyasında bulunamadı."
    )

# MODEL
MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)