"""
SmartHire AI - Configuration
"""

import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def get_api_key():
    key = os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_KEY") or os.getenv("API_KEY")

    if not key and hasattr(st, "secrets"):
        try:
            for k in ("GEMINI_API_KEY", "gemini_api_key", "GEMINI_KEY", "GEMINI", "default"):
                if k in st.secrets:
                    val = st.secrets[k]
                    if isinstance(val, str):
                        key = val
                        break
                    elif isinstance(val, dict) and "GEMINI_API_KEY" in val:
                        key = val["GEMINI_API_KEY"]
                        break

            if not key:
                for k, val in st.secrets.items():
                    if isinstance(val, str) and (val.startswith("AQ") or len(val) > 20):
                        key = val
                        break
                    elif isinstance(val, dict):
                        for subk, subval in val.items():
                            if isinstance(subval, str) and (subval.startswith("AQ") or len(subval) > 20):
                                key = subval
                                break
                        if key:
                            break
        except Exception:
            pass

    if key:
        key = str(key).strip().strip('"').strip("'")
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