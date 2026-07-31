# database/queries.py
from datetime import datetime
from typing import Optional, List

from sqlalchemy.orm import Session

from database.models import (
    User,
    CVBilgileri,
    MulakatOturumu,
    MulakatSorulari,
    Sonuclar,
    KullaniciAyarlari,
)


# =====================================================
# 1. KULLANICI İŞLEMLERİ
# =====================================================

def create_user(
    db: Session,
    ad_soyad: str,
    email: str,
    sifre_hash: str,
    hedef_pozisyon: Optional[str] = None,
    kullanim_kosullari_onayi: bool = False,
):
    new_user = User(
        ad_soyad=ad_soyad,
        email=email,
        sifre_hash=sifre_hash,
        hedef_pozisyon=hedef_pozisyon,
        avatar_baslangic_harfleri="".join(
            parca[0].upper() for parca in ad_soyad.split()[:2]
        ) or None,
        kullanim_kosullari_onayi=kullanim_kosullari_onayi,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def update_user_alan(db: Session, user_id: int, alan: str):
    """Geriye dönük uyumluluk için korunan fonksiyon."""
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.mezuniyet_alani = alan
        db.commit()
        db.refresh(user)
    return user


def update_user_profile(
    db: Session,
    user_id: int,
    ad_soyad: Optional[str] = None,
    email: Optional[str] = None,
    hedef_pozisyon: Optional[str] = None,
):
    """profile.py -> 'Bilgileri Güncelle' formu için."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None

    if ad_soyad:
        user.ad_soyad = ad_soyad
        user.avatar_baslangic_harfleri = "".join(
            parca[0].upper() for parca in ad_soyad.split()[:2]
        ) or user.avatar_baslangic_harfleri

    if email:
        user.email = email

    if hedef_pozisyon is not None:
        user.hedef_pozisyon = hedef_pozisyon

    db.commit()
    db.refresh(user)
    return user


# =====================================================
# 2. CV İŞLEMLERİ
# =====================================================

def save_cv(
    db: Session,
    user_id: int,
    ham_metin: Optional[str] = None,
    **ek_alanlar,
):
    """
    CV oluşturur veya (kullanıcının zaten bir CV'si varsa) günceller.
    upload_cv.py akışında CV her yüklendiğinde bu fonksiyon çağrılmalıdır.

    ek_alanlar: dosya_adi, temiz_metin, sayfa_sayisi, tespit_edilen_isim,
    tespit_edilen_email, telefon, linkedin, github, kaggle, medium,
    gitlab, stackoverflow, website, pozisyon, deneyim_seviyesi,
    ilan_metni, beceriler, ingilizce_seviyesi, uyum_orani,
    eslesen_beceriler, eksik_beceriler, ai_cv_ozeti, cv_uyum_ai_ile_mi,
    yuklendi_mi gibi CVBilgileri sütunlarından herhangi biri olabilir.
    """
    cv = db.query(CVBilgileri).filter(CVBilgileri.user_id == user_id).first()

    if cv is None:
        cv = CVBilgileri(user_id=user_id, ham_metin=ham_metin, yuklendi_mi=True)
        db.add(cv)
    else:
        if ham_metin is not None:
            cv.ham_metin = ham_metin
        cv.guncellenme_tarihi = datetime.utcnow()

    for alan, deger in ek_alanlar.items():
        if hasattr(cv, alan):
            setattr(cv, alan, deger)

    db.commit()
    db.refresh(cv)
    return cv


def get_cv_by_user(db: Session, user_id: int):
    return db.query(CVBilgileri).filter(CVBilgileri.user_id == user_id).first()


def update_cv_analysis(
    db: Session,
    user_id: int,
    uyum_orani: Optional[int] = None,
    eslesen_beceriler: Optional[list] = None,
    eksik_beceriler: Optional[list] = None,
    ai_cv_ozeti: Optional[str] = None,
    cv_uyum_ai_ile_mi: bool = False,
):
    """ai_processing.py -> evaluate_cv_match() sonucunu kaydeder."""
    cv = db.query(CVBilgileri).filter(CVBilgileri.user_id == user_id).first()
    if not cv:
        return None

    cv.uyum_orani = uyum_orani
    cv.eslesen_beceriler = eslesen_beceriler
    cv.eksik_beceriler = eksik_beceriler
    cv.ai_cv_ozeti = ai_cv_ozeti
    cv.cv_uyum_ai_ile_mi = cv_uyum_ai_ile_mi
    cv.guncellenme_tarihi = datetime.utcnow()

    db.commit()
    db.refresh(cv)
    return cv


def delete_cv(db: Session, user_id: int):
    """upload_cv.py -> '🗑️ CV'yi Sil ve Yeni CV Yükle' butonu için."""
    cv = db.query(CVBilgileri).filter(CVBilgileri.user_id == user_id).first()
    if cv:
        db.delete(cv)
        db.commit()
    return True


# =====================================================
# 3. MÜLAKAT OTURUMU İŞLEMLERİ
# =====================================================

def create_interview_session(
    db: Session,
    user_id: int,
    oturum_kodu: str,
    pozisyon: Optional[str] = None,
    deneyim_seviyesi: Optional[str] = None,
    toplam_soru_sayisi: int = 0,
):
    """utils.session.reset_interview_state() ile eşleşen yeni oturum kaydı."""
    oturum = MulakatOturumu(
        user_id=user_id,
        oturum_kodu=oturum_kodu,
        pozisyon=pozisyon,
        deneyim_seviyesi=deneyim_seviyesi,
        toplam_soru_sayisi=toplam_soru_sayisi,
    )
    db.add(oturum)
    db.commit()
    db.refresh(oturum)
    return oturum


def get_session_by_kod(db: Session, oturum_kodu: str):
    return (
        db.query(MulakatOturumu)
        .filter(MulakatOturumu.oturum_kodu == oturum_kodu)
        .first()
    )


def get_user_sessions(db: Session, user_id: int):
    """interview_history.py listesi için, en yeni oturum en üstte."""
    return (
        db.query(MulakatOturumu)
        .filter(MulakatOturumu.user_id == user_id)
        .order_by(MulakatOturumu.baslangic_tarihi.desc())
        .all()
    )


def complete_interview_session(
    db: Session,
    oturum_kodu: str,
    erken_sonlandirildi_mi: bool = False,
    sonlandirma_nedeni: Optional[str] = None,
):
    """
    Mülakat tamamlandığında ya da erken sonlandırıldığında
    (SessionManager.complete_current_interview / _terminate_abandoned_interview)
    çağrılır.
    """
    oturum = (
        db.query(MulakatOturumu)
        .filter(MulakatOturumu.oturum_kodu == oturum_kodu)
        .first()
    )
    if not oturum:
        return None

    oturum.tamamlandi_mi = True
    oturum.erken_sonlandirildi_mi = erken_sonlandirildi_mi
    oturum.sonlandirma_nedeni = sonlandirma_nedeni
    oturum.tamamlanma_tarihi = datetime.utcnow()

    db.commit()
    db.refresh(oturum)
    return oturum


# =====================================================
# 4. MÜLAKAT SORULARI İŞLEMLERİ
# =====================================================

def save_question(
    db: Session,
    user_id: int,
    oturum_id: int,
    soru_metni: str,
    kategori: Optional[str] = None,
    soru_sirasi: Optional[int] = None,
):
    new_question = MulakatSorulari(
        user_id=user_id,
        oturum_id=oturum_id,
        soru_metni=soru_metni,
        kategori=kategori,
        soru_sirasi=soru_sirasi,
    )
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question


def save_answer_and_score(
    db: Session,
    question_id: int,
    cevap: str,
    puan: Optional[int] = None,
    geri_bildirim: Optional[str] = None,
    icerik_puani: Optional[int] = None,
    aciklik_puani: Optional[int] = None,
    iliskililik_puani: Optional[int] = None,
):
    question = (
        db.query(MulakatSorulari).filter(MulakatSorulari.id == question_id).first()
    )
    if question:
        question.kullanici_cevabi = cevap
        question.puan = puan
        question.geri_bildirim = geri_bildirim
        question.icerik_puani = icerik_puani
        question.aciklik_puani = aciklik_puani
        question.iliskililik_puani = iliskililik_puani
        question.cevaplanma_tarihi = datetime.utcnow()
        db.commit()
        db.refresh(question)
    return question


def get_user_questions(db: Session, user_id: int):
    return db.query(MulakatSorulari).filter(MulakatSorulari.user_id == user_id).all()


def get_session_questions(db: Session, oturum_id: int):
    return (
        db.query(MulakatSorulari)
        .filter(MulakatSorulari.oturum_id == oturum_id)
        .order_by(MulakatSorulari.soru_sirasi)
        .all()
    )


# =====================================================
# 5. SONUÇ İŞLEMLERİ
# =====================================================

def save_result(
    db: Session,
    user_id: int,
    oturum_id: int,
    ise_alim_orani: Optional[float] = None,
    onerilen_kaynaklar: Optional[str] = None,
    hazirlik_skoru: Optional[int] = None,
    cv_uyum_skoru: Optional[int] = None,
    iletisim_skoru: Optional[int] = None,
    kategori_skorlari: Optional[list] = None,
    guclu_yonler: Optional[list] = None,
    gelisim_alanlari: Optional[list] = None,
    onerilen_kaynaklar_detay: Optional[dict] = None,
    dil_tutarliligi: Optional[str] = None,
    ai_geri_bildirimi: Optional[str] = None,
    ai_ile_degerlendirildi_mi: bool = False,
):
    """
    Bir mülakat oturumu için nihai sonuç kaydını oluşturur (oturum başına
    tek kayıt). build_result_summary() çıktısının tamamını karşılar.
    """
    result = (
        db.query(Sonuclar).filter(Sonuclar.oturum_id == oturum_id).first()
    )

    if result is None:
        result = Sonuclar(user_id=user_id, oturum_id=oturum_id)
        db.add(result)

    result.ise_alim_orani = ise_alim_orani
    result.onerilen_kaynaklar = onerilen_kaynaklar
    result.hazirlik_skoru = hazirlik_skoru
    result.cv_uyum_skoru = cv_uyum_skoru
    result.iletisim_skoru = iletisim_skoru
    result.kategori_skorlari = kategori_skorlari
    result.guclu_yonler = guclu_yonler
    result.gelisim_alanlari = gelisim_alanlari
    result.onerilen_kaynaklar_detay = onerilen_kaynaklar_detay
    result.dil_tutarliligi = dil_tutarliligi
    result.ai_geri_bildirimi = ai_geri_bildirimi
    result.ai_ile_degerlendirildi_mi = ai_ile_degerlendirildi_mi
    result.tamamlanma_tarihi = datetime.utcnow()

    db.commit()
    db.refresh(result)
    return result


def get_result_by_session(db: Session, oturum_id: int):
    return db.query(Sonuclar).filter(Sonuclar.oturum_id == oturum_id).first()


def get_user_results(db: Session, user_id: int):
    return (
        db.query(Sonuclar)
        .filter(Sonuclar.user_id == user_id)
        .order_by(Sonuclar.tamamlanma_tarihi.desc())
        .all()
    )


# =====================================================
# 6. KULLANICI AYARLARI İŞLEMLERİ
# =====================================================

def get_or_create_settings(db: Session, user_id: int):
    """settings.py sayfasının varsayılan değerleriyle eşleşir."""
    ayar = (
        db.query(KullaniciAyarlari)
        .filter(KullaniciAyarlari.user_id == user_id)
        .first()
    )
    if ayar is None:
        ayar = KullaniciAyarlari(user_id=user_id)
        db.add(ayar)
        db.commit()
        db.refresh(ayar)
    return ayar


def update_settings(
    db: Session,
    user_id: int,
    email_bildirimleri: Optional[bool] = None,
    hatirlatma_bildirimleri: Optional[bool] = None,
    varsayilan_deneyim_seviyesi: Optional[str] = None,
    uygulama_dili: Optional[str] = None,
):
    ayar = get_or_create_settings(db, user_id)

    if email_bildirimleri is not None:
        ayar.email_bildirimleri = email_bildirimleri
    if hatirlatma_bildirimleri is not None:
        ayar.hatirlatma_bildirimleri = hatirlatma_bildirimleri
    if varsayilan_deneyim_seviyesi is not None:
        ayar.varsayilan_deneyim_seviyesi = varsayilan_deneyim_seviyesi
    if uygulama_dili is not None:
        ayar.uygulama_dili = uygulama_dili

    db.commit()
    db.refresh(ayar)
    return ayar
