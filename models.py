print("1. TEST: Python dosyayı okumaya başladı...")
# database/models.py
from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database.connection import Base, engine

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    ad_soyad = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    sifre_hash = Column(String, nullable=False)
    mezuniyet_alani = Column(String, nullable=True)
    olusturulma_tarihi = Column(DateTime, default=datetime.utcnow)

    # Diğer tablolarla bağlantılar (İlişkiler)
    cv = relationship("CVBilgileri", back_populates="user", uselist=False)
    sorular = relationship("MulakatSorulari", back_populates="user")
    sonuclar = relationship("Sonuclar", back_populates="user")

class CVBilgileri(Base):
    __tablename__ = "cv_bilgileri"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    ham_metin = Column(Text, nullable=False)
    yuklenme_tarihi = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="cv")

class MulakatSorulari(Base):
    __tablename__ = "mulakat_sorulari"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    soru_metni = Column(Text, nullable=False)
    kullanici_cevabi = Column(Text, nullable=True)
    puan = Column(Integer, nullable=True)
    geri_bildirim = Column(Text, nullable=True)
    olusturulma_tarihi = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="sorular")

class Sonuclar(Base):
    __tablename__ = "sonuclar"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    ise_alim_orani = Column(Numeric, nullable=True)
    onerilen_kaynaklar = Column(Text, nullable=True)
    tamamlanma_tarihi = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="sonuclar")

# Tabloları Supabase üzerinde canlı olarak oluşturacak komut
def create_tables():
    print("2. TEST: Tablo oluşturma fonksiyonu tetiklendi...")
    Base.metadata.create_all(bind=engine)
    print("Harika! Tablolar Supabase veritabanında başarıyla oluşturuldu!")

if __name__ == "__main__":
    print("3. TEST: Ana çalıştırma bloğuna (main) girildi...")
    create_tables()