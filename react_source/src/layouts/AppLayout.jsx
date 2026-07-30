import { useState } from 'react';
import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import {
  LayoutDashboard,
  MessageSquare,
  History,
  Settings,
  FileText,
  Clock,
  ArrowRight,
} from 'lucide-react';
import Sidebar from '../components/Sidebar/Sidebar';
import Navbar from '../components/Navbar/Navbar';
import Modal from '../components/Modal/Modal';
import Select from '../components/Select/Select';
import Button from '../components/Button/Button';
import { useToast } from '../components/Toast/Toast';
import './AppLayout.css';

// Geçmiş ilanlar — gerçek uygulamada API'den gelir
const PAST_POSITIONS = [
  { value: 'frontend-dev-techcorp', label: 'Frontend Developer — Tech Corp (24 Tem)' },
  { value: 'react-dev-startupxyz', label: 'React Developer — Startup XYZ (18 Tem)' },
  { value: 'fullstack-agencyabc', label: 'Full Stack Developer — Agency ABC (10 Tem)' },
];

// Geçici mock kullanıcı
const MOCK_USER = {
  name: 'Senan Aliyev',
  role: 'Frontend Developer Adayı',
  avatarSrc: null,
};

/**
 * AppLayout — Authenticated ekranlar
 * Sidebar (desktop 240px / 64px) + Navbar (mobil) + Content + BottomNav (mobil)
 * "Mülakat" sidebar linki direkt /interview'a GİTMEZ — pozisyon seçim modalını açar.
 * Yarım kalan oturumlar bu modaldan değil, Geçmiş sayfasından görüntülenir.
 */
export default function AppLayout() {
  const [collapsed, setCollapsed] = useState(false);
  const navigate = useNavigate();
  const toast = useToast();

  // Interview start modal
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedPast, setSelectedPast] = useState('');
  const [pastError, setPastError] = useState('');

  const openInterviewModal = (e) => {
    // NavLink default navigasyonunu engelle
    if (e) e.preventDefault();
    setSelectedPast('');
    setPastError('');
    setModalOpen(true);
  };

  const handleNewJob = () => {
    setModalOpen(false);
    navigate('/onboarding?step=job');
  };

  const handlePastJob = () => {
    if (!selectedPast) { setPastError('Lütfen bir pozisyon seçin.'); return; }
    setModalOpen(false);
    toast.info('Mülakat hazırlanıyor', 'Seçtiğin pozisyon için sorular oluşturuluyor…');
    setTimeout(() => navigate('/interview'), 700);
  };

  // Nav items — Mülakat özel handler ile
  const BOTTOM_NAV_ITEMS = [
    { to: '/dashboard', icon: <LayoutDashboard size={20} />, label: 'Dashboard' },
    { to: '/interview', icon: <MessageSquare size={20} />,   label: 'Mülakat',  onClick: openInterviewModal },
    { to: '/history',   icon: <History size={20} />,         label: 'Geçmiş' },
    { to: '/settings',  icon: <Settings size={20} />,        label: 'Ayarlar' },
  ];

  return (
    <>
      {/* ---- Mülakat Başlatma Modalı (AppLayout seviyesinde) ---- */}
      <Modal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        title="Yeni Mülakat Başlat"
      >
        <div className="interview-modal">
          {/* Seçenek 1: Yeni ilan */}
          <button className="interview-modal__option" onClick={handleNewJob} id="layout-modal-new-job">
            <div className="interview-modal__option-icon interview-modal__option-icon--blue">
              <FileText size={20} />
            </div>
            <div className="interview-modal__option-text">
              <p className="interview-modal__option-label">Yeni ilan gir</p>
              <p className="interview-modal__option-sub">Yeni bir iş ilanı veya pozisyon adı ekle. CV zaten kayıtlı.</p>
            </div>
            <ArrowRight size={16} className="interview-modal__option-arrow" />
          </button>

          <div className="interview-modal__divider"><span>veya</span></div>

          {/* Seçenek 2: Geçmiş ilan */}
          <div className="interview-modal__option-group">
            <div className="interview-modal__past-head">
              <div className="interview-modal__option-icon interview-modal__option-icon--purple">
                <Clock size={20} />
              </div>
              <div>
                <p className="interview-modal__option-label">Geçmiş ilanlardan seç</p>
                <p className="interview-modal__option-sub">Daha önce kullandığın pozisyonla direkt mülakata gir.</p>
              </div>
            </div>
            <Select
              id="layout-modal-past-position"
              placeholder="Pozisyon seçin…"
              options={PAST_POSITIONS}
              value={selectedPast}
              onChange={(e) => { setSelectedPast(e.target.value); if (e.target.value) setPastError(''); }}
              state={pastError ? 'error' : 'default'}
              errorMsg={pastError}
            />
            <Button variant="primary" fullWidth onClick={handlePastJob} rightIcon={<ArrowRight size={15} />} disabled={!selectedPast}>
              Mülakata başla
            </Button>
          </div>
        </div>
      </Modal>

      {/* ---- Layout ---- */}
      <div className="app-layout">
        {/* Desktop sidebar — openInterviewModal callback geçiliyor */}
        <Sidebar
          user={MOCK_USER}
          collapsed={collapsed}
          onToggle={() => setCollapsed((v) => !v)}
          onInterviewClick={openInterviewModal}
        />

        {/* Content area */}
        <div className="app-layout__content">
          <Navbar user={MOCK_USER} />
          <main className="app-layout__main">
            <Outlet />
          </main>
        </div>

        {/* Mobile bottom navigation */}
        <nav className="bottom-nav" aria-label="Mobil alt menü">
          <ul className="bottom-nav__list">
            {BOTTOM_NAV_ITEMS.map(({ to, icon, label, onClick }) => (
              <li key={to} style={{ display: 'contents' }}>
                <NavLink
                  to={to}
                  onClick={onClick}
                  className={({ isActive }) =>
                    `bottom-nav__item${isActive ? ' bottom-nav__item--active' : ''}`
                  }
                  aria-label={label}
                >
                  {icon}
                  <span>{label}</span>
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>
      </div>
    </>
  );
}
