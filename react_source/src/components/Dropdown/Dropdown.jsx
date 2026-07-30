import { useState, useRef, useEffect } from 'react';
import './Dropdown.css';

/**
 * Dropdown
 * trigger  — ReactNode (trigger element)
 * items    — Array<{ label, icon?, onClick?, href?, danger?, divider? }>
 * align    — 'left' | 'right'
 */
export default function Dropdown({ trigger, items = [], align = 'left' }) {
  const [open, setOpen] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    const handler = (e) => {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false);
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  return (
    <div className="dropdown" ref={ref}>
      <div onClick={() => setOpen((v) => !v)} style={{ cursor: 'pointer' }}>
        {trigger}
      </div>

      {open && (
        <div
          className={`dropdown__menu${align === 'right' ? ' dropdown__menu--right' : ''}`}
          role="menu"
        >
          {items.map((item, i) => {
            if (item.divider) return <div key={i} className="dropdown__divider" aria-hidden="true" />;
            return (
              <button
                key={i}
                className={`dropdown__item${item.danger ? ' dropdown__item--danger' : ''}`}
                role="menuitem"
                onClick={() => { item.onClick?.(); setOpen(false); }}
              >
                {item.icon && <span aria-hidden="true">{item.icon}</span>}
                {item.label}
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
}
