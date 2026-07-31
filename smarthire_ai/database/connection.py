import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

# .env dosyasındaki gizli bilgileri yükle
load_dotenv()

# NOT: Önceki sürümde bağlantı adresi (şifre içermeden) doğrudan kod
# içine sabitlenmişti; bu haliyle Supabase'e asla bağlanamıyordu ve
# üretilen hiçbir veri kalıcı olarak saklanamıyordu. Artık bağlantı
# bilgisi .env / ortam değişkenlerinden okunuyor; sabit adres yalnızca
# geliştirme ortamı için son çare (fallback) olarak korunuyor.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:@db.gehcgymeopafoovquafs.supabase.co:5432/postgres",
)

# Veritabanı motorunu oluştur.
# pool_pre_ping: Supabase gibi bir süre işlem yapılmayınca bağlantıyı
# kesen sağlayıcılarda "SSL connection has been closed unexpectedly"
# gibi hatalarla karşılaşmamak için her kullanımdan önce bağlantıyı test eder.
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
)

# Veritabanında işlem yapabilmek için oturum (session) oluşturucu
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tüm tablolarımızın miras alacağı ana şablon sınıfı
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
