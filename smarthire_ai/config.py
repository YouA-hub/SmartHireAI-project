"""
SmartHire AI - Configuration
"""

import os
from dotenv import load_dotenv

load_dotenv()

# API KEY
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY .env dosyasında bulunamadı."
    )

# MODEL
MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)