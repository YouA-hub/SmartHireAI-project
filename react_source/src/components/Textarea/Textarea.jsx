import { AlertCircle } from 'lucide-react';
import './Textarea.css';

/**
 * Textarea — SmartHire AI Component Library
 *
 * Props:
 *   label     — string
 *   required  — boolean
 *   state     — 'default' | 'error' | 'warning'
 *   errorMsg  — string
 *   hint      — string
 *   noResize  — boolean
 *   rows      — number
 *   ...rest   — native textarea props
 */
export default function Textarea({
  label,
  required = false,
  state = 'default',
  errorMsg,
  hint,
  noResize = false,
  className = '',
  id,
  ...rest
}) {
  const textareaId = id || (label ? `textarea-${label.toLowerCase().replace(/\s+/g, '-')}` : undefined);

  const fieldClasses = [
    'textarea-field',
    state === 'error' && 'textarea-field--error',
    state === 'warning' && 'textarea-field--warning',
    noResize && 'textarea-field--no-resize',
    className,
  ]
    .filter(Boolean)
    .join(' ');

  return (
    <div className="input-wrapper">
      {label && (
        <label
          htmlFor={textareaId}
          className={`input-label${required ? ' input-label--required' : ''}`}
        >
          {label}
        </label>
      )}

      <textarea
        id={textareaId}
        className={fieldClasses}
        aria-invalid={state === 'error'}
        aria-describedby={
          errorMsg ? `${textareaId}-error` : hint ? `${textareaId}-hint` : undefined
        }
        {...rest}
      />

      {state === 'error' && errorMsg && (
        <span id={`${textareaId}-error`} className="input-error-msg" role="alert">
          <AlertCircle size={12} aria-hidden="true" />
          {errorMsg}
        </span>
      )}

      {hint && state !== 'error' && (
        <span
          id={`${textareaId}-hint`}
          className={`input-hint${state === 'warning' ? ' input-hint--warning' : ''}`}
        >
          {hint}
        </span>
      )}
    </div>
  );
}
