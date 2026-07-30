import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Plus,
  AlertTriangle,
  BookOpen,
  ChevronRight,
  TrendingUp,
  FileText,
  History,
  Lightbulb,
  Target,
  CheckCircle,
  ArrowRight,
  Clock,
} from 'lucide-react';

import Button from '../../components/Button/Button';
import Card from '../../components/Card/Card';
import Badge from '../../components/Badge/Badge';
import ProgressBar from '../../components/ProgressBar/ProgressBar';
import EmptyState from '../../components/EmptyState/EmptyState';
import Modal from '../../components/Modal/Modal';
import Select from '../../components/Select/Select';
import { SkeletonCard, SkeletonMetric } from '../../components/Skeleton/Skeleton';
import { useToast } from '../../components/Toast/Toast';
import './Dashboard.css';

/* ---- Mock data ---- */
const METRICS = {
  readinessScore: 72,
  lastInterviewScore: 68,
  cvMatchRate: 81,
};

// Geçmiş ilanlar (gerçek uygulamada API'den gelir)
const PAST_POSITIONS = [
  { value: 'frontend-dev-techcorp', label: 'Frontend Developer — Tech Corp (24 Tem)' },
  { value: 'react-dev-startupxyz', label: 'React Developer — Startup XYZ (18 Tem)' },
  { value: 'fullstack-agencyabc', label: 'Full Stack Developer — Agency ABC (10 Tem)' },
];

const SUGGESTIONS = [
  {
    id: 1,
    icon: <AlertTriangle size={16} />,
    iconVariant: 'warning',
    title: 'Sistem tasarımı konusunu güçlendir',
    desc: 'Son mülakatta sistem tasarımı sorularında %45 puan aldın.',
    badge: 'Yüksek öncelik',
    badgeVariant: 'warning',
  },
  {
    id: 2,
    icon: <BookOpen size={16} />,
    iconVariant: 'info',
    title: 'Veri yapıları pratik yap',
    desc: 'LeetCode ile günde 2 soru çözümü öneriliyor.',
    badge: 'Orta öncelik',
    badgeVariant: 'primary',
  },
  {
    id: 3,
    icon: <CheckCircle size={16} />,
    iconVariant: 'success',
    title: 'React bilgin güçlü — devam et',
    desc: 'Hooks ve performans optimizasyonu konularında %88 aldın.',
    badge: 'Güçlü alan',
    badgeVariant: 'success',
  },
  {
    id: 4,
    icon: <Target size={16} />,
    iconVariant: 'info',
    title: 'İletişim becerilerini geliştir',
    desc: 'Cevaplarında daha net yapılandırma (STAR metodu) önerilir.',
    badge: 'Orta öncelik',
    badgeVariant: 'primary',
  },
];

const QUICK_ACTIONS = [
  {
    id: 'new-interview',
    icon: <Plus size={18} />,
    iconBg: 'rgba(37,99,235,0.1)',
    iconColor: 'var(--color-primary)',
    label: 'Yeni mülakat başlat',
    sub: 'AI ile pratik yap',
    action: 'interview-modal', // özel aksiyon
  },
  {
    id: 'development-plan',
    icon: <TrendingUp size={18} />,
    iconBg: 'rgba(139,92,246,0.1)',
    iconColor: 'var(--color-accent)',
    label: 'Gelişim yol haritası',
    sub: 'Kişisel öğrenme planın',
    to: '/development-plan',
  },
  {
    id: 'cv-upload',
    icon: <FileText size={18} />,
    iconBg: 'var(--color-success-bg)',
    iconColor: 'var(--color-success-text)',
    label: 'CV\'ni güncelle',
    sub: 'Yeni bir pozisyon için analiz et',
    to: '/onboarding',
  },
  {
    id: 'history',
    icon: <History size={18} />,
    iconBg: 'var(--color-bg)',
    iconColor: 'var(--color-muted)',
    label: 'Mülakat geçmişi',
    sub: '3 mülakat tamamlandı',
    to: '/history',
  },
];

