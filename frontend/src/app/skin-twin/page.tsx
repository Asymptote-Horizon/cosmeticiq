'use client';

import { useState, useRef, useCallback, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Camera,
  Upload,
  Sparkles,
  Droplets,
  Sun,
  Eye,
  AlertTriangle,
  CheckCircle,
  ArrowLeft,
  RefreshCw,
  SwitchCamera,
  Loader2,
  Clock,
  Save,
  FileText,
  X,
  Zap,
  Heart,
  Shield,
} from 'lucide-react';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

interface SkinMetric {
  name: string;
  score: number;
  icon: React.ElementType;
  color: string;
  barColor: string;
}

interface ProductRecommendation {
  name: string;
  reason: string;
  category: string;
  priority: 'high' | 'medium' | 'low';
}

interface DominantConcern {
  name: string;
  score: number;
  priority: 'high' | 'medium' | 'low';
}

interface SkinAnalysisResult {
  overall_score: number;
  skin_type: string;
  estimated_age_range: string;
  metrics: SkinMetric[];
  dominant_concerns: DominantConcern[];
  product_recommendations: ProductRecommendation[];
  timestamp: string;
}

interface HistoryEntry {
  id: string;
  timestamp: string;
  overall_score: number;
  skin_type: string;
  thumbnail: string;
}

const ANALYSIS_STEPS = [
  'Detecting face...',
  'Analyzing skin texture...',
  'Measuring pigmentation...',
  'Evaluating hydration...',
  'Generating your skin profile...',
];

const metricConfig: Record<string, { icon: React.ElementType; color: string; barColor: string }> = {
  acne: { icon: AlertTriangle, color: 'text-red-500', barColor: 'from-red-400 to-red-600' },
  pigmentation: { icon: Sun, color: 'text-amber-500', barColor: 'from-amber-400 to-amber-600' },
  wrinkles: { icon: Eye, color: 'text-purple-500', barColor: 'from-purple-400 to-purple-600' },
  oiliness: { icon: Droplets, color: 'text-blue-500', barColor: 'from-blue-400 to-blue-600' },
  redness: { icon: Heart, color: 'text-rose-500', barColor: 'from-rose-400 to-rose-600' },
  dark_circles: { icon: Eye, color: 'text-indigo-500', barColor: 'from-indigo-400 to-indigo-600' },
  pores: { icon: Shield, color: 'text-teal-500', barColor: 'from-teal-400 to-teal-600' },
};

function getScoreLevel(score: number): { label: string; color: string; bg: string } {
  if (score <= 3) return { label: 'Low', color: 'text-green-600', bg: 'bg-green-100' };
  if (score <= 6) return { label: 'Moderate', color: 'text-yellow-600', bg: 'bg-yellow-100' };
  return { label: 'High', color: 'text-red-600', bg: 'bg-red-100' };
}

function getOverallColor(score: number): string {
  if (score >= 70) return '#22c55e';
  if (score >= 40) return '#eab308';
  return '#ef4444';
}

function getOverallGradient(score: number): string {
  if (score >= 70) return 'from-green-400 to-emerald-500';
  if (score >= 40) return 'from-yellow-400 to-amber-500';
  return 'from-red-400 to-rose-500';
}

function getOverallLabel(score: number): string {
  if (score >= 70) return 'Good';
  if (score >= 40) return 'Moderate';
  return 'Needs Attention';
}

function formatTimestamp(ts: string): string {
  const d = new Date(ts);
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric', hour: '2-digit', minute: '2-digit' });
}

