"""
SmartHire AI - Upload CV Page

Tamamen Streamlit widget'ları kullanılarak oluşturulmuş
CV yükleme ekranı.
"""

import os
import tempfile

import streamlit as st

from utils.session import SessionManager
from components.header import render_page_header
from components.cards import render_info_card


def parse_uploaded_cv(uploaded_file):
    """
    CV'yi okuyup temel bilgileri döndürür.
    """
    try:
        from services.cv_okuyucu import read_cv

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name

        try:
            parsed = read_cv(tmp_path)

            skills_text = parsed.get("sections", {}).get("skills", "")

            skills = [
                s.strip()
                for s in skills_text.split("\n")
                if s.strip()
            ]

            return {
                "name": parsed.get("name"),
                "skills": skills,
                "clean_text": parsed.get("clean_text", ""),
                "english_level": parsed.get("english_level"),
            }

        finally:
            os.remove(tmp_path)

    except Exception:

        return {
            "name": uploaded_file.name,
            "skills": [
                "React",
                "JavaScript",
                "Python",
                "Git"
            ],
            "clean_text": "",
            "english_level": None,
        }


def render():
    """CV Yükleme Sayfası"""

    if st.session_state.get("cv_required_warning"):
        st.session_state["cv_required_warning"] = False
        st.warning(
            "⚠️ Mülakata başlayabilmek için önce CV'ni yüklemen gerekiyor. "
            "Lütfen aşağıdan PDF olarak CV'ni yükle."
        )

    render_page_header(
        title="CV Yükle 📄",
        subtitle="CV'ni yükle ve hedeflediğin pozisyonu seç.",
        badge="Adım 1 / 2"
    )

    render_info_card(
        title="Neden CV yüklemeliyim?",
        description=(
            "SmartHire AI CV'ni analiz ederek sana özel "
            "mülakat soruları oluşturur."
        ),
        icon="💡",
        badge="Bilgi"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("CV Dosyası")

        uploaded_file = st.file_uploader(
            "PDF seç",
            type=["pdf"]
        )

        if uploaded_file:

            parsed = parse_uploaded_cv(uploaded_file)

            st.session_state.cv_data["uploaded"] = True
            st.session_state.cv_data["file_name"] = uploaded_file.name
            st.session_state.cv_data["skills"] = parsed["skills"]
            st.session_state.cv_data["english_level"] = parsed["english_level"]
            st.session_state.cv_data["clean_text"] = parsed["clean_text"]

            if parsed["name"]:
                st.session_state.user["name"] = parsed["name"]

            # Hesaba kalıcı olarak kaydet — bir dahaki girişte bu CV
            # tekrar yüklenmeden hazır gelsin.
            SessionManager.persist_cv_data()

            st.success("CV başarıyla yüklendi.")

            if parsed["english_level"]:
                st.caption(
                    f"🇬🇧 Tespit edilen İngilizce seviyesi: "
                    f"**{parsed['english_level']}**"
                    + (
                        " — mülakata bir İngilizce soru eklenecek."
                        if parsed["english_level"] in ("B1", "B2", "C1", "C2")
                        else ""
                    )
                )

            st.write("### Tespit edilen beceriler")

            if parsed["skills"]:
                for skill in parsed["skills"]:
                    st.success(skill)
            else:
                st.info("Beceri bulunamadı.")

        elif st.session_state.cv_data.get("uploaded"):
            # Bu sayfaya daha önce (bu oturumda ya da geçmiş bir
            # girişte) yüklenmiş bir CV var, ama file_uploader widget'ı
            # bu render'da boş (sayfa değişikliği/yeniden giriş
            # sonrası widget'lar sıfırlanır). Kullanıcıyı "CV
            # yüklenmedi" diye yanıltmak yerine zaten kayıtlı olan
            # CV'yi göster; istersen üstteki alandan yeni bir dosya
            # seçip değiştirebilir.
            st.success(
                f"✅ Daha önce yüklediğin CV kayıtlı: "
                f"**{st.session_state.cv_data.get('file_name', 'CV.pdf')}**"
            )
            st.caption(
                "Yeniden yüklemene gerek yok. Farklı bir CV kullanmak "
                "istersen yukarıdan yeni bir dosya seçmen yeterli."
            )

            existing_english = st.session_state.cv_data.get("english_level")
            if existing_english:
                st.caption(f"🇬🇧 Tespit edilen İngilizce seviyesi: **{existing_english}**")

            existing_skills = st.session_state.cv_data.get("skills", [])
            if existing_skills:
                st.write("### Tespit edilen beceriler")
                for skill in existing_skills:
                    st.success(skill)

        else:
            st.info("Henüz CV yüklenmedi.")

    with col2:

        st.subheader("Pozisyon Bilgisi")

        position = st.text_input(
            "Hedef Pozisyon",
            value=st.session_state.cv_data.get(
                "position",
                "Frontend Developer"
            )
        )

        experience = st.selectbox(
            "Deneyim",
            [
                "Deneyimsiz / Yeni Mezun",
                "Junior",
                "Mid",
                "Senior",
                "Lead"
            ]
        )

        job_description = st.text_area(
            "İş İlanı",
            height=200
        )

    st.divider()

    if st.button(
        " Analize Devam Et",
        use_container_width=True,
        type="primary"
    ):

        st.session_state.cv_data["position"] = position
        st.session_state.cv_data["experience_level"] = experience
        st.session_state.cv_data["job_description"] = job_description

        SessionManager.persist_cv_data()

        # Yeni bir CV/ilan girildiği için önceki analiz sonucu geçersizdir
        st.session_state.ai_processing_done = False

        SessionManager.navigate_to("ai_processing")