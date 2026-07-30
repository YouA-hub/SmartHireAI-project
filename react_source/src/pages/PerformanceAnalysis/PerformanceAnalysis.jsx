import { useNavigate } from 'react-router-dom';
import {
  TrendingUp,
  TrendingDown,
  AlertTriangle,
  CheckCircle,
  RotateCcw,
  Download,
  ChevronRight,
  Languages,
} from 'lucide-react';
import Button from '../../components/Button/Button';
import Card from '../../components/Card/Card';
import Badge from '../../components/Badge/Badge';
import ProgressBar from '../../components/ProgressBar/ProgressBar';
import Breadcrumb from '../../components/Breadcrumb/Breadcrumb';
import './PerformanceAnalysis.css';

/*
  Kategori skorları — "Problem çözme" ve "İletişim" gibi soyut kategoriler KALDIRILDI.
  Bunun yerine pozisyona özgü teknik alt başlıklar kullanılır.
  "İletişim kalitesi" skoru teknik cevapların açıklık/yapılandırılmışlık
  düzeyinden LLM tarafından türetiliyor — ayrı bir soru türü DEĞİL.
*/
const CATEGORY_SCORES = [
  { label: 'React & Hooks', score: 88, variant: 'success' },
  { label: 'JavaScript (Event Loop / Async)', score: 74, variant: 'primary' },
  { label: 'TypeScript (Generics & Types)', score: 71, variant: 'primary' },
  { label: 'Sistem Tasarımı', score: 45, variant: 'warning' },
  {
    label: 'Cevap Netliği (LLM türetilmiş)',
    score: 80,
    variant: 'primary',
    note: 'Teknik cevapların yapılandırılmışlık düzeyinden türetildi — ayrı bir soru değil.',
  },
];

const STRENGTHS = [
  { icon: <CheckCircle size={16} />, text: 'React hooks ve state yönetimi konusunda üst düzey bilgi.' },
  { icon: <CheckCircle size={16} />, text: 'Kavramları net ve anlaşılır biçimde açıklıyor.' },
  { icon: <CheckCircle size={16} />, text: 'JavaScript event loop ve async mekanizmalarına hâkim.' },
];

const WEAKNESSES = [
  { icon: <AlertTriangle size={16} />, text: 'Sistem tasarımı sorularında yapılandırma eksik.' },
  { icon: <AlertTriangle size={16} />, text: 'Ölçeklenebilirlik senaryolarında daha fazla pratik gerekiyor.' },
];

/*
  Dil tutarlılık kontrolü — CV beyanı ile mülakattaki İngilizce cevabın karşılaştırması.
  Bu resmi bir CEFR sınavı DEĞİL — sadece bir tutarlılık sinyali.
*/
const LANGUAGE_CHECK = {
  cvLevel: 'B2',           // CV'de beyan edilen seviye (null ise gösterilmez)
  detectedLevel: 'B2',     // LLM'in İngilizce cevaptan çıkardığı tahmin
  consistent: true,        // true → yeşil onay, false → amber uyarı
  note: 'Cevabınızda net yapı, uygun kelime haznesi ve doğru dilbilgisi gözlemlendi.',
};

