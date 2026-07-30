from __future__ import annotations

import re
import unicodedata
from pathlib import Path
from typing import Optional, Dict, List


class CVOkumaHatasi(Exception):
    pass


class DosyaBulunamadiHatasi(CVOkumaHatasi):
    pass


class GecersizDosyaTuruHatasi(CVOkumaHatasi):
    pass


class BozukPDFHatasi(CVOkumaHatasi):
    pass


class DosyaCokBuyukHatasi(CVOkumaHatasi):
    pass


class BosPDFHatasi(CVOkumaHatasi):
    pass


# ---------------------------------------------------------------------------
# İletişim bilgisi desenleri
# ---------------------------------------------------------------------------

EMAIL_PATTERN = re.compile(
    r"[\w\.\-+]+@[\w\-]+\.[\w\.\-]+"
)

PHONE_PATTERN = re.compile(
    r"(\+90[\s\-]?)?(0[\s\-]?)?5\d{2}[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}"
)

LINKEDIN_PATTERN = re.compile(
    r"(https?://)?(www\.)?linkedin\.com/in/[\w\-]+/?",
    re.IGNORECASE
)

GITHUB_PATTERN = re.compile(
    r"(https?://)?(www\.)?github\.com/[\w\-]+/?",
    re.IGNORECASE
)

KAGGLE_PATTERN = re.compile(
    r"(https?://)?(www\.)?kaggle\.com/[\w\-]+/?",
    re.IGNORECASE
)

MEDIUM_PATTERN = re.compile(
    r"(https?://)?(www\.)?medium\.com/@?[\w\-\.]+/?",
    re.IGNORECASE
)

GITLAB_PATTERN = re.compile(
    r"(https?://)?(www\.)?gitlab\.com/[\w\-]+/?",
    re.IGNORECASE
)

STACKOVERFLOW_PATTERN = re.compile(
    r"(https?://)?(www\.)?stackoverflow\.com/users/[\w\-/]+",
    re.IGNORECASE
)

# Genel URL yakalayici; portfolyo / kisisel website tespiti ve
# sertifika linklerinin bulunmasi icin kullanilir.
GENEL_URL_PATTERN = re.compile(
    r"https?://[^\s,;]+",
    re.IGNORECASE
)

# Bilinen platform alan adlari; genel URL'nin "website" olarak
# sayilmamasi icin bu liste disinda kalmasi gerekir.
BILINEN_PLATFORM_ALANLARI = (
    "linkedin.com", "github.com", "kaggle.com",
    "medium.com", "gitlab.com", "stackoverflow.com",
)


# ---------------------------------------------------------------------------
# Dil yeterliligi desenleri (birden fazla yazim seklini destekler)
# ---------------------------------------------------------------------------

LANGUAGE_PATTERNS: List[re.Pattern] = [
    # Ingilizce (B2) / English - B2 / English: B2
    re.compile(
        r"(ingilizce|english|almanca|german|fransızca|fransizca|french|"
        r"ispanyolca|spanish|italyanca|italian|rusça|rusca|russian|"
        r"arapça|arapca|arabic)\s*[\(:\-]\s*(A1|A2|B1|B2|C1|C2)\)?",
        re.IGNORECASE
    ),
    # English (Upper Intermediate) / Ingilizce (Ileri)
    re.compile(
        r"(ingilizce|english|almanca|german|fransızca|fransizca|french)"
        r"\s*\(?\s*(native|fluent|advanced|upper[\s\-]intermediate|"
        r"intermediate|pre[\s\-]intermediate|elementary|beginner|"
        r"temel|orta|ileri|başlangıç|baslangic|anadil)\)?",
        re.IGNORECASE
    ),
    re.compile(r"\bCEFR\s*[:\-]?\s*(A1|A2|B1|B2|C1|C2)\b", re.IGNORECASE),
    re.compile(r"\bIELTS\b\s*[:\-]?\s*\d(\.\d)?", re.IGNORECASE),
    re.compile(r"\bTOEFL\b(\s*(IBT|PBT))?\s*[:\-]?\s*\d{0,3}", re.IGNORECASE),
    re.compile(r"\bYDS\b\s*[:\-]?\s*\d{0,3}", re.IGNORECASE),
    re.compile(r"\bYÖKDİL\b\s*[:\-]?\s*\d{0,3}", re.IGNORECASE),
]


# ---------------------------------------------------------------------------
# Bölüm başlığı eş anlamlıları (Türkçe + İngilizce, genişletilmiş)
# ---------------------------------------------------------------------------

