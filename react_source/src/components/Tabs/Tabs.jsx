import { useState } from 'react';
import './Tabs.css';

/**
 * Tabs — SmartHire AI Component Library
 * tabs        — Array<{ id, label, icon?: ReactNode, content: ReactNode }>
 * defaultTab  — string (tab id) | number (index)
 * defaultIndex — number (legacy, fallback)
 */
export default function Tabs({ tabs = [], defaultTab, defaultIndex = 0 }) {
  const resolveDefault = () => {
    if (defaultTab !== undefined) {
      const idx = tabs.findIndex(t => t.id === defaultTab);
      return idx >= 0 ? idx : 0;
    }
    return defaultIndex;
  };

  const [active, setActive] = useState(resolveDefault);

  return (
    <div className="tabs">
      <div className="tabs__list" role="tablist">
        {tabs.map((tab, i) => (
          <button
            key={tab.id ?? i}
            id={tab.id ? `tab-${tab.id}` : undefined}
            role="tab"
            aria-selected={active === i}
            aria-controls={tab.id ? `tabpanel-${tab.id}` : undefined}
            className={`tabs__tab${active === i ? ' tabs__tab--active' : ''}`}
            onClick={() => setActive(i)}
          >
            {tab.icon && (
              <span className="tabs__tab-icon" aria-hidden="true">{tab.icon}</span>
            )}
            {tab.label}
          </button>
        ))}
      </div>
      <div
        className="tabs__content"
        role="tabpanel"
        id={tabs[active]?.id ? `tabpanel-${tabs[active].id}` : undefined}
        aria-labelledby={tabs[active]?.id ? `tab-${tabs[active].id}` : undefined}
      >
        {tabs[active]?.content}
      </div>
    </div>
  );
}
