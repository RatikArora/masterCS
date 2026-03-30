import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Building2, ChevronRight, AlertTriangle, ArrowRight, Network, Cpu, Code2, BookOpen, Calculator, Crown, Target } from 'lucide-react';
import { conceptsApi, type SubjectResponse } from '../api/concepts';
import { progressApi, type StreakInfo, type WeakArea } from '../api/progress';
import { badgesApi, type LevelInfo } from '../api/badges';
import { useAuthStore } from '../store/authStore';
import PageContainer from '../components/layout/PageContainer';
import Card from '../components/ui/Card';
import MascotGuide from '../components/ui/MascotGuide';
import StreakCounter from '../components/progress/StreakCounter';
import XPBar from '../components/progress/XPBar';
import Loading from '../components/ui/Loading';

const DEGREE_OPTIONS = [
  { value: 'B.Tech', label: 'B.Tech (CS/IT)', desc: 'Computer Science, GATE CS prep' },
  { value: 'B.Arch', label: 'B.Arch', desc: 'Architecture & Planning, GATE AR prep' },
  { value: 'M.Tech', label: 'M.Tech', desc: 'Postgrad Engineering' },
  { value: 'M.Arch', label: 'M.Arch', desc: 'Postgrad Architecture' },
];

interface SubjectTheme {
  from: string;
  to: string;
  text: string;
  accent: string;
}

const SUBJECT_THEME: Record<string, SubjectTheme> = {
  network:         { from: 'from-blue-500',    to: 'to-indigo-600',  text: 'text-blue-600',    accent: 'bg-blue-50 text-blue-600' },
  algorithm:       { from: 'from-violet-500',  to: 'to-purple-600',  text: 'text-violet-600',  accent: 'bg-violet-50 text-violet-600' },
  programming:     { from: 'from-emerald-500', to: 'to-teal-600',    text: 'text-emerald-600', accent: 'bg-emerald-50 text-emerald-600' },
  architecture:    { from: 'from-amber-500',   to: 'to-orange-600',  text: 'text-amber-600',   accent: 'bg-amber-50 text-amber-600' },
  aptitude:        { from: 'from-rose-500',    to: 'to-pink-600',    text: 'text-rose-600',    accent: 'bg-rose-50 text-rose-600' },
  operating:       { from: 'from-cyan-500',    to: 'to-sky-600',     text: 'text-cyan-600',    accent: 'bg-cyan-50 text-cyan-600' },
  python:          { from: 'from-yellow-400',  to: 'to-amber-500',   text: 'text-yellow-600',  accent: 'bg-yellow-50 text-yellow-600' },
  default:         { from: 'from-indigo-500',  to: 'to-violet-600',  text: 'text-indigo-600',  accent: 'bg-indigo-50 text-indigo-600' },
};

function getSubjectTheme(name: string): SubjectTheme {
  const n = name.toLowerCase();
  if (n.includes('network'))                                    return SUBJECT_THEME.network;
  if (n.includes('algorithm'))                                  return SUBJECT_THEME.algorithm;
  if (n.includes('programming') || n.includes('data structure')) return SUBJECT_THEME.programming;
  if (n.includes('architecture'))                               return SUBJECT_THEME.architecture;
  if (n.includes('aptitude'))                                   return SUBJECT_THEME.aptitude;
  if (n.includes('operating'))                                  return SUBJECT_THEME.operating;
  if (n.includes('python'))                                     return SUBJECT_THEME.python;
  return SUBJECT_THEME.default;
}

function getSubjectIcon(name: string, size = 18, cls = 'text-white') {
  const n = name.toLowerCase();
  if (n.includes('architecture')) return <Building2 size={size} strokeWidth={1.5} className={cls} />;
  if (n.includes('network')) return <Network size={size} strokeWidth={1.5} className={cls} />;
  if (n.includes('algorithm')) return <Cpu size={size} strokeWidth={1.5} className={cls} />;
  if (n.includes('programming') || n.includes('data structure')) return <Code2 size={size} strokeWidth={1.5} className={cls} />;
  if (n.includes('aptitude')) return <Calculator size={size} strokeWidth={1.5} className={cls} />;
  return <BookOpen size={size} strokeWidth={1.5} className={cls} />;
}

