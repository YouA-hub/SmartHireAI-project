"""
SmartHire AI - Main Application Entry Point (Root Wrapper for Deployments)
"""

import os
import sys

# Ensure smarthire_ai directory is in sys.path
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "smarthire_ai")
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import runpy

runpy.run_path(os.path.join(BASE_DIR, "app.py"), run_name="__main__")
