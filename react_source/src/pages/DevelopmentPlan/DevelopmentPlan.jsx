import { useNavigate } from 'react-router-dom';
import {
  BookOpen,
  ExternalLink,
  RotateCcw,
  ChevronRight,
  Flame,
  Star,
  Zap,
  AlertTriangle,
} from 'lucide-react';
import Button from '../../components/Button/Button';
import Card from '../../components/Card/Card';
import Badge from '../../components/Badge/Badge';
import Accordion from '../../components/Accordion/Accordion';
import Breadcrumb from '../../components/Breadcrumb/Breadcrumb';
import './DevelopmentPlan.css';

const PRIORITY_CARDS = [
  {
    id: 1,
    priority: 1,
    icon: <Flame size={18} />,
    iconVariant: 'warning',
    title: 'Sistem Tasarımı',
    score: 45,
    badge: 'Yüksek öncelik',
    badgeVariant: 'warning',
    goal: 'Büyük ölçekli sistemlerin temel bileşenlerini (load balancer, CDN, veritabanı sharding) açıklayabilmek.',
    resources: [
      {
        title: 'System Design Primer',
        url: 'https://github.com/donnemartin/system-design-primer',
        type: 'Özet Rehber',
      },
      {
        title: 'ByteByteGo — System Design 101',
        url: 'https://blog.bytebytego.com/p/system-design-101',
        type: 'Makale',
      },
      {
        title: 'roadmap.sh — System Design',
        url: 'https://roadmap.sh/system-design',
        type: 'Özet Rehber',
      },
    ],
    estimate: '3–4 hafta',
  },
  {
    id: 2,
    priority: 2,
    icon: <AlertTriangle size={18} />,
    iconVariant: 'warning',
    title: 'Algoritma & Veri Yapıları',
    score: 62,
    badge: 'Orta öncelik',
    badgeVariant: 'warning',
    goal: 'LeetCode Medium seviye sorularını 20 dakikada çözebilmek.',
    resources: [
      {
        title: 'NeetCode 150',
        url: 'https://neetcode.io/practice',
        type: 'İnteraktif Platform',
      },
      {
        title: 'roadmap.sh — Data Structures',
        url: 'https://roadmap.sh/datastructures-and-algorithms',
        type: 'Özet Rehber',
      },
      {
        title: 'CS50x — Harvard (YouTube)',
        url: 'https://www.youtube.com/c/cs50',
        type: 'Video',
      },
    ],
    estimate: '6–8 hafta',
  },
  {
    id: 3,
    priority: 3,
    icon: <Star size={18} />,
    iconVariant: 'primary',
    title: 'TypeScript İleri Seviye',
    score: 71,
    badge: 'Orta öncelik',
    badgeVariant: 'primary',
    goal: 'Generic types, utility types ve advanced patterns konularında yetkinlik kazanmak.',
    resources: [
      {
        title: 'TypeScript Deep Dive',
        url: 'https://basarat.gitbook.io/typescript/',
        type: 'Özet Rehber',
      },
      {
        title: 'Matt Pocock — TypeScript Tips (YouTube)',
        url: 'https://www.youtube.com/@mattpocockuk',
        type: 'Video',
      },
      {
        title: 'TypeScript Exercises',
        url: 'https://typescript-exercises.github.io/',
        type: 'İnteraktif Platform',
      },
    ],
    estimate: '2–3 hafta',
  },
];


const FAQ_ITEMS = [
  {
    title: 'Bu planı ne sıklıkla güncelleyebilirim?',
    content: 'Yeni bir mülakat tamamladığınızda plan otomatik olarak güncellenir. Ayrıca profil sayfanızdan manuel olarak da hedeflerinizi düzenleyebilirsiniz.',
  },
  {
    title: 'Önerilerdeki kaynaklar nasıl belirleniyor?',
    content: 'AI, mülakat yanıtlarınızdaki zayıf noktaları tespit ederek alakalı, ücretsiz ve kaliteli kaynak önerileri sunar. Kaynaklar endüstri standardı materyallerden seçilir.',
  },
  {
    title: 'Ne zaman tekrar mülakat yapmalıyım?',
    content: 'Haftada en az 2 pratik mülakat önerilir. Dashboard\'daki hazırlık skorunuz %80\'in üzerine çıktığında gerçek mülakatlar için hazır sayılırsınız.',
  },
];

export default function DevelopmentPlan() {
  const navigate = useNavigate();

  return (
    <div className="dev-plan">
      <Breadcrumb
        items={[
          { label: 'Dashboard', to: '/dashboard' },
          { label: 'Gelişim Yol Haritası' },
        ]}
      />

      <div className="page-header">
        <div className="page-header__left">
          <h1 className="page-header__title">Gelişim Yol Haritası</h1>
          <p className="page-header__subtitle">Son mülakat verilerine göre kişiselleştirildi • 24 Temmuz 2024</p>
        </div>
        <div className="page-header__actions">
          <Button variant="primary" leftIcon={<RotateCcw size={15} />} onClick={() => navigate('/interview')}>
            Tekrar mülakat yap
          </Button>
        </div>
      </div>

      {/* Priority cards */}
      <div className="dev-plan__grid">
        {PRIORITY_CARDS.map(card => (
          <Card key={card.id} className="priority-card">
            <div className="priority-card__header">
              <div className={`priority-card__icon priority-card__icon--${card.iconVariant}`}>
                {card.icon}
              </div>
              <div className="priority-card__meta">
                <div className="priority-card__title-row">
                  <h3 className="priority-card__title">{card.title}</h3>
                  <Badge variant={card.badgeVariant} size="sm">{card.badge}</Badge>
                </div>
                <p className="priority-card__score">Mevcut skor: <strong>{card.score}%</strong></p>
              </div>
            </div>

            <div className="priority-card__goal">
              <p className="priority-card__goal-label">Hedef</p>
              <p className="priority-card__goal-text">{card.goal}</p>
            </div>

            <div className="priority-card__resources">
              <p className="priority-card__resources-label">
                <BookOpen size={13} /> Önerilen kaynaklar
              </p>
              {card.resources.map((r, i) => (
                <a key={i} href={r.url} target="_blank" rel="noopener noreferrer" className="priority-card__resource">
                  <span>{r.title}</span>
                  <div className="priority-card__resource-right">
                    <Badge variant="primary" size="sm">{r.type}</Badge>
                    <ExternalLink size={12} />
                  </div>
                </a>
              ))}
            </div>

            <div className="priority-card__footer">
              <Zap size={13} />
              <span>Tahmini süre: <strong>{card.estimate}</strong></span>
            </div>
          </Card>
        ))}
      </div>

      {/* CTA retry strip */}
      <div className="dev-plan__retry-strip">
        <div className="dev-plan__retry-text">
          <RotateCcw size={18} />
          <div>
            <p className="dev-plan__retry-title">Planda ilerleme kaydettim</p>
            <p className="dev-plan__retry-sub">Yeni bir mülakat yaparak güncel skorunu gör ve planı otomatik güncelle.</p>
          </div>
        </div>
        <Button variant="primary" rightIcon={<ChevronRight size={15} />} onClick={() => navigate('/interview')}>
          Yeni mülakat başlat
        </Button>
      </div>

      {/* FAQ Accordion */}
      <Card>
        <Card.Header title="Sık Sorulan Sorular" />
        <Accordion items={FAQ_ITEMS} />
      </Card>
    </div>
  );
}