SECTION_SYNONYMS: Dict[str, list] = {

    "education": [
        "education", "egitim", "ogrenim", "akademik egitim",
        "academic background", "academic history",
        "egitim bilgileri", "egitim bilgisi", "ogrenim bilgisi",
        "akademik gecmis",
    ],

    "experience": [
        "experience", "work experience", "deneyim", "is deneyimi",
        "staj", "internship", "professional experience", "employment",
        "career", "calisma deneyimi", "kariyer", "is tecrubesi",
    ],

    "skills": [
        "skills", "skill", "yetenekler", "beceriler",
        "teknik beceriler", "technical skills", "teknik yetkinlikler",
        "teknolojiler", "competencies", "technologies", "yetenek",
    ],

    "projects": [
        "projects", "project", "projeler", "akademik projeler",
        "personal projects", "kisisel projeler",
    ],

    "certificates": [
        "certificates", "certificate", "certifications",
        "sertifikalar", "sertifika", "certifications and courses",
        "kurslar", "courses", "sertifikalar ve kurslar",
    ],

    "languages": [
        "languages", "language", "diller", "yabanci dil",
        "yabanci diller", "yabanci dil bilgisi", "dil bilgisi",
    ],

    "summary": [
        "summary", "about", "profile", "ozet", "hakkimda",
        "career objective", "objective", "kariyer hedefi",
    ],
}


# ---------------------------------------------------------------------------
# Başlıksız "skills" tespiti icin teknoloji anahtar kelimeleri
# ---------------------------------------------------------------------------

TEKNOLOJI_ANAHTAR_KELIMELERI = {
    "python", "java", "javascript", "typescript", "c", "c++", "c#",
    "sql", "nosql", "html", "css", "react", "angular", "vue",
    "node.js", "node", "django", "flask", "spring", "spring boot",
    "php", "ruby", "swift", "kotlin", "go", "golang", "rust", "r",
    "matlab", "power bi", "tableau", "excel", "tensorflow", "pytorch",
    "keras", "scikit-learn", "sklearn", "pandas", "numpy", "docker",
    "kubernetes", "git", "github", "gitlab", "aws", "azure", "gcp",
    "linux", "bash", "jenkins", "ci/cd", "cicd", "mongodb", "mysql",
    "postgresql", "postgres", "oracle", "firebase", "redis", "figma",
    "photoshop", "illustrator", "word", "powerpoint", "jira", "scrum",
    "agile", "rest api", "graphql", "kafka", "spark", "hadoop",
    "airflow", "unity", "unreal engine", "opencv", "selenium",
    "next.js", "nextjs", "express", "laravel", ".net", "asp.net",
    "power query", "vba", "sas", "spss", "unity3d", "swiftui",
}


# ---------------------------------------------------------------------------
# Başlıksız "education" tespiti icin ipucu kelimeleri
# ---------------------------------------------------------------------------

EGITIM_IPUCU_KELIMELERI = {
    "university", "üniversite", "universite", "üniversitesi",
    "universitesi", "institute", "enstitü", "enstitu", "faculty",
    "fakülte", "fakulte", "bachelor", "lisans", "master",
    "yüksek lisans", "yuksek lisans", "doktora", "phd", "b.sc",
    "m.sc", "bsc", "msc", "college", "onlisans", "on lisans",
}


# ---------------------------------------------------------------------------
# Başlıksız "certificates" tespiti icin platform isimleri
# ---------------------------------------------------------------------------

SERTIFIKA_PLATFORMLARI = {
    "linkedin learning", "coursera", "udemy", "btk akademi",
    "google certificate", "google certificates", "microsoft learn",
    "cisco", "edx", "udacity", "datacamp", "kodluyoruz", "turkcell",
    "aws certified", "pluralsight",
}


MAKS_BASLIK_UZUNLUGU = 40
ISIM_ARAMA_SATIR_SAYISI = 5

ISIM_ADAYI_KARA_LISTESI = {
    "curriculum vitae",
    "resume",
    "cv",
    "ozgecmis",
    "ozgecmis formu",
}

MAKS_DOSYA_BOYUTU_MB = 10

# İki kolonlu sayfalarda kolon ayrimi icin, sayfa genisliginin
# yuzde kaci kadar bir bosluk bulunursa gercek bir kolon sinirinin
# var sayilacagini belirler.
KOLON_BOSLUK_ESIGI_ORANI = 0.04

# Kolon ayriminin anlamli sayilmasi icin her kolonda en az
# bulunmasi gereken kelime sayisi (gurultuyu ayiklamak icin).
KOLON_MIN_KELIME_SAYISI = 3

