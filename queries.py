# database/queries.py
from sqlalchemy.orm import Session
from database.models import User, CVBilgileri, MulakatSorulari, Sonuclar

# --- 1. KULLANICI İŞLEMLERİ ---
def create_user(db: Session, ad_soyad: str, email: str, sifre_hash: str):
    new_user = User(ad_soyad=ad_soyad, email=email, sifre_hash=sifre_hash)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def update_user_alan(db: Session, user_id: int, alan: str):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.mezuniyet_alani = alan
        db.commit()
        db.refresh(user)
    return user

# --- 2. CV İŞLEMLERİ ---
def save_cv(db: Session, user_id: int, ham_metin: str):
    new_cv = CVBilgileri(user_id=user_id, ham_metin=ham_metin)
    db.add(new_cv)
    db.commit()
    db.refresh(new_cv)
    return new_cv

def get_cv_by_user(db: Session, user_id: int):
    return db.query(CVBilgileri).filter(CVBilgileri.user_id == user_id).first()

# --- 3. MÜLAKAT SORULARI İŞLEMLERİ ---
def save_question(db: Session, user_id: int, soru_metni: str):
    new_question = MulakatSorulari(user_id=user_id, soru_metni=soru_metni)
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question

def save_answer_and_score(db: Session, question_id: int, cevap: str, puan: int, geri_bildirim: str):
    question = db.query(MulakatSorulari).filter(MulakatSorulari.id == question_id).first()
    if question:
        question.kullanici_cevabi = cevap
        question.puan = puan
        question.geri_bildirim = geri_bildirim
        db.commit()
        db.refresh(question)
    return question

def get_user_questions(db: Session, user_id: int):
    return db.query(MulakatSorulari).filter(MulakatSorulari.user_id == user_id).all()

# --- 4. SONUÇ İŞLEMLERİ ---
def save_result(db: Session, user_id: int, ise_alim_orani: float, onerilen_kaynaklar: str):
    new_result = Sonuclar(user_id=user_id, ise_alim_orani=ise_alim_orani, onerilen_kaynaklar=onerilen_kaynaklar)
    db.add(new_result)
    db.commit()
    db.refresh(new_result)
    return new_result