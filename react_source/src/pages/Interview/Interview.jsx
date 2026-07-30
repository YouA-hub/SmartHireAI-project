import { useState, useEffect, useRef, useCallback } from 'react';
import { useNavigate, useBlocker } from 'react-router-dom';
import {
  Clock,
  ChevronRight,
  Send,
  SkipForward,
  AlertTriangle,
  CheckCircle,
  Mic,
} from 'lucide-react';
import Button from '../../components/Button/Button';
import Textarea from '../../components/Textarea/Textarea';
import ProgressBar from '../../components/ProgressBar/ProgressBar';
import Badge from '../../components/Badge/Badge';
import Breadcrumb from '../../components/Breadcrumb/Breadcrumb';
import Modal from '../../components/Modal/Modal';
import { useToast } from '../../components/Toast/Toast';
import './Interview.css';

const QUESTIONS = [
  // ---- Teknik sorular (pozisyona özgü) ----
  {
    id: 1,
    category: 'React',
    difficulty: 'Orta',
    difficultyVariant: 'warning',
    text: 'React\'te virtual DOM nasıl çalışır? Gerçek DOM ile farkını ve performansa katkısını açıklayın.',
    tip: 'Diffing algoritması ve reconciliation sürecinden bahsedin.',
    isEnglish: false,
  },
  {
    id: 2,
    category: 'JavaScript',
    difficulty: 'Orta',
    difficultyVariant: 'warning',
    text: 'Event loop nedir ve JavaScript\'in single-threaded çalışmasına nasıl olanak tanır? Microtask ile macrotask arasındaki farkı açıklayın.',
    tip: 'Call stack, callback queue ve microtask queue\'yu ele alın.',
    isEnglish: false,
  },
  {
    id: 3,
    category: 'TypeScript',
    difficulty: 'Orta',
    difficultyVariant: 'warning',
    text: 'TypeScript\'te generic types ne işe yarar? Utility types (Partial, Pick, Omit) ile birlikte bir örnek üzerinden açıklayın.',
    tip: 'Type safety ve kod tekrarını azaltma üzerine odaklanın.',
    isEnglish: false,
  },
  {
    id: 4,
    category: 'Sistem Tasarımı',
    difficulty: 'Zor',
    difficultyVariant: 'danger',
    text: 'Yüksek trafikli bir e-ticaret sitesinin frontend mimarisini sıfırdan tasarlayın. SSR vs CSR tercihinizi ve caching stratejinizi açıklayın.',
    tip: 'SSR vs CSR, CDN kullanımı, lazy loading ve code splitting hakkında konuşun.',
    isEnglish: false,
  },
  // ---- Opsiyonel motivasyon sorusu ----
  {
    id: 5,
    category: 'Motivasyon',
    difficulty: 'Kolay',
    difficultyVariant: 'success',
    text: 'Bu pozisyona neden başvurdunuz ve şimdiye kadarki en çok gurur duyduğunuz teknik projeyi kısaca anlatır mısınız?',
    tip: 'STAR (Durum–Görev–Eylem–Sonuç) yapısını kullanın.',
    isEnglish: false,
    isOptional: true,
  },
  // ---- İngilizce dil tutarlılık sorusu (her mülakatın sonu) ----
  {
    id: 6,
    category: 'English',
    difficulty: 'Orta',
    difficultyVariant: 'primary',
    text: 'Describe a challenging technical problem you solved recently. What was the problem, what approach did you take, and what was the outcome?',
    tip: 'Answer in English. Focus on clarity and structure — this also serves as a language consistency check.',
    isEnglish: true,
  },
];


const TOTAL_TIME = 90; // seconds per question

