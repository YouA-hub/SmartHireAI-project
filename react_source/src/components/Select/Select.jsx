import { ChevronDown, AlertCircle } from 'lucide-react';
import './Select.css';

/**
 * Select — SmartHire AI Component Library
 *
 * Props:
 *   label    — string
 *   required — boolean
 *   state    — 'default' | 'error'
 *   errorMsg — string
 *   hint     — string
 *   options  — Array<{ value, label }> | Array<string>
 *   ...rest  — native select props
 */
export default function Select({
  label,
  required = false,
  state = 'default',
  errorMsg,
  hint,
  options = [],
  placeholder,
  className = '',
  id,
  ...rest
}) {
  const selectId = id || (label ? `select-${label.toLowerCase().replace(/\s+/g, '-')}` : undefined);

  const fieldClasses = [
    'select-field',
    state === 'error' && 'select-field--error',
    className,
  ]
    .filter(Boolean)
    .join(' ');

  return (
    <div className="input-wrapper">
      {label && (
        <label
          htmlFor={selectId}
          className={`input-label${required ? ' input-label--required' : ''}`}
        >
          {label}
        </label>
      )}

      <div className="select-wrapper">
        <select
          id={selectId}
          className={fieldClasses}
          aria-invalid={state === 'error'}
          {...rest}
        >
          {placeholder && (
            <option value="" disabled>
              {placeholder}
            </option>
          )}
          {options.map((opt) => {
            const val = typeof opt === 'string' ? opt : opt.value;
            const lbl = typeof opt === 'string' ? opt : opt.label;
            return (
              <option key={val} value={val}>
                {lbl}
              </option>
            );
          })}
        </select>

        <span className="select-chevron" aria-hidden="true">
          <ChevronDown size={16} />
        </span>
      </div>

      {state === 'error' && errorMsg && (
        <span className="input-error-msg" role="alert">
          <AlertCircle size={12} aria-hidden="true" />
          {errorMsg}
        </span>
      )}

      {hint && state !== 'error' && (
        <span className="input-hint">{hint}</span>
      )}
    </div>
  );
}
