import { useEffect, useRef } from 'react';
import './ProgressBar.css';

/**
 * ProgressBar — SmartHire AI Component Library
 *
 * Props:
 *   value       — number (0-100)
 *   animated    — boolean (0'dan hedef değere ease-out animasyonu)
 *   size        — 'thin' | 'base' | 'large'
 *   showLabel   — boolean (yüzde yazısı barın içinde — sadece base ve large)
 *   label       — string (barın üstünde sol etiket)
 *   valueLabel  — string (barın üstünde sağ değer — varsayılan: value%)
 */
export default function ProgressBar({
  value = 0,
  animated = false,
  size = 'base',
  showLabel = false,
  label,
  valueLabel,
}) {
  const fillRef = useRef(null);
  const clampedValue = Math.min(100, Math.max(0, value));

  useEffect(() => {
    if (!fillRef.current) return;
    // CSS custom property ile target width ayarla
    fillRef.current.style.setProperty('--target-width', `${clampedValue}%`);
  }, [clampedValue]);

  const fillClasses = [
    'progress-bar__fill',
    animated && 'progress-bar__fill--animated',
  ]
    .filter(Boolean)
    .join(' ');

  const barClasses = [
    'progress-bar',
    `progress-bar--${size}`,
  ].join(' ');

  return (
    <div>
      {(label || valueLabel !== undefined) && (
        <div className="progress-bar__header">
          {label && (
            <span className="progress-bar__segment-label">{label}</span>
          )}
          {(valueLabel !== undefined || showLabel) && (
            <span className="progress-bar__segment-value">
              {valueLabel !== undefined ? valueLabel : `${clampedValue}%`}
            </span>
          )}
        </div>
      )}

      <div
        className={barClasses}
        role="progressbar"
        aria-valuenow={clampedValue}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-label={label}
      >
        <div ref={fillRef} className={fillClasses}>
          {showLabel && size !== 'thin' && (
            <span className="progress-bar__label">{clampedValue}%</span>
          )}
        </div>
      </div>
    </div>
  );
}