# Ayni satira ait kelimelerin gruplanmasinda kullanilan dikey
# tolerans (pdfplumber "top" birimi cinsinden).
SATIR_GRUPLAMA_TOLERANSI = 3.0


# ---------------------------------------------------------------------------
# Dosya dogrulama
# ---------------------------------------------------------------------------

def validate_pdf(dosya_yolu: Path) -> None:

    import pdfplumber

    if not dosya_yolu.exists():
        raise DosyaBulunamadiHatasi(
            f"CV dosyasi bulunamadi: {dosya_yolu}"
        )

    if dosya_yolu.suffix.lower() != ".pdf":
        raise GecersizDosyaTuruHatasi(
            "Sadece PDF dosyalari desteklenmektedir."
        )

    boyut_mb = dosya_yolu.stat().st_size / (1024 * 1024)

    if boyut_mb > MAKS_DOSYA_BOYUTU_MB:
        raise DosyaCokBuyukHatasi(
            f"Dosya cok buyuk: {boyut_mb:.1f} MB"
        )

    try:
        with pdfplumber.open(dosya_yolu) as pdf:
            if len(pdf.pages) == 0:
                raise BozukPDFHatasi(
                    "PDF sayfa icermiyor."
                )
    except Exception as e:
        raise BozukPDFHatasi(
            f"PDF acilamadi: {e}"
        )


# ---------------------------------------------------------------------------
# Kolon-farkinda metin cikarimi
#
# pdfplumber'in varsayilan extract_text() metodu, iki kolonlu
# sayfalarda satirlari soldan saga okuyup birlestirdigi icin farkli
# kolonlardaki icerikleri ayni satirda birlestirebilir. Bunu onlemek
# icin once kelimelerin (word) x0 konumlarina bakarak sayfada belirgin
# bir dikey bosluk (kolon sinirinin) olup olmadigi tespit edilir; boyle
# bir sinir bulunursa kelimeler kolonlara ayrilir ve her kolon kendi
# icinde yukaridan asagiya okunup sirayla birlestirilir.
# ---------------------------------------------------------------------------

KOLON_BIN_GENISLIGI = 2.0  # pdfplumber birimi (nokta) cinsinden histogram hucre genisligi


