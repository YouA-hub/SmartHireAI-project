import { useState } from 'react';
import { User, Mail, Phone, Briefcase, Save, Camera } from 'lucide-react';
import Button from '../../components/Button/Button';
import Input from '../../components/Input/Input';
import Textarea from '../../components/Textarea/Textarea';
import Avatar from '../../components/Avatar/Avatar';
import Card from '../../components/Card/Card';
import Breadcrumb from '../../components/Breadcrumb/Breadcrumb';
import { useToast } from '../../components/Toast/Toast';
import './Profile.css';

export default function Profile() {
  const toast = useToast();
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({
    name: 'Senan Öztürk',
    email: 'senan@ornek.com',
    phone: '+90 555 123 4567',
    title: 'Frontend Developer',
    bio: 'React ve TypeScript konusunda tutkulu bir yazılım geliştirici. Kullanıcı deneyimine odaklanan ürünler geliştirmeyi seviyorum.',
    linkedin: 'linkedin.com/in/senan',
    github: 'github.com/senan',
    targetRole: 'Senior Frontend Developer',
    experience: '3 yıl',
  });

  const handleChange = (key) => (e) => {
    setForm(prev => ({ ...prev, [key]: e.target.value }));
  };

  const handleSave = async () => {
    setLoading(true);
    await new Promise(r => setTimeout(r, 900));
    setLoading(false);
    toast.success('Profil güncellendi', 'Değişiklikler kaydedildi.');
  };

  return (
    <div className="profile">
      <Breadcrumb items={[{ label: 'Dashboard', to: '/dashboard' }, { label: 'Profil' }]} />

      <div className="page-header">
        <div className="page-header__left">
          <h1 className="page-header__title">Profil Bilgileri</h1>
          <p className="page-header__subtitle">Kişisel bilgilerinizi güncelleyin</p>
        </div>
        <div className="page-header__actions">
          <Button variant="primary" leftIcon={<Save size={15} />} loading={loading} onClick={handleSave}>
            {loading ? 'Kaydediliyor…' : 'Kaydet'}
          </Button>
        </div>
      </div>

      <div className="profile__layout">
        {/* Avatar card */}
        <Card className="profile__avatar-card">
          <div className="profile__avatar-section">
            <div className="profile__avatar-wrap">
              <Avatar size="xl" name={form.name} />
              <button className="profile__avatar-edit" aria-label="Fotoğraf değiştir">
                <Camera size={14} />
              </button>
            </div>
            <div className="profile__avatar-info">
              <p className="profile__name">{form.name}</p>
              <p className="profile__title">{form.title}</p>
            </div>
          </div>

          <div className="profile__stats">
            <div className="profile__stat">
              <span className="profile__stat-num">5</span>
              <span className="profile__stat-label">Mülakat</span>
            </div>
            <div className="profile__stat-div" />
            <div className="profile__stat">
              <span className="profile__stat-num">72%</span>
              <span className="profile__stat-label">Ort. Skor</span>
            </div>
            <div className="profile__stat-div" />
            <div className="profile__stat">
              <span className="profile__stat-num">+4</span>
              <span className="profile__stat-label">Son artış</span>
            </div>
          </div>
        </Card>

        {/* Form */}
        <div className="profile__form-area">
          {/* Personal */}
          <Card>
            <Card.Header title="Kişisel Bilgiler" />
            <div className="profile__form-grid">
              <Input id="profile-name" label="Ad Soyad" value={form.name} onChange={handleChange('name')} leftIcon={<User size={15} />} />
              <Input id="profile-email" label="E-posta" type="email" value={form.email} onChange={handleChange('email')} leftIcon={<Mail size={15} />} />
              <Input id="profile-phone" label="Telefon" value={form.phone} onChange={handleChange('phone')} leftIcon={<Phone size={15} />} />
              <Input id="profile-title" label="Unvan" value={form.title} onChange={handleChange('title')} leftIcon={<Briefcase size={15} />} />
            </div>
            <Textarea
              id="profile-bio"
              label="Hakkımda"
              value={form.bio}
              onChange={handleChange('bio')}
              rows={3}
              className="profile__bio"
            />
          </Card>

          {/* Career */}
          <Card>
            <Card.Header title="Kariyer Hedefleri" />
            <div className="profile__form-grid">
              <Input id="profile-target" label="Hedef pozisyon" value={form.targetRole} onChange={handleChange('targetRole')} leftIcon={<Briefcase size={15} />} />
              <Input id="profile-exp" label="Deneyim süresi" value={form.experience} onChange={handleChange('experience')} />
              <Input id="profile-linkedin" label="LinkedIn" value={form.linkedin} onChange={handleChange('linkedin')} />
              <Input id="profile-github" label="GitHub" value={form.github} onChange={handleChange('github')} />
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
