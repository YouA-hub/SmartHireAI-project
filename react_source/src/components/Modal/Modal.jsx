import { useEffect, useCallback } from 'react';
import { createPortal } from 'react-dom';
import { X } from 'lucide-react';
import Button from '../Button/Button';
import './Modal.css';

/**
 * Modal — SmartHire AI Component Library
 * Dialog component'i kaldırıldı — onay aksiyonları Modal ile yapılır.
 *
 * Props:
 *   isOpen         — boolean
 *   onClose        — () => void
 *   title          — string
 *   description    — string  (onay dialogları için açıklama metni)
 *   icon           — ReactNode (başlık yanında ikon)
 *   iconVariant    — 'danger' | 'warning' | 'success' | 'primary'
 *   confirmLabel   — string  (onay butonu metni, varsa footer otomatik render edilir)
 *   confirmVariant — 'danger' | 'primary' | 'secondary'
 *   onConfirm      — () => void
 *   children       — ReactNode
 *   footer         — ReactNode (özel footer; confirmLabel varsa kullanılmaz)
 *   closeOnOverlay — boolean (default: true)
 */
export default function Modal({
  isOpen,
  onClose,
  title,
  description,
  icon,
  iconVariant = 'primary',
  confirmLabel,
  confirmVariant = 'primary',
  onConfirm,
  children,
  footer,
  closeOnOverlay = true,
}) {
  const handleEsc = useCallback(
    (e) => {
      if (e.key === 'Escape') onClose();
    },
    [onClose]
  );

  useEffect(() => {
    if (!isOpen) return;
    document.addEventListener('keydown', handleEsc);
    document.body.style.overflow = 'hidden';
    return () => {
      document.removeEventListener('keydown', handleEsc);
      document.body.style.overflow = '';
    };
  }, [isOpen, handleEsc]);

  if (!isOpen) return null;

  // Auto-build footer for confirm dialogs
  const resolvedFooter =
    footer ||
    (confirmLabel ? (
      <>
        <Button variant="ghost" onClick={onClose}>İptal</Button>
        <Button variant={confirmVariant} onClick={onConfirm}>{confirmLabel}</Button>
      </>
    ) : null);

  return createPortal(
    <div
      className="modal-overlay"
      onClick={closeOnOverlay ? onClose : undefined}
      role="dialog"
      aria-modal="true"
      aria-labelledby={title ? 'modal-title' : undefined}
    >
      <div
        className="modal"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        {title && (
          <div className="modal__header">
            {icon && (
              <span className={`modal__header-icon modal__header-icon--${iconVariant}`} aria-hidden="true">
                {icon}
              </span>
            )}
            <h2 id="modal-title" className="modal__title">
              {title}
            </h2>
            <button
              className="modal__close"
              onClick={onClose}
              aria-label="Modalı kapat"
            >
              <X size={20} aria-hidden="true" />
            </button>
          </div>
        )}

        {/* Description (onay dialogları) */}
        {description && (
          <p className="modal__description">{description}</p>
        )}

        {/* Body */}
        {children && <div className="modal__body">{children}</div>}

        {/* Footer */}
        {resolvedFooter && <div className="modal__footer">{resolvedFooter}</div>}
      </div>
    </div>,
    document.body
  );
}
