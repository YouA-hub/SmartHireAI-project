import { useState } from 'react';
import { Save, Bell, User, Shield, Trash2, AlertTriangle } from 'lucide-react';
import Button from '../../components/Button/Button';
import Input from '../../components/Input/Input';
import Card from '../../components/Card/Card';
import Tabs from '../../components/Tabs/Tabs';
import Modal from '../../components/Modal/Modal';
import Breadcrumb from '../../components/Breadcrumb/Breadcrumb';
import { useToast } from '../../components/Toast/Toast';
import './Settings.css';

/* ---- Tab: Profil ---- */
function ProfileTab() {
  const toast = useToast();
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({ name: 'Senan Öztürk', email: 'senan@ornek.com', language: 'Türkçe' });

  const handleSave = async () => {
    setLoading(true);
    await new Promise(r => setTimeout(r, 800));
    setLoading(false);
    toast.success('Ayarlar kaydedildi');
  };

  return (
    <div className="settings-tab">
      <Card>
        <Card.Header title="Genel Ayarlar" />
        <div className="settings-form">
          <Input id="settings-name" label="Ad Soyad" value={form.name} onChange={e => setForm(p => ({ ...p, name: e.target.value }))} leftIcon={<User size={15} />} />
          <Input id="settings-email" label="E-posta" type="email" value={form.email} onChange={e => setForm(p => ({ ...p, email: e.target.value }))} />
          <div className="settings-field">
            <label className="settings-label">Dil</label>
            <select className="settings-select" value={form.language} onChange={e => setForm(p => ({ ...p, language: e.target.value }))}>
              <option>Türkçe</option>
              <option>English</option>
            </select>
          </div>
        </div>
        <Button variant="primary" leftIcon={<Save size={15} />} loading={loading} onClick={handleSave}>
          {loading ? 'Kaydediliyor…' : 'Kaydet'}
        </Button>
      </Card>

      <Card>
        <Card.Header title="Şifre Değiştir" />
        <div className="settings-form">
          <Input id="settings-pw-current" label="Mevcut şifre" type="password" placeholder="••••••••" />
          <Input id="settings-pw-new" label="Yeni şifre" type="password" placeholder="En az 8 karakter" />
          <Input id="settings-pw-confirm" label="Şifreyi onayla" type="password" placeholder="••••••••" />
        </div>
        <Button variant="secondary">Şifreyi güncelle</Button>
      </Card>
    </div>
  );
}

/* ---- Tab: Bildirimler ---- */
function NotificationsTab() {
  const toast = useToast();
  const [notifs, setNotifs] = useState({
    email_reminders: true,
    email_reports: true,
    email_tips: false,
    push_new_q: true,
    push_score: false,
  });

  const toggle = (key) => setNotifs(prev => ({ ...prev, [key]: !prev[key] }));

  const NOTIF_ITEMS = [
    { key: 'email_reminders', label: 'E-posta hatırlatıcılar', sub: 'Haftalık pratik mülakat hatırlatması', group: 'E-posta' },
    { key: 'email_reports', label: 'Mülakat raporları', sub: 'Mülakat tamamlandığında detaylı rapor', group: 'E-posta' },
    { key: 'email_tips', label: 'Gelişim ipuçları', sub: 'AI destekli kişisel öğrenme ipuçları', group: 'E-posta' },
    { key: 'push_new_q', label: 'Yeni sorular', sub: 'Pozisyonuna özel yeni sorular eklendiğinde', group: 'Uygulama içi' },
    { key: 'push_score', label: 'Skor güncellemeleri', sub: 'Hazırlık skorun değiştiğinde bildirim al', group: 'Uygulama içi' },
  ];

  const groups = [...new Set(NOTIF_ITEMS.map(n => n.group))];

  return (
    <div className="settings-tab">
      {groups.map(g => (
        <Card key={g}>
          <Card.Header title={g} />
          <div className="notif-list">
            {NOTIF_ITEMS.filter(n => n.group === g).map(n => (
              <div key={n.key} className="notif-item">
                <div className="notif-item__text">
                  <p className="notif-item__label">{n.label}</p>
                  <p className="notif-item__sub">{n.sub}</p>
                </div>
                <button
                  className={`toggle ${notifs[n.key] ? 'toggle--on' : ''}`}
                  onClick={() => toggle(n.key)}
                  role="switch"
                  aria-checked={notifs[n.key]}
                  id={`notif-${n.key}`}
                >
                  <span className="toggle__thumb" />
                </button>
              </div>
            ))}
          </div>
        </Card>
      ))}
      <Button variant="primary" leftIcon={<Save size={15} />} onClick={() => toast.success('Bildirim ayarları kaydedildi')}>Kaydet</Button>
    </div>
  );
}

