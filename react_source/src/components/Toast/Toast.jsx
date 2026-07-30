import { createContext, useContext, useCallback, useState } from 'react';
import { createPortal } from 'react-dom';
import {
  CheckCircle,
  AlertTriangle,
  XCircle,
  Info,
  X,
} from 'lucide-react';
import './Toast.css';

/* ---- Context ---- */
const ToastContext = createContext(null);

const ICONS = {
  success: <CheckCircle size={16} aria-hidden="true" />,
  warning: <AlertTriangle size={16} aria-hidden="true" />,
  danger:  <XCircle size={16} aria-hidden="true" />,
  info:    <Info size={16} aria-hidden="true" />,
};

const DEFAULT_DURATION = 3500; // 3-4 saniye arası

/* ---- Single Toast ---- */
function ToastItem({ id, type = 'info', title, message, onRemove }) {
  return (
    <div className={`toast toast--${type}`} role="alert" aria-live="polite">
      <span className="toast__icon">{ICONS[type]}</span>

      <div className="toast__content">
        {title && <p className="toast__title">{title}</p>}
        {message && <p className="toast__message">{message}</p>}
      </div>

      <button
        className="toast__close"
        onClick={() => onRemove(id)}
        aria-label="Bildirimi kapat"
      >
        <X size={14} aria-hidden="true" />
      </button>
    </div>
  );
}

/* ---- Provider ---- */
export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);

  const removeToast = useCallback((id) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  const addToast = useCallback(
    ({ type = 'info', title, message, duration = DEFAULT_DURATION }) => {
      const id = Date.now();
      setToasts((prev) => [...prev, { id, type, title, message }]);
      if (duration > 0) {
        setTimeout(() => removeToast(id), duration);
      }
    },
    [removeToast]
  );

  return (
    <ToastContext.Provider value={{ addToast, removeToast }}>
      {children}
      {createPortal(
        <div className="toast-container" aria-label="Bildirimler">
          {toasts.map((toast) => (
            <ToastItem key={toast.id} {...toast} onRemove={removeToast} />
          ))}
        </div>,
        document.body
      )}
    </ToastContext.Provider>
  );
}

/* ---- Hook ---- */
export function useToast() {
  const ctx = useContext(ToastContext);
  if (!ctx) throw new Error('useToast must be used within <ToastProvider>');

  return {
    success: (title, message, opts) =>
      ctx.addToast({ type: 'success', title, message, ...opts }),
    warning: (title, message, opts) =>
      ctx.addToast({ type: 'warning', title, message, ...opts }),
    danger:  (title, message, opts) =>
      ctx.addToast({ type: 'danger', title, message, ...opts }),
    info:    (title, message, opts) =>
      ctx.addToast({ type: 'info', title, message, ...opts }),
    dismiss: ctx.removeToast,
  };
}
