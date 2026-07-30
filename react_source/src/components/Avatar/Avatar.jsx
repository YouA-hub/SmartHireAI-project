import './Avatar.css';

/**
 * Avatar — SmartHire AI Component Library
 *
 * Props:
 *   src      — string (image URL)
 *   alt      — string
 *   name     — string (baş harf fallback için)
 *   size     — 'sm' | 'md' | 'lg' | 'xl'
 */
export default function Avatar({
  src,
  alt = '',
  name = '',
  size = 'md',
  className = '',
  ...rest
}) {
  const classes = ['avatar', `avatar--${size}`, className]
    .filter(Boolean)
    .join(' ');

  const initials = name
    ? name
        .split(' ')
        .slice(0, 2)
        .map((part) => part[0]?.toUpperCase())
        .join('')
    : '?';

  return (
    <div className={classes} aria-label={alt || name} {...rest}>
      {src ? (
        <img
          src={src}
          alt={alt || name}
          className="avatar__img"
          onError={(e) => {
            e.currentTarget.style.display = 'none';
          }}
        />
      ) : (
        <span className="avatar__initials" aria-hidden="true">
          {initials}
        </span>
      )}
    </div>
  );
}
