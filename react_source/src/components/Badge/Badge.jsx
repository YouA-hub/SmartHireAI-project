import './Badge.css';

/**
 * Badge — SmartHire AI Component Library
 *
 * Props:
 *   variant — 'success' | 'warning' | 'danger' | 'primary' | 'neutral' | 'accent'
 *   size    — 'sm' | 'md' | 'lg'
 *   dot     — boolean (sol tarafta renkli nokta)
 *   icon    — ReactNode
 *   children— ReactNode
 */
export default function Badge({
  variant = 'neutral',
  size = 'md',
  dot = false,
  icon,
  children,
  className = '',
  ...rest
}) {
  const classes = [
    'badge',
    `badge--${variant}`,
    size !== 'md' && `badge--${size}`,
    className,
  ]
    .filter(Boolean)
    .join(' ');

  return (
    <span className={classes} {...rest}>
      {dot && <span className="badge__dot" aria-hidden="true" />}
      {icon && <span aria-hidden="true">{icon}</span>}
      {children}
    </span>
  );
}
