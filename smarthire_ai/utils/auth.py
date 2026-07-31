"""
SmartHire AI - Password Hashing & Auth Utilities
"""

import bcrypt


def hash_password(password: str) -> str:
    """Hashes a password string using bcrypt."""
    if isinstance(password, str):
        password_bytes = password.encode("utf-8")
    else:
        password_bytes = password
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    """Verifies a plain text password against a stored bcrypt hash."""
    if not password or not hashed:
        return False
    try:
        if isinstance(password, str):
            password_bytes = password.encode("utf-8")
        else:
            password_bytes = password

        if isinstance(hashed, str):
            hashed_bytes = hashed.encode("utf-8")
        else:
            hashed_bytes = hashed

        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception as e:
        print(f"[Auth Warning] Password verification error: {e}")
        return False
