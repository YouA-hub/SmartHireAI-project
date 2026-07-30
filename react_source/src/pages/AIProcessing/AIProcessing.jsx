import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Zap } from 'lucide-react';
import ProgressBar from '../../components/ProgressBar/ProgressBar';
import './AIProcessing.css';

const PHASES = [
  { label: 'CV analiz ediliyor', sub: 'Deneyim ve becerileriniz işleniyor…', duration: 2200 },
  { label: 'İş ilanı yorumlanıyor', sub: 'Gereksinimler çıkarılıyor…', duration: 2000 },
  { label: 'Mülakat soruları oluşturuluyor', sub: 'Pozisyona özel içerik hazırlanıyor…', duration: 2000 },
  { label: 'Kişiselleştirme tamamlanıyor', sub: 'Her şey hazır — yönlendiriliyorsunuz…', duration: 1500 },
];

export default function AIProcessing() {
  const navigate = useNavigate();
  const [phaseIndex, setPhaseIndex] = useState(0);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    let total = 0;
    const durations = PHASES.map(p => p.duration);
    const totalDuration = durations.reduce((a, b) => a + b, 0);

    // Progress ticker
    const tick = 80; // ms
    let elapsed = 0;
    const timer = setInterval(() => {
      elapsed += tick;
      setProgress(Math.min(100, Math.round((elapsed / totalDuration) * 100)));

      let cumulative = 0;
      let currentPhase = 0;
      for (let i = 0; i < durations.length; i++) {
        cumulative += durations[i];
        if (elapsed < cumulative) { currentPhase = i; break; }
        currentPhase = durations.length - 1;
      }
      setPhaseIndex(currentPhase);

      if (elapsed >= totalDuration) {
        clearInterval(timer);
        setTimeout(() => navigate('/cv-confirm'), 400);
      }
    }, tick);

    return () => clearInterval(timer);
  }, [navigate]);

  const phase = PHASES[phaseIndex];

  return (
    <div className="ai-processing">
      {/* Animated background */}
      <div className="ai-processing__bg">
        <div className="ai-pulse ai-pulse--1" />
        <div className="ai-pulse ai-pulse--2" />
        <div className="ai-pulse ai-pulse--3" />
      </div>

      <div className="ai-processing__content">
        {/* Logo */}
        <div className="ai-processing__logo">
          <Zap size={24} fill="currentColor" />
          SmartHire AI
        </div>

        {/* Main orb */}
        <div className="ai-orb">
          <div className="ai-orb__inner">
            <Zap size={32} fill="currentColor" />
          </div>
          <div className="ai-orb__ring ai-orb__ring--1" />
          <div className="ai-orb__ring ai-orb__ring--2" />
          <div className="ai-orb__ring ai-orb__ring--3" />
        </div>

        {/* Phase text */}
        <div className="ai-processing__text">
          <h1 className="ai-processing__phase" key={phaseIndex}>
            {phase.label}
          </h1>
          <p className="ai-processing__sub">{phase.sub}</p>
        </div>

        {/* Phase dots */}
        <div className="ai-processing__dots">
          {PHASES.map((_, i) => (
            <div
              key={i}
              className={`ai-dot ${i < phaseIndex ? 'ai-dot--done' : ''} ${i === phaseIndex ? 'ai-dot--active' : ''}`}
            />
          ))}
        </div>

        {/* Progress */}
        <div className="ai-processing__progress">
          <ProgressBar value={progress} animated size="thin" />
          <span className="ai-processing__pct">{progress}%</span>
        </div>

        <p className="ai-processing__hint">
          Bu işlem genellikle 8–10 saniye sürer.
        </p>
      </div>
    </div>
  );
}