def _kolon_sinirini_bul(kelimeler: list, sayfa_genisligi: float) -> Optional[float]:
    """
    Sayfada iki kolonlu bir duzen olup olmadigini tespit eder.

    Yontem: sayfadaki TUM kelimelerin x-araliklarini (x0-x1) bir
    "kapsama" histogramina isler. Gercek bir kolon ayraci (gutter),
    sayfanin tum dikey uzunlugu boyunca hicbir kelimenin dokunmadigi
    surekli bos bir seritir; rastgele bir satirdaki tesadufi bosluktan
    farkli olarak, bu serit sayfanin butun satirlarinda tutarlidir.
    Bu yuzden tek bir satirdaki genis araliklar (ör. sag hizali tarih)
    yanlislikla kolon sinirinin sanilmaz - sadece TUM kelimeler
    birlikte degerlendirildiginde hala bos kalan bir serit aranir.
    """
    if not kelimeler or sayfa_genisligi <= 0:
        return None

    bin_genisligi = KOLON_BIN_GENISLIGI
    bin_sayisi = max(1, int(sayfa_genisligi // bin_genisligi) + 1)
    kapsama = [0] * bin_sayisi

    for k in kelimeler:
        baslangic_bin = max(0, int(k["x0"] // bin_genisligi))
        bitis_bin = min(bin_sayisi - 1, int(k["x1"] // bin_genisligi))
        for b in range(baslangic_bin, bitis_bin + 1):
            kapsama[b] += 1

    # Kolon sinirinin sayfanin govdesinde olmasini bekliyoruz (kenarlarda
    # degil); bu yuzden aramayi orta banda sinirliyoruz.
    orta_bant_basi_bin = int((sayfa_genisligi * 0.2) // bin_genisligi)
    orta_bant_sonu_bin = min(bin_sayisi, int((sayfa_genisligi * 0.8) // bin_genisligi))

    en_uzun_bosluk = 0
    en_uzun_baslangic = None
    mevcut_baslangic = None

    for b in range(orta_bant_basi_bin, orta_bant_sonu_bin):
        if kapsama[b] == 0:
            if mevcut_baslangic is None:
                mevcut_baslangic = b
        else:
            if mevcut_baslangic is not None:
                uzunluk = b - mevcut_baslangic
                if uzunluk > en_uzun_bosluk:
                    en_uzun_bosluk = uzunluk
                    en_uzun_baslangic = mevcut_baslangic
                mevcut_baslangic = None

    if mevcut_baslangic is not None:
        uzunluk = orta_bant_sonu_bin - mevcut_baslangic
        if uzunluk > en_uzun_bosluk:
            en_uzun_bosluk = uzunluk
            en_uzun_baslangic = mevcut_baslangic

    bosluk_genisligi = en_uzun_bosluk * bin_genisligi

    if en_uzun_baslangic is not None and bosluk_genisligi > sayfa_genisligi * KOLON_BOSLUK_ESIGI_ORANI:
        return (en_uzun_baslangic * bin_genisligi) + (bosluk_genisligi / 2)

    return None


def _kelimeleri_satirlara_grupla(kelimeler: list, tolerans: float = SATIR_GRUPLAMA_TOLERANSI) -> str:
    if not kelimeler:
        return ""

    siralanmis = sorted(kelimeler, key=lambda k: (k["top"], k["x0"]))

    satirlar = []
    mevcut_satir = [siralanmis[0]]
    mevcut_top = siralanmis[0]["top"]

    for kelime in siralanmis[1:]:
        if abs(kelime["top"] - mevcut_top) > tolerans:
            satirlar.append(mevcut_satir)
            mevcut_satir = [kelime]
            mevcut_top = kelime["top"]
        else:
            mevcut_satir.append(kelime)

    satirlar.append(mevcut_satir)

    satir_metinleri = []
    for satir in satirlar:
        satir_siralanmis = sorted(satir, key=lambda k: k["x0"])
        satir_metinleri.append(
            " ".join(k["text"] for k in satir_siralanmis)
        )

    return "\n".join(satir_metinleri)


def _sayfadan_metin_cikar(sayfa) -> str:
    try:
        kelimeler = sayfa.extract_words(use_text_flow=False, keep_blank_chars=False)
    except Exception:
        kelimeler = None

    if not kelimeler:
        return sayfa.extract_text() or ""

    sinir = _kolon_sinirini_bul(kelimeler, sayfa.width)

    if sinir is not None:
        sol_kolon = [k for k in kelimeler if k["x0"] < sinir]
        sag_kolon = [k for k in kelimeler if k["x0"] >= sinir]

        if len(sol_kolon) >= KOLON_MIN_KELIME_SAYISI and len(sag_kolon) >= KOLON_MIN_KELIME_SAYISI:
            parcalar = [
                _kelimeleri_satirlara_grupla(sol_kolon),
                _kelimeleri_satirlara_grupla(sag_kolon),
            ]
            return "\n\n".join(p for p in parcalar if p)

    return _kelimeleri_satirlara_grupla(kelimeler)


def extract_text(dosya_yolu: Path) -> tuple[str, int]:

    import pdfplumber

    sayfa_metinleri = []

    try:
        with pdfplumber.open(dosya_yolu) as pdf:
            sayfa_sayisi = len(pdf.pages)
            for sayfa in pdf.pages:
                metin = _sayfadan_metin_cikar(sayfa)
                sayfa_metinleri.append(metin if metin else "")
    except Exception as e:
        raise BozukPDFHatasi(
            f"PDF okunurken hata: {e}"
        )

    ham_metin = "\n\n".join(sayfa_metinleri)

    if not ham_metin.strip():
        raise BosPDFHatasi(
            "PDF'ten metin okunamadi."
        )

    return ham_metin, sayfa_sayisi


def clean_text(ham_metin: str) -> str:

    if not ham_metin:
        return ""

    metin = ham_metin.replace("\t", " ")

    satirlar = []
    for satir in metin.split("\n"):
        satir = re.sub(r"[ ]{2,}", " ", satir).strip()
        satirlar.append(satir)

    metin = "\n".join(satirlar)
    metin = re.sub(r"\n{3,}", "\n\n", metin)

    return metin.strip()


# ---------------------------------------------------------------------------
# İletişim bilgisi çıkarımı
# ---------------------------------------------------------------------------

def extract_contact_info(temiz_metin: str) -> Dict[str, Optional[str]]:
    email = EMAIL_PATTERN.search(temiz_metin)
    phone = PHONE_PATTERN.search(temiz_metin)
    linkedin = LINKEDIN_PATTERN.search(temiz_metin)
    github = GITHUB_PATTERN.search(temiz_metin)
    kaggle = KAGGLE_PATTERN.search(temiz_metin)
    medium = MEDIUM_PATTERN.search(temiz_metin)
    gitlab = GITLAB_PATTERN.search(temiz_metin)
    stackoverflow = STACKOVERFLOW_PATTERN.search(temiz_metin)

    website = None
    for eslesme in GENEL_URL_PATTERN.finditer(temiz_metin):
        url = eslesme.group(0)
        lower = url.lower()
        if any(alan in lower for alan in BILINEN_PLATFORM_ALANLARI):
            continue
        website = url
        break

    return {
        "email": email.group(0) if email else None,
        "phone": phone.group(0).strip() if phone else None,
        "linkedin": linkedin.group(0) if linkedin else None,
        "github": github.group(0) if github else None,
        "kaggle": kaggle.group(0) if kaggle else None,
        "medium": medium.group(0) if medium else None,
        "gitlab": gitlab.group(0) if gitlab else None,
        "stackoverflow": stackoverflow.group(0) if stackoverflow else None,
        "website": website,
    }


def extract_name(temiz_metin: str) -> Optional[str]:
    satirlar = [
        s.strip()
        for s in temiz_metin.split("\n")
        if s.strip()
    ]
    for satir in satirlar[:ISIM_ARAMA_SATIR_SAYISI]:
        if EMAIL_PATTERN.search(satir):
            continue
        if PHONE_PATTERN.search(satir):
            continue
        if LINKEDIN_PATTERN.search(satir) or GITHUB_PATTERN.search(satir):
            continue
        if any(karakter.isdigit() for karakter in satir):
            continue
        if satir.lower() in ISIM_ADAYI_KARA_LISTESI:
            continue
        kelimeler = satir.split()
        if 2 <= len(kelimeler) <= 4:
            return satir
    return None


# ---------------------------------------------------------------------------
# Bölüm başlığı tespiti
# ---------------------------------------------------------------------------

def _normalize_baslik(metin: str) -> str:
    metin = re.sub(r"[^a-zA-ZçğıöşüÇĞİÖŞÜ\s]", "", metin)

    # Python'un varsayilan str.lower() metodu Turkce buyuk "İ" harfini
    # "i" + GORUNMEZ BIRLESIK NOKTA isaretine (U+0307) cevirir. Bu da
    # "EĞİTİM" / "DENEYİM" gibi TUMU BUYUK Turkce basliklarin normalize
    # sonrasi "egitim" / "deneyim" ile hic eslesmemesine, yani basliklarin
    # hic taninmamasina yol aciyordu. Bu yuzden Turkce "İ"/"I" harflerini
    # once elle sade "i" harfine cevirip oyle kucultuyoruz.
    metin = metin.replace("İ", "i").replace("I", "i")
    metin = metin.lower().strip()

    harita = str.maketrans("çğıöşü", "cgiosu")
    metin = metin.translate(harita)

    # Guvenlik amacli: olasi baska birlesik (combining) karakterleri de temizle.
    metin = "".join(
        karakter for karakter in unicodedata.normalize("NFKD", metin)
        if not unicodedata.combining(karakter)
    )

    return metin


def _baslik_mi(satir: str) -> Optional[str]:
    if len(satir) > MAKS_BASLIK_UZUNLUGU:
        return None

    normalize = _normalize_baslik(satir)
    if not normalize:
        return None

    # Birden fazla bolum eş anlamlısı satirla eşleşebilir (ör. "kariyer"
    # hem "experience" hem "kariyer hedefi" icinde gecer). Bu durumda en
    # uzun / en spesifik eşleşmeyi kazandiriyoruz, yoksa genel kelimeler
    # yanlis bolume yonlendirebilir.
    en_iyi_bolum = None
    en_iyi_uzunluk = -1

    for bolum_adi, alternatifler in SECTION_SYNONYMS.items():
        for alternatif in alternatifler:
            if alternatif in normalize and len(alternatif) > en_iyi_uzunluk:
                en_iyi_bolum = bolum_adi
                en_iyi_uzunluk = len(alternatif)

    return en_iyi_bolum


def split_sections(temiz_metin: str) -> Dict[str, Optional[str]]:
    sonuc = {bolum: None for bolum in SECTION_SYNONYMS}

    satirlar = temiz_metin.split("\n")
    basliklar = []

    for index, satir in enumerate(satirlar):
        bolum = _baslik_mi(satir)
        if bolum:
            basliklar.append((bolum, index))

    if not basliklar:
        return sonuc

    for i, (bolum_adi, baslangic) in enumerate(basliklar):
        bitis = basliklar[i + 1][1] if i + 1 < len(basliklar) else len(satirlar)
        satirlar_icerik = satirlar[baslangic + 1: bitis]

        icerik = "\n".join(
            s.strip() for s in satirlar_icerik if s.strip()
        )

        if icerik:
            if sonuc[bolum_adi]:
                sonuc[bolum_adi] += "\n" + icerik
            else:
                sonuc[bolum_adi] = icerik

    return sonuc


# ---------------------------------------------------------------------------
# Başlıksız bölümler icin sezgisel (heuristic) tamamlama fonksiyonlari
# ---------------------------------------------------------------------------

def _satiri_tokenlara_ayir(satir: str) -> List[str]:
    ayirici = re.compile(r"[,/|•;]+")
    tokenlar = []
    for parca in ayirici.split(satir):
        parca = parca.strip(" .-")
        if parca:
            tokenlar.append(parca)
    return tokenlar


def _satir_teknoloji_agirlikli_mi(satir: str) -> bool:
    if not satir or len(satir) > 120:
        return False

    tokenlar = _satiri_tokenlara_ayir(satir)
    if not tokenlar:
        return False

    eslesen = sum(
        1 for token in tokenlar
        if token.lower() in TEKNOLOJI_ANAHTAR_KELIMELERI
    )
    oran = eslesen / len(tokenlar)

    # Satir tek bir kelimeden olusuyorsa (ör. iki kolonlu bir CV'de
    # "Python" / "Docker" / "Git" gibi alt alta yazilmis tekli beceri
    # listeleri), yanlis pozitifi onlemek icin TAM eslesme ariyoruz.
    if len(tokenlar) == 1:
        return oran == 1.0

    return oran >= 0.5


def _metinden_teknoloji_satirlarini_topla(temiz_metin: str) -> Optional[str]:
    bulunanlar = []
    for satir in temiz_metin.split("\n"):
        satir = satir.strip()
        if not satir or _baslik_mi(satir):
            continue
        if _satir_teknoloji_agirlikli_mi(satir):
            bulunanlar.append(satir)

    if not bulunanlar:
        return None

    return "\n".join(dict.fromkeys(bulunanlar))


def _metinden_egitim_ipucu_satirlarini_topla(temiz_metin: str) -> Optional[str]:
    bulunanlar = []
    for satir in temiz_metin.split("\n"):
        satir_str = satir.strip()
        if not satir_str or _baslik_mi(satir_str):
            continue
        lower = satir_str.lower()
        if any(ipucu in lower for ipucu in EGITIM_IPUCU_KELIMELERI):
            bulunanlar.append(satir_str)

    if not bulunanlar:
        return None

    return "\n".join(dict.fromkeys(bulunanlar))


def _sertifika_ipucu_satirlarini_topla(temiz_metin: str) -> Optional[str]:
    bulunanlar = []
    for satir in temiz_metin.split("\n"):
        satir_str = satir.strip()
        if not satir_str:
            continue
        lower = satir_str.lower()

        if any(platform in lower for platform in SERTIFIKA_PLATFORMLARI):
            bulunanlar.append(satir_str)
            continue

        if ("sertifika" in lower or "certificate" in lower or "certification" in lower) \
                and GENEL_URL_PATTERN.search(satir_str):
            bulunanlar.append(satir_str)

    if not bulunanlar:
        return None

    return "\n".join(dict.fromkeys(bulunanlar))


def _sertifika_yapisina_donustur(ham_metin: Optional[str]) -> Optional[Dict[str, Optional[str]]]:
    """
    Duz metin halindeki sertifika bilgisini {"text": ..., "url": ...}
    yapisina cevirir. Boylece sertifika linki, aciklama metninden ayri
    olarak dogrudan kullanilabilir hale gelir.
    """
    if not ham_metin:
        return None

    url_eslesme = GENEL_URL_PATTERN.search(ham_metin)

    return {
        "text": ham_metin,
        "url": url_eslesme.group(0) if url_eslesme else None,
    }


def _dil_bilgisini_tespit_et(temiz_metin: str) -> Optional[str]:
    bulunanlar = []
    for desen in LANGUAGE_PATTERNS:
        for eslesme in desen.finditer(temiz_metin):
            metin = eslesme.group(0).strip()
            if metin not in bulunanlar:
                bulunanlar.append(metin)

    if not bulunanlar:
        return None

    return ", ".join(bulunanlar)


# ---------------------------------------------------------------------------
# İngilizce yeterliliğini CEFR seviyesine (A1-C2) indirgeme
# ---------------------------------------------------------------------------

CEFR_SIRALAMASI = ["A1", "A2", "B1", "B2", "C1", "C2"]

# Sözel seviye tanımlarının CEFR karşılığı (yaklaşık, resmi bir denklik
# tablosu değildir — CV'lerde en sık görülen ifadelere dayanır).
SOZEL_SEVIYE_ESLESMESI = {
    "native": "C2", "anadil": "C2",
    "fluent": "C1", "advanced": "C1", "ileri": "C1",
    "upper-intermediate": "B2", "upper intermediate": "B2",
    "intermediate": "B1", "orta": "B1",
    "pre-intermediate": "A2", "pre intermediate": "A2",
    "elementary": "A2", "temel": "A2",
    "beginner": "A1", "başlangıç": "A1", "baslangic": "A1",
}

# Sınav puanlarının YAKLAŞIK CEFR karşılığı. Resmi denklik tabloları
# kaynak bazlı küçük farklar gösterebilir; burada muhafazakar
# (olduğundan düşük seviye verecek şekilde) eşikler kullanılmıştır.
IELTS_ESIKLERI = [(7.0, "C1"), (5.5, "B2"), (4.0, "B1"), (0.0, "A2")]
TOEFL_IBT_ESIKLERI = [(95, "C1"), (72, "B2"), (42, "B1"), (0, "A2")]
YDS_YOKDIL_ESIKLERI = [(85, "C1"), (65, "B2"), (45, "B1"), (0, "A2")]


def _puani_cefre_cevir(puan: float, esikler: list) -> Optional[str]:
    for taban, seviye in esikler:
        if puan >= taban:
            return seviye
    return None


def _ingilizce_cumlesi_mi(cumle: str) -> bool:
    return bool(re.search(r"ingilizce|english", cumle, re.IGNORECASE))


def detect_english_level(temiz_metin: str) -> Optional[str]:
    """
    CV metninden İngilizce yeterlilik seviyesini CEFR formatında (A1-C2)
    tespit etmeye çalışır. Şu kaynaklardan (öncelik sırasıyla) faydalanır:

      1. Doğrudan CEFR ifadesi: "English (B2)", "İngilizce: B2"
      2. Sözel seviye ifadesi: "English (Upper-Intermediate)", "İngilizce (İleri)"
      3. Standart sınav puanı: IELTS, TOEFL iBT, YDS/YÖKDİL

    Hiçbir eşleşme bulunamazsa None döner — bu durumda mülakatta
    İngilizce soru SORULMAZ (temkinli/varsayılan davranış: kanıt yoksa
    yeterlilik varsayılmaz).

    Not: Bu tespit, gerçek bir CEFR sınavının yerini tutmaz; CV'de yazılı
    beyana dayalı yaklaşık bir sezgiseldir (heuristic).
    """
    if not temiz_metin:
        return None

    en_yuksek: Optional[str] = None

    def _guncelle(aday: Optional[str]):
        nonlocal en_yuksek
        if aday and aday in CEFR_SIRALAMASI:
            if en_yuksek is None or CEFR_SIRALAMASI.index(aday) > CEFR_SIRALAMASI.index(en_yuksek):
                en_yuksek = aday

    # 1) Doğrudan CEFR ifadesi (yalnızca İngilizce'ye ait olanlar)
    for eslesme in LANGUAGE_PATTERNS[0].finditer(temiz_metin):
        cumle = eslesme.group(0)
        if _ingilizce_cumlesi_mi(cumle):
            cefr_arama = re.search(r"A1|A2|B1|B2|C1|C2", cumle, re.IGNORECASE)
            if cefr_arama:
                _guncelle(cefr_arama.group(0).upper())

    for eslesme in re.finditer(r"\bCEFR\s*[:\-]?\s*(A1|A2|B1|B2|C1|C2)\b", temiz_metin, re.IGNORECASE):
        _guncelle(eslesme.group(1).upper())

    # 2) Sözel seviye ifadesi (yalnızca İngilizce'ye ait olanlar)
    for eslesme in LANGUAGE_PATTERNS[1].finditer(temiz_metin):
        cumle = eslesme.group(0)
        if _ingilizce_cumlesi_mi(cumle):
            for ifade, seviye in SOZEL_SEVIYE_ESLESMESI.items():
                if ifade in cumle.lower():
                    _guncelle(seviye)
                    break

    # 3) Standart sınav puanları
    ielts_eslesme = re.search(r"\bIELTS\b\s*[:\-]?\s*(\d(?:\.\d)?)", temiz_metin, re.IGNORECASE)
    if ielts_eslesme:
        _guncelle(_puani_cefre_cevir(float(ielts_eslesme.group(1)), IELTS_ESIKLERI))

    toefl_eslesme = re.search(r"\bTOEFL\b(?:\s*(?:IBT|PBT))?\s*[:\-]?\s*(\d{2,3})", temiz_metin, re.IGNORECASE)
    if toefl_eslesme:
        _guncelle(_puani_cefre_cevir(float(toefl_eslesme.group(1)), TOEFL_IBT_ESIKLERI))

    for desen in (r"\bYDS\b\s*[:\-]?\s*(\d{2,3})", r"\bYÖKDİL\b\s*[:\-]?\s*(\d{2,3})"):
        eslesme = re.search(desen, temiz_metin, re.IGNORECASE)
        if eslesme:
            _guncelle(_puani_cefre_cevir(float(eslesme.group(1)), YDS_YOKDIL_ESIKLERI))

    return en_yuksek


def normalize_sections(
    sections: Dict[str, Optional[str]],
    temiz_metin: str
) -> Dict[str, object]:

    # Dil bilgisi otomatik yakalama (birden fazla format destekli)
    if not sections["languages"]:
        dil = _dil_bilgisini_tespit_et(temiz_metin)
        if dil:
            sections["languages"] = dil

    # Sertifika platformu / link tespiti, yoksa genel bir isaret birak
    if not sections["certificates"]:
        sertifika_satirlari = _sertifika_ipucu_satirlarini_topla(temiz_metin)
        if sertifika_satirlari:
            sections["certificates"] = sertifika_satirlari
        else:
            lower_text = temiz_metin.lower()
            if any(k in lower_text for k in ("certificate", "certificates", "sertifika", "certification")):
                sections["certificates"] = "View My Certificates"

    # Baslik bulunamadiysa universite/lisans gibi ipuclarindan egitimi topla
    if not sections["education"]:
        egitim_satirlari = _metinden_egitim_ipucu_satirlarini_topla(temiz_metin)
        if egitim_satirlari:
            sections["education"] = egitim_satirlari

    # Baslik bulunamadiysa teknoloji agirlikli satirlardan skills olustur
    if not sections["skills"]:
        teknoloji_satirlari = _metinden_teknoloji_satirlarini_topla(temiz_metin)
        if teknoloji_satirlari:
            sections["skills"] = teknoloji_satirlari

    # Bilinen yazim hatalarini duzelt
    if sections["skills"]:
        sections["skills"] = sections["skills"].replace("Phyton", "Python")

    # Sertifika alanini, kaynagi ne olursa olsun (baslikli bolum, ipucu
    # tespiti ya da genel isaret) tutarli bir {"text","url"} yapisina cevir.
    sections["certificates"] = _sertifika_yapisina_donustur(sections["certificates"])


    return sections


# ---------------------------------------------------------------------------
# Ana giris noktasi
# ---------------------------------------------------------------------------

def read_cv(dosya_yolu) -> dict:
    yol = Path(dosya_yolu)

    validate_pdf(yol)

    raw_text, sayfa_sayisi = extract_text(yol)
    temiz_metin = clean_text(raw_text)

    iletisim = extract_contact_info(temiz_metin)
    isim = extract_name(temiz_metin)

    bolumler = split_sections(temiz_metin)
    bolumler = normalize_sections(bolumler, temiz_metin)

    ingilizce_seviyesi = detect_english_level(temiz_metin)

    return {
        "raw_text": raw_text,
        "clean_text": temiz_metin,
        "page_count": sayfa_sayisi,
        "name": isim,
        "email": iletisim["email"],
        "phone": iletisim["phone"],
        "github": iletisim["github"],
        "linkedin": iletisim["linkedin"],
        "kaggle": iletisim["kaggle"],
        "medium": iletisim["medium"],
        "gitlab": iletisim["gitlab"],
        "stackoverflow": iletisim["stackoverflow"],
        "website": iletisim["website"],
        "sections": bolumler,
        "english_level": ingilizce_seviyesi,
    }


if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 2:
        print("Kullanim: python cv_okuyucu.py <pdf_yolu>")
        sys.exit(1)

    try:
        sonuc = read_cv(sys.argv[1])
        ozet = {
            anahtar: deger
            for anahtar, deger in sonuc.items()
            if anahtar not in ("raw_text", "clean_text")
        }
        print(json.dumps(ozet, ensure_ascii=False, indent=2))
        print(f"\nclean_text uzunlugu: {len(sonuc['clean_text'])} karakter")
    except CVOkumaHatasi as hata:
        print(f"HATA: {hata}")