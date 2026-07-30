import './Button.css';

/**
 * Button — SmartHire AI Component Library
 *
 * Props:
 *   variant   — 'primary' | 'secondary' | 'ghost' | 'danger' | 'danger-outline'
 *   size      — 'sm' | 'md' | 'lg'
 *   loading   — boolean
 *   disabled  — boolean
 *   full      — boolean (full width)
 *   iconOnly  — boolean
 *   as        — 'button' | 'a' (renders as anchor)
 *   leftIcon  — ReactNode
 *   rightIcon — ReactNode
 *   children  — ReactNode
 *   ...rest   — any other button/anchor props
 */
export default function Button({
  variant = 'primary',
  size = 'md',
  loading = false,
  disabled = false,
  full = false,
  fullWidth = false,   // alias for full
  iconOnly = false,
  as: Tag = 'button',
  leftIcon,
  rightIcon,
  children,
  className = '',
  ...rest
}) {
  const classes = [
    'btn',
    `btn--${variant}`,
    size !== 'md' && `btn--${size}`,
    loading && 'btn--loading',
    (full || fullWidth) && 'btn--full',
    iconOnly && 'btn--icon-only',
    className,
  ]

    .filter(Boolean)
    .join(' ');

  return (
    <Tag
      className={classes}
      disabled={Tag === 'button' ? disabled || loading : undefined}
      aria-disabled={disabled || loading}
      {...rest}
    >
      {loading ? (
        <>
          <span className="btn__spinner" aria-hidden="true" />
          {!iconOnly && <span>İşleniyor...</span>}
        </>
      ) : (
        <>
          {leftIcon && <span className="btn__icon btn__icon--left" aria-hidden="true">{leftIcon}</span>}
          {children}
          {rightIcon && <span className="btn__icon btn__icon--right" aria-hidden="true">{rightIcon}</span>}
        </>
      )}
    </Tag>
  );
}
