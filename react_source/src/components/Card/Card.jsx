import './Card.css';

/**
 * Card — SmartHire AI Component Library
 *
 * Props:
 *   variant  — 'default' | 'gradient' | 'borderless'
 *   metric   — boolean (metrik kartı modu)
 *   padding  — 'sm' | 'md' | 'lg'
 *   label    — string (metric modunda üst etiket)
 *   value    — string | number (metric modunda büyük sayı)
 *   sub      — string (metric modunda alt açıklama)
 *   children — ReactNode
 *   className— string
 */
export default function Card({
  variant = 'default',
  metric = false,
  padding = 'md',
  label,
  value,
  sub,
  children,
  className = '',
  ...rest
}) {
  const classes = [
    'card',
    variant === 'gradient' && 'card--gradient',
    variant === 'borderless' && 'card--borderless',
    metric && 'card--metric',
    padding !== 'md' && `card--pad-${padding}`,
    className,
  ]
    .filter(Boolean)
    .join(' ');

  if (metric) {
    return (
      <div className={classes} {...rest}>
        {label && <span className="card__metric-label">{label}</span>}
        {value !== undefined && <span className="card__metric-value">{value}</span>}
        {sub && <span className="card__metric-sub">{sub}</span>}
        {children}
      </div>
    );
  }

  return (
    <div className={classes} {...rest}>
      {children}
    </div>
  );
}

/**
 * Card.Header — title + optional right content
 */
Card.Header = function CardHeader({ title, children, className = '' }) {
  return (
    <div className={`card__header ${className}`}>
      {title && <h2 className="card__title">{title}</h2>}
      {children}
    </div>
  );
};

/**
 * Card.Body
 */
Card.Body = function CardBody({ children, className = '' }) {
  return <div className={`card__body ${className}`}>{children}</div>;
};

/**
 * Card.Footer
 */
Card.Footer = function CardFooter({ children, className = '' }) {
  return <div className={`card__footer ${className}`}>{children}</div>;
};
