import { Link } from 'react-router-dom';
import { ChevronRight } from 'lucide-react';
import './Breadcrumb.css';

/**
 * Breadcrumb
 * items — Array<{ label, to? }> (son item aktif, to yok)
 */
export default function Breadcrumb({ items = [] }) {
  return (
    <nav className="breadcrumb" aria-label="Breadcrumb">
      <ol style={{ display: 'contents' }}>
        {items.map((item, i) => {
          const isLast = i === items.length - 1;
          return (
            <li
              key={i}
              className={`breadcrumb__item${isLast ? ' breadcrumb__item--active' : ''}`}
              aria-current={isLast ? 'page' : undefined}
            >
              {!isLast ? (
                <>
                  {item.to ? (
                    <Link to={item.to} className="breadcrumb__link">
                      {item.label}
                    </Link>
                  ) : (
                    <span className="breadcrumb__link">{item.label}</span>
                  )}
                  <span className="breadcrumb__separator" aria-hidden="true">
                    <ChevronRight size={14} />
                  </span>
                </>
              ) : (
                <span className="breadcrumb__label">{item.label}</span>
              )}
            </li>
          );
        })}
      </ol>
    </nav>
  );
}
