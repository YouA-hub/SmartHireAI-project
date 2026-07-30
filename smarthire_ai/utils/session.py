"""
SmartHire AI - Session & State Management Utility
TÜBİTAK 2209-A Projesi için geliştirilmiştir.

st.session_state yönetimi,
kullanıcı verisi,
mülakat durumu,
sayfa akışı
"""

import uuid
import streamlit as st

from utils import user_store


class SessionManager:
    """Streamlit oturum durumunu ve sayfa akışını yöneten yardımcı sınıf."""

    PAGES = {
        "landing": "Ana Sayfa",
        "login": "Giriş Yap",
        "register": "Kayıt Ol",
        "dashboard": "Dashboard",
        "upload_cv": "CV Yükle",
        "ai_processing": "Analiz Ediliyor",
        "cv_confirm": "CV Onay",
        "ready": "Mülakat Hazırlık",
        "interview": "Mülakat",
        "result": "Sonuç",
        "dev_plan": "Gelişim Planı",
        "interview_history": "Geçmiş Mülakatlar",
        "profile": "Profilim",
        "settings": "Ayarlar"
    }

    # Oturum açmadan erişilebilen sayfalar (auth guard buradan okunur)
    PUBLIC_PAGES = ("landing", "login", "register")

    @staticmethod
    def init_session():
        """Uygulamanın ihtiyaç duyduğu tüm session_state alanlarını oluşturur."""

        if "is_authenticated" not in st.session_state:
            st.session_state.is_authenticated = False

        if "active_page" not in st.session_state:
            st.session_state.active_page = (
                "dashboard"
                if st.session_state.is_authenticated
                else "landing"
            )

        if "user" not in st.session_state:
            st.session_state.user = {
                "name": "Senan Aliyev",
                "email": "senan@example.com",
                "role": "Frontend Developer Adayı",
                "avatar_initials": "SA"
            }

        if "cv_data" not in st.session_state:
            st.session_state.cv_data = {
                "file_name": None,
                "uploaded": False,
                "position": "",
                "experience_level": "",
                "match_rate": None,
                "english_level": None,
                "skills": [],
            }

        if "interview_state" not in st.session_state:
            SessionManager.reset_interview_state()

        if "ai_processing_done" not in st.session_state:
            st.session_state.ai_processing_done = False

        if "interview_history" not in st.session_state:
            st.session_state.interview_history = []

        # Mülakat sırasında sidebar'dan başka bir sayfaya geçmek istendiğinde
        # önce onay diyaloğu göstermek için bekleyen hedef sayfa.
        # "__logout__" özel değeri çıkış isteğini temsil eder.
        if "pending_nav_target" not in st.session_state:
            st.session_state.pending_nav_target = None

        # Terkedilen (erken sonlandırılmış) bir mülakatın sonucu ilk kez
        # gösterildiğinde bir kerelik uyarı diyaloğu açmak için kullanılır.
        if "abandon_dialog_shown_for" not in st.session_state:
            st.session_state.abandon_dialog_shown_for = None

    @staticmethod
    def reset_interview_state():
        """
        Yeni mülakat başladığında tüm mülakat verilerini sıfırlar.
        """

        st.session_state.interview_state = {
            "session_id": str(uuid.uuid4())[:8],
            "current_question_index": 0,
            "total_questions": 6,
            "answers": [],
            "is_completed": False,
            "readiness_score": 65,
            "hireability_rate": 60,
            "cv_match_score": 70,
            "category_scores": [],
            "strengths": [],
            "improvement_areas": [],
            "ai_feedback": "",
            "evaluated_by_ai": False,
            # Mülakat normal şekilde (son soru cevaplanarak) mı bitti,
            # yoksa sayfa değişikliği / sekme değişikliği yüzünden mi
            # erken sonlandırıldı — sonuç ekranındaki uyarı bunu okur.
            "was_abandoned": False,
            "abandon_reason": None,
        }

        st.session_state.interview_questions = []
        st.session_state.abandon_dialog_shown_for = None

    # Bu sayfalara girebilmek için gerçek bir CV yüklenmiş olması gerekir.
    # Aksi halde eski/demo veriyle sahte bir mülakat başlatılabiliyordu.
    CV_REQUIRED_PAGES = ("cv_confirm", "ready", "interview")

    @staticmethod
    def is_interview_active() -> bool:
        """Şu an yarım kalmış (tamamlanmamış) bir mülakat oturumu var mı?"""

        interview_state = st.session_state.get("interview_state", {})
        return (
            st.session_state.get("active_page") == "interview"
            and not interview_state.get("is_completed", False)
        )

    @staticmethod
    def request_navigation(page_key: str):
        """
        Sidebar/navbar'dan tetiklenen bir sayfa geçiş isteği.

        Kullanıcı aktif (tamamlanmamış) bir mülakattayken başka bir sayfaya
        geçmeye çalışırsa, sayfayı doğrudan değiştirmek yerine bir onay
        diyaloğu açılması için 'pending_nav_target' bayrağını set eder.
        Aksi halde geçiş doğrudan yapılır.
        """

        if page_key != "interview" and SessionManager.is_interview_active():
            st.session_state.pending_nav_target = page_key
            st.rerun()
            return

        SessionManager.navigate_to(page_key)

    @staticmethod
    def request_logout():
        """Çıkış isteği — aktif mülakat varsa önce onay diyaloğu açılır."""

        if SessionManager.is_interview_active():
            st.session_state.pending_nav_target = "__logout__"
            st.rerun()
            return

        SessionManager.logout_user()

    @staticmethod
    def cancel_pending_navigation():
        """Onay diyaloğunda 'Mülakata Devam Et' seçilince çağrılır."""

        st.session_state.pending_nav_target = None
        st.rerun()

    @staticmethod
    def confirm_pending_navigation():
        """
        Onay diyaloğunda 'Mülakatı Sonlandır ve Ayrıl' seçilince çağrılır.
        Aktif mülakatı erken-sonlandırılmış olarak işaretler ve bekleyen
        hedefe (ya da çıkışa) yönlendirir.
        """

        target = st.session_state.pending_nav_target
        st.session_state.pending_nav_target = None

        SessionManager._terminate_abandoned_interview(reason="navigation")

        if target == "__logout__":
            SessionManager.logout_user()
            return

        SessionManager.navigate_to(target)

    @staticmethod
    def navigate_to(page_key: str):
        """Sayfalar arasında geçiş yapar."""

        if page_key not in SessionManager.PAGES:
            return

        if (
            not st.session_state.is_authenticated
            and page_key not in SessionManager.PUBLIC_PAGES
        ):
            st.session_state.active_page = "landing"
            st.rerun()
            return

        if (
            page_key in SessionManager.CV_REQUIRED_PAGES
            and not st.session_state.get("cv_data", {}).get("uploaded", False)
        ):
            st.session_state.active_page = "upload_cv"
            st.session_state.cv_required_warning = True
            st.rerun()
            return

        # Kullanıcı devam eden (tamamlanmamış) bir mülakattan başka bir
        # sayfaya çıkarsa, bu mülakat kalıcı olarak sonlanır. Kaldığı
        # yerden devam ETMEZ; tekrar "Mülakat"a girildiğinde bu
        # terkedilmiş mülakatın sonucu gösterilir.
        interview_state = st.session_state.get("interview_state", {})
        if (
            st.session_state.get("active_page") == "interview"
            and page_key != "interview"
            and not interview_state.get("is_completed", False)
        ):
            # Normalde bu duruma artık request_navigation() içindeki onay
            # diyaloğu sayesinde gelinmemesi gerekir; yine de doğrudan
            # navigate_to() çağrılan yerler için güvenlik ağı olarak kalır.
            SessionManager._terminate_abandoned_interview(reason="navigation")

        if (
            page_key == "interview"
            and st.session_state.get("interview_state", {}).get("is_completed")
        ):
            st.session_state.active_page = "result"
            st.rerun()
            return

        st.session_state.active_page = page_key
        st.rerun()

    @staticmethod
    def _terminate_abandoned_interview(reason: str = "navigation"):
        """
        Kullanıcı mülakatı tamamlamadan sayfadan/siteden ayrıldığında çağrılır.
        Mülakatı 'tamamlandı' (ama başarısız/yarım kalmış) olarak işaretler.

        reason:
            "navigation"  -> sidebar üzerinden başka bir sayfaya geçildi
            "tab_switch"  -> sekme/pencere/site değiştirildi
        """
        interview_state = st.session_state.interview_state

        interview_state["evaluated_by_ai"] = False
        interview_state["readiness_score"] = 0
        interview_state["hireability_rate"] = 0
        interview_state["strengths"] = []
        interview_state["was_abandoned"] = True
        interview_state["abandon_reason"] = reason

        if reason == "tab_switch":
            interview_state["improvement_areas"] = [
                "Mülakat boyunca aynı sekmede/pencerede kalarak tamamlama"
            ]
            interview_state["ai_feedback"] = (
                "Bu mülakat, sekme veya pencere değişikliği tespit edildiği "
                "için erken sonlandırıldı. Adil bir değerlendirme "
                "yapılabilmesi adına mülakat boyunca başka bir sekmeye/siteye "
                "geçilmemesi gerekir."
            )
        else:
            interview_state["improvement_areas"] = [
                "Mülakatı yarıda bırakmadan tek oturumda tamamlama"
            ]
            interview_state["ai_feedback"] = (
                "Bu mülakat, tamamlanmadan sayfadan çıkıldığı için erken "
                "sonlandırıldı. Adil bir değerlendirme yapılabilmesi adına "
                "mülakatın baştan sona kesintisiz tamamlanması gerekir."
            )

        interview_state["is_completed"] = True

    @staticmethod
    def get_current_page():
        """Aktif sayfayı döndürür."""

        active = st.session_state.get("active_page", "landing")

        if (
            not st.session_state.get("is_authenticated", False)
            and active not in SessionManager.PUBLIC_PAGES
        ):
            return "landing"

        if (
            active == "interview"
            and st.session_state.get("interview_state", {}).get("is_completed")
        ):
            return "result"

        return active

    @staticmethod
    def login_user(
        email: str = "senan@example.com",
        name: str = "Senan Aliyev"
    ):
        """Kullanıcı girişi."""

        st.session_state.is_authenticated = True

        st.session_state.user["name"] = name
        st.session_state.user["email"] = email
        st.session_state.user["avatar_initials"] = "".join(
            part[0].upper()
            for part in name.split()[:2]
        )

        # Bu hesap için diskte kayıtlı bir CV verisi var mı diye bak.
        # Varsa yükle ki kullanıcı her girişte CV'sini yeniden
        # yüklemek zorunda kalmasın. Yoksa (bu hesap ilk kez giriş
        # yapıyor ya da başka bir hesaptan geçildi) temiz bir CV
        # durumuyla başla — böylece önceki hesaptan kalma veri
        # yanlışlıkla bu hesaba karışmaz.
        saved_cv_data = user_store.load_cv_data(email)

        if saved_cv_data:
            st.session_state.cv_data.update(saved_cv_data)
        else:
            st.session_state.cv_data = {
                "file_name": None,
                "uploaded": False,
                "position": "",
                "experience_level": "",
                "match_rate": None,
                "english_level": None,
                "skills": [],
            }

        SessionManager.navigate_to("dashboard")

    @staticmethod
    def persist_cv_data():
        """
        Şu anki cv_data'yı, giriş yapmış kullanıcının hesabına kalıcı
        olarak kaydeder. CV yüklendiğinde ya da pozisyon/ilan bilgisi
        değiştiğinde çağrılmalı.
        """
        email = st.session_state.get("user", {}).get("email")
        if email:
            user_store.save_cv_data(email, st.session_state.cv_data)

    @staticmethod
    def logout_user():
        """Çıkış yap."""

        st.session_state.is_authenticated = False
        st.session_state.active_page = "landing"

        SessionManager.reset_interview_state()

        st.rerun()

    @staticmethod
    def complete_current_interview():
        """
        Aktif mülakatı 'tamamlandı' olarak işaretler.
        """
        st.session_state.interview_state["is_completed"] = True

    @staticmethod
    def record_completed_interview():
        """
        Tamamlanan bir mülakatı geçmiş listesine (interview_history) kaydeder.
        """

        import datetime

        interview_state = st.session_state.interview_state
        session_id = interview_state["session_id"]

        already_logged = any(
            record["session_id"] == session_id
            for record in st.session_state.interview_history
        )

        if already_logged:
            return

        cv_data = st.session_state.cv_data

        st.session_state.interview_history.append({
            "session_id": session_id,
            "date": datetime.date.today().strftime("%d.%m.%Y"),
            "position": cv_data.get("position", "Frontend Developer"),
            "readiness_score": interview_state["readiness_score"],
            "hireability_rate": interview_state["hireability_rate"],
            "cv_match_score": interview_state["cv_match_score"],
            "question_count": interview_state["total_questions"],
        })

    @staticmethod
    def start_new_interview():
        """
        Yeni mülakat başlatır.
        """

        SessionManager.reset_interview_state()
        SessionManager.navigate_to("ready")