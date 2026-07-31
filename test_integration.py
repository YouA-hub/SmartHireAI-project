"""
SmartHire AI - Integration & DB Fallback Verification Test
"""

import sys
import os

# Robust path resolution for smarthire_ai directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWN_SMARTHIRE_DIR = r"c:\Users\senan\OneDrive\Desktop\SmartHire-Streamlit\smarthire_ai"

target_dir = None
if os.path.exists(os.path.join(BASE_DIR, "smarthire_ai")):
    target_dir = os.path.join(BASE_DIR, "smarthire_ai")
elif os.path.exists(KNOWN_SMARTHIRE_DIR):
    target_dir = KNOWN_SMARTHIRE_DIR
else:
    curr = BASE_DIR
    for _ in range(5):
        candidate = os.path.join(curr, "smarthire_ai")
        if os.path.exists(candidate):
            target_dir = candidate
            break
        curr = os.path.dirname(curr)

if target_dir and target_dir not in sys.path:
    sys.path.insert(0, target_dir)


from utils.auth import hash_password, verify_password
from database.connection import run_db_query
import database.queries as queries


def test_auth_hashing():
    print("Testing password hashing...")
    pw = "SuperSecret123!"
    h = hash_password(pw)
    assert verify_password(pw, h) is True
    assert verify_password("WrongPassword", h) is False
    print("[OK] Auth hashing test passed!")


def test_db_fallback():
    print("Testing DB query fallback behavior...")
    # Intentional failing query callback to test fallback return
    result = run_db_query(lambda db: db.execute(queries.get_user_by_email(db, "nonexistent@example.com")), default="FALLBACK_OK")
    assert result == "FALLBACK_OK"
    print("[OK] DB query fallback test passed!")


if __name__ == "__main__":
    test_auth_hashing()
    test_db_fallback()
    print("ALL INTEGRATION TESTS PASSED SUCCESSFULLY!")
