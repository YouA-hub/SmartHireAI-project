import { ChevronLeft, ChevronRight } from 'lucide-react';
import './Pagination.css';

/**
 * Pagination
 * page      — current page (1-indexed)
 * totalPages— total pages
 * onChange  — (page: number) => void
 */
export default function Pagination({ page = 1, totalPages = 1, onChange }) {
  const pages = Array.from({ length: totalPages }, (_, i) => i + 1);

  const getVisible = () => {
    if (totalPages <= 7) return pages;
    if (page <= 4) return [...pages.slice(0, 5), '...', totalPages];
    if (page >= totalPages - 3) return [1, '...', ...pages.slice(totalPages - 5)];
    return [1, '...', page - 1, page, page + 1, '...', totalPages];
  };

  return (
    <nav className="pagination" aria-label="Sayfalama">
      <button
        className="pagination__btn"
        onClick={() => onChange(page - 1)}
        disabled={page === 1}
        aria-label="Önceki sayfa"
      >
        <ChevronLeft size={16} aria-hidden="true" />
      </button>

      {getVisible().map((p, i) =>
        p === '...' ? (
          <span key={`ellipsis-${i}`} className="pagination__ellipsis">…</span>
        ) : (
          <button
            key={p}
            className={`pagination__btn${p === page ? ' pagination__btn--active' : ''}`}
            onClick={() => onChange(p)}
            aria-label={`Sayfa ${p}`}
            aria-current={p === page ? 'page' : undefined}
          >
            {p}
          </button>
        )
      )}

      <button
        className="pagination__btn"
        onClick={() => onChange(page + 1)}
        disabled={page === totalPages}
        aria-label="Sonraki sayfa"
      >
        <ChevronRight size={16} aria-hidden="true" />
      </button>
    </nav>
  );
}
