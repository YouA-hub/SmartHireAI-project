"""
SmartHire AI - Results Page

Tamamen Streamlit widget'ları kullanılarak oluşturulmuş
mülakat sonuç ekranı. Skorlar, kategori bazlı performans, güçlü/zayıf
yönler ve AI geri bildirimi artık sabit demo veri DEĞİL — mülakat
bitiminde `evaluate_interview_answers()` tarafından hesaplanıp
`st.session_state.interview_state` içine yazılan gerçek sonuçlardır
(bkz. pages/interview.py -> _finish_interview()).
"""

from datetime import date

import streamlit as st

from utils.session import SessionManager
from utils.pdf_generator import generate_pdf_report
from components.header import render_page_header
from components.cards import render_stat_card, render_info_card
from components.progressbar import render_progress_bar


def _render_abandoned_warning(abandon_reason):
    """
    Mülakat, sayfa/sekme değişikliği yüzünden erken sonlandırıldıysa
    bunu net biçimde gösteren uyarı bandı + bir kerelik açılan uyarı
    diyaloğu. Kullanıcının kaldığı yerden devam edemeyeceğini ve yeni bir
    mülakat başlatması gerektiğini vurgular.
    """

    if abandon_reason == "tab_switch":
        reason_text = (
            "mülakat sırasında başka bir sekmeye, pencereye veya siteye "
            "geçiş yapıldığı"
        )
    else:
        reason_text = (
            "mülakat tamamlanmadan navigasyon menüsünden başka bir sayfaya "
            "geçildiği"
        )

    st.error(
        f"⚠️ Bu mülakat, {reason_text} için sistem tarafından erken "
        "sonlandırıldı. Bu bir gerçek performans sonucu DEĞİLDİR ve "
        "kaldığın yerden devam edemezsin — aşağıdaki **🚀 Yeni Mülakat** "
        "butonuyla baştan başlayabilirsin."
    )

    session_id = st.session_state.interview_state.get("session_id")
    if st.session_state.get("abandon_dialog_shown_for") != session_id:

        @st.dialog("⚠️ Mülakat Erken Sonlandırıldı")
        def _dialog():
            st.write(
                f"Bu mülakat {reason_text} için otomatik olarak "
                "sonlandırıldı ve yarım kalan oturum kaydedilmedi."
            )
            st.write(
                "Kaldığın yerden devam etmek mümkün değil. Yeni bir "
                "mülakat başlatmak veya başka bir sayfaya geçmek "
                "istersin."
            )

            col_new, col_close = st.columns(2)
            with col_new:
                if st.button(
                    "🚀 Yeni Mülakat Başlat",
                    use_container_width=True,
                    type="primary",
                ):
                    st.session_state.abandon_dialog_shown_for = session_id
                    SessionManager.start_new_interview()
            with col_close:
                if st.button("Tamam, Anladım", use_container_width=True):
                    st.session_state.abandon_dialog_shown_for = session_id
                    st.rerun()

        _dialog()


