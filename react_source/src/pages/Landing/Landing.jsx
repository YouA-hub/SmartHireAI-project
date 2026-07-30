import { useNavigate } from 'react-router-dom';
import {
  Zap,
  FileText,
  BarChart2,
  BookOpen,
  CheckCircle,
  ArrowRight,
  Star,
  Users,
  Target,
  Brain,
  ChevronRight,
} from 'lucide-react';
import Button from '../../components/Button/Button';
import Badge from '../../components/Badge/Badge';
import './Landing.css';

const FEATURES = [
  {
    id: 1,
    icon: <Brain size={24} />,
    title: 'AI Destekli Mülakat',
    desc: 'GPT tabanlı mülakat simülatörü gerçek pozisyona özel sorular üretir ve anında geri bildirim verir.',
    color: 'blue',
  },
  {
    id: 2,
    icon: <FileText size={24} />,
    title: 'CV Analizi',
    desc: 'CV\'ni yükle, AI ilan ile uyumunu analiz etsin. Eksik alanları amber rengiyle gösterir.',
    color: 'purple',
  },
  {
    id: 3,
    icon: <BarChart2 size={24} />,
    title: 'Performans Skoru',
    desc: 'Hazırlık skoru, güçlü/zayıf yönler ve kategori bazlı ince skor barları ile net görünürlük.',
    color: 'blue',
  },
  {
    id: 4,
    icon: <BookOpen size={24} />,
    title: 'Gelişim Yol Haritası',
    desc: 'Önceliklendirilmiş öğrenme önerileri ve kaynak listesiyle kişisel gelişim planın hazır.',
    color: 'purple',
  },
  {
    id: 5,
    icon: <Target size={24} />,
    title: 'Hedef Takibi',
    desc: 'Mülakat geçmişin ve ilerleme verilerinle gerçek zamanlı hazırlık durumunu takip et.',
    color: 'blue',
  },
  {
    id: 6,
    icon: <Users size={24} />,
    title: 'Sektör Odaklı',
    desc: 'Yazılım mühendisliği, ürün yönetimi, veri bilimi ve daha fazla alan için özelleştirilmiş içerik.',
    color: 'purple',
  },
];

const STEPS = [
  {
    num: '01',
    title: 'CV\'ni yükle',
    desc: 'PDF olarak CV\'ni yükle veya iş ilanı metnini yapıştır. AI saniyeler içinde analiz eder.',
  },
  {
    num: '02',
    title: 'Mülakata gir',
    desc: 'AI, pozisyona özel mülakat soruları oluşturur. Yanıtlarını yaz, ses veya metin fark etmez.',
  },
  {
    num: '03',
    title: 'Sonuçları gör',
    desc: 'Anlık performans skoru, güçlü/zayıf analiz ve kişisel gelişim planı ile hazırlık sürecini hızlandır.',
  },
];

const TESTIMONIALS = [
  {
    id: 1,
    name: 'Ayşe Demir',
    role: 'Frontend Developer @ Trendyol',
    text: 'SmartHire ile 3 hafta pratik yaptım ve Google mülakatını geçtim. Sistem tasarımı konusundaki zayıflığımı tam tespit etti.',
    stars: 5,
  },
  {
    id: 2,
    name: 'Mert Kaya',
    role: 'Data Scientist @ Getir',
    text: 'CV analizi inanılmaz. Uyum skoru %94\'e çıktı ve rakip adaylardan sıyrıldım. Kesinlikle tavsiye ederim.',
    stars: 5,
  },
  {
    id: 3,
    name: 'Zeynep Arslan',
    role: 'Product Manager @ Insider',
    text: 'İlk kez bir mülakat simülatörü bu kadar gerçekçi hissettirdi. Sorular gerçekten pozisyona özel geliyordu.',
    stars: 5,
  },
];

