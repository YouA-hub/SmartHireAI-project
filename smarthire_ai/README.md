# SmartHire AI — Streamlit Mülakat Simülasyon Platformu

> **TÜBİTAK 2209-A Üniversite Öğrencileri Araştırma Projeleri Destekleme Programı** kapsamında geliştirilmiştir.

SmartHire AI, adayların yapay zeka destekli mülakat simülasyonları ile kendilerini geliştirmelerini sağlayan web tabanlı bir platformdur. Bu proje, React arayüzündeki modern UI/UX tasarım sistemini (renk paleti, tipografi, grid yapısı, buton ve kart tasarımları) birebir koruyarak **Python Streamlit** mimarisine aktarılmıştır.

---

## 📁 Proje Dosya Yapısı

```text
smarthire_ai/
├── app.py                     # Ana Streamlit uygulaması ve sayfa yönlendirici (Router)
├── requirements.txt           # Bağımlılıklar (streamlit)
├── README.md                  # Proje dokümantasyonu
├── assets/
│   └── style.css              # React tokens.css tabanlı CSS Tasarım Sistemi
├── utils/
│   └── session.py             # Oturum yönetimi & State Manager (SOLID)
├── components/
│   ├── navbar.py              # Header & Navigasyon bileşeni
│   ├── cards.py               # Stat, Info ve Container Kart bileşenleri
│   ├── buttons.py             # Özelleştirilmiş buton stilleri
│   ├── timer.py               # Mülakat süresi geri sayım sayacı
│   └── footer.py              # Alt bilgi bileşeni
└── pages/                     # Modüler ekran bileşenleri
    ├── login.py               # Giriş Yap ekranı
    ├── register.py            # Kayıt Ol ekranı
    ├── upload_cv.py           # CV Yükleme & Pozisyon seçimi
    ├── ready.py               # Mülakat hazırlık ekranı
    ├── interview.py           # Mülakat simülasyon ekranı
    └── result.py              # Performans ve sonuç analiz raporu
```

---

## 🚀 Çalıştırma Talimatları

1. **Bağımlılıkları yükleyin:**
   ```bash
   pip install -r smarthire_ai/requirements.txt
   ```

2. **Streamlit uygulamasını başlatın:**
   ```bash
   streamlit run smarthire_ai/app.py
   ```

---

## 🛠️ Geleceğe Yönelik Backend Entegrasyon Planı
Tasarım tamamen modüler olarak kurgulanmıştır. İlerleyen aşamalarda aşağıdaki sistemler kolaylıkla bağlanabilir:
- **Gemini API**: Mülakat sorularını dinamik oluşturma ve yanıt analizi.
- **PostgreSQL / SQLAlchemy**: Kullanıcı verileri ve mülakat geçmişi saklama.
- **pdfplumber**: CV dosyalarını otomatik ayrıştırma.
