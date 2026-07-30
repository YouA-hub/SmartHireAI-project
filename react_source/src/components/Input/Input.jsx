import { AlertCircle } from 'lucide-react';
import './Input.css';

/**
 * Input — SmartHire AI Component Library
 *
 * Props:
 *   label      — string
 *   required   — boolean
 *   state      — 'default' | 'error' | 'warning'
 *   errorMsg   — string (state='error' olduğunda gösterilir)
 *   hint       — string (yardımcı metin)
 *   leftIcon   — ReactNode
 *   rightIcon  — ReactNode
 *   ...rest    — native input props
 */
export default function Input({
  label,
  required = false,
  state = 'default',
  errorMsg,
  hint,
  leftIcon,
  rightIcon,
  className = '',
  id,
  ...rest
}) {
  const inputId = id || (label ? `input-${label.toLowerCase().replace(/\s+/g, '-')}` : undefined);

  const fieldClasses = [
    'input-field',
    state === 'error' && 'input-field--error',
    state === 'warning' && 'input-field--warning',
    leftIcon && 'input-field--with-left-icon',
    rightIcon && 'input-field--with-right-icon',
    className,
  ]
    .filter(Boolean)
    .join(' ');

  return (
    <div className="input-wrapper">
      {label && (
        <label
          htmlFor={inputId}
          className={`input-label${required ? ' input-label--required' : ''}`}
        >
          {label}
        </label>
      )}

      <div className="input-field-wrapper">
        {leftIcon && (
          <span className="input-icon input-icon--left" aria-hidden="true">
            {leftIcon}
          </span>
        )}

        <input
          id={inputId}
          className={fieldClasses}
          aria-invalid={state === 'error'}
          aria-describedby={
            errorMsg ? `${inputId}-error` : hint ? `${inputId}-hint` : undefined
          }
          {...rest}
        />

        {rightIcon && (
          <span className="input-icon input-icon--right" aria-hidden="true">
            {rightIcon}
          </span>
        )}
      </div>

      {state === 'error' && errorMsg && (
        <span id={`${inputId}-error`} className="input-error-msg" role="alert">
          <AlertCircle size={12} aria-hidden="true" />
          {errorMsg}
        </span>
      )}

      {hint && state !== 'error' && (
        <span
          id={`${inputId}-hint`}
          className={`input-hint${state === 'warning' ? ' input-hint--warning' : ''}`}
        >
          {hint}
        </span>
      )}
    </div>
  );
}
