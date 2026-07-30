"""
SmartHire AI - Configuration
"""

import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def get_api_key():
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        try:
            if hasattr(st, "secrets"):
                if "GEMINI_API_KEY" in st.secrets:
                    key = st.secrets["GEMINI_API_KEY"]
                elif "GEMINI" in st.secrets and "GEMINI_API_KEY" in st.secrets["GEMINI"]:
                    key = st.secrets["GEMINI"]["GEMINI_API_KEY"]
        except Exception:
            pass
    return key or ""

GEMINI_API_KEY = get_api_key()

# MODEL
MODEL_NAME = os.getenv("GEMINI_MODEL")

if not MODEL_NAME:
    try:
        MODEL_NAME = st.secrets.get("GEMINI_MODEL")
    except Exception:
        pass

if not MODEL_NAME:
    MODEL_NAME = "gemini-3.5-flash-lite"