def render():
    """Mülakat Sonuç Sayfası"""

    cv_info = st.session_state.get("cv_data", {})
    position = cv_info.get("position", "Frontend Developer")

    user = st.session_state.get("user", {})
    user_name = user.get("name", "Kullanıcı")

    interview_state = st.session_state.interview_state

    readiness_score = interview_state.get("readiness_score", 65)
    hireability_rate = interview_state.get("hireability_rate", 60)
    cv_match_score = interview_state.get("cv_match_score", 70)
    category_scores = interview_state.get("category_scores", [])
    strengths = interview_state.get("strengths", [])
    improvement_areas = interview_state.get("improvement_areas", [])
    ai_feedback = interview_state.get("ai_feedback", "")
    evaluated_by_ai = interview_state.get("evaluated_by_ai", False)

    was_abandoned = interview_state.get("was_abandoned", False)
    abandon_reason = interview_state.get("abandon_reason")

    # Bu mülakatı geçmiş listesine kaydet (InterviewHistory sayfası için)
    SessionManager.record_completed_interview()

    render_page_header(
        title="📊 Mülakat Değerlendirme Raporu",
        subtitle=f"{position} • {date.today().strftime('%d.%m.%Y')}",
        badge="Erken Sonlandırıldı" if was_abandoned else "Sonuç Raporu"
    )

    if was_abandoned:
        _render_abandoned_warning(abandon_reason)

    if not evaluated_by_ai:
        st.warning(
            "⚠️ Yapay zeka değerlendirmesi şu anda kullanılamadığı için "
            "aşağıdaki skorlar yaklaşık (fallback) değerlerdir. Gerçek "
            "bir değerlendirme için lütfen daha sonra tekrar dene."
        )

    pdf_bytes = generate_pdf_report(
        user_name=user_name,
        position=position,
        date_str=date.today().strftime("%d.%m.%Y"),
        overall_score=readiness_score,
        hireability=hireability_rate,
        cv_match=cv_match_score
    )

    st.download_button(
        "📄 PDF Raporunu İndir",
        data=pdf_bytes,
        file_name=f"SmartHire_AI_Rapor_{user_name.replace(' ', '_')}.pdf",
        mime="application/pdf",
        use_container_width=True,
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        render_stat_card(
            "İşe Alınma Olasılığı",
            f"%{hireability_rate}",
            "🎯",
            "Yüksek" if hireability_rate >= 70 else "Orta" if hireability_rate >= 40 else "Düşük"
        )
        render_progress_bar(hireability_rate)

    with col2:
        render_stat_card(
            "Genel Mülakat Skoru",
            f"%{readiness_score}",
            "📊",
            "Başarılı" if readiness_score >= 70 else "Geliştirilmeli"
        )
        render_progress_bar(readiness_score)

    with col3:
        render_stat_card(
            "CV Uyum Oranı",
            f"%{cv_match_score}",
            "📄",
            "Pozisyona Uygun" if cv_match_score >= 70 else "Kısmen Uygun"
        )
        render_progress_bar(cv_match_score)

    st.divider()

    st.subheader("📈 Kategori Bazlı Performans")

    if category_scores:
        for item in category_scores:
            st.write(f"**{item['category']}**")
            render_progress_bar(item["score"], value_label=f"%{item['score']}")
    else:
        st.info("Kategori bazlı skor üretilemedi.")

    st.divider()

    render_info_card(
        title="🤖 Yapay Zeka Genel Değerlendirmesi",
        description=ai_feedback or (
            "Bu mülakat için henüz bir AI değerlendirmesi bulunmuyor."
        ),
        icon="🤖",
        badge="LLM Analizi"
    )

    st.divider()

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("✅ Güçlü Yönlerin")

        if strengths:
            for item in strengths:
                st.success(item)
        else:
            st.caption("Belirgin bir güçlü yön tespit edilemedi.")

    with col_right:
        st.subheader("⚠️ Gelişim Alanların")

        if improvement_areas:
            for item in improvement_areas:
                st.warning(item)
        else:
            st.caption("Belirgin bir gelişim alanı tespit edilemedi.")

    st.divider()

    render_info_card(
        title="💡 Kişisel Çalışma Planı",
        description=(
            "Gelişim alanlarına odaklanarak yeni bir mülakat simülasyonu "
            "yapman ve Gelişim Yol Haritası sayfasındaki kaynaklara "
            "göz atman önerilir."
        ),
        icon="📚",
        badge="Öneri"
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button(
            "🗺️ Gelişim Planı",
            use_container_width=True,
            type="primary",
        ):
            SessionManager.navigate_to("dev_plan")

    with col2:
        if st.button(
            "🚀 Yeni Mülakat",
            use_container_width=True,
            type="primary" if was_abandoned else "secondary",
        ):
            SessionManager.start_new_interview()

    with col3:
        if st.button(
            "🏠 Dashboard",
            use_container_width=True,
        ):
            SessionManager.navigate_to("dashboard")