export default function SkinTwinPage() {
  const [view, setView] = useState<'upload' | 'loading' | 'results' | 'history'>('upload');
  const [capturedImage, setCapturedImage] = useState<string | null>(null);
  const [cameraActive, setCameraActive] = useState(false);
  const [cameraFacing, setCameraFacing] = useState<'user' | 'environment'>('user');
  const [cameraError, setCameraError] = useState<string | null>(null);
  const [videoReady, setVideoReady] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const [loadingStep, setLoadingStep] = useState(0);
  const [loadingProgress, setLoadingProgress] = useState(0);
  const [result, setResult] = useState<SkinAnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [history, setHistory] = useState<HistoryEntry[]>([]);

  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const loadingIntervalRef = useRef<NodeJS.Timeout | null>(null);

  const stopCamera = useCallback(() => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((t) => t.stop());
      streamRef.current = null;
    }
    if (videoRef.current) videoRef.current.srcObject = null;
    setCameraActive(false);
    setVideoReady(false);
  }, []);

  const startCamera = useCallback(async () => {
    setCameraError(null);
    setVideoReady(false);
    setCapturedImage(null);

    if (streamRef.current) {
      streamRef.current.getTracks().forEach((t) => t.stop());
      streamRef.current = null;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: cameraFacing, width: { ideal: 1280 }, height: { ideal: 720 } },
        audio: false,
      });
      streamRef.current = stream;
      setCameraActive(true);

      await new Promise<void>((resolve) => {
        const check = () => {
          if (videoRef.current) {
            videoRef.current.srcObject = stream;
            videoRef.current.onloadedmetadata = () => {
              videoRef.current?.play().then(() => { setVideoReady(true); resolve(); }).catch(() => resolve());
            };
          } else {
            setTimeout(check, 50);
          }
        };
        check();
      });
    } catch (err: any) {
      setCameraActive(false);
      if (err.name === 'NotAllowedError') setCameraError('Camera permission denied. Please allow camera access in your browser settings.');
      else if (err.name === 'NotFoundError') setCameraError('No camera found on this device.');
      else if (err.name === 'NotReadableError') setCameraError('Camera is in use by another application.');
      else setCameraError(`Camera error: ${err.message}`);
    }
  }, [cameraFacing]);

  useEffect(() => {
    return () => stopCamera();
  }, [stopCamera]);

  useEffect(() => {
    if (cameraActive && cameraFacing) {
      stopCamera();
      startCamera();
    }
  }, [cameraFacing]);

  useEffect(() => {
    if (view === 'loading') {
      let step = 0;
      loadingIntervalRef.current = setInterval(() => {
        step += 1;
        setLoadingStep(step);
        setLoadingProgress(Math.min((step / ANALYSIS_STEPS.length) * 100, 100));
        if (step >= ANALYSIS_STEPS.length) {
          if (loadingIntervalRef.current) clearInterval(loadingIntervalRef.current);
        }
      }, 800);
      return () => { if (loadingIntervalRef.current) clearInterval(loadingIntervalRef.current); };
    }
  }, [view]);

  const capturePhoto = useCallback(() => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    if (!video || !canvas || !video.videoWidth || !video.videoHeight) return;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    if (cameraFacing === 'user') {
      ctx.translate(canvas.width, 0);
      ctx.scale(-1, 1);
    }
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    ctx.setTransform(1, 0, 0, 1, 0, 0);

    const dataUrl = canvas.toDataURL('image/jpeg', 0.85);
    setCapturedImage(dataUrl);
    stopCamera();
  }, [cameraFacing, stopCamera]);

  const handleFileUpload = useCallback((file: File) => {
    if (!file.type.startsWith('image/')) {
      setError('Please upload an image file.');
      return;
    }
    const reader = new FileReader();
    reader.onload = (e) => {
      setCapturedImage(e.target?.result as string);
      setError(null);
    };
    reader.readAsDataURL(file);
  }, []);

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleFileUpload(file);
  };

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFileUpload(file);
  }, [handleFileUpload]);

  const analyzeSkin = async () => {
    if (!capturedImage) return;

    setView('loading');
    setLoadingStep(0);
    setLoadingProgress(0);
    setError(null);

    try {
      const response = await fetch(`${API_BASE}/skin-analysis/analyze-base64`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image_base64: capturedImage }),
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.detail || errData.message || `Analysis failed (${response.status})`);
      }

      const data = await response.json();
      const metrics: SkinMetric[] = (data.metrics || []).map((m: any) => {
        const key = (m.name || '').toLowerCase().replace(/\s+/g, '_').replace('-', '_');
        const cfg = metricConfig[key] || { icon: Zap, color: 'text-gray-500', barColor: 'from-gray-400 to-gray-600' };
        return {
          name: m.name,
          score: m.score,
          icon: cfg.icon,
          color: cfg.color,
          barColor: cfg.barColor,
        };
      });

      const parsed: SkinAnalysisResult = {
        overall_score: data.overall_score ?? 70,
        skin_type: data.skin_type ?? 'Normal',
        estimated_age_range: data.estimated_age_range ?? '25-34',
        metrics,
        dominant_concerns: data.dominant_concerns ?? [],
        product_recommendations: data.product_recommendations ?? [],
        timestamp: new Date().toISOString(),
      };

      setResult(parsed);

      const historyEntry: HistoryEntry = {
        id: Date.now().toString(),
        timestamp: parsed.timestamp,
        overall_score: parsed.overall_score,
        skin_type: parsed.skin_type,
        thumbnail: capturedImage,
      };
      setHistory((prev) => [historyEntry, ...prev]);

      setView('results');
    } catch (err: any) {
      setError(err.message || 'Something went wrong during analysis. Please try again.');
      setView('upload');
    }
  };

  const resetToUpload = () => {
    setCapturedImage(null);
    setResult(null);
    setError(null);
    setView('upload');
  };

  const circularProgress = (score: number, size = 200, strokeWidth = 12) => {
    const radius = (size - strokeWidth) / 2;
    const circumference = 2 * Math.PI * radius;
    const offset = circumference - (score / 100) * circumference;
    const color = getOverallColor(score);

    return (
      <div className="relative" style={{ width: size, height: size }}>
        <svg width={size} height={size} className="-rotate-90">
          <circle cx={size / 2} cy={size / 2} r={radius} fill="none" stroke="#e5e7eb" strokeWidth={strokeWidth} />
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            stroke={color}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            strokeLinecap="round"
            className="transition-all duration-1000 ease-out"
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-5xl font-bold text-gray-900">{score}</span>
          <span className="text-sm text-gray-500">/ 100</span>
          <span className={`text-sm font-medium mt-1 ${score >= 70 ? 'text-green-600' : score >= 40 ? 'text-yellow-600' : 'text-red-600'}`}>
            {getOverallLabel(score)}
          </span>
        </div>
      </div>
    );
  };

  const priorityBadge = (priority: string) => {
    const styles: Record<string, string> = {
      high: 'bg-red-100 text-red-700 border-red-200',
      medium: 'bg-yellow-100 text-yellow-700 border-yellow-200',
      low: 'bg-green-100 text-green-700 border-green-200',
    };
    return (
      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${styles[priority] || styles.medium}`}>
        {priority.charAt(0).toUpperCase() + priority.slice(1)}
      </span>
    );
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <canvas ref={canvasRef} className="hidden" />

      {/* Header */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-2 flex items-center justify-center gap-3">
          <Sparkles className="w-9 h-9 text-pink-500" />
          AI Skin Digital Twin
        </h1>
        <p className="text-gray-500 max-w-xl mx-auto">
          Upload a selfie and get a comprehensive AI-powered analysis of your skin health with personalized recommendations.
        </p>
      </motion.div>

      {/* Navigation Tabs */}
      <div className="flex justify-center gap-3">
        {[
          { id: 'upload' as const, label: 'Analyze', icon: Camera },
          { id: 'history' as const, label: 'History', icon: Clock },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => { if (tab.id === 'history') setView('history'); else if (view === 'history') resetToUpload(); }}
            className={`flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-medium transition-all ${
              view === tab.id || (view === 'results' && tab.id === 'upload')
                ? 'bg-gradient-to-r from-pink-500 to-purple-500 text-white shadow-lg shadow-pink-500/25'
                : 'bg-white border border-gray-200 text-gray-600 hover:border-gray-300 hover:text-gray-900'
            }`}
          >
            <tab.icon className="w-4 h-4" />
            {tab.label}
          </button>
        ))}
      </div>

      {/* Error Display */}
      <AnimatePresence>
        {error && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="bg-red-50 border border-red-200 rounded-xl p-4 flex items-center gap-3"
          >
            <AlertTriangle className="w-5 h-5 text-red-500 flex-shrink-0" />
            <span className="text-red-700 text-sm flex-1">{error}</span>
            <button onClick={() => setError(null)} className="text-red-400 hover:text-red-600">
              <X className="w-4 h-4" />
            </button>
          </motion.div>
        )}
      </AnimatePresence>

      {/* ==================== UPLOAD SECTION ==================== */}
      {view === 'upload' && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
          {/* Camera Preview */}
          <AnimatePresence>
            {cameraActive && !capturedImage && (
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                className="relative rounded-2xl overflow-hidden bg-gray-900"
              >
                <video
                  ref={videoRef}
                  autoPlay
                  playsInline
                  muted
                  className="w-full rounded-2xl"
                  style={{ transform: cameraFacing === 'user' ? 'scaleX(-1)' : 'none' }}
                />
                {cameraActive && videoReady && (
                  <div className="absolute inset-0 flex items-end justify-center pb-6 gap-4">
                    <button
                      onClick={() => setCameraFacing((f) => f === 'user' ? 'environment' : 'user')}
                      className="p-3 bg-white/80 backdrop-blur-md rounded-full text-gray-800 hover:bg-white transition-all shadow-lg"
                      title="Switch Camera"
                    >
                      <SwitchCamera className="w-5 h-5" />
                    </button>
                    <button
                      onClick={capturePhoto}
                      className="w-16 h-16 rounded-full bg-white border-4 border-pink-500 hover:bg-pink-50 transition-all flex items-center justify-center shadow-lg shadow-pink-500/30"
                      title="Capture Photo"
                    >
                      <div className="w-12 h-12 rounded-full bg-pink-500" />
                    </button>
                    <button
                      onClick={stopCamera}
                      className="p-3 bg-white/80 backdrop-blur-md rounded-full text-gray-800 hover:bg-white transition-all shadow-lg"
                      title="Close Camera"
                    >
                      <X className="w-5 h-5" />
                    </button>
                  </div>
                )}
                {cameraActive && (
                  <div className="absolute top-4 left-4 right-4 flex justify-center">
                    <span className="px-3 py-1 bg-white/80 backdrop-blur-sm rounded-full text-gray-800 text-xs flex items-center gap-2 shadow">
                      <span className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
                      Live
                    </span>
                  </div>
                )}
                {/* Face guide */}
                <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                  <div className="w-48 h-64 md:w-56 md:h-72 border-2 border-white/40 rounded-[50%]">
                    <div className="absolute top-0 left-0 w-8 h-8 border-t-2 border-l-2 border-pink-400 rounded-tl-full" />
                    <div className="absolute top-0 right-0 w-8 h-8 border-t-2 border-r-2 border-pink-400 rounded-tr-full" />
                    <div className="absolute bottom-0 left-0 w-8 h-8 border-b-2 border-l-2 border-pink-400 rounded-bl-full" />
                    <div className="absolute bottom-0 right-0 w-8 h-8 border-b-2 border-r-2 border-pink-400 rounded-br-full" />
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Camera Error */}
          {cameraError && !cameraActive && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="bg-red-50 border border-red-200 rounded-xl p-6 text-center">
              <AlertTriangle className="w-10 h-10 text-red-400 mx-auto mb-3" />
              <p className="text-red-700 text-sm mb-4">{cameraError}</p>
              <div className="flex justify-center gap-3">
                <button onClick={startCamera} className="px-4 py-2 bg-gradient-to-r from-pink-500 to-purple-500 text-white rounded-xl text-sm font-medium shadow-lg shadow-pink-500/25 hover:from-pink-600 hover:to-purple-600 transition-all">
                  Try Again
                </button>
                <button onClick={() => fileInputRef.current?.click()} className="px-4 py-2 bg-white border border-gray-200 text-gray-700 rounded-xl text-sm font-medium hover:border-gray-300 transition-all">
                  <Upload className="w-4 h-4 mr-1.5 inline" /> Upload Instead
                </button>
              </div>
            </motion.div>
          )}

          {/* Preview of captured / uploaded image */}
          {capturedImage && view === 'upload' && (
            <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} className="space-y-4">
              <div className="relative rounded-2xl overflow-hidden bg-white border border-gray-200 shadow-sm">
                <img src={capturedImage} alt="Preview" className="w-full max-h-[500px] object-contain" />
                <button
                  onClick={resetToUpload}
                  className="absolute top-4 right-4 p-2 bg-white/80 backdrop-blur-md rounded-full text-gray-700 hover:bg-white transition-all shadow"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
              <div className="flex justify-center gap-4">
                <button onClick={resetToUpload} className="px-6 py-3 bg-white border border-gray-200 text-gray-700 rounded-xl font-medium hover:border-gray-300 transition-all flex items-center gap-2 shadow-sm">
                  <RefreshCw className="w-4 h-4" /> Retake
                </button>
                <button onClick={analyzeSkin} className="px-8 py-3 bg-gradient-to-r from-pink-500 to-purple-500 text-white rounded-xl font-semibold shadow-lg shadow-pink-500/25 hover:from-pink-600 hover:to-purple-600 transition-all flex items-center gap-2">
                  <Sparkles className="w-5 h-5" /> Analyze My Skin
                </button>
              </div>
            </motion.div>
          )}

          {/* Upload Zone (shown when no image and camera is off) */}
          {!capturedImage && !cameraActive && (
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="space-y-6">
              <div
                onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
                onDragLeave={() => setIsDragging(false)}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
                className={`border-2 border-dashed rounded-2xl p-16 text-center cursor-pointer transition-all duration-300 ${
                  isDragging ? 'border-pink-500 bg-pink-50' : 'border-gray-300 hover:border-pink-400 hover:bg-gray-50 bg-white'
                }`}
              >
                <div className="w-16 h-16 bg-gradient-to-r from-pink-500/20 to-purple-500/20 rounded-2xl flex items-center justify-center mx-auto mb-5">
                  <Camera className="w-8 h-8 text-pink-500" />
                </div>
                <p className="text-lg font-semibold text-gray-900 mb-2">Upload a selfie or take a photo</p>
                <p className="text-sm text-gray-500 mb-5">Drag & drop your image here, or click to browse</p>
                <div className="flex justify-center gap-3">
                  <span className="px-5 py-2.5 bg-gradient-to-r from-pink-500 to-purple-500 text-white rounded-xl text-sm font-medium shadow-lg shadow-pink-500/25 hover:from-pink-600 hover:to-purple-600 transition-all inline-flex items-center gap-2">
                    <Upload className="w-4 h-4" /> Choose from Gallery
                  </span>
                </div>
              </div>

              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleFileInput}
                className="hidden"
              />

              <div className="flex justify-center">
                <button
                  onClick={startCamera}
                  className="px-6 py-3 bg-white border border-gray-200 text-gray-700 rounded-xl font-medium hover:border-gray-300 hover:text-gray-900 transition-all flex items-center gap-2 shadow-sm"
                >
                  <Camera className="w-5 h-5" /> Take Photo
                </button>
              </div>

              {/* Tips */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {[
                  { icon: Sun, title: 'Good Lighting', desc: 'Face a natural light source for best results' },
                  { icon: Eye, title: 'Front-Facing', desc: 'Look straight at the camera with a neutral expression' },
                  { icon: Sparkles, title: 'No Makeup', desc: 'Remove makeup and filters for accurate analysis' },
                ].map((tip, idx) => (
                  <motion.div
                    key={tip.title}
                    initial={{ opacity: 0, y: 15 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 + idx * 0.1 }}
                    className="bg-white border border-gray-200 rounded-xl p-4 text-center shadow-sm"
                  >
                    <tip.icon className="w-6 h-6 text-pink-500 mx-auto mb-2" />
                    <p className="text-sm font-medium text-gray-900 mb-1">{tip.title}</p>
                    <p className="text-xs text-gray-500">{tip.desc}</p>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          )}
        </motion.div>
      )}

      {/* ==================== LOADING SECTION ==================== */}
      {view === 'loading' && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="max-w-lg mx-auto text-center py-16 space-y-8">
          <div className="w-20 h-20 bg-gradient-to-r from-pink-500 to-purple-500 rounded-2xl flex items-center justify-center mx-auto shadow-lg shadow-pink-500/25">
            <Sparkles className="w-10 h-10 text-white animate-pulse" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Analyzing Your Skin</h2>
            <p className="text-gray-500">Our AI is examining your skin in detail...</p>
          </div>
          <div className="space-y-4">
            <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
              <motion.div
                className="h-full bg-gradient-to-r from-pink-500 to-purple-500 rounded-full"
                initial={{ width: '0%' }}
                animate={{ width: `${loadingProgress}%` }}
                transition={{ duration: 0.5 }}
              />
            </div>
            <AnimatePresence mode="wait">
              <motion.p
                key={loadingStep}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="text-sm text-gray-600 font-medium"
              >
                {loadingStep > 0 ? ANALYSIS_STEPS[Math.min(loadingStep - 1, ANALYSIS_STEPS.length - 1)] : 'Preparing...'}
              </motion.p>
            </AnimatePresence>
          </div>
          <div className="flex justify-center gap-3">
            {ANALYSIS_STEPS.map((_, idx) => (
              <div
                key={idx}
                className={`w-2.5 h-2.5 rounded-full transition-all duration-300 ${
                  idx < loadingStep ? 'bg-gradient-to-r from-pink-500 to-purple-500 scale-110' : 'bg-gray-200'
                }`}
              />
            ))}
          </div>
        </motion.div>
      )}

      {/* ==================== RESULTS SECTION ==================== */}
      {view === 'results' && result && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-8">
          {/* Back Button */}
          <button
            onClick={resetToUpload}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors text-sm font-medium"
          >
            <ArrowLeft className="w-4 h-4" /> Back to Upload
          </button>

          {/* Overall Score + Skin Type */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="bg-white border border-gray-200 rounded-2xl p-8 shadow-sm">
            <div className="flex flex-col md:flex-row items-center gap-8">
              <div className="flex-shrink-0">{circularProgress(result.overall_score)}</div>
              <div className="flex-1 text-center md:text-left">
                <h2 className="text-2xl font-bold text-gray-900 mb-1">Your Skin Health Score</h2>
                <p className="text-gray-500 mb-4">Based on AI analysis of your latest photo</p>
                <div className="flex flex-wrap justify-center md:justify-start gap-3">
                  <span className="inline-flex items-center px-3 py-1.5 rounded-full text-sm font-medium bg-pink-100 text-pink-700 border border-pink-200">
                    <Sparkles className="w-3.5 h-3.5 mr-1.5" /> {result.skin_type}
                  </span>
                  <span className="inline-flex items-center px-3 py-1.5 rounded-full text-sm font-medium bg-purple-100 text-purple-700 border border-purple-200">
                    <Eye className="w-3.5 h-3.5 mr-1.5" /> Est. Age: {result.estimated_age_range}
                  </span>
                </div>
              </div>
              <div className="hidden lg:block">
                {capturedImage && (
                  <img src={capturedImage} alt="Your selfie" className="w-24 h-24 rounded-xl object-cover border-2 border-gray-200" />
                )}
              </div>
            </div>
          </motion.div>

          {/* Skin Metrics Grid */}
          <div>
            <h3 className="text-xl font-bold text-gray-900 mb-4">Skin Metrics</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {result.metrics.map((metric, idx) => {
                const level = getScoreLevel(metric.score);
                const MetricIcon = metric.icon;
                return (
                  <motion.div
                    key={metric.name}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: idx * 0.07 }}
                    className="bg-white border border-gray-200 rounded-xl p-5 shadow-sm hover:border-gray-300 hover:shadow-md transition-all"
                  >
                    <div className="flex items-center gap-3 mb-3">
                      <div className={`w-10 h-10 rounded-lg bg-gradient-to-r ${metric.barColor} bg-opacity-10 flex items-center justify-center`}
                        style={{ backgroundColor: `${metric.score <= 3 ? '#dcfce7' : metric.score <= 6 ? '#fef9c3' : '#fee2e2'}` }}>
                        <MetricIcon className={`w-5 h-5 ${metric.color}`} />
                      </div>
                      <div className="flex-1">
                        <p className="text-sm font-semibold text-gray-900">{metric.name}</p>
                        <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${level.bg} ${level.color}`}>
                          {level.label}
                        </span>
                      </div>
                      <span className="text-lg font-bold text-gray-900">{metric.score}<span className="text-xs text-gray-400 font-normal">/10</span></span>
                    </div>
                    <div className="w-full bg-gray-100 rounded-full h-2 overflow-hidden">
                      <motion.div
                        className={`h-full rounded-full bg-gradient-to-r ${metric.barColor}`}
                        initial={{ width: 0 }}
                        animate={{ width: `${(metric.score / 10) * 100}%` }}
                        transition={{ delay: 0.3 + idx * 0.07, duration: 0.6 }}
                      />
                    </div>
                  </motion.div>
                );
              })}
            </div>
          </div>

          {/* Dominant Concerns */}
          {result.dominant_concerns.length > 0 && (
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}>
              <h3 className="text-xl font-bold text-gray-900 mb-4">Dominant Concerns</h3>
              <div className="flex flex-wrap gap-3">
                {result.dominant_concerns.map((concern, idx) => (
                  <motion.div
                    key={concern.name}
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.4 + idx * 0.1 }}
                    className="bg-white border border-gray-200 rounded-xl px-5 py-3 shadow-sm flex items-center gap-3"
                  >
                    <AlertTriangle className={`w-5 h-5 ${concern.priority === 'high' ? 'text-red-500' : concern.priority === 'medium' ? 'text-yellow-500' : 'text-green-500'}`} />
                    <div>
                      <p className="text-sm font-semibold text-gray-900">{concern.name}</p>
                      <p className="text-xs text-gray-500">Score: {concern.score}/10</p>
                    </div>
                    {priorityBadge(concern.priority)}
                  </motion.div>
                ))}
              </div>
            </motion.div>
          )}

          {/* Product Recommendations */}
          {result.product_recommendations.length > 0 && (
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }}>
              <h3 className="text-xl font-bold text-gray-900 mb-4">Product Recommendations</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {result.product_recommendations.map((rec, idx) => (
                  <motion.div
                    key={rec.name}
                    initial={{ opacity: 0, y: 15 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.5 + idx * 0.08 }}
                    className="bg-white border border-gray-200 rounded-xl p-5 shadow-sm hover:border-gray-300 hover:shadow-md transition-all"
                  >
                    <div className="flex items-start justify-between gap-2 mb-3">
                      <h4 className="text-sm font-bold text-gray-900 leading-tight">{rec.name}</h4>
                      {priorityBadge(rec.priority)}
                    </div>
                    <p className="text-xs text-gray-500 mb-3 line-clamp-2">{rec.reason}</p>
                    <div className="flex items-center gap-2">
                      <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-700 border border-purple-200">
                        {rec.category}
                      </span>
                    </div>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          )}

          {/* Action Buttons */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.6 }} className="flex flex-wrap justify-center gap-4 pt-4">
            <button
              onClick={resetToUpload}
              className="px-6 py-3 bg-white border border-gray-200 text-gray-700 rounded-xl font-medium hover:border-gray-300 hover:text-gray-900 transition-all flex items-center gap-2 shadow-sm"
            >
              <RefreshCw className="w-4 h-4" /> Retake Photo
            </button>
            <button
              onClick={() => {
                try {
                  const saved = JSON.parse(localStorage.getItem('skinTwinHistory') || '[]');
                  const entry = { ...result, thumbnail: capturedImage, savedAt: new Date().toISOString() };
                  localStorage.setItem('skinTwinHistory', JSON.stringify([entry, ...saved].slice(0, 20)));
                  alert('Analysis saved to your profile!');
                } catch { alert('Failed to save. Please try again.'); }
              }}
              className="px-6 py-3 bg-gradient-to-r from-pink-500 to-purple-500 text-white rounded-xl font-semibold shadow-lg shadow-pink-500/25 hover:from-pink-600 hover:to-purple-600 transition-all flex items-center gap-2"
            >
              <Save className="w-4 h-4" /> Save to Profile
            </button>
            <button
              onClick={() => alert('Full report feature coming soon!')}
              className="px-6 py-3 bg-white border border-gray-200 text-gray-700 rounded-xl font-medium hover:border-gray-300 hover:text-gray-900 transition-all flex items-center gap-2 shadow-sm"
            >
              <FileText className="w-4 h-4" /> View Full Report
            </button>
          </motion.div>
        </motion.div>
      )}

      {/* ==================== HISTORY SECTION ==================== */}
      {view === 'history' && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
          <button
            onClick={resetToUpload}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors text-sm font-medium"
          >
            <ArrowLeft className="w-4 h-4" /> Back to Upload
          </button>

          <h2 className="text-2xl font-bold text-gray-900">Analysis History</h2>

          {history.length === 0 ? (
            <div className="bg-white border border-gray-200 rounded-2xl p-16 text-center shadow-sm">
              <Clock className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">No analyses yet</h3>
              <p className="text-gray-500 text-sm mb-6">Your skin analysis history will appear here</p>
              <button
                onClick={resetToUpload}
                className="px-6 py-3 bg-gradient-to-r from-pink-500 to-purple-500 text-white rounded-xl font-semibold shadow-lg shadow-pink-500/25 hover:from-pink-600 hover:to-purple-600 transition-all inline-flex items-center gap-2"
              >
                <Camera className="w-4 h-4" /> Start First Analysis
              </button>
            </div>
          ) : (
            <div className="relative">
              {/* Timeline line */}
              <div className="absolute left-6 top-0 bottom-0 w-0.5 bg-gray-200" />
              <div className="space-y-6">
                {history.map((entry, idx) => {
                  const scoreColor = entry.overall_score >= 70 ? 'bg-green-500' : entry.overall_score >= 40 ? 'bg-yellow-500' : 'bg-red-500';
                  return (
                    <motion.div
                      key={entry.id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: idx * 0.1 }}
                      className="relative pl-14"
                    >
                      {/* Timeline dot */}
                      <div className={`absolute left-4 top-6 w-5 h-5 rounded-full ${scoreColor} border-4 border-white shadow-sm`} />

                      <div className="bg-white border border-gray-200 rounded-xl p-4 shadow-sm hover:border-gray-300 hover:shadow-md transition-all">
                        <div className="flex items-center gap-4">
                          {entry.thumbnail && (
                            <img src={entry.thumbnail} alt="Thumbnail" className="w-14 h-14 rounded-lg object-cover border border-gray-200 flex-shrink-0" />
                          )}
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-3 mb-1">
                              <span className="text-lg font-bold text-gray-900">{entry.overall_score}/100</span>
                              <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${
                                entry.overall_score >= 70 ? 'bg-green-100 text-green-700' : entry.overall_score >= 40 ? 'bg-yellow-100 text-yellow-700' : 'bg-red-100 text-red-700'
                              }`}>
                                {getOverallLabel(entry.overall_score)}
                              </span>
                            </div>
                            <div className="flex items-center gap-3 text-xs text-gray-500">
                              <span className="capitalize">{entry.skin_type}</span>
                              <span>|</span>
                              <span>{formatTimestamp(entry.timestamp)}</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    </motion.div>
                  );
                })}
              </div>
            </div>
          )}
        </motion.div>
      )}
    </div>
  );
}