export default function Dashboard() {
  const { user, updateProfile, refreshUser } = useAuthStore();
  const [subjects, setSubjects] = useState<SubjectResponse[]>([]);
  const [streak, setStreak] = useState<StreakInfo | null>(null);
  const [weakAreas, setWeakAreas] = useState<WeakArea[]>([]);
  const [level, setLevel] = useState<LevelInfo | null>(null);
  const [todayXP, setTodayXP] = useState(0);
  const [loading, setLoading] = useState(true);
  const [pickingDegree, setPickingDegree] = useState(false);
  const navigate = useNavigate();

  const loadData = () => {
    setLoading(true);
    Promise.all([
      conceptsApi.getSubjects().then((r) => setSubjects(r.data)),
      progressApi.getStreak().then((r) => {
        setStreak(r.data);
        setTodayXP(r.data.xp_today || 0);
      }),
      badgesApi.getBadges().then((r) => setLevel(r.data.level)).catch(() => {}),
    ]).finally(() => setLoading(false));
  };

  useEffect(() => {
    if (!user?.degree) {
      setPickingDegree(true);
      setLoading(false);
    } else {
      loadData();
    }
  }, [user?.degree]);

  useEffect(() => {
    if (subjects.length > 0) {
      // Load weak areas from ALL subjects, not just the first one
      Promise.all(
        subjects.map((s) =>
          progressApi.getWeakAreas(s.id)
            .then((r) => (r.data.items || []).map((w: WeakArea) => ({ ...w, subject_id: s.id, subject_name: s.name })))
            .catch(() => [] as WeakArea[])
        )
      ).then((results) => {
        const all = results.flat().sort((a, b) => a.confidence_score - b.confidence_score);
        setWeakAreas(all.slice(0, 5));
      });
    }
  }, [subjects]);

  const handleDegreePick = async (degree: string) => {
    try {
      await updateProfile({ degree });
      await refreshUser();
      setPickingDegree(false);
      loadData();
    } catch {
      // silent
    }
  };

  if (pickingDegree) {
    return (
      <PageContainer>
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.25 }} className="py-8">
          <h1 className="text-xl font-semibold text-slate-900 mb-1">Welcome to {user?.degree?.toLowerCase().includes('arch') ? 'MasterAR' : 'MasterCS'}</h1>
          <p className="text-slate-500 text-sm mb-8">Select your degree to see relevant subjects.</p>
          <div className="space-y-2.5">
            {DEGREE_OPTIONS.map((opt) => (
              <button
                key={opt.value}
                onClick={() => handleDegreePick(opt.value)}
                className="w-full text-left p-4 bg-white rounded-2xl border border-slate-200/60 hover:border-indigo-300 hover:shadow-sm transition-all duration-200 group"
              >
                <p className="font-semibold text-sm text-slate-900 group-hover:text-indigo-600 transition-colors">{opt.label}</p>
                <p className="text-xs text-slate-400 mt-0.5">{opt.desc}</p>
              </button>
            ))}
          </div>
          <p className="text-[10px] text-slate-400 text-center mt-6">You can change this later in settings.</p>
        </motion.div>
      </PageContainer>
    );
  }

  if (loading) return <Loading text="Loading dashboard..." />;

  return (
    <PageContainer>
      <div className="space-y-6">
        {/* Greeting with mascot */}
        <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.2 }} className="flex items-center gap-4">
          <MascotGuide
            context="dashboard"
            size={56}
            stats={{
              streak: streak?.current_streak ?? 0,
              todayCompleted: streak?.today_completed ?? false,
              todayQuestions: streak?.questions_today ?? 0,
              totalXP: todayXP,
              level: level?.level,
              weakAreas: weakAreas.length,
            }}
            userName={user?.display_name || user?.username}
            className="flex-shrink-0"
          />
          <div>
            <h1 className="text-xl font-semibold text-slate-900">
              Hey, {user?.display_name || user?.username}
            </h1>
            <p className="text-slate-500 text-sm mt-0.5">
              {streak && streak.current_streak >= 7
                ? `${streak.current_streak}-day streak! You're on fire!`
                : streak?.today_completed
                  ? 'Great job today! Keep it up!'
                  : 'Ready to learn something new?'}
            </p>
          </div>
        </motion.div>

        {/* Stats pills + XP bar */}
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.05, duration: 0.2 }}
          className="space-y-3"
        >
          <div className="flex items-center gap-2">
            <StreakCounter count={streak?.current_streak || 0} isActive={streak?.today_completed} />
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl text-xs font-bold bg-gradient-to-r from-indigo-50 to-violet-50 text-indigo-600 border border-indigo-200/70 shadow-sm">
              <svg className="w-4 h-4 text-indigo-500" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clipRule="evenodd" />
              </svg>
              <span className="tabular-nums">{(user?.total_xp || 0).toLocaleString()} XP</span>
            </div>
          </div>
          {streak && (
            <XPBar current={todayXP} goal={150} questionsToday={streak.questions_today} />
          )}
        </motion.div>

        {/* Daily Quest */}
        {streak && (() => {
          const questGoal = 20;
          const questDone = streak.questions_today >= questGoal;
          const questPct = Math.min((streak.questions_today / questGoal) * 100, 100);
          return (
            <motion.div
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.08, duration: 0.2 }}
            >
              <div className={`flex items-center gap-3 rounded-2xl px-4 py-3 border shadow-sm ${questDone ? 'bg-gradient-to-r from-emerald-50 to-teal-50 border-emerald-200/60' : 'bg-gradient-to-r from-amber-50 to-yellow-50 border-amber-200/60'}`}>
                <div className={`w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 shadow-sm ${questDone ? 'bg-gradient-to-br from-emerald-500 to-teal-600 shadow-emerald-500/20' : 'bg-gradient-to-br from-amber-400 to-orange-500 shadow-amber-500/20'}`}>
                  <Target size={18} strokeWidth={1.5} className="text-white" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <p className="text-sm font-semibold text-slate-800">Daily Quest</p>
                    {questDone
                      ? <span className="text-[10px] font-bold text-emerald-600 bg-emerald-100 rounded-full px-2 py-0.5">Complete!</span>
                      : <span className="text-[10px] text-slate-400 tabular-nums">{streak.questions_today}/{questGoal}</span>
                    }
                  </div>
                  <p className="text-[11px] text-slate-500 mt-0.5">Answer {questGoal} questions today</p>
                  <div className="mt-2 bg-white/60 rounded-full h-1.5 overflow-hidden">
                    <motion.div
                      className={`h-full rounded-full ${questDone ? 'bg-gradient-to-r from-emerald-500 to-teal-600' : 'bg-gradient-to-r from-amber-400 to-orange-500'}`}
                      initial={{ width: 0 }}
                      animate={{ width: `${questPct}%` }}
                      transition={{ delay: 0.1, duration: 0.5 }}
                    />
                  </div>
                </div>
              </div>
            </motion.div>
          );
        })()}

        {/* Level card */}
        {level && (
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1, duration: 0.2 }}
          >
            <Link to="/badges" className="block">
              <div className="bg-gradient-to-br from-indigo-50 via-violet-50 to-purple-50 border border-indigo-200/60 rounded-2xl px-4 py-3 shadow-md hover:shadow-lg hover:border-indigo-300 transition-all duration-200">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-violet-600 rounded-xl flex items-center justify-center flex-shrink-0 shadow-sm shadow-indigo-500/30">
                    <Crown size={18} strokeWidth={1.5} className="text-white" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <p className="text-sm font-bold text-slate-800">Level {level.level} · {level.title}</p>
                      <ChevronRight size={16} strokeWidth={1.5} className="text-slate-300 flex-shrink-0" />
                    </div>
                    <div className="flex items-center gap-2 mt-1.5">
                      <div className="flex-1 bg-white/70 rounded-full h-1.5 overflow-hidden">
                        <motion.div
                          className="bg-gradient-to-r from-indigo-500 to-violet-600 h-full rounded-full"
                          initial={{ width: 0 }}
                          animate={{ width: `${level.progress * 100}%` }}
                          transition={{ delay: 0.15, duration: 0.5 }}
                        />
                      </div>
                      <span className="text-[10px] text-slate-500 tabular-nums">{level.current_xp}/{level.xp_for_next} XP</span>
                    </div>
                    <p className="text-[10px] text-indigo-400 mt-0.5">{level.xp_for_next - level.current_xp} XP to Level {level.level + 1}</p>
                  </div>
                </div>
              </div>
            </Link>
          </motion.div>
        )}

        {/* Subjects */}
        <div>
          <h2 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-3">Your Subjects</h2>
          {subjects.length === 0 && (
            <Card padding="lg">
              <p className="text-slate-400 text-sm text-center">No subjects available yet. Seed the database first!</p>
            </Card>
          )}
          <div className="space-y-2.5">
            {subjects.map((subject, i) => {
              const theme = getSubjectTheme(subject.name);
              return (
                <motion.div
                  key={subject.id}
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1 + i * 0.04, duration: 0.2 }}
                >
                  <Card hover onClick={() => navigate(`/topics?subject=${subject.id}`)}>
                    <div className="flex items-center gap-3">
                      <div className={`w-10 h-10 bg-gradient-to-br ${theme.from} ${theme.to} rounded-xl flex items-center justify-center flex-shrink-0 shadow-sm`}>
                        {getSubjectIcon(subject.name)}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2">
                          <h3 className="text-sm font-semibold text-slate-900 truncate">{subject.name}</h3>
                          {subject.progress_percent > 0 && (
                            <span className={`text-[10px] font-semibold rounded-full px-2 py-0.5 flex-shrink-0 ${theme.accent}`}>
                              {Math.round(subject.progress_percent)}%
                            </span>
                          )}
                        </div>
                        <p className="text-xs text-slate-400 truncate mt-0.5">{subject.description}</p>
                        <div className="flex items-center gap-2 mt-2">
                          <div className="flex-1 bg-slate-100 rounded-full h-1.5 overflow-hidden">
                            <motion.div
                              className={`bg-gradient-to-r ${theme.from} ${theme.to} h-full rounded-full`}
                              initial={{ width: 0 }}
                              animate={{ width: `${Math.min(subject.progress_percent, 100)}%` }}
                              transition={{ delay: 0.15 + i * 0.04, duration: 0.5 }}
                            />
                          </div>
                        </div>
                        <div className="flex items-center gap-3 mt-1">
                          <span className="text-[10px] text-slate-400">{subject.topic_count} topics</span>
                          <button
                            onClick={(e) => { e.stopPropagation(); navigate(`/progress?subject=${subject.id}`); }}
                            className={`text-[10px] ${theme.text} hover:opacity-80 font-medium transition-opacity ml-auto`}
                          >
                            View Stats
                          </button>
                        </div>
                      </div>
                      <ChevronRight size={16} strokeWidth={1.5} className="text-slate-300 flex-shrink-0" />
                    </div>
                  </Card>
                </motion.div>
              );
            })}
          </div>
        </div>

        {/* Weak Areas */}
        {weakAreas.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.15, duration: 0.2 }}
          >
            <h2 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-3">Needs Practice</h2>
            <div className="space-y-2">
              {weakAreas.map((area: any) => (
                <button
                  key={area.concept_id}
                  onClick={() => navigate(`/learn?subject=${area.subject_id || subjects[0]?.id}&concept=${area.concept_id}`)}
                  className="w-full flex items-center gap-3 px-4 py-3 bg-amber-50/50 rounded-2xl border border-slate-200/60 hover:border-amber-300 shadow-sm transition-all duration-200 text-left"
                >
                  <div className="w-8 h-8 bg-amber-100 rounded-xl flex items-center justify-center flex-shrink-0">
                    <AlertTriangle size={14} strokeWidth={1.5} className="text-amber-600" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <p className="text-sm font-medium text-slate-800 truncate">{area.concept_name}</p>
                      <span className="text-[10px] font-semibold text-rose-600 bg-rose-50 rounded-full px-2 py-0.5 flex-shrink-0">
                        {Math.round(area.accuracy)}%
                      </span>
                    </div>
                    <p className="text-[11px] text-slate-400">
                      {area.subject_name ? `${area.subject_name} · ` : ''}{area.topic_name}
                    </p>
                  </div>
                  <ChevronRight size={14} strokeWidth={1.5} className="text-slate-300 flex-shrink-0" />
                </button>
              ))}
            </div>
          </motion.div>
        )}

        {/* CTA */}
        {subjects.length > 1 && (
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2, duration: 0.2 }}
            className="text-center text-xs text-slate-400"
          >
            Tap a subject to start learning
          </motion.p>
        )}
        {subjects.length === 1 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2, duration: 0.2 }}
          >
            <Link
              to={`/learn?subject=${subjects[0].id}`}
              className="flex items-center justify-center gap-2 w-full py-3 bg-gradient-to-r from-indigo-500 to-violet-600 text-white text-center text-sm font-medium rounded-2xl hover:opacity-90 transition-all duration-200 shadow-lg shadow-indigo-500/25"
            >
              Start Learning
              <ArrowRight size={16} strokeWidth={1.5} />
            </Link>
          </motion.div>
        )}
      </div>
    </PageContainer>
  );
}
