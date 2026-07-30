import { useState, useRef } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import {
  Upload,
  FileText,
  X,
  CheckCircle,
  ChevronRight,
  Zap,
  Briefcase,
  ClipboardList,
} from 'lucide-react';
import Button from '../../components/Button/Button';
import Textarea from '../../components/Textarea/Textarea';
import Input from '../../components/Input/Input';
import ProgressBar from '../../components/ProgressBar/ProgressBar';
import { useToast } from '../../components/Toast/Toast';
import './Onboarding.css';

const STEPS = ['CV Yükle', 'İş İlanı'];

// CV zaten yüklüyse (gerçek uygulamada auth context'ten gelir)
const CV_ALREADY_UPLOADED = true;

export default function Onboarding() {
  const navigate = useNavigate();
  const toast = useToast();
  const [searchParams] = useSearchParams();
  const fileInputRef = useRef(null);

  // ?step=job → CV zaten yüklüyse direkt 2. adımdan başla
  const startStep = searchParams.get('step') === 'job' && CV_ALREADY_UPLOADED ? 1 : 0;

  const [step, setStep] = useState(startStep); // 0: CV, 1: Job
  const [cvFile, setCvFile] = useState(null);
  const [cvDragging, setCvDragging] = useState(false);
  const [jobMode, setJobMode] = useState('paste'); // 'paste' | 'upload'
  const [jobText, setJobText] = useState('');
  const [jobFile, setJobFile] = useState(null);
  const [position, setPosition] = useState('');
  const [loading, setLoading] = useState(false);
  const jobFileRef = useRef(null);


  /* ---- CV Drop ---- */
  const handleCvDrop = (e) => {
    e.preventDefault();
    setCvDragging(false);
    const file = e.dataTransfer.files[0];
    if (file && file.type === 'application/pdf') {
      setCvFile(file);
    } else {
      toast.warning('Hatalı format', 'Lütfen PDF dosyası yükleyin.');
    }
  };

  const handleCvFile = (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'application/pdf') setCvFile(file);
  };

  /* ---- Job File ---- */
  const handleJobFile = (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'application/pdf') setJobFile(file);
  };

  /* ---- Submit ---- */
  const handleNext = () => {
    if (step === 0) {
      if (!cvFile) { toast.warning('CV gerekli', 'Lütfen CV\'nizi yükleyin.'); return; }
      setStep(1);
      return;
    }

    const hasJob = jobMode === 'paste' ? jobText.trim().length > 20 : !!jobFile;
    if (!hasJob) { toast.warning('İlan gerekli', 'Lütfen iş ilanını ekleyin.'); return; }
    if (!position.trim()) { toast.warning('Pozisyon gerekli', 'Lütfen hedef pozisyonu girin.'); return; }

    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      toast.info('CV analiz ediliyor', 'AI verilerini işliyor…');
      navigate('/ai-processing');
    }, 1000);
  };

  const progressValue = step === 0 ? 50 : 100;

  return (
    <div className="onboarding">
      {/* Header */}
      <div className="onboarding__header">
        <div className="onboarding__logo">
          <Zap size={18} fill="currentColor" />
          SmartHire AI
        </div>

        {/* Step indicator */}
        <div className="onboarding__steps">
          {STEPS.map((s, i) => (
            <div key={i} className={`onboarding__step ${i <= step ? 'onboarding__step--active' : ''} ${i < step ? 'onboarding__step--done' : ''}`}>
              <div className="onboarding__step-dot">
                {i < step ? <CheckCircle size={14} /> : i + 1}
              </div>
              <span className="onboarding__step-label">{s}</span>
            </div>
          ))}
        </div>

        <div className="onboarding__progress-bar">
          <ProgressBar value={progressValue} animated size="thin" />
        </div>
      </div>

      {/* Content */}
      <div className="onboarding__content">
        {step === 0 ? (
          /* ---- Step 1: CV ---- */
          <div className="onboarding__panel">
            <div className="onboarding__panel-head">
              <div className="onboarding__panel-icon">
                <FileText size={22} />
              </div>
              <div>
                <h1 className="onboarding__panel-title">CV'nizi yükleyin</h1>
                <p className="onboarding__panel-sub">AI, CV'nizi iş ilanıyla karşılaştırıp kişisel mülakat soruları oluşturacak.</p>
              </div>
            </div>

            {/* Drop zone */}
            <div
              className={`cv-drop ${cvDragging ? 'cv-drop--dragging' : ''} ${cvFile ? 'cv-drop--filled' : ''}`}
              onDragOver={(e) => { e.preventDefault(); setCvDragging(true); }}
              onDragLeave={() => setCvDragging(false)}
              onDrop={handleCvDrop}
              onClick={() => !cvFile && fileInputRef.current?.click()}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf"
                style={{ display: 'none' }}
                onChange={handleCvFile}
              />
              {cvFile ? (
                <div className="cv-drop__filled">
                  <div className="cv-drop__file-icon">
                    <FileText size={24} />
                  </div>
                  <div className="cv-drop__file-info">
                    <p className="cv-drop__file-name">{cvFile.name}</p>
                    <p className="cv-drop__file-size">{(cvFile.size / 1024).toFixed(0)} KB • PDF</p>
                  </div>
                  <button
                    className="cv-drop__remove"
                    onClick={(e) => { e.stopPropagation(); setCvFile(null); }}
                    aria-label="Dosyayı kaldır"
                  >
                    <X size={16} />
                  </button>
                </div>
              ) : (
                <>
                  <div className="cv-drop__icon">
                    <Upload size={28} />
                  </div>
                  <p className="cv-drop__title">CV'nizi buraya sürükleyin</p>
                  <p className="cv-drop__sub">veya tıklayın — yalnızca PDF, max 5 MB</p>
                </>
              )}
            </div>

            <Button
              variant="primary"
              fullWidth
              onClick={handleNext}
              rightIcon={<ChevronRight size={16} />}
              disabled={!cvFile}
            >
              Devam et
            </Button>
          </div>
        ) : (
          /* ---- Step 2: Job ---- */
          <div className="onboarding__panel">
            <div className="onboarding__panel-head">
              <div className="onboarding__panel-icon onboarding__panel-icon--purple">
                <Briefcase size={22} />
              </div>
              <div>
                <h1 className="onboarding__panel-title">İş ilanını ekleyin</h1>
                <p className="onboarding__panel-sub">Hedef pozisyon ve iş ilanını girin, AI size özel sorular üretsin.</p>
              </div>
            </div>

            <Input
              id="onboarding-position"
              label="Hedef pozisyon"
              placeholder="ör. Frontend Developer"
              value={position}
              onChange={(e) => setPosition(e.target.value)}
              leftIcon={<ClipboardList size={16} />}
            />

            {/* Mode toggle */}
            <div className="onboarding__mode-toggle">
              <button
                className={`onboarding__mode-btn ${jobMode === 'paste' ? 'onboarding__mode-btn--active' : ''}`}
                onClick={() => setJobMode('paste')}
              >
                Metin yapıştır
              </button>
              <button
                className={`onboarding__mode-btn ${jobMode === 'upload' ? 'onboarding__mode-btn--active' : ''}`}
                onClick={() => setJobMode('upload')}
              >
                PDF yükle
              </button>
            </div>

            {jobMode === 'paste' ? (
              <Textarea
                id="onboarding-jobtext"
                label="İş ilanı metni"
                placeholder="İş ilanındaki gereksinimleri, beklentileri ve sorumlulukları buraya yapıştırın…"
                value={jobText}
                onChange={(e) => setJobText(e.target.value)}
                rows={8}
              />
            ) : (
              <div
                className={`cv-drop ${jobFile ? 'cv-drop--filled' : ''}`}
                onClick={() => !jobFile && jobFileRef.current?.click()}
              >
                <input
                  ref={jobFileRef}
                  type="file"
                  accept=".pdf"
                  style={{ display: 'none' }}
                  onChange={handleJobFile}
                />
                {jobFile ? (
                  <div className="cv-drop__filled">
                    <div className="cv-drop__file-icon">
                      <FileText size={24} />
                    </div>
                    <div className="cv-drop__file-info">
                      <p className="cv-drop__file-name">{jobFile.name}</p>
                      <p className="cv-drop__file-size">{(jobFile.size / 1024).toFixed(0)} KB • PDF</p>
                    </div>
                    <button
                      className="cv-drop__remove"
                      onClick={(e) => { e.stopPropagation(); setJobFile(null); }}
                      aria-label="Dosyayı kaldır"
                    >
                      <X size={16} />
                    </button>
                  </div>
                ) : (
                  <>
                    <div className="cv-drop__icon"><Upload size={28} /></div>
                    <p className="cv-drop__title">İş ilanı PDF'ini buraya sürükleyin</p>
                    <p className="cv-drop__sub">veya tıklayın — yalnızca PDF</p>
                  </>
                )}
              </div>
            )}

            <div className="onboarding__btn-row">
              <Button variant="ghost" onClick={() => setStep(0)}>
                Geri
              </Button>
              <Button
                variant="primary"
                onClick={handleNext}
                loading={loading}
                rightIcon={!loading && <Zap size={16} fill="currentColor" />}
              >
                {loading ? 'Analiz başlatılıyor…' : 'Analizi başlat'}
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