/* ---- Tab: Hesap ---- */
function AccountTab() {
  const [deleteModal, setDeleteModal] = useState(false);
  const toast = useToast();

  return (
    <div className="settings-tab">
      <Card>
        <Card.Header title="Veri Yönetimi" />
        <div className="account-items">
          <div className="account-item">
            <div>
              <p className="account-item__label">Tüm mülakat verilerini indir</p>
              <p className="account-item__sub">Tüm mülakat geçmişinizi ve raporlarınızı JSON formatında indirin.</p>
            </div>
            <Button variant="secondary" size="sm" onClick={() => toast.info('Hazırlanıyor', 'Verileriniz hazırlanıyor…')}>
              İndir
            </Button>
          </div>
          <div className="account-item">
            <div>
              <p className="account-item__label">Mülakat geçmişini temizle</p>
              <p className="account-item__sub">Tüm mülakat verilerinizi kalıcı olarak silin.</p>
            </div>
            <Button variant="ghost" size="sm" onClick={() => toast.warning('Yakında', 'Bu özellik çok yakında gelecek.')}>
              Temizle
            </Button>
          </div>
        </div>
      </Card>

      <Card className="settings__danger-card">
        <Card.Header title="Tehlikeli Bölge" />
        <div className="danger-zone">
          <div>
            <p className="danger-zone__label">Hesabı kalıcı olarak sil</p>
            <p className="danger-zone__sub">Bu işlem geri alınamaz. Tüm verileriniz kalıcı olarak silinir.</p>
          </div>
          <Button variant="danger" leftIcon={<Trash2 size={16} />} onClick={() => setDeleteModal(true)}>
            Hesabı sil
          </Button>
        </div>
      </Card>

      <Modal
        isOpen={deleteModal}
        onClose={() => setDeleteModal(false)}
        title="Hesabı Sil"
        description="Bu işlem geri alınamaz. Tüm mülakat geçmişiniz, raporlarınız ve kişisel verileriniz kalıcı olarak silinecektir."
        icon={<AlertTriangle size={24} />}
        iconVariant="danger"
        confirmLabel="Evet, hesabı sil"
        confirmVariant="danger"
        onConfirm={() => {
          setDeleteModal(false);
          toast.danger('Hesap silme', 'Gerçek uygulamada hesap silinirdi.');
        }}
      />
    </div>
  );
}

export default function Settings() {
  const TABS = [
    { id: 'profile', label: 'Profil', icon: <User size={15} />, content: <ProfileTab /> },
    { id: 'notifications', label: 'Bildirimler', icon: <Bell size={15} />, content: <NotificationsTab /> },
    { id: 'account', label: 'Hesap', icon: <Shield size={15} />, content: <AccountTab /> },
  ];

  return (
    <div className="settings">
      <Breadcrumb items={[{ label: 'Dashboard', to: '/dashboard' }, { label: 'Ayarlar' }]} />

      <div className="page-header">
        <div className="page-header__left">
          <h1 className="page-header__title">Ayarlar</h1>
          <p className="page-header__subtitle">Hesap ve uygulama tercihlerinizi yönetin</p>
        </div>
      </div>

      <Tabs tabs={TABS} defaultTab="profile" />
    </div>
  );
}
