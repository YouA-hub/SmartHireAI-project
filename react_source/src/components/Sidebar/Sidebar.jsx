import { NavLink, Link } from 'react-router-dom';
import {
  LayoutDashboard,
  MessageSquare,
  History,
  Settings,
  ChevronLeft,
  ChevronRight,
  Zap,
} from 'lucide-react';
import Avatar from '../Avatar/Avatar';
import './Sidebar.css';

/**
 * Sidebar — SmartHire AI Component Library
 *
 * Props:
 *   user             — { name, role, avatarSrc }
 *   collapsed        — boolean (controlled)
 *   onToggle         — () => void
 *   onInterviewClick — (e) => void  — "Mülakat" linkine tıklanınca modal aç
 */
export default function Sidebar({ user = {}, collapsed = false, onToggle, onInterviewClick }) {
  const NAV_ITEMS = [
    { to: '/dashboard', icon: <LayoutDashboard size={20} />, label: 'Dashboard' },
    {
      to: '/interview',
      icon: <MessageSquare size={20} />,
      label: 'Mülakat',
      // Modal açıyoruz, direkt navigasyon değil
      onClick: onInterviewClick,
    },
    { to: '/history',  icon: <History size={20} />,  label: 'Geçmiş' },
    { to: '/settings', icon: <Settings size={20} />, label: 'Ayarlar' },
  ];

  return (
    <aside className={`sidebar${collapsed ? ' sidebar--collapsed' : ''}`}>
      {/* Logo */}
      <Link to="/dashboard" className="sidebar__logo" aria-label="SmartHire AI Ana Sayfa">
        <div className="sidebar__logo-icon" aria-hidden="true">
          <Zap size={18} />
        </div>
        <span className="sidebar__logo-text">SmartHire AI</span>
      </Link>

      {/* Navigation */}
      <nav className="sidebar__nav" aria-label="Ana menü">
        {NAV_ITEMS.map(({ to, icon, label, onClick }) => (
          <NavLink
            key={to}
            to={to}
            onClick={onClick}   // modal açanlar için preventDefault içinde yapılıyor
            className={({ isActive }) =>
              `sidebar__nav-item${isActive ? ' sidebar__nav-item--active' : ''}`
            }
            aria-label={collapsed ? label : undefined}
            title={collapsed ? label : undefined}
          >
            <span className="sidebar__nav-icon" aria-hidden="true">{icon}</span>
            <span className="sidebar__nav-label">{label}</span>
          </NavLink>
        ))}
      </nav>

      {/* Collapse toggle */}
      {onToggle && (
        <div className="sidebar__toggle-row">
          <button
            className="sidebar__toggle"
            onClick={onToggle}
            aria-label={collapsed ? "Sidebar'ı genişlet" : "Sidebar'ı daralt"}
          >
            {collapsed
              ? <ChevronRight size={16} aria-hidden="true" />
              : <ChevronLeft  size={16} aria-hidden="true" />
            }
          </button>
        </div>
      )}

      {/* User profile */}
      <Link
        to="/profile"
        className="sidebar__user"
        aria-label={`Profil: ${user.name || 'Kullanıcı'}`}
      >
        <Avatar
          src={user.avatarSrc}
          name={user.name || 'Kullanıcı'}
          size="md"
        />
        <div className="sidebar__user-info">
          <p className="sidebar__user-name">{user.name || 'Kullanıcı'}</p>
          <p className="sidebar__user-role">{user.role || 'Aday'}</p>
        </div>
      </Link>
    </aside>
  );
}
