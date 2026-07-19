'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Shield,
  AlertTriangle,
  Zap,
  CheckCircle,
  Search,
  X,
  ChevronDown,
  ChevronRight,
  Sparkles,
} from 'lucide-react';

interface Ingredient {
  name: string;
  category: string;
  description: string;
  pairs_well_with: string[];
  avoid_with: string[];
  safety_level: string;
}

interface Interaction {
  ingredient_1: string;
  ingredient_2: string;
  severity: 'synergistic' | 'caution' | 'avoid' | 'safe';
  description: string;
  recommendation: string;
  scientific_basis: string;
}

interface CheckResult {
  interactions: Interaction[];
  overall_safety: 'safe' | 'caution' | 'avoid';
  safety_score: number;
  routine_tip: string;
  conflicts_count: number;
  synergies_count: number;
  safe_count: number;
}

interface PopularCombo {
  name: string;
  ingredients: string[];
  safety: string;
  description: string;
}

interface Encyclopedia {
  avoid: { pair: string; description: string }[];
  caution: { pair: string; description: string }[];
  synergistic: { pair: string; description: string }[];
  total_interactions: number;
}

const QUICK_ADD = ['Retinol', 'Vitamin C', 'Niacinamide', 'AHA', 'BHA', 'Hyaluronic Acid', 'SPF'];

const INGREDIENT_COLORS: Record<string, string> = {
  retinol: 'bg-amber-100 text-amber-800 border-amber-300',
  'vitamin c': 'bg-orange-100 text-orange-800 border-orange-300',
  niacinamide: 'bg-blue-100 text-blue-800 border-blue-300',
  aha: 'bg-pink-100 text-pink-800 border-pink-300',
  bha: 'bg-purple-100 text-purple-800 border-purple-300',
  'hyaluronic acid': 'bg-cyan-100 text-cyan-800 border-cyan-300',
  spf: 'bg-green-100 text-green-800 border-green-300',
};

const DEFAULT_COLOR = 'bg-gray-100 text-gray-800 border-gray-300';

function getIngredientColor(name: string): string {
  const lower = name.toLowerCase();
  for (const [key, color] of Object.entries(INGREDIENT_COLORS)) {
    if (lower.includes(key)) return color;
  }
  const colors = [
    'bg-teal-100 text-teal-800 border-teal-300',
    'bg-indigo-100 text-indigo-800 border-indigo-300',
    'bg-rose-100 text-rose-800 border-rose-300',
    'bg-lime-100 text-lime-800 border-lime-300',
    'bg-fuchsia-100 text-fuchsia-800 border-fuchsia-300',
  ];
  let hash = 0;
  for (let i = 0; i < lower.length; i++) hash = lower.charCodeAt(i) + ((hash << 5) - hash);
  return colors[Math.abs(hash) % colors.length];
}

function getSeverityIcon(severity: string) {
  switch (severity) {
    case 'avoid':
      return <AlertTriangle className="w-5 h-5 text-red-500" />;
    case 'caution':
      return <Shield className="w-5 h-5 text-yellow-500" />;
    case 'synergistic':
      return <Zap className="w-5 h-5 text-green-500" />;
    default:
      return <CheckCircle className="w-5 h-5 text-gray-400" />;
  }
}

function getSeverityBadge(severity: string) {
  const base = 'px-2.5 py-0.5 rounded-full text-xs font-semibold uppercase tracking-wide';
  switch (severity) {
    case 'avoid':
      return `${base} bg-red-100 text-red-700`;
    case 'caution':
      return `${base} bg-yellow-100 text-yellow-700`;
    case 'synergistic':
      return `${base} bg-green-100 text-green-700`;
    default:
      return `${base} bg-gray-100 text-gray-600`;
  }
}

function getSafetyBannerColor(safety: string) {
  switch (safety) {
    case 'avoid':
      return 'from-red-500 to-red-600';
    case 'caution':
      return 'from-yellow-500 to-amber-500';
    default:
      return 'from-green-500 to-emerald-500';
  }
}

function getSafetyScoreColor(score: number) {
  if (score >= 70) return 'text-green-600';
  if (score >= 40) return 'text-yellow-600';
  return 'text-red-600';
}

function getScoreRingColor(score: number) {
  if (score >= 70) return '#22c55e';
  if (score >= 40) return '#eab308';
  return '#ef4444';
}

