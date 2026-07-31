print("1. TEST: Python dosyayı okumaya başladı...")
# database/models.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Numeric,
    Boolean,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime

from database.connection import Base, engine


class User(Base):
    """Kayıtlı kullanıcı. Kayıt ekranında toplanan tüm alanları içerir."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    ad_soyad = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    sifre_hash = Column(String, nullable=False)

    # Kayıt ekranında seçilen/yazılan hedef pozisyon (register.py -> role/custom_role)
    hedef_pozisyon = Column(String, nullable=True)

    # Geriye dönük uyumluluk için korunan alan (önceki şemadan)
    mezuniyet_alani = Column(String, nullable=True)

    avatar_baslangic_harfleri = Column(String(4), nullable=True)

    kullanim_kosullari_onayi = Column(Boolean, default=False, nullable=False)

    olusturulma_tarihi = Column(DateTime, default=datetime.utcnow)
    guncellenme_tarihi = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # İlişkiler
    cv = relationship(
        "CVBilgileri",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    mulakat_oturumlari = relationship(
        "MulakatOturumu",
        back_populates="user",
        cascade="all, delete-orphan",
        order_by="MulakatOturumu.baslangic_tarihi",
    )
    sorular = relationship(
        "MulakatSorulari",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    sonuclar = relationship(
        "Sonuclar",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    ayarlar = relationship(
        "KullaniciAyarlari",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )


class CVBilgileri(Base):
    """
    Kullanıcının yüklediği CV'den çıkarılan ve upload_cv / ai_processing /
    cv_confirm ekranlarında üretilen tüm veriler.
    Kullanıcı başına tek (aktif) CV tutulur; yeniden yükleme/silme bu
    kaydı günceller.
    """

    __tablename__ = "cv_bilgileri"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )

    # Dosya / ham içerik
    dosya_adi = Column(String, nullable=True)  # cv_data.file_name
    yuklendi_mi = Column(Boolean, default=False, nullable=False)  # cv_data.uploaded
    ham_metin = Column(Text, nullable=True)  # cv_okuyucu.read_cv -> raw_text
    temiz_metin = Column(Text, nullable=True)  # cv_data.clean_text
    sayfa_sayisi = Column(Integer, nullable=True)  # cv_okuyucu -> page_count

    # CV'den ayrıştırılan iletişim / kimlik bilgileri (cv_okuyucu.extract_contact_info)
    tespit_edilen_isim = Column(String, nullable=True)
    tespit_edilen_email = Column(String, nullable=True)
    telefon = Column(String, nullable=True)
    linkedin = Column(String, nullable=True)
    github = Column(String, nullable=True)
    kaggle = Column(String, nullable=True)
    medium = Column(String, nullable=True)
    gitlab = Column(String, nullable=True)
    stackoverflow = Column(String, nullable=True)
    website = Column(String, nullable=True)

    # Pozisyon / ilan bilgisi (upload_cv.py)
    pozisyon = Column(String, nullable=True)  # cv_data.position
    deneyim_seviyesi = Column(String, nullable=True)  # cv_data.experience_level
    ilan_metni = Column(Text, nullable=True)  # cv_data.job_description

    # CV'den çıkarılan beceriler ve dil seviyesi
    beceriler = Column(JSONB, nullable=True)  # cv_data.skills (list[str])
    ingilizce_seviyesi = Column(String(2), nullable=True)  # cv_data.english_level (A1-C2)

    # ai_processing.py -> evaluate_cv_match() sonucu
    uyum_orani = Column(Integer, nullable=True)  # cv_data.match_rate
    eslesen_beceriler = Column(JSONB, nullable=True)  # cv_data.matched_skills
    eksik_beceriler = Column(JSONB, nullable=True)  # cv_data.missing_skills
    ai_cv_ozeti = Column(Text, nullable=True)  # cv_data.ai_cv_summary
    cv_uyum_ai_ile_mi = Column(Boolean, default=False, nullable=False)  # cv_match_evaluated_by_ai

    yuklenme_tarihi = Column(DateTime, default=datetime.utcnow)
    guncellenme_tarihi = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    user = relationship("User", back_populates="cv")


class MulakatOturumu(Base):
    """
    Tek bir mülakat oturumunu (interview_state) temsil eder. Kullanıcı
    başına birden çok oturum olabilir (interview_history listesi).
    """

    __tablename__ = "mulakat_oturumlari"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    # utils.session.reset_interview_state() -> session_id (uuid4 ilk 8 hanesi)
    oturum_kodu = Column(String(32), unique=True, index=True, nullable=False)

    # Oturum başlarken kullanılan CV/pozisyon bilgisinin anlık görüntüsü
    pozisyon = Column(String, nullable=True)
    deneyim_seviyesi = Column(String, nullable=True)

    toplam_soru_sayisi = Column(Integer, default=0, nullable=False)

    tamamlandi_mi = Column(Boolean, default=False, nullable=False)  # is_completed
    ai_ile_degerlendirildi_mi = Column(Boolean, default=False, nullable=False)  # evaluated_by_ai

    # Erken sonlandırma bilgisi (sekme değişikliği / navigasyon)
    erken_sonlandirildi_mi = Column(Boolean, default=False, nullable=False)  # was_abandoned
    sonlandirma_nedeni = Column(String, nullable=True)  # abandon_reason: navigation | tab_switch

    baslangic_tarihi = Column(DateTime, default=datetime.utcnow)
    tamamlanma_tarihi = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="mulakat_oturumlari")
    sorular = relationship(
        "MulakatSorulari",
        back_populates="oturum",
        cascade="all, delete-orphan",
        order_by="MulakatSorulari.soru_sirasi",
    )
    sonuc = relationship(
        "Sonuclar",
        back_populates="oturum",
        uselist=False,
        cascade="all, delete-orphan",
    )


class MulakatSorulari(Base):
    """
    Bir mülakat oturumundaki tek bir soru + cevap + AI puanlaması.
    (services/ai_degerlendirici.py -> generate_interview_questions /
    evaluate_interview_answers)
    """

    __tablename__ = "mulakat_sorulari"

    id = Column(Integer, primary_key=True, index=True)

    # Denormalize edilmiş kullanıcı referansı: oturum silinse bile
    # kullanıcının tüm sorularını tek sorguda çekebilmek için tutulur.
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    oturum_id = Column(
        Integer,
        ForeignKey("mulakat_oturumlari.id", ondelete="CASCADE"),
        nullable=False,
    )

    soru_sirasi = Column(Integer, nullable=True)  # current_question_index
    kategori = Column(String, nullable=True)  # question["category"]
    soru_metni = Column(Text, nullable=False)
    kullanici_cevabi = Column(Text, nullable=True)

    # evaluate_interview_answers() -> question_scores
    icerik_puani = Column(Integer, nullable=True)  # content_score
    aciklik_puani = Column(Integer, nullable=True)  # clarity_score
    iliskililik_puani = Column(Integer, nullable=True)  # relevance_score
    puan = Column(Integer, nullable=True)  # final_score (eski alan adı korunuyor)

    geri_bildirim = Column(Text, nullable=True)

    olusturulma_tarihi = Column(DateTime, default=datetime.utcnow)
    cevaplanma_tarihi = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="sorular")
    oturum = relationship("MulakatOturumu", back_populates="sorular")


class Sonuclar(Base):
    """
    Bir mülakat oturumunun nihai değerlendirme özeti.
    (services/ai_degerlendirici.build_result_summary() ve
    screens/result.py çıktısının tamamı)
    """

    __tablename__ = "sonuclar"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    oturum_id = Column(
        Integer,
        ForeignKey("mulakat_oturumlari.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    # Ana skorlar (result.py üst kartları)
    hazirlik_skoru = Column(Integer, nullable=True)  # readiness_score / interview_score
    ise_alim_orani = Column(Numeric, nullable=True)  # hireability_rate (eski alan korunuyor)
    cv_uyum_skoru = Column(Integer, nullable=True)  # cv_match_score
    iletisim_skoru = Column(Integer, nullable=True)  # communication_score

    # Kategori bazlı performans (interview_state.category_scores)
    kategori_skorlari = Column(JSONB, nullable=True)  # [{"category": ..., "score": ...}]

    guclu_yonler = Column(JSONB, nullable=True)  # strengths (list[str])
    gelisim_alanlari = Column(JSONB, nullable=True)  # improvement_areas (list[str])
    onerilen_kaynaklar = Column(Text, nullable=True)  # eski alan adı korunuyor (özet metin)
    onerilen_kaynaklar_detay = Column(JSONB, nullable=True)  # suggest_learning_resources() çıktısı

    dil_tutarliligi = Column(String, nullable=True)  # language_consistency
    ai_geri_bildirimi = Column(Text, nullable=True)  # ai_feedback
    ai_ile_degerlendirildi_mi = Column(Boolean, default=False, nullable=False)

    tamamlanma_tarihi = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="sonuclar")
    oturum = relationship("MulakatOturumu", back_populates="sonuc")


class KullaniciAyarlari(Base):
    """Ayarlar ekranında (settings.py) yönetilen kullanıcı tercihleri."""

    __tablename__ = "kullanici_ayarlari"
    __table_args__ = (UniqueConstraint("user_id", name="uq_kullanici_ayarlari_user_id"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    email_bildirimleri = Column(Boolean, default=True, nullable=False)
    hatirlatma_bildirimleri = Column(Boolean, default=True, nullable=False)
    varsayilan_deneyim_seviyesi = Column(
        String, default="Mid Level (2-5 Yıl)", nullable=False
    )
    uygulama_dili = Column(String, default="Türkçe", nullable=False)

    guncellenme_tarihi = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    user = relationship("User", back_populates="ayarlar")


# Tabloları Supabase üzerinde canlı olarak oluşturacak komut
def create_tables():
    print("2. TEST: Tablo oluşturma fonksiyonu tetiklendi...")
    Base.metadata.create_all(bind=engine)
    print("Harika! Tablolar Supabase veritabanında başarıyla oluşturuldu!")


if __name__ == "__main__":
    print("3. TEST: Ana çalıştırma bloğuna (main) girildi...")
    create_tables()
