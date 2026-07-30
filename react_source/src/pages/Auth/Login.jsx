import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Zap, Mail, Lock, Eye, EyeOff, ArrowRight } from 'lucide-react';
import Button from '../../components/Button/Button';
import Input from '../../components/Input/Input';
import { useToast } from '../../components/Toast/Toast';
import './Auth.css';

export default function Login() {
  const navigate = useNavigate();
  const toast = useToast();

  const [form, setForm] = useState({ email: '', password: '' });
  const [showPw, setShowPw] = useState(false);
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  const validate = () => {
    const errs = {};
    if (!form.email.includes('@')) errs.email = 'Geçerli bir e-posta girin';
    if (!form.password) errs.password = 'Şifre zorunludur';
    return errs;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const errs = validate();
    if (Object.keys(errs).length) { setErrors(errs); return; }
    setLoading(true);
    await new Promise(r => setTimeout(r, 1000));
    setLoading(false);
    toast.success('Giriş başarılı!', 'Dashboard\'a yönlendiriliyorsunuz.');
    setTimeout(() => navigate('/dashboard'), 600);
  };

  const handleChange = (field) => (e) => {
    setForm(prev => ({ ...prev, [field]: e.target.value }));
    if (errors[field]) setErrors(prev => ({ ...prev, [field]: undefined }));
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-card__logo">
          <Zap size={20} fill="currentColor" />
          SmartHire AI
        </div>

        <div className="auth-card__head">
          <h1 className="auth-card__title">Tekrar hoş geldin</h1>
          <p className="auth-card__subtitle">Hesabına giriş yap ve devam et</p>
        </div>

        <form className="auth-card__form" onSubmit={handleSubmit} noValidate>
          <Input
            id="login-email"
            type="email"
            label="E-posta"
            placeholder="sen@ornek.com"
            value={form.email}
            onChange={handleChange('email')}
            error={errors.email}
            leftIcon={<Mail size={16} />}
          />
          <Input
            id="login-password"
            type={showPw ? 'text' : 'password'}
            label="Şifre"
            placeholder="••••••••"
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

          <div className="auth-card__forgot">
            <a href="#" className="auth-card__link">Şifremi unuttum</a>
          </div>

          <Button
            type="submit"
            variant="primary"
            fullWidth
            loading={loading}
            rightIcon={!loading && <ArrowRight size={16} />}
          >
            {loading ? 'Giriş yapılıyor…' : 'Giriş yap'}
          </Button>
        </form>

        <div className="auth-card__divider"><span>veya</span></div>

        <p className="auth-card__footer">
          Hesabın yok mu?{' '}
          <Link to="/register" className="auth-card__link">Ücretsiz kaydol</Link>
        </p>
      </div>

      <div className="auth-bg">
        <div className="auth-bg__orb auth-bg__orb--1" />
        <div className="auth-bg__orb auth-bg__orb--2" />
      </div>
    </div>
  );
}
