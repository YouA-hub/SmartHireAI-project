import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Menu, X, Zap } from 'lucide-react';
import Sidebar from '../Sidebar/Sidebar';
import './Navbar.css';

/**
 * Navbar — SmartHire AI Component Library
 * Sadece mobilde görünür (≤640px).
 * Desktop'ta Sidebar navigasyonu üstlenir.
 *
 * Props:
 *   user — { name, role, avatarSrc }
 */
export default function Navbar({ user = {} }) {
  const [drawerOpen, setDrawerOpen] = useState(false);

  const openDrawer  = () => setDrawerOpen(true);
  const closeDrawer = () => setDrawerOpen(false);

  return (
    <>
      <header className="navbar">
        <Link to="/dashboard" className="navbar__logo" aria-label="SmartHire AI">
          <div className="navbar__logo-icon" aria-hidden="true">
            <Zap size={16} />
          </div>
          <span className="navbar__logo-text">SmartHire AI</span>
        </Link>

        <button
          className="navbar__hamburger"
          onClick={openDrawer}
          aria-label="Menüyü aç"
          aria-expanded={drawerOpen}
        >
          <Menu size={20} aria-hidden="true" />
        </button>
      </header>

      {/* Mobile drawer overlay */}
      <div
        className={`navbar-drawer-overlay${drawerOpen ? ' navbar-drawer-overlay--open' : ''}`}
        onClick={closeDrawer}
        aria-hidden="true"
      />

      {/* Mobile drawer */}
      <nav
        className={`navbar-drawer${drawerOpen ? ' navbar-drawer--open' : ''}`}
        aria-label="Mobil menü"
        aria-hidden={!drawerOpen}
      >
        <div style={{ display: 'flex', justifyContent: 'flex-end', padding: 'var(--space-2)' }}>
          <button
            onClick={closeDrawer}
            aria-label="Menüyü kapat"
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              width: 36,
              height: 36,
              border: 'none',
              background: 'transparent',
              cursor: 'pointer',
              borderRadius: 'var(--radius-sm)',
              color: 'var(--color-muted)',
            }}
          >
            <X size={20} aria-hidden="true" />
          </button>
        </div>
        {/* Sidebar'ı drawer içinde kullanıyoruz */}
        <Sidebar user={user} />
      </nav>
    </>
  );
}
