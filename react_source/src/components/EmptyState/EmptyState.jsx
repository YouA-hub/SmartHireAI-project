import './EmptyState.css';

/**
 * EmptyState — SmartHire AI Component Library (ZORUNLU)
 *
 * Props:
 *   icon        — ReactNode (Lucide icon)
 *   title       — string
 *   description — string
 *   action      — ReactNode (CTA button)
 *   variant     — 'default' | 'error'
 */
export default function EmptyState({
  icon,
  title,
  description,
  action,
  variant = 'default',
  className = '',
}) {
  const classes = [
    'empty-state',
    variant === 'error' && 'empty-state--error',
    className,
  ]
    .filter(Boolean)
    .join(' ');

  return (
    <div className={classes}>
      {icon && (
        <div className="empty-state__icon" aria-hidden="true">
          {icon}
        </div>
      )}
      {title && <h3 className="empty-state__title">{title}</h3>}
      {description && (
        <p className="empty-state__description">{description}</p>
      )}
      {action && <div className="empty-state__action">{action}</div>}
    </div>
  );
}
