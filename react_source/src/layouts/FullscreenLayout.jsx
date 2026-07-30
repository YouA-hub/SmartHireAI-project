import { Link, Outlet } from 'react-router-dom';
import { Zap } from 'lucide-react';
import './FullscreenLayout.css';

/**
 * FullscreenLayout — Auth / Onboarding / AI Processing ekranlar
 * Sidebar yok, merkezi hizalanmış içerik
 *
 * Props (Outlet context yoluyla değil, doğrudan kullanılır):
 *   contentAlign — 'center' | 'top'
 */
export default function FullscreenLayout({ contentAlign = 'center' }) {
  return (
    <div className="fullscreen-layout">
      <header className="fullscreen-layout__header">
        <Link to="/" className="fullscreen-layout__logo" aria-label="SmartHire AI">
          <div className="fullscreen-layout__logo-icon" aria-hidden="true">
            <Zap size={16} />
          </div>
          <span className="fullscreen-layout__logo-text">SmartHire AI</span>
        </Link>
      </header>

      <div className={`fullscreen-layout__content${contentAlign === 'top' ? ' fullscreen-layout__content--top' : ''}`}>
        <Outlet />
      </div>
    </div>
  );
}
