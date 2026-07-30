"""
SmartHire AI - Basit Kalıcı Kullanıcı Verisi Deposu

Bu proje gerçek bir veritabanı kullanmıyor; her şey st.session_state
içinde tutuluyor. Bu da tarayıcı oturumu bittiğinde (çıkış yapıp tekrar
girince, ya da sayfa yeniden yüklenince) yüklenen CV'nin ve analiz
sonuçlarının kaybolmasına, kullanıcının her girişte CV'sini yeniden
yüklemek zorunda kalmasına yol açıyordu.

Bu modül, e-posta adresine göre anahtarlanmış basit bir JSON dosya
deposu sağlar. Gerçek bir veritabanının yerini tutmaz ama tek makinede
çalışan bu prototip için hesaba özel CV verisinin (yüklendi mi,
beceriler, pozisyon, İngilizce seviyesi vb.) kalıcı olmasını sağlar.
"""

from __future__ import annotations

import hashlib
import json
import os
from typing import Optional

# Depo dosyaları proje kökünün altında ayrı bir klasörde tutulur.
_STORE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "user_store",
)

# Diskte kalıcı tutulacak cv_data alanları. Buradaki alanlar dışındaki
# (örn. anlık işlem bayrakları) session_state alanları kaydedilmez.
_PERSISTED_CV_FIELDS = (
    "file_name",
    "uploaded",
    "position",
    "experience_level",
    "match_rate",
    "english_level",
    "skills",
    "clean_text",
    "job_description",
)


def _safe_key(email: str) -> str:
    """E-postayı dosya adı olarak güvenli hale getirir."""
    return hashlib.sha256(email.strip().lower().encode("utf-8")).hexdigest()


def _path_for(email: str) -> str:
    return os.path.join(_STORE_DIR, f"{_safe_key(email)}.json")


def load_cv_data(email: str) -> Optional[dict]:
    """
    Bu e-postaya ait daha önce kaydedilmiş CV verisini döndürür.
    Kayıt yoksa None döner.
    """
    if not email:
        return None

    path = _path_for(email)
    if not os.path.exists(path):
        return None

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def save_cv_data(email: str, cv_data: dict) -> None:
    """
    cv_data içindeki kalıcı tutulması gereken alanları bu e-postaya
    ait dosyaya yazar. Hesaba her girişte tekrar okunur.
    """
    if not email:
        return

    os.makedirs(_STORE_DIR, exist_ok=True)

    to_save = {
        field: cv_data.get(field)
        for field in _PERSISTED_CV_FIELDS
        if field in cv_data
    }

    try:
        with open(_path_for(email), "w", encoding="utf-8") as f:
            json.dump(to_save, f, ensure_ascii=False, indent=2)
    except OSError:
        # Diske yazamıyorsak (örn. salt-okunur ortam) sessizce geç;
        # oturum içi kullanım yine de session_state ile çalışmaya
        # devam eder, sadece kalıcılık sağlanamaz.
        pass
