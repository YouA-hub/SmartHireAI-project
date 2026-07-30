import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Zap, Mail, Lock, User, Eye, EyeOff, ArrowRight } from 'lucide-react';
import Button from '../../components/Button/Button';
import Input from '../../components/Input/Input';
import { useToast } from '../../components/Toast/Toast';
import './Auth.css';

export default function Register() {
  const navigate = useNavigate();
  const toast = useToast();

  const [form, setForm] = useState({ name: '', email: '', password: '' });
  const [showPw, setShowPw] = useState(false);
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  const validate = () => {
    const errs = {};
    if (!form.name.trim()) errs.name = 'Ad Soyad zorunludur';
    if (!form.email.includes('@')) errs.email = 'Geçerli bir e-posta girin';
    if (form.password.length < 8) errs.password = 'En az 8 karakter olmalı';
    return errs;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const errs = validate();
    if (Object.keys(errs).length) { setErrors(errs); return; }
    setLoading(true);
    // Simulate API call
    await new Promise(r => setTimeout(r, 1200));
    setLoading(false);
    toast.success('Hesap oluşturuldu!', 'Onboarding sürecine yönlendiriliyorsunuz.');
    setTimeout(() => navigate('/onboarding'), 800);
  };

  const handleChange = (field) => (e) => {
    setForm(prev => ({ ...prev, [field]: e.target.value }));
    if (errors[field]) setErrors(prev => ({ ...prev, [field]: undefined }));
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        {/* Logo */}
        <div className="auth-card__logo">
          <Zap size={20} fill="currentColor" />
          SmartHire AI
        </div>

        <div className="auth-card__head">
          <h1 className="auth-card__title">Hesap oluştur</h1>
          <p className="auth-card__subtitle">Ücretsiz başla — kredi kartı gerekmez</p>
        </div>

        <form className="auth-card__form" onSubmit={handleSubmit} noValidate>
          <Input
            id="register-name"
            label="Ad Soyad"
            placeholder="Senan Öztürk"
            value={form.name}
            onChange={handleChange('name')}
            error={errors.name}
            leftIcon={<User size={16} />}
          />
          <Input
            id="register-email"
            type="email"
            label="E-posta"
            placeholder="sen@ornek.com"
            value={form.email}
            onChange={handleChange('email')}
            error={errors.email}
            leftIcon={<Mail size={16} />}
          />
          <Input
            id="register-password"
            type={showPw ? 'text' : 'password'}
            label="Şifre"
            placeholder="En az 8 karakter"
            value={form.password}
            onChange={handleChange('password')}
            error={errors.password}
            leftIcon={<Lock size={16} />}
            rightIcon={
              <button
                type="button"
                className="auth-card__pw-toggle"
                onClick={() => setShowPw(v => !v)}
                aria-label={showPw ? 'Şifreyi gizle' : 'Şifreyi göster'}
              >
                {showPw ? <EyeOff size={16} /> : <Eye size={16} />}
              </button>
            }
          />

          <Button
            type="submit"
            variant="primary"
            fullWidth
            loading={loading}
            rightIcon={!loading && <ArrowRight size={16} />}
          >
            {loading ? 'Hesap oluşturuluyor…' : 'Hesap oluştur'}
          </Button>
        </form>

        <div className="auth-card__divider"><span>veya</span></div>

        <p className="auth-card__footer">
          Zaten hesabın var mı?{' '}
          <Link to="/login" className="auth-card__link">Giriş yap</Link>
        </p>

        <p className="auth-card__terms">
          Devam ederek{' '}
          <a href="#" className="auth-card__link">Kullanım Koşulları</a>
          {' '}ve{' '}
          <a href="#" className="auth-card__link">Gizlilik Politikası</a>'nı
          kabul etmiş olursunuz.
        </p>
      </div>

      {/* Background decoration */}
      <div className="auth-bg">
        <div className="auth-bg__orb auth-bg__orb--1" />
        <div className="auth-bg__orb auth-bg__orb--2" />
      </div>
    </div>
  );
}
