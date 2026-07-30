import { useNavigate } from 'react-router-dom';
import {
  Download,
  Share2,
  Printer,
  CheckCircle,
  AlertTriangle,
  TrendingUp,
  TrendingDown,
  Zap,
} from 'lucide-react';
import Button from '../../components/Button/Button';
import Badge from '../../components/Badge/Badge';
import ProgressBar from '../../components/ProgressBar/ProgressBar';
import Breadcrumb from '../../components/Breadcrumb/Breadcrumb';
import { useToast } from '../../components/Toast/Toast';
import './PDFReport.css';

const CATEGORY_SCORES = [
  { label: 'React & Hooks', score: 88 },
  { label: 'JavaScript', score: 74 },
  { label: 'TypeScript', score: 71 },
  { label: 'Sistem Tasarımı', score: 45 },
  { label: 'Algoritma & Veri Yapıları', score: 62 },
];

const STRENGTHS = [
  'React hooks ve state yönetiminde üst düzey bilgi',
  'Kavramları net ve anlaşılır biçimde açıklama',
  'JavaScript event loop ve async mekanizmalarına hâkimiyet',
];

const IMPROVEMENTS = [
  'Sistem tasarımı sorularında yapılandırma geliştirmeli',
  'Ölçeklenebilirlik senaryolarında daha fazla pratik gerekiyor',
];

export default function PDFReport() {
  const navigate = useNavigate();
  const toast = useToast();

  const handleDownload = () => {
    toast.info('Rapor hazırlanıyor', 'PDF indirme başlatılıyor…');
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="pdf-report">
      <Breadcrumb
        items={[
          { label: 'Dashboard', to: '/dashboard' },
          { label: 'Mülakat Geçmişi', to: '/history' },
          { label: 'PDF Rapor' },
        ]}
      />

      <div className="page-header">
        <div className="page-header__left">
          <h1 className="page-header__title">Mülakat Raporu</h1>
          <p className="page-header__subtitle">Frontend Developer • 24 Temmuz 2024</p>
        </div>
        <div className="page-header__actions">
          <Button variant="ghost" leftIcon={<Share2 size={15} />} disabled>Paylaş</Button>
          <Button variant="ghost" leftIcon={<Printer size={15} />} onClick={handlePrint}>Yazdır</Button>
          <Button variant="primary" leftIcon={<Download size={15} />} onClick={handleDownload}>PDF İndir</Button>
        </div>
      </div>

      {/* Report preview */}
      <div className="pdf-preview" id="pdf-preview">
        {/* Report header */}
        <div className="pdf-preview__header">
          <div className="pdf-preview__logo">
            <Zap size={16} fill="currentColor" />
            SmartHire AI — Mülakat Raporu
          </div>
          <div className="pdf-preview__meta">
            <p>Senan Öztürk</p>
            <p>24 Temmuz 2024 • Frontend Developer</p>
          </div>
        </div>

        {/* Score section */}
        <div className="pdf-preview__score-section">
          <div className="pdf-score-card">
            <p className="pdf-score-label">Genel Skor</p>
            <p className="pdf-score-value">72%</p>
            <ProgressBar value={72} animated size="thin" />
          </div>
          <div className="pdf-score-meta">
            <div className="pdf-stat">
              <span className="pdf-stat__label">Toplam soru</span>
              <span className="pdf-stat__value">5</span>
            </div>
            <div className="pdf-stat">
              <span className="pdf-stat__label">Yanıtlanan</span>
              <span className="pdf-stat__value">5</span>
            </div>
            <div className="pdf-stat">
              <span className="pdf-stat__label">Süre</span>
              <span className="pdf-stat__value">38 dk</span>
            </div>
            <div className="pdf-stat">
              <span className="pdf-stat__label">Karşılaştırma</span>
              <Badge variant="success" size="sm">
                <TrendingUp size={10} /> +4 puan
              </Badge>
            </div>
          </div>
        </div>

        <div className="pdf-preview__divider" />

        {/* Category scores */}
        <div className="pdf-section">
          <h2 className="pdf-section__title">Kategori Skorları</h2>
          <div className="pdf-categories">
            {CATEGORY_SCORES.map(c => (
              <div key={c.label} className="pdf-cat">
                <div className="pdf-cat__header">
                  <span className="pdf-cat__label">{c.label}</span>
                  <span className="pdf-cat__val">{c.score}%</span>
                </div>
                <ProgressBar value={c.score} size="thin" />
              </div>
            ))}
          </div>
        </div>

        <div className="pdf-preview__divider" />

        {/* Strengths & Improvements */}
        <div className="pdf-preview__two-col">
          <div className="pdf-section">
            <h2 className="pdf-section__title">
              <TrendingUp size={16} /> Güçlü Yönler
            </h2>
            <ul className="pdf-list pdf-list--success">
              {STRENGTHS.map((s, i) => (
                <li key={i}>
                  <CheckCircle size={14} />
                  <span>{s}</span>
                </li>
              ))}
            </ul>
          </div>
          <div className="pdf-section">
            <h2 className="pdf-section__title">
              <TrendingDown size={16} /> Geliştirilmesi Gerekenler
            </h2>
            <ul className="pdf-list pdf-list--warning">
              {IMPROVEMENTS.map((s, i) => (
                <li key={i}>
                  <AlertTriangle size={14} />
                  <span>{s}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="pdf-preview__divider" />

        {/* Footer */}
        <div className="pdf-preview__footer">
          <p>Bu rapor SmartHire AI tarafından otomatik oluşturulmuştur. TÜBİTAK 2209-A Destekli Proje.</p>
          <p>smarthire.ai • {new Date().getFullYear()}</p>
        </div>
      </div>
    </div>
  );
}