export default function InteractionsPage() {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState<Ingredient[]>([]);
  const [selected, setSelected] = useState<string[]>([]);
  const [result, setResult] = useState<CheckResult | null>(null);
  const [popular, setPopular] = useState<PopularCombo[]>([]);
  const [encyclopedia, setEncyclopedia] = useState<Encyclopedia | null>(null);
  const [loading, setLoading] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [expandedInteractions, setExpandedInteractions] = useState<Set<number>>(new Set());
  const [expandedEncyc, setExpandedEncyc] = useState<Set<string>>(new Set());
  const searchRef = useRef<HTMLDivElement>(null);
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    fetch('http://localhost:8000/api/v1/interactions/popular')
      .then((r) => r.json())
      .then(setPopular)
      .catch(() => {});
    fetch('http://localhost:8000/api/v1/interactions/encyclopedia')
      .then((r) => r.json())
      .then(setEncyclopedia)
      .catch(() => {});
  }, []);

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (searchRef.current && !searchRef.current.contains(e.target as Node)) {
        setShowSuggestions(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSearch = useCallback((value: string) => {
    setQuery(value);
    if (debounceRef.current) clearTimeout(debounceRef.current);
    if (!value.trim()) {
      setSuggestions([]);
      setShowSuggestions(false);
      return;
    }
    debounceRef.current = setTimeout(() => {
      fetch(`http://localhost:8000/api/v1/interactions/ingredients/search/${encodeURIComponent(value.trim())}`)
        .then((r) => r.json())
        .then((data: Ingredient[]) => {
          setSuggestions(data.filter((i) => !selected.includes(i.name)));
          setShowSuggestions(true);
        })
        .catch(() => setSuggestions([]));
    }, 300);
  }, [selected]);

  function addIngredient(name: string) {
    if (!selected.includes(name)) {
      setSelected((prev) => [...prev, name]);
      setResult(null);
    }
    setQuery('');
    setSuggestions([]);
    setShowSuggestions(false);
  }

  function removeIngredient(name: string) {
    setSelected((prev) => prev.filter((i) => i !== name));
    setResult(null);
  }

  async function checkInteractions() {
    if (selected.length < 2) return;
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/api/v1/interactions/check', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ingredients: selected }),
      });
      const data: CheckResult = await res.json();
      setResult(data);
      setExpandedInteractions(new Set());
    } catch {
      console.error('Failed to check interactions');
    } finally {
      setLoading(false);
    }
  }

  function toggleInteraction(index: number) {
    setExpandedInteractions((prev) => {
      const next = new Set(prev);
      if (next.has(index)) next.delete(index);
      else next.add(index);
      return next;
    });
  }

  function toggleEncyc(section: string) {
    setExpandedEncyc((prev) => {
      const next = new Set(prev);
      if (next.has(section)) next.delete(section);
      else next.add(section);
      return next;
    });
  }

  function loadPopular(combo: PopularCombo) {
    setSelected(combo.ingredients);
    setResult(null);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  const safetyScore = result?.safety_score ?? 0;
  const circumference = 2 * Math.PI * 44;
  const dashoffset = circumference - (safetyScore / 100) * circumference;

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-br from-violet-600 via-purple-600 to-indigo-700 text-white">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-10 left-10 w-72 h-72 bg-white rounded-full blur-3xl" />
          <div className="absolute bottom-10 right-10 w-96 h-96 bg-white rounded-full blur-3xl" />
        </div>
        <div className="relative max-w-5xl mx-auto px-4 py-20 text-center">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}>
            <Shield className="w-16 h-16 mx-auto mb-6 opacity-90" />
            <h1 className="text-4xl md:text-5xl font-bold mb-4">Ingredient Interaction Checker</h1>
            <p className="text-lg md:text-xl text-purple-100 max-w-2xl mx-auto">
              Discover which skincare ingredients work beautifully together and which ones should never meet. Build a safer, more effective routine.
            </p>
          </motion.div>
        </div>
      </section>

      <div className="max-w-5xl mx-auto px-4 py-10 space-y-12">
        {/* Input Section */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.5 }}
          className="glass-card bg-white rounded-2xl shadow-lg border border-gray-200 p-6 md:p-8"
        >
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <Search className="w-5 h-5 text-purple-500" />
            Add Ingredients
          </h2>

          <div className="relative mb-4" ref={searchRef}>
            <input
              type="text"
              value={query}
              onChange={(e) => handleSearch(e.target.value)}
              onFocus={() => suggestions.length > 0 && setShowSuggestions(true)}
              placeholder="Search for an ingredient..."
              className="input-glass w-full px-4 py-3 rounded-xl border border-gray-200 bg-gray-50 text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-400 focus:border-transparent transition-all"
            />
            <AnimatePresence>
              {showSuggestions && suggestions.length > 0 && (
                <motion.div
                  initial={{ opacity: 0, y: -4 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -4 }}
                  className="absolute z-20 mt-1 w-full bg-white rounded-xl shadow-xl border border-gray-200 max-h-64 overflow-y-auto"
                >
                  {suggestions.map((s) => (
                    <button
                      key={s.name}
                      onClick={() => addIngredient(s.name)}
                      className="w-full text-left px-4 py-3 hover:bg-purple-50 transition-colors flex flex-col gap-0.5"
                    >
                      <span className="font-medium text-gray-900">{s.name}</span>
                      <span className="text-xs text-gray-500">{s.category} — {s.description}</span>
                    </button>
                  ))}
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Selected Chips */}
          <div className="flex flex-wrap gap-2 mb-4 min-h-[40px]">
            <AnimatePresence mode="popLayout">
              {selected.map((ing) => (
                <motion.span
                  key={ing}
                  layout
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.8 }}
                  className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-sm font-medium border ${getIngredientColor(ing)}`}
                >
                  {ing}
                  <button onClick={() => removeIngredient(ing)} className="hover:opacity-60 transition-opacity">
                    <X className="w-3.5 h-3.5" />
                  </button>
                </motion.span>
              ))}
            </AnimatePresence>
            {selected.length === 0 && (
              <span className="text-sm text-gray-400 py-1.5">No ingredients selected yet</span>
            )}
          </div>

          {/* Quick Add */}
          <div className="flex flex-wrap gap-2 mb-6">
            <span className="text-xs font-medium text-gray-500 uppercase tracking-wide self-center mr-1">Quick add:</span>
            {QUICK_ADD.map((ing) => (
              <button
                key={ing}
                onClick={() => addIngredient(ing)}
                disabled={selected.includes(ing)}
                className="px-3 py-1.5 rounded-full text-xs font-semibold border transition-all disabled:opacity-30 disabled:cursor-not-allowed border-purple-200 text-purple-700 bg-purple-50 hover:bg-purple-100"
              >
                + {ing}
              </button>
            ))}
          </div>

          {/* Check Button */}
          <button
            onClick={checkInteractions}
            disabled={selected.length < 2 || loading}
            className="w-full md:w-auto px-8 py-3.5 rounded-xl font-semibold text-white bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 shadow-lg shadow-purple-200 transition-all disabled:opacity-40 disabled:cursor-not-allowed disabled:shadow-none flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <svg className="animate-spin w-5 h-5" viewBox="0 0 24 24" fill="none">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
                Checking...
              </>
            ) : (
              <>
                <Zap className="w-5 h-5" />
                Check Interactions
              </>
            )}
          </button>
        </motion.section>

        {/* Results Section */}
        <AnimatePresence>
          {result && (
            <motion.section
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.5 }}
              className="space-y-6"
            >
              {/* Safety Banner */}
              <div className={`bg-gradient-to-r ${getSafetyBannerColor(result.overall_safety)} rounded-2xl p-6 text-white text-center shadow-lg`}>
                <div className="flex items-center justify-center gap-3 mb-2">
                  {result.overall_safety === 'avoid' && <AlertTriangle className="w-7 h-7" />}
                  {result.overall_safety === 'caution' && <Shield className="w-7 h-7" />}
                  {result.overall_safety === 'safe' && <CheckCircle className="w-7 h-7" />}
                  <span className="text-2xl font-bold uppercase tracking-wide">
                    {result.overall_safety === 'avoid' && 'Conflicts Detected'}
                    {result.overall_safety === 'caution' && 'Use With Caution'}
                    {result.overall_safety === 'safe' && 'Safe Combination'}
                  </span>
                </div>
                <p className="text-sm opacity-90">Your ingredient combination has been analyzed for safety.</p>
              </div>

              {/* Score + Stats */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                {/* Score Circle */}
                <div className="glass-card bg-white rounded-2xl shadow-md border border-gray-200 p-6 flex flex-col items-center justify-center md:col-span-1">
                  <svg width="100" height="100" className="mb-2">
                    <circle cx="50" cy="50" r="44" fill="none" stroke="#e5e7eb" strokeWidth="8" />
                    <circle
                      cx="50"
                      cy="50"
                      r="44"
                      fill="none"
                      stroke={getScoreRingColor(safetyScore)}
                      strokeWidth="8"
                      strokeLinecap="round"
                      strokeDasharray={circumference}
                      strokeDashoffset={dashoffset}
                      transform="rotate(-90 50 50)"
                      className="transition-all duration-1000 ease-out"
                    />
                    <text x="50" y="48" textAnchor="middle" className={`text-2xl font-bold ${getSafetyScoreColor(safetyScore)}`} fill="currentColor">
                      {safetyScore}
                    </text>
                    <text x="50" y="64" textAnchor="middle" className="text-[10px] font-medium fill-gray-500">
                      SAFETY
                    </text>
                  </svg>
                </div>

                {/* Stats */}
                {[
                  { label: 'Conflicts', value: result.conflicts_count, icon: <AlertTriangle className="w-5 h-5 text-red-500" />, bg: 'bg-red-50', border: 'border-red-200' },
                  { label: 'Synergies', value: result.synergies_count, icon: <Zap className="w-5 h-5 text-green-500" />, bg: 'bg-green-50', border: 'border-green-200' },
                  { label: 'Safe', value: result.safe_count, icon: <CheckCircle className="w-5 h-5 text-gray-400" />, bg: 'bg-gray-50', border: 'border-gray-200' },
                ].map((stat) => (
                  <div key={stat.label} className={`glass-card ${stat.bg} rounded-2xl shadow-md border ${stat.border} p-5 flex items-center gap-4`}>
                    <div className="p-2.5 rounded-xl bg-white shadow-sm">{stat.icon}</div>
                    <div>
                      <div className="text-2xl font-bold text-gray-900">{stat.value}</div>
                      <div className="text-sm text-gray-500">{stat.label}</div>
                    </div>
                  </div>
                ))}
              </div>

              {/* Interaction Cards */}
              {result.interactions.length > 0 && (
                <div className="space-y-3">
                  <h3 className="text-lg font-semibold flex items-center gap-2">
                    <Sparkles className="w-5 h-5 text-purple-500" />
                    Interaction Details
                  </h3>
                  {result.interactions.map((inter, idx) => (
                    <motion.div
                      key={idx}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: idx * 0.05 }}
                      className="glass-card bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden"
                    >
                      <button
                        onClick={() => toggleInteraction(idx)}
                        className="w-full px-5 py-4 flex items-center gap-3 text-left hover:bg-gray-50 transition-colors"
                      >
                        <span className="font-medium text-gray-900">{inter.ingredient_1}</span>
                        <span className="flex-shrink-0">{getSeverityIcon(inter.severity)}</span>
                        <span className="font-medium text-gray-900">{inter.ingredient_2}</span>
                        <span className={`${getSeverityBadge(inter.severity)} ml-auto mr-2`}>{inter.severity}</span>
                        {expandedInteractions.has(idx) ? (
                          <ChevronDown className="w-4 h-4 text-gray-400" />
                        ) : (
                          <ChevronRight className="w-4 h-4 text-gray-400" />
                        )}
                      </button>
                      <AnimatePresence>
                        {expandedInteractions.has(idx) && (
                          <motion.div
                            initial={{ height: 0, opacity: 0 }}
                            animate={{ height: 'auto', opacity: 1 }}
                            exit={{ height: 0, opacity: 0 }}
                            transition={{ duration: 0.3 }}
                            className="overflow-hidden"
                          >
                            <div className="px-5 pb-4 space-y-3 border-t border-gray-100 pt-4">
                              <p className="text-sm text-gray-600">{inter.description}</p>
                              <div className="bg-purple-50 rounded-lg p-3">
                                <p className="text-sm font-medium text-purple-800 mb-1">Recommendation</p>
                                <p className="text-sm text-purple-700">{inter.recommendation}</p>
                              </div>
                              <div className="bg-gray-50 rounded-lg p-3">
                                <p className="text-sm font-medium text-gray-700 mb-1">Scientific Basis</p>
                                <p className="text-sm text-gray-600">{inter.scientific_basis}</p>
                              </div>
                            </div>
                          </motion.div>
                        )}
                      </AnimatePresence>
                    </motion.div>
                  ))}
                </div>
              )}

              {/* Routine Tip */}
              {result.routine_tip && (
                <div className="glass-card bg-gradient-to-r from-violet-50 to-indigo-50 rounded-2xl shadow-md border border-violet-200 p-6">
                  <div className="flex items-start gap-3">
                    <Sparkles className="w-6 h-6 text-violet-500 flex-shrink-0 mt-0.5" />
                    <div>
                      <h4 className="font-semibold text-gray-900 mb-1">Routine Tip</h4>
                      <p className="text-sm text-gray-700">{result.routine_tip}</p>
                    </div>
                  </div>
                </div>
              )}
            </motion.section>
          )}
        </AnimatePresence>

        {/* Popular Combinations */}
        {popular.length > 0 && (
          <section>
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-amber-500" />
              Popular Combinations
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {popular.map((combo) => (
                <motion.button
                  key={combo.name}
                  whileHover={{ y: -2 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => loadPopular(combo)}
                  className="glass-card bg-white rounded-xl shadow-md border border-gray-200 p-5 text-left hover:shadow-lg transition-shadow"
                >
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="font-semibold text-gray-900">{combo.name}</h3>
                    <span
                      className={`w-2.5 h-2.5 rounded-full ${
                        combo.safety === 'safe' ? 'bg-green-400' : combo.safety === 'caution' ? 'bg-yellow-400' : 'bg-red-400'
                      }`}
                    />
                  </div>
                  <div className="flex flex-wrap gap-1 mb-2">
                    {combo.ingredients.map((ing) => (
                      <span key={ing} className="text-xs px-2 py-0.5 rounded-full bg-gray-100 text-gray-600 border border-gray-200">
                        {ing}
                      </span>
                    ))}
                  </div>
                  <p className="text-xs text-gray-500 line-clamp-2">{combo.description}</p>
                </motion.button>
              ))}
            </div>
          </section>
        )}

        {/* Encyclopedia */}
        {encyclopedia && (
          <section>
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <Shield className="w-5 h-5 text-indigo-500" />
              Interaction Encyclopedia
            </h2>
            <p className="text-sm text-gray-500 mb-4">{encyclopedia.total_interactions} total known interactions in database</p>
            <div className="space-y-3">
              {[
                {
                  key: 'avoid',
                  title: 'Avoid Together',
                  icon: <AlertTriangle className="w-5 h-5 text-red-500" />,
                  data: encyclopedia.avoid,
                  bg: 'bg-red-50',
                  border: 'border-red-200',
                  badge: 'bg-red-100 text-red-700',
                },
                {
                  key: 'caution',
                  title: 'Use With Caution',
                  icon: <Shield className="w-5 h-5 text-yellow-500" />,
                  data: encyclopedia.caution,
                  bg: 'bg-yellow-50',
                  border: 'border-yellow-200',
                  badge: 'bg-yellow-100 text-yellow-700',
                },
                {
                  key: 'synergistic',
                  title: 'Synergistic Pairs',
                  icon: <Zap className="w-5 h-5 text-green-500" />,
                  data: encyclopedia.synergistic,
                  bg: 'bg-green-50',
                  border: 'border-green-200',
                  badge: 'bg-green-100 text-green-700',
                },
              ].map((section) => (
                <div key={section.key} className={`glass-card bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden`}>
                  <button
                    onClick={() => toggleEncyc(section.key)}
                    className={`w-full px-5 py-4 flex items-center gap-3 text-left ${section.bg} hover:brightness-95 transition-all`}
                  >
                    {section.icon}
                    <span className="font-semibold text-gray-900">{section.title}</span>
                    <span className={`ml-auto text-xs font-semibold px-2 py-0.5 rounded-full ${section.badge}`}>
                      {section.data.length}
                    </span>
                    {expandedEncyc.has(section.key) ? (
                      <ChevronDown className="w-4 h-4 text-gray-500" />
                    ) : (
                      <ChevronRight className="w-4 h-4 text-gray-500" />
                    )}
                  </button>
                  <AnimatePresence>
                    {expandedEncyc.has(section.key) && (
                      <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: 'auto', opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        transition={{ duration: 0.3 }}
                        className="overflow-hidden"
                      >
                        <div className="divide-y divide-gray-100">
                          {section.data.map((item, i) => (
                            <div key={i} className="px-5 py-3 hover:bg-gray-50 transition-colors">
                              <p className="text-sm font-medium text-gray-900">{item.pair}</p>
                              <p className="text-xs text-gray-500 mt-0.5">{item.description}</p>
                            </div>
                          ))}
                          {section.data.length === 0 && (
                            <p className="px-5 py-4 text-sm text-gray-400">No entries found.</p>
                          )}
                        </div>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
              ))}
            </div>
          </section>
        )}
      </div>
    </div>
  );
}
