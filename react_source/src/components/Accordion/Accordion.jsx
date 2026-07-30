import { useState } from 'react';
import { ChevronDown } from 'lucide-react';
import './Accordion.css';

/**
 * Accordion
 * items — Array<{ title, content: ReactNode }>
 * allowMultiple — boolean
 */
export default function Accordion({ items = [], allowMultiple = false }) {
  const [openItems, setOpenItems] = useState(new Set());

  const toggle = (i) => {
    setOpenItems((prev) => {
      const next = new Set(allowMultiple ? prev : []);
      if (prev.has(i)) next.delete(i);
      else next.add(i);
      return next;
    });
  };

  return (
    <div className="accordion">
      {items.map((item, i) => {
        const isOpen = openItems.has(i);
        return (
          <div
            key={i}
            className={`accordion__item${isOpen ? ' accordion__item--open' : ''}`}
          >
            <button
              className="accordion__trigger"
              onClick={() => toggle(i)}
              aria-expanded={isOpen}
            >
              <span className="accordion__trigger-label">{item.title}</span>
              <ChevronDown size={16} className="accordion__chevron" aria-hidden="true" />
            </button>
            {isOpen && (
              <div className="accordion__content">{item.content}</div>
            )}
          </div>
        );
      })}
    </div>
  );
}