export default function Landing() {
  const navigate = useNavigate();

  return (
    <div className="landing">
      {/* Navbar */}
      <nav className="landing-nav">
        <div className="landing-nav__inner">
          <div className="landing-nav__logo">
            <Zap size={20} fill="currentColor" />
            SmartHire AI
          </div>
          <div className="landing-nav__links">
            <a href="#features" className="landing-nav__link">Özellikler</a>
            <a href="#how" className="landing-nav__link">Nasıl çalışır</a>
            <a href="#testimonials" className="landing-nav__link">Yorumlar</a>
          </div>
          <div className="landing-nav__actions">
            <Button variant="ghost" size="sm" onClick={() => navigate('/login')}>Giriş yap</Button>
            <Button variant="primary" size="sm" onClick={() => navigate('/register')}>Ücretsiz başla</Button>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="landing-hero">
        <div className="landing-hero__inner">
          <Badge variant="primary" className="landing-hero__tag">
            <Zap size={11} fill="currentColor" /> AI Destekli Mülakat Koçu
          </Badge>
          <h1 className="landing-hero__title">
            Hayalindeki işe<br />
            <span className="landing-hero__title-grad">AI ile hazırlan</span>
          </h1>
          <p className="landing-hero__desc">
            CV'ni analiz et, pozisyona özel mülakat soruları al, anlık geri bildirimle gelişim planını oluştur.
            Türkiye'nin ilk AI mülakat koçu ile rakiplerinden bir adım önde ol.
          </p>
          <div className="landing-hero__ctas">
            <Button
              variant="primary"
              size="lg"
              onClick={() => navigate('/register')}
              rightIcon={<ArrowRight size={16} />}
            >
              Ücretsiz dene — kredi kartı gerekmez
            </Button>
            <Button variant="ghost" size="lg" onClick={() => navigate('/login')}>
              Giriş yap
            </Button>
          </div>
          <div className="landing-hero__stats">
            <div className="landing-hero__stat">
              <span className="landing-hero__stat-num">12.000+</span>
              <span className="landing-hero__stat-label">Aktif kullanıcı</span>
            </div>
            <div className="landing-hero__divider" />
            <div className="landing-hero__stat">
              <span className="landing-hero__stat-num">%87</span>
              <span className="landing-hero__stat-label">İş bulma başarı oranı</span>
            </div>
            <div className="landing-hero__divider" />
            <div className="landing-hero__stat">
              <span className="landing-hero__stat-num">50+</span>
              <span className="landing-hero__stat-label">Desteklenen rol</span>
            </div>
          </div>
        </div>

        {/* Hero visual */}
        <div className="landing-hero__visual">
          <div className="hero-card">
            <div className="hero-card__header">
              <div className="hero-card__avatar">SÖ</div>
              <div>
                <p className="hero-card__name">Senan Öztürk</p>
                <p className="hero-card__role">Frontend Developer Adayı</p>
              </div>
              <Badge variant="success" size="sm" className="hero-card__badge">Canlı</Badge>
            </div>
            <div className="hero-card__score-row">
              <p className="hero-card__score-label">Hazırlık Skoru</p>
              <p className="hero-card__score-value">72%</p>
            </div>
            <div className="hero-card__progress">
              <div className="hero-card__progress-fill" />
            </div>
            <div className="hero-card__question">
              <p className="hero-card__q-label">AI Soru</p>
              <p className="hero-card__q-text">React'te virtual DOM nasıl çalışır ve performansa katkısı nedir?</p>
            </div>
            <div className="hero-card__bars">
              {[
                { label: 'React', w: 88 },
                { label: 'Sistem Tasarımı', w: 45 },
                { label: 'Algoritmalar', w: 67 },
              ].map(b => (
                <div key={b.label} className="hero-card__bar-row">
                  <span className="hero-card__bar-label">{b.label}</span>
                  <div className="hero-card__bar-track">
                    <div className="hero-card__bar-fill" style={{ width: `${b.w}%` }} />
                  </div>
                  <span className="hero-card__bar-val">{b.w}%</span>
                </div>
              ))}
            </div>
          </div>

          {/* Floating badges */}
          <div className="landing-float landing-float--tl">
            <CheckCircle size={14} /> Sistem tasarımı zayıf
          </div>
          <div className="landing-float landing-float--br">
            <Zap size={14} fill="currentColor" /> Anlık geri bildirim
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="landing-section">
        <div className="landing-section__inner">
          <div className="landing-section__head">
            <Badge variant="primary">Özellikler</Badge>
            <h2 className="landing-section__title">Mülakat hazırlığında ihtiyacın olan her şey</h2>
            <p className="landing-section__subtitle">
              CV analizinden kişisel gelişim planına kadar tüm süreç tek platformda.
            </p>
          </div>
          <div className="feature-grid">
            {FEATURES.map(f => (
              <div key={f.id} className={`feature-card feature-card--${f.color}`}>
                <div className="feature-card__icon">{f.icon}</div>
                <h3 className="feature-card__title">{f.title}</h3>
                <p className="feature-card__desc">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How it works */}
      <section id="how" className="landing-section landing-section--alt">
        <div className="landing-section__inner">
          <div className="landing-section__head">
            <Badge variant="primary">Nasıl çalışır</Badge>
            <h2 className="landing-section__title">3 adımda mülakatlara hazır ol</h2>
            <p className="landing-section__subtitle">Kayıt olduktan sonra 5 dakika içinde ilk mülakatına girebilirsin.</p>
          </div>
          <div className="steps">
            {STEPS.map((s, i) => (
              <div key={s.num} className="step">
                <div className="step__num">{s.num}</div>
                <div className="step__body">
                  <h3 className="step__title">{s.title}</h3>
                  <p className="step__desc">{s.desc}</p>
                </div>
                {i < STEPS.length - 1 && <ChevronRight size={20} className="step__arrow" />}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section id="testimonials" className="landing-section">
        <div className="landing-section__inner">
          <div className="landing-section__head">
            <Badge variant="primary">Yorumlar</Badge>
            <h2 className="landing-section__title">Kullanıcılarımız ne diyor</h2>
          </div>
          <div className="testimonial-grid">
            {TESTIMONIALS.map(t => (
              <div key={t.id} className="testimonial-card">
                <div className="testimonial-card__stars">
                  {Array.from({ length: t.stars }).map((_, i) => (
                    <Star key={i} size={14} fill="currentColor" />
                  ))}
                </div>
                <p className="testimonial-card__text">"{t.text}"</p>
                <div className="testimonial-card__author">
                  <div className="testimonial-card__avatar">{t.name.charAt(0)}</div>
                  <div>
                    <p className="testimonial-card__name">{t.name}</p>
                    <p className="testimonial-card__role">{t.role}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Banner */}
      <section className="landing-cta">
        <div className="landing-cta__inner">
          <h2 className="landing-cta__title">Hayalindeki işe bir adım daha yakın ol</h2>
          <p className="landing-cta__desc">Ücretsiz hesap oluştur, ilk mülakatını hemen başlat.</p>
          <Button
            variant="primary"
            size="lg"
            onClick={() => navigate('/register')}
            rightIcon={<ArrowRight size={16} />}
          >
            Ücretsiz başla
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        <div className="landing-footer__inner">
          <div className="landing-footer__logo">
            <Zap size={16} fill="currentColor" />
            SmartHire AI
          </div>
          <p className="landing-footer__copy">© 2024 SmartHire AI. TÜBİTAK 2209-A Destekli Proje.</p>
          <div className="landing-footer__links">
            <a href="#" className="landing-footer__link">Gizlilik</a>
            <a href="#" className="landing-footer__link">Kullanım Koşulları</a>
            <a href="#" className="landing-footer__link">İletişim</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