/* ---- Component ---- */
export default function Dashboard() {
  const navigate = useNavigate();
  const toast = useToast();
  const [loading] = useState(false);

  // Interview modal state
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedPast, setSelectedPast] = useState('');
  const [pastError, setPastError] = useState('');

  const openInterviewModal = () => {
    setSelectedPast('');
    setPastError('');
    setModalOpen(true);
  };

  const handleQuickAction = (action) => {
    if (action.action === 'interview-modal') {
      openInterviewModal();
    } else {
      navigate(action.to);
    }
  };

  /* Seçenek 1: Yeni ilan gir → Onboarding (sadece ilan adımı) */
  const handleNewJob = () => {
    setModalOpen(false);
    // CV zaten yüklü → onboarding'e ?step=job parametresiyle git
    navigate('/onboarding?step=job');
  };

  /* Seçenek 2: Geçmiş ilanı seç → direkt mülakata */
  const handlePastJob = () => {
    if (!selectedPast) {
      setPastError('Lütfen bir pozisyon seçin.');
      return;
    }
    setModalOpen(false);
    toast.info('Mülakat hazırlanıyor', 'Seçtiğin pozisyon için sorular oluşturuluyor…');
    setTimeout(() => navigate('/interview'), 700);
  };

  if (loading) {
    return (
      <div className="dashboard">
        <div style={{ marginBottom: 'var(--space-6)', height: 64 }}>
          <SkeletonCard />
        </div>
        <div className="dashboard__metrics">
          <SkeletonMetric />
          <SkeletonMetric />
          <SkeletonMetric />
        </div>
      </div>
    );
  }

  return (
    <>
      {/* ---- Mülakat Başlatma Modalı ---- */}
      <Modal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        title="Yeni Mülakat Başlat"
      >
        <div className="interview-modal">
          {/* Seçenek 1 */}
          <button
            className="interview-modal__option"
            onClick={handleNewJob}
            id="modal-new-job"
          >
            <div className="interview-modal__option-icon interview-modal__option-icon--blue">
              <FileText size={20} />
            </div>
            <div className="interview-modal__option-text">
              <p className="interview-modal__option-label">Yeni ilan gir</p>
              <p className="interview-modal__option-sub">
                Yeni bir iş ilanı veya pozisyon adı ekle. CV zaten kayıtlı.
              </p>
            </div>
            <ArrowRight size={16} className="interview-modal__option-arrow" />
          </button>

          <div className="interview-modal__divider">
            <span>veya</span>
          </div>

          {/* Seçenek 2 */}
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
              id="modal-past-position"
              placeholder="Pozisyon seçin…"
              options={PAST_POSITIONS}
              value={selectedPast}
              onChange={(e) => {
                setSelectedPast(e.target.value);
                if (e.target.value) setPastError('');
              }}
              state={pastError ? 'error' : 'default'}
              errorMsg={pastError}
            />

            <Button
              variant="primary"
              fullWidth
              onClick={handlePastJob}
              rightIcon={<ArrowRight size={15} />}
              disabled={!selectedPast}
            >
              Mülakata başla
            </Button>
          </div>
        </div>
      </Modal>

      {/* ---- Dashboard ---- */}
      <div className="dashboard">
        {/* Welcome + CTA */}
        <div className="page-header">
          <div className="page-header__left">
            <h1 className="page-header__title">Merhaba, Senan 👋</h1>
            <p className="page-header__subtitle">
              Hazırlık skorun <strong style={{ color: 'var(--color-primary)', fontWeight: 500 }}>{METRICS.readinessScore}%</strong> — hedefi geçmek için devam et.
            </p>
          </div>
          <div className="page-header__actions">
            <Button variant="primary" onClick={openInterviewModal} leftIcon={<Plus size={16} />}>
              Yeni mülakat başlat
            </Button>
          </div>
        </div>

        {/* Metric Cards */}
        <div className="dashboard__metrics">
          <Card variant="gradient" className="dashboard__score-card">
            <p className="dashboard__score-label">Hazırlık Skoru</p>
            <p className="dashboard__score-value">{METRICS.readinessScore}%</p>
            <ProgressBar value={METRICS.readinessScore} animated size="thin" />
            <p className="dashboard__score-source">3 mülakat verisi • Son güncelleme bugün</p>
          </Card>

          <Card metric label="Son Mülakat Skoru" value={`${METRICS.lastInterviewScore}%`} sub="Frontend Developer — 24 Temmuz">
            <div style={{ marginTop: 'var(--space-2)' }}>
              <ProgressBar value={METRICS.lastInterviewScore} size="thin" />
            </div>
          </Card>

          <Card metric label="CV Uyum Oranı" value={`${METRICS.cvMatchRate}%`} sub="React Developer pozisyonu ile">
            <div style={{ marginTop: 'var(--space-2)' }}>
              <ProgressBar value={METRICS.cvMatchRate} size="thin" />
            </div>
          </Card>
        </div>

        {/* Content: Suggestions + Quick Actions */}
        <div className="dashboard__content">

          {/* Gelişim önerileri */}
          <Card>
            <Card.Header title="Gelişim Önerileri">
              <Badge variant="primary">{SUGGESTIONS.length} öneri</Badge>
            </Card.Header>

            {SUGGESTIONS.length === 0 ? (
              <EmptyState
                icon={<Lightbulb size={24} />}
                title="Henüz öneri yok"
                description="İlk mülakatını tamamladığında kişisel öneriler burada görünecek."
                action={
                  <Button variant="secondary" size="sm" onClick={openInterviewModal}>
                    Mülakat başlat
                  </Button>
                }
              />
            ) : (
              <div className="suggestion-list">
                {SUGGESTIONS.map((s) => (
                  <div key={s.id} className="suggestion-item">
                    <div className={`suggestion-item__icon suggestion-item__icon--${s.iconVariant}`}>
                      {s.icon}
                    </div>
                    <div className="suggestion-item__body">
                      <p className="suggestion-item__title">{s.title}</p>
                      <p className="suggestion-item__desc">{s.desc}</p>
                    </div>
                    <Badge variant={s.badgeVariant} size="sm">{s.badge}</Badge>
                  </div>
                ))}
              </div>
            )}
          </Card>

          {/* Hızlı işlemler */}
          <Card>
            <Card.Header title="Hızlı İşlemler" />
            <div className="quick-actions">
              {QUICK_ACTIONS.map((action) => (
                <div
                  key={action.id}
                  className="quick-action-item"
                  role="button"
                  tabIndex={0}
                  onClick={() => handleQuickAction(action)}
                  onKeyDown={(e) => e.key === 'Enter' && handleQuickAction(action)}
                >
                  <div
                    className="quick-action-item__icon"
                    style={{ background: action.iconBg, color: action.iconColor }}
                    aria-hidden="true"
                  >
                    {action.icon}
                  </div>
                  <div className="quick-action-item__text">
                    <p className="quick-action-item__label">{action.label}</p>
                    <p className="quick-action-item__sub">{action.sub}</p>
                  </div>
                  <ChevronRight size={16} className="quick-action-item__arrow" aria-hidden="true" />
                </div>
              ))}
            </div>
          </Card>

        </div>
      </div>
    </>
  );
}
