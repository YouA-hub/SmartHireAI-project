"""
SmartHire AI - PDF Report Generator Utility
Herhangi bir dış kütüphaneye ihtiyaç duymadan saf Python ile geçerli PDF dosyası (bytes) üretir.
TÜBİTAK 2209-A projesi için özel olarak hazırlanmıştır.
"""

def generate_pdf_report(user_name: str, position: str, date_str: str, overall_score: int, hireability: int, cv_match: int) -> bytes:
    """
    Kullanıcı mülakat sonuç raporunu standart PDF formatında üretir ve bytes olarak döndürür.
    """
    
    # Standart PDF 1.4 Yapısı
    pdf_content = f"""%PDF-1.4
1 0 obj
<<
  /Type /Catalog
  /Pages 2 0 R
>>
endobj

2 0 obj
<<
  /Type /Pages
  /Kids [3 0 R]
  /Count 1
>>
endobj

3 0 obj
<<
  /Type /Page
  /Parent 2 0 R
  /Resources <<
    /Font <<
      /F1 4 0 R
      /F2 5 0 R
    >>
  >>
  /MediaBox [0 0 595 842]
  /Contents 6 0 R
>>
endobj

4 0 obj
<<
  /Type /Font
  /Subtype /Type1
  /BaseFont /Helvetica-Bold
>>
endobj

5 0 obj
<<
  /Type /Font
  /Subtype /Type1
  /BaseFont /Helvetica
>>
endobj

6 0 obj
<<
  /Length 1400
>>
stream
BT
/F1 18 Tf
40 800 Td
(SmartHire AI - Mulakat Degerlendirme ve Gelisim Raporu) Tj

/F2 11 Tf
0 -22 Td
(Aday Bilgisi: {user_name}  |  Hedef Pozisyon: {position}) Tj
0 -15 Td
(Mulakat Tarihi: {date_str}  |  Platform: SmartHire AI v1.0) Tj

/F1 13 Tf
0 -30 Td
(1. GENEL METRIKLER VE UYUM OZETI) Tj

/F2 10 Tf
0 -18 Td
(Tahmini Ise Alinma Olasiligi: %{hireability}  [Yuksek Uyum Sinyali]) Tj
0 -15 Td
(Genel Mulakat Skoru: %{overall_score}  [+4 Puan Artis]) Tj
0 -15 Td
(CV - Is Ilani Uyum Puani: %{cv_match}  [Ilan Gereksinim Uyumlu]) Tj

/F1 13 Tf
0 -30 Td
(2. TEKNIK KATEGORI SKORLARI) Tj

/F2 10 Tf
0 -18 Td
(- React & Hooks: %88) Tj
0 -15 Td
(- JavaScript Event Loop & Async: %74) Tj
0 -15 Td
(- TypeScript Generics & Types: %71) Tj
0 -15 Td
(- Sistem Tasarimi & API Mimarisi: %45) Tj
0 -15 Td
(- Cevap Netligi & Yapilandirma (STAR): %80) Tj

/F1 13 Tf
0 -30 Td
(3. GUCLU YONLER) Tj

/F2 10 Tf
0 -18 Td
([+] React hooks ve state yonetiminde yuksek teknik hakimiyet.) Tj
0 -15 Td
([+] Kavramlari acik, hedefe yonelik ve yapilandirilmis ifade etme becerisi.) Tj
0 -15 Td
([+] JavaScript event loop ve asenkron mekanizmalara hakimiyet.) Tj

/F1 13 Tf
0 -30 Td
(4. GELISTIRILMESI GEREKEN ALANLAR) Tj

/F2 10 Tf
0 -18 Td
([!] Sistem tasarimi, olceklenebilirlik ve CDN caching konularinda mimari eksiklik.) Tj
0 -15 Td
([!] İlişkisel veritabanı indeksleme ve sorgu optimizasyonu pratigi.) Tj

/F1 13 Tf
0 -30 Td
(5. YAPAY ZEKA GERI BILDIRIMI) Tj

/F2 10 Tf
0 -18 Td
(Aday teknik sorularda yuksek basari gostermistir. Sistem tasarimi sorularinda) Tj
0 -15 Td
(load balancer, caching ve veritabani sharding mimarilerine odaklanmasi onerilir.) Tj

/F1 13 Tf
0 -30 Td
(6. ONERILEN OGRENME KAYNAKLARI) Tj

/F2 10 Tf
0 -18 Td
(1. ByteByteGo - System Design 101 (Video / Makale)) Tj
0 -15 Td
(2. System Design Primer (donnemartin GitHub) (Dokumantasyon)) Tj
0 -15 Td
(3. roadmap.sh - System Design Path (Interaktif Platform)) Tj
0 -15 Td
(4. PostgreSQL Documentation & SQLBolt (Dokumantasyon / Interaktif)) Tj

0 -35 Td
(TUBITAK 2209-A Programi Kapsaminda Uretilmistir. (c) 2026 SmartHire AI) Tj
ET
endstream
endobj

xref
0 7
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
0000000264 00000 n
0000000330 00000 n
0000000391 00000 n
trailer
<<
  /Size 7
  /Root 1 0 R
>>
startxref
1850
%%EOF
"""
    return pdf_content.encode("latin-1", errors="replace")
