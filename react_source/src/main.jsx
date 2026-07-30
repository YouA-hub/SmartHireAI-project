import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';

/* Design tokens — en önce import edilmeli */
import './tokens/tokens.css';

/* Base styles */
import './styles/reset.css';
import './styles/typography.css';
import './styles/animations.css';

import App from './App.jsx';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
