import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  CheckCircle,
  AlertTriangle,
  User,
  Briefcase,
  GraduationCap,
  Code,
  ChevronRight,
} from 'lucide-react';
import Button from '../../components/Button/Button';
import Input from '../../components/Input/Input';
import Textarea from '../../components/Textarea/Textarea';
import Badge from '../../components/Badge/Badge';
import { useToast } from '../../components/Toast/Toast';
import './CVConfirm.css';

/* Mock AI extracted data */
const INITIAL_DATA = {
  name: 'Senan Öztürk',
  email: 'senan@ornek.com',
  phone: '+90 555 123 4567',
  position: 'Frontend Developer',
  experience: '3 yıl deneyim — React, TypeScript, Next.js geliştirme',
  education: 'Bilgisayar Mühendisliği — İstanbul Teknik Üniversitesi, 2021',
  skills: 'React, TypeScript, Next.js, Tailwind CSS, GraphQL, Git',
  summary: '', // Boş alan — amber uyarısı gösterilecek
  linkedin: '',  // Boş alan — amber uyarısı
};

const FIELDS = [
  { key: 'name', label: 'Ad Soyad', icon: <User size={14} />, required: true, type: 'input' },
  { key: 'email', label: 'E-posta', icon: <User size={14} />, required: true, type: 'input' },
  { key: 'phone', label: 'Telefon', icon: <User size={14} />, required: false, type: 'input' },
  { key: 'position', label: 'Hedef pozisyon', icon: <Briefcase size={14} />, required: true, type: 'input' },
  { key: 'experience', label: 'Deneyim özeti', icon: <Briefcase size={14} />, required: true, type: 'textarea' },
  { key: 'education', label: 'Eğitim', icon: <GraduationCap size={14} />, required: true, type: 'input' },
  { key: 'skills', label: 'Teknik beceriler', icon: <Code size={14} />, required: true, type: 'input' },
  { key: 'summary', label: 'Profesyonel özet', icon: <User size={14} />, required: false, type: 'textarea' },
  { key: 'linkedin', label: 'LinkedIn profil linki', icon: <User size={14} />, required: false, type: 'input' },
];

export default function CVConfirm() {
  const navigate = useNavigate();
  const toast = useToast();
  const [data, setData] = useState(INITIAL_DATA);
  const [loading, setLoading] = useState(false);

  const isEmpty = (val) => !val || val.trim() === '';

  const emptyCount = FIELDS.filter(f => isEmpty(data[f.key])).length;
  const missingRequired = FIELDS.filter(f => f.required && isEmpty(data[f.key]));

  const handleChange = (key) => (e) => {
    setData(prev => ({ ...prev, [key]: e.target.value }));
  };

  const handleConfirm = async () => {
    if (missingRequired.length > 0) {
      toast.warning('Eksik zorunlu alan', `Lütfen ${missingRequired[0].label} alanını doldurun.`);
      return;
    }
    setLoading(true);
    await new Promise(r => setTimeout(r, 900));
    setLoading(false);
    toast.success('Onaylandı!', 'Mülakat hazır. İyi şanslar!');
    setTimeout(() => navigate('/interview'), 700);
  };

  return (
    <div className="cv-confirm">
      {/* Header — logo FullscreenLayout navbar'da zaten var, tekrar koyma */}
      <div className="cv-confirm__header">
        <div className="cv-confirm__header-title">
          <h2 className="cv-confirm__header-h">CV Onayı</h2>
          <p className="cv-confirm__header-sub">AI'ın çıkardığı bilgileri kontrol edip düzenleyin</p>
        </div>
      </div>

      <div className="cv-confirm__layout">
        {/* Sidebar summary */}
        <aside className="cv-confirm__aside">
          <div className="cv-confirm__aside-card">
            <div className="cv-confirm__aside-icon">
              <CheckCircle size={20} />
            </div>
            <p className="cv-confirm__aside-title">Analiz tamamlandı</p>
            <p className="cv-confirm__aside-sub">CV'niz ve iş ilanı başarıyla işlendi.</p>
          </div>

          {emptyCount > 0 && (
            <div className="cv-confirm__aside-card cv-confirm__aside-card--warn">
              <div className="cv-confirm__aside-icon cv-confirm__aside-icon--warn">
                <AlertTriangle size={20} />
              </div>
              <p className="cv-confirm__aside-title">{emptyCount} eksik alan</p>
              <p className="cv-confirm__aside-sub">Amber renkli alanlar CV'nizde bulunamadı. Dilerseniz tamamlayabilirsiniz.</p>
            </div>
          )}

          <div className="cv-confirm__match">
            <p className="cv-confirm__match-label">İlan uyum skoru</p>
            <p className="cv-confirm__match-value">81%</p>
            <div className="cv-confirm__match-bar">
              <div className="cv-confirm__match-fill" style={{ width: '81%' }} />
            </div>
            <p className="cv-confirm__match-note">React Developer pozisyonu ile</p>
          </div>
        </aside>

        {/* Form */}
        <div className="cv-confirm__form-area">
          <div className="cv-confirm__form">
            {FIELDS.map(f => {
              const val = data[f.key];
              const missing = isEmpty(val);
              const state = missing ? 'warning' : 'default';

              return (
                <div key={f.key} className="cv-confirm__field">
                  <div className="cv-confirm__field-header">
                    <span className="cv-confirm__field-label">
                      {f.icon}
                      {f.label}
                    </span>
                    {missing ? (
                      <Badge variant="warning" size="sm">Eksik</Badge>
                    ) : (
                      <Badge variant="success" size="sm">
                        <CheckCircle size={10} />
                        Dolu
                      </Badge>
                    )}
                  </div>
                  {f.type === 'textarea' ? (
                    <Textarea
                      id={`cvconfirm-${f.key}`}
                      placeholder={`${f.label} girin…`}
                      value={val}
                      onChange={handleChange(f.key)}
                      state={state}
                      rows={3}
                    />
                  ) : (
                    <Input
                      id={`cvconfirm-${f.key}`}
                      placeholder={`${f.label} girin…`}
                      value={val}
                      onChange={handleChange(f.key)}
                      state={state}
                    />
                  )}
                </div>
              );
            })}
          </div>

          <div className="cv-confirm__actions">
            <Button variant="ghost" onClick={() => navigate('/onboarding')}>
              Geri dön
            </Button>
            <Button
              variant="primary"
              onClick={handleConfirm}
              loading={loading}
              rightIcon={!loading && <ChevronRight size={16} />}
            >
              {loading ? 'Onaylanıyor…' : 'Onayla ve mülakata geç'}
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