export default function Interview() {
  const navigate = useNavigate();
  const toast = useToast();

  const [qIndex, setQIndex] = useState(0);
  const [answer, setAnswer] = useState('');
  const [answers, setAnswers] = useState({});
  const [timeLeft, setTimeLeft] = useState(TOTAL_TIME);
  const [showTip, setShowTip] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const timerRef = useRef(null);

  // Çıkış guard state
  const [exitModalOpen, setExitModalOpen] = useState(false);
  const pendingNavRef = useRef(null); // bekleyen router navigasyonu

  // ---- Page Visibility API (4 saniye kuralı) ----
  const [isTerminated, setIsTerminated] = useState(false);
  const tabAwayTimerRef = useRef(null);

  const isActive = !submitted && !isTerminated; // mülakat devam ediyor mu

  useEffect(() => {
    if (!isActive) return;

    const handleVisibilityChange = () => {
      if (document.hidden) {
        // Sekmeden/pencereden ayrıldı -> 4 saniye zamanlayıcı başlat
        tabAwayTimerRef.current = setTimeout(() => {
          setIsTerminated(true);
          setSubmitted(true);
          toast.danger(
            'Mülakat Sonlandırıldı',
            'Mülakat sırasında başka bir sekmeye geçtiğiniz tespit edildi, deneme sonlandırıldı.'
          );
        }, 4000);
      } else {
        // 4 saniyeden kısa sürede geri döndü -> zamanlayıcıyı iptal et
        if (tabAwayTimerRef.current) {
          clearTimeout(tabAwayTimerRef.current);
          tabAwayTimerRef.current = null;
        }
      }
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange);
      if (tabAwayTimerRef.current) clearTimeout(tabAwayTimerRef.current);
    };
  }, [isActive, toast]);

  // ---- React Router useBlocker ----
  const blocker = useBlocker(
    useCallback(
      ({ currentLocation, nextLocation }) =>
        isActive && currentLocation.pathname !== nextLocation.pathname,
      [isActive]
    )
  );

  // Blocker tetiklendiğinde modal aç
  useEffect(() => {
    if (blocker.state === 'blocked') {
      pendingNavRef.current = blocker;
      setExitModalOpen(true);
    }
  }, [blocker.state]);

  // ---- Tarayıcı sekme/pencere kapatma / yenileme ----
  useEffect(() => {
    if (!isActive) return;
    const handleBeforeUnload = (e) => {
      e.preventDefault();
      e.returnValue = 'Mülakattan çıkarsan bu deneme yarım kalmış sayılacak.';
    };
    window.addEventListener('beforeunload', handleBeforeUnload);
    return () => window.removeEventListener('beforeunload', handleBeforeUnload);
  }, [isActive]);

  // ---- Çıkış aksiyonları ----
  const handleExitConfirm = () => {
    // Mülakatı "yarım kaldı" olarak işaretle (gerçek uygulamada API çağrısı)
    toast.warning('Mülakat yarım bırakıldı', 'Bu oturum geçmişe "Yarım bırakıldı" olarak kaydedildi.');
    setExitModalOpen(false);
    if (pendingNavRef.current?.state === 'blocked') {
      pendingNavRef.current.proceed();
    }
    pendingNavRef.current = null;
  };

  const handleExitCancel = () => {
    setExitModalOpen(false);
    if (pendingNavRef.current?.state === 'blocked') {
      pendingNavRef.current.reset();
    }
    pendingNavRef.current = null;
  };

  // ---- Timer ----
  useEffect(() => {
    setTimeLeft(TOTAL_TIME);
    setShowTip(false);
    timerRef.current = setInterval(() => {
      setTimeLeft(t => {
        if (t <= 1) {
          clearInterval(timerRef.current);
          return 0;
        }
        return t - 1;
      });
    }, 1000);
    return () => clearInterval(timerRef.current);
  }, [qIndex]);

  const formatTime = (s) => `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`;

  const q = QUESTIONS[qIndex];
  const progress = (qIndex / QUESTIONS.length) * 100;
  const timeProgress = (timeLeft / TOTAL_TIME) * 100;
  const isLow = timeLeft <= 20;

  const handleSubmit = () => {
    if (!answer.trim()) { toast.warning('Yanıt boş', 'Lütfen yanıtınızı yazın.'); return; }
    clearInterval(timerRef.current);
    setAnswers(prev => ({ ...prev, [q.id]: answer }));

    if (qIndex < QUESTIONS.length - 1) {
      setQIndex(i => i + 1);
      setAnswer('');
    } else {
      setSubmitted(true);
      toast.success('Mülakat tamamlandı!', 'Performansınız analiz ediliyor…');
      setTimeout(() => navigate('/performance'), 1200);
    }
  };

  const handleSkip = () => {
    clearInterval(timerRef.current);
    if (qIndex < QUESTIONS.length - 1) {
      setQIndex(i => i + 1);
      setAnswer('');
    } else {
      navigate('/performance');
    }
  };

  if (submitted) {
    if (isTerminated) {
      return (
        <div className="interview-done interview-done--warn">
          <AlertTriangle size={48} className="interview-done__icon--danger" />
          <h2>Deneme Sonlandırıldı</h2>
          <p>Mülakat sırasında başka bir sekmeye geçtiğiniz tespit edildi, deneme sonlandırıldı.</p>
          <div style={{ marginTop: 'var(--space-4)' }}>
            <Button variant="primary" onClick={() => navigate('/history')}>
              Geçmişe Git
            </Button>
          </div>
        </div>
      );
    }
    return (
      <div className="interview-done">
        <CheckCircle size={48} />
        <h2>Mülakat tamamlandı</h2>
        <p>Analiz yükleniyor…</p>
      </div>
    );
  }

  return (
    <>
      {/* ---- Çıkış Onay Modalı ---- */}
      <Modal
        isOpen={exitModalOpen}
        onClose={handleExitCancel}
        closeOnOverlay={false}
        title="Mülakatı Bırak"
        description="Mülakattan çıkarsan bu deneme yarım kalmış sayılacak ve geçmişe 'Yarım bırakıldı' olarak kaydedilecek. Emin misin?"
        icon={<AlertTriangle size={22} />}
        iconVariant="warning"
        confirmLabel="Evet, çık"
        confirmVariant="danger"
        onConfirm={handleExitConfirm}
      />

      <div className="interview">
        <Breadcrumb
          items={[
            { label: 'Dashboard', to: '/dashboard' },
            { label: 'Mülakat' },
          ]}
        />

        {/* Progress header */}
        <div className="interview__header">
          <div className="interview__meta">
            <span className="interview__counter">
              Soru {qIndex + 1} / {QUESTIONS.length}
            </span>
            <Badge variant={q.difficultyVariant} size="sm">{q.difficulty}</Badge>
            <Badge variant="primary" size="sm">{q.category}</Badge>
            {q.isOptional && <Badge variant="success" size="sm">Opsiyonel</Badge>}
            {q.isEnglish && <Badge variant="info" size="sm">🇬🇧 English</Badge>}
          </div>
          <div className="interview__progress">
            <ProgressBar value={progress} size="thin" />
          </div>
        </div>

        {/* Timer */}
        <div className={`interview__timer ${isLow ? 'interview__timer--low' : ''}`}>
          <Clock size={16} />
          <span className="interview__timer-val">{formatTime(timeLeft)}</span>
          <div className="interview__timer-bar">
            <ProgressBar value={timeProgress} size="thin" />
          </div>
          {isLow && <AlertTriangle size={14} />}
        </div>

        {/* Question card */}
        <div className="interview__question-card" key={q.id}>
          {q.isEnglish && (
            <div className="interview__english-notice">
              🇬🇧 This question must be answered in English — it is used as a language consistency check.
            </div>
          )}
          <p className="interview__q-text">{q.text}</p>


          {showTip ? (
            <div className="interview__tip">
              <span className="interview__tip-label">💡 İpucu</span>
              <p>{q.tip}</p>
            </div>
          ) : (
            <button
              className="interview__tip-toggle"
              onClick={() => setShowTip(true)}
            >
              İpucu göster
            </button>
          )}
        </div>

        {/* Answer area */}
        <div className="interview__answer">
          <Textarea
            id="interview-answer"
            label="Yanıtınız"
            placeholder="Yanıtınızı buraya yazın… Net ve yapılandırılmış bir cevap vermeye çalışın."
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            rows={8}
          />
          <div className="interview__char-count">
            {answer.length} karakter
          </div>
        </div>

        {/* Actions */}
        <div className="interview__actions">
          <Button
            variant="ghost"
            size="sm"
            leftIcon={<SkipForward size={14} />}
            onClick={handleSkip}
          >
            Soruyu geç
          </Button>
          <div className="interview__actions-right">
            <Button
              variant="ghost"
              size="sm"
              leftIcon={<Mic size={14} />}
              disabled
            >
              Sesli yanıt (yakında)
            </Button>
            <Button
              variant="primary"
              leftIcon={<Send size={15} />}
              onClick={handleSubmit}
              disabled={!answer.trim()}
            >
              {qIndex < QUESTIONS.length - 1 ? 'Yanıtla ve devam et' : 'Mülakatı bitir'}
              <ChevronRight size={15} />
            </Button>
          </div>
        </div>
      </div>
    </>
  );
}
