"""
SmartHire AI - PDF Report Generator Utility
Herhangi bir dış kütüphaneye ihtiyaç duymadan saf Python ile geçerli PDF dosyası (bytes) üretir.
TÜBİTAK 2209-A projesi için özel olarak hazırlanmıştır.

NOT (düzeltme): Önceki sürümde bu fonksiyon; teknik kategori skorları, güçlü/zayıf
yönler ve AI geri bildirimi metnini SABİT (demo) veri olarak basıyordu — sonuç ekranında
(result.py) hesaplanan gerçek AI değerlendirmesiyle hiçbir bağlantısı yoktu. Artık bu
alanlar dışarıdan parametre olarak alınıyor ve result.py zaten session_state'te tuttuğu
gerçek `category_scores`, `strengths`, `improvement_areas`, `ai_feedback` değerlerini
buraya geçiriyor. Ayrıca xref byte-offset tablosu ve stream /Length değeri artık içerik
uzunluğuna göre DİNAMİK hesaplanıyor (önceki sabit sayılar, değişken uzunluktaki isim/puan
verileriyle birlikte geçersiz/bozuk bir xref tablosuna yol açabiliyordu).
"""


def _pdf_escape(text: str) -> str:
    """PDF literal string içinde özel anlamı olan (, ), \\ karakterlerini kaçışlar."""
    if text is None:
        return ""
    text = str(text)
    text = text.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")
    return text.encode("latin-1", errors="ignore").decode("latin-1")


def _wrap_text(text: str, max_chars: int = 95):
    """Uzun metinleri (ör. AI geri bildirimi) PDF'te satır satır basabilmek için böler."""
    if not text:
        return []
    words = text.split()
    lines, current = [], ""
    for w in words:
        candidate = f"{current} {w}".strip()
        if len(candidate) > max_chars:
            if current:
                lines.append(current)
            current = w
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def generate_pdf_report(
    user_name: str,
    position: str,
    date_str: str,
    overall_score: int,
    hireability: int,
    cv_match: int,
    category_scores=None,
    strengths=None,
    improvement_areas=None,
    ai_feedback: str = "",
) -> bytes:
    """
    Kullanıcı mülakat sonuç raporunu standart PDF formatında üretir ve bytes olarak döndürür.

    category_scores: [{"category": str, "score": int}, ...]  (result.py'deki ile aynı yapı)
    strengths / improvement_areas: [str, ...]
    ai_feedback: serbest metin AI geri bildirimi
    """
    category_scores = category_scores or []
    strengths = strengths or []
    improvement_areas = improvement_areas or []

    lines = []

    lines.append(("F1", 18, 0, "SmartHire AI - Mulakat Degerlendirme ve Gelisim Raporu"))
    lines.append(("F2", 11, -22, f"Aday Bilgisi: {user_name}  |  Hedef Pozisyon: {position}"))
    lines.append(("F2", 11, -15, f"Mulakat Tarihi: {date_str}  |  Platform: SmartHire AI v1.0"))

    lines.append(("F1", 13, -30, "1. GENEL METRIKLER VE UYUM OZETI"))
    lines.append(("F2", 10, -18, f"Tahmini Ise Alinma Olasiligi: %{hireability}"))
    lines.append(("F2", 10, -15, f"Genel Mulakat Skoru: %{overall_score}"))
    lines.append(("F2", 10, -15, f"CV - Is Ilani Uyum Puani: %{cv_match}"))

    lines.append(("F1", 13, -30, "2. KATEGORI BAZLI PERFORMANS"))
    if category_scores:
        first = True
        for item in category_scores:
            cat = item.get("category", "-")
            score = item.get("score", 0)
            lines.append(("F2", 10, -18 if first else -15, f"- {cat}: %{score}"))
            first = False
    else:
        lines.append(("F2", 10, -18, "Bu mulakat icin kategori bazli skor hesaplanamadi."))

    lines.append(("F1", 13, -30, "3. GUCLU YONLER"))
    if strengths:
        for i, s in enumerate(strengths):
            lines.append(("F2", 10, -18 if i == 0 else -15, f"[+] {s}"))
    else:
        lines.append(("F2", 10, -18, "Belirgin bir guclu yon tespit edilemedi."))

    lines.append(("F1", 13, -30, "4. GELISTIRILMESI GEREKEN ALANLAR"))
    if improvement_areas:
        for i, s in enumerate(improvement_areas):
            lines.append(("F2", 10, -18 if i == 0 else -15, f"[!] {s}"))
    else:
        lines.append(("F2", 10, -18, "Belirgin bir gelisim alani tespit edilemedi."))

    lines.append(("F1", 13, -30, "5. YAPAY ZEKA GERI BILDIRIMI"))
    feedback_lines = _wrap_text(ai_feedback) or ["Bu mulakat icin AI geri bildirimi mevcut degil."]
    for i, fl in enumerate(feedback_lines):
        lines.append(("F2", 10, -18 if i == 0 else -15, fl))

    lines.append(("F2", 8, -35, "TUBITAK 2209-A Programi Kapsaminda Uretilmistir."))

    body_parts = ["BT", "40 800 Td"]
    current_font, current_size = None, None
    for font, size, dy, text in lines:
        if font != current_font or size != current_size:
            body_parts.append(f"/{font} {size} Tf")
            current_font, current_size = font, size
        body_parts.append(f"0 {dy} Td")
        body_parts.append(f"({_pdf_escape(text)}) Tj")
    body_parts.append("ET")
    stream_content = "\n".join(body_parts)
    stream_bytes = stream_content.encode("latin-1", errors="replace")

    header = b"%PDF-1.4\n"

    objects = []
    objects.append(b"1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n")
    objects.append(b"2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n")
    objects.append(
        b"3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/Resources <<\n/Font <<\n"
        b"/F1 4 0 R\n/F2 5 0 R\n>>\n>>\n/MediaBox [0 0 595 842]\n/Contents 6 0 R\n>>\nendobj\n"
    )
    objects.append(b"4 0 obj\n<<\n/Type /Font\n/Subtype /Type1\n/BaseFont /Helvetica-Bold\n>>\nendobj\n")
    objects.append(b"5 0 obj\n<<\n/Type /Font\n/Subtype /Type1\n/BaseFont /Helvetica\n>>\nendobj\n")
    objects.append(
        b"6 0 obj\n<<\n/Length " + str(len(stream_bytes)).encode() + b"\n>>\nstream\n"
        + stream_bytes + b"\nendstream\nendobj\n"
    )

    offsets = [0]
    pdf_bytes = bytearray(header)
    for obj in objects:
        offsets.append(len(pdf_bytes))
        pdf_bytes += obj

    xref_offset = len(pdf_bytes)
    n_objects = len(objects) + 1

    xref_lines = ["xref", f"0 {n_objects}", "0000000000 65535 f "]
    for off in offsets[1:]:
        xref_lines.append(f"{off:010d} 00000 n ")
    xref_block = ("\n".join(xref_lines) + "\n").encode("latin-1")

    trailer = (
        f"trailer\n<<\n/Size {n_objects}\n/Root 1 0 R\n>>\nstartxref\n{xref_offset}\n%%EOF"
    ).encode("latin-1")

    pdf_bytes += xref_block + trailer
    return bytes(pdf_bytes)
