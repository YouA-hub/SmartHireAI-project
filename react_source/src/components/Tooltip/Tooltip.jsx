import './Tooltip.css';

/** Tooltip — wraps any child, shows text on hover */
export default function Tooltip({ text, children }) {
  return (
    <span className="tooltip-wrapper">
      {children}
      {text && <span className="tooltip__bubble" role="tooltip">{text}</span>}
    </span>
  );
}
