import './Skeleton.css';

/**
 * Skeleton — SmartHire AI Component Library
 * Loading + Skeleton birleşik component
 *
 * Props:
 *   variant — 'text' | 'text-sm' | 'title' | 'button' | 'avatar-sm' | 'avatar-md' | 'avatar-lg' | 'full' | 'half' | 'third'
 *   width   — CSS width string (override)
 *   height  — CSS height string (override)
 *   style   — additional inline styles
 */
export default function Skeleton({
  variant = 'text',
  width,
  height,
  style = {},
  className = '',
}) {
  const isAvatar = variant.startsWith('avatar');

  const classes = [
    'skeleton',
    variant && `skeleton--${variant}`,
    className,
  ]
    .filter(Boolean)
    .join(' ');

  return (
    <span
      className={classes}
      style={{ width, height, ...style }}
      aria-hidden="true"
      role="presentation"
    />
  );
}

/**
 * SkeletonCard — Kart yükleme placeholder'ı
 * Spec §2.9: skeleton kart (gri animasyonlu dikdörtgenler)
 */
export function SkeletonCard() {
  return (
    <div className="skeleton-card" aria-busy="true" aria-label="Yükleniyor...">
      <div className="skeleton-card__header">
        <Skeleton variant="avatar-md" />
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: 6 }}>
          <Skeleton variant="title" />
          <Skeleton variant="text-sm" />
        </div>
      </div>
      <Skeleton variant="text" />
      <Skeleton variant="text" />
      <Skeleton variant="half" style={{ height: 14 }} />
    </div>
  );
}

/**
 * SkeletonMetric — Metrik kartı yükleme placeholder'ı
 */
export function SkeletonMetric() {
  return (
    <div className="skeleton-card" aria-busy="true" aria-label="Yükleniyor...">
      <Skeleton variant="text-sm" style={{ width: '60%' }} />
      <Skeleton variant="title" style={{ height: 28, width: '40%' }} />
      <Skeleton variant="text-sm" style={{ width: '80%' }} />
    </div>
  );
}