export default function PerformanceAnalysis() {
  const navigate = useNavigate();
  const score = 72;

  const langConsistent = LANGUAGE_CHECK.consistent;

  return (
    <div className="performance">
      <Breadcrumb
        items={[
          { label: 'Dashboard', to: '/dashboard' },
          { label: 'Mülakat Değerlendirmesi' },
        ]}
      />

      <div className="page-header">
        <div className="page-header__left">
          <h1 className="page-header__title">Mülakat Değerlendirmesi</h1>
          <p className="page-header__subtitle">Frontend Developer • 24 Temmuz 2024 • 6 soru</p>
        </div>
        <div className="page-header__actions">
          <Button variant="secondary" leftIcon={<Download size={15} />} onClick={() => navigate('/pdf-report')}>
            PDF Rapor
          </Button>
        </div>
      </div>

      <div className="performance__layout">
        {/* Gradient score card */}
        <Card variant="gradient" className="performance__score-card">
          <p className="performance__score-label">Genel Hazırlık Skoru</p>
          <p className="performance__score-value">{score}%</p>
          <ProgressBar value={score} animated size="thin" />
          <p className="performance__score-note">3 mülakat ortalaması • Son 30 gün</p>
          <div className="performance__score-change">
            <TrendingUp size={14} />
            <span>+4 puan önceki mülakata göre</span>
          </div>
        </Card>

        {/* Category scores */}
        <Card>
          <Card.Header title="Kategori Skorları">
            <Badge variant="primary" size="sm">Teknik</Badge>
          </Card.Header>
          <div className="performance__categories">
            {CATEGORY_SCORES.map(c => (
              <div key={c.label} className="perf-cat">
                <div className="perf-cat__header">
                  <span className="perf-cat__label">
                    {c.label}
                    {c.note && (
                      <span className="perf-cat__note" title={c.note}> ⓘ</span>
                    )}
                  </span>
                  <span className="perf-cat__val">{c.score}%</span>
                </div>
                <ProgressBar value={c.score} size="thin" />
              </div>
            ))}
          </div>
        </Card>

        {/* Strengths */}
        <Card>
          <Card.Header title="Güçlü Yönler">
            <Badge variant="success" size="sm">{STRENGTHS.length} alan</Badge>
          </Card.Header>
          <div className="perf-list">
            {STRENGTHS.map((s, i) => (
              <div key={i} className="perf-list__item perf-list__item--success">
                <span className="perf-list__icon">{s.icon}</span>
                <p className="perf-list__text">{s.text}</p>
              </div>
            ))}
          </div>
        </Card>

        {/* Weaknesses */}
        <Card>
          <Card.Header title="Geliştirilmesi Gerekenler">
            <Badge variant="warning" size="sm">{WEAKNESSES.length} alan</Badge>
          </Card.Header>
          <div className="perf-list">
            {WEAKNESSES.map((w, i) => (
              <div key={i} className="perf-list__item perf-list__item--warning">
                <span className="perf-list__icon">{w.icon}</span>
                <p className="perf-list__text">{w.text}</p>
              </div>
            ))}
          </div>
        </Card>

        {/* ---- Dil Tutarlılık Kontrolü ---- */}
        {LANGUAGE_CHECK.cvLevel && (
          <Card>
            <Card.Header title="Dil Tutarlılık Kontrolü">
              <Badge variant={langConsistent ? 'success' : 'warning'} size="sm">
                {langConsistent ? 'CV ile tutarlı' : 'Farklılık var'}
              </Badge>
            </Card.Header>
            <div className={`lang-check lang-check--${langConsistent ? 'ok' : 'warn'}`}>
              <div className="lang-check__icon">
                <Languages size={20} />
              </div>
              <div className="lang-check__body">
                <p className="lang-check__title">
                  {langConsistent
                    ? `CV'deki ${LANGUAGE_CHECK.cvLevel} seviyesiyle tutarlı`
                    : `CV'deki ${LANGUAGE_CHECK.cvLevel} seviyesiyle farklılık gösteriyor (cevabınız ${LANGUAGE_CHECK.detectedLevel} seviyesine yakın)`
                  }
                </p>
                <p className="lang-check__note">{LANGUAGE_CHECK.note}</p>
                <p className="lang-check__disclaimer">
                  Bu bir resmi dil yeterlilik testi değildir — yalnızca CV beyanı ile mülakat yanıtı arasındaki tutarlılık sinyalidir.
                </p>
              </div>
              <div className="lang-check__status">
                {langConsistent
                  ? <CheckCircle size={20} className="lang-check__status--ok" />
                  : <AlertTriangle size={20} className="lang-check__status--warn" />
                }
              </div>
            </div>
          </Card>
        )}

        {/* CTA strip */}
        <div className="performance__cta-strip">
          <div className="performance__cta-text">
            <TrendingDown size={18} />
            <div>
              <p className="performance__cta-title">Sistem tasarımını güçlendir</p>
              <p className="performance__cta-sub">Gelişim yol haritana özel kaynaklar hazırlandı.</p>
            </div>
          </div>
          <div className="performance__cta-actions">
            <Button variant="primary" rightIcon={<ChevronRight size={15} />} onClick={() => navigate('/development-plan')}>
              Gelişim planını gör
            </Button>
            <Button variant="ghost" leftIcon={<RotateCcw size={14} />} onClick={() => navigate('/interview')}>
              Tekrar dene
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
