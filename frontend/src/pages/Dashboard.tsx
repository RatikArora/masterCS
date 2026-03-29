import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Globe, Building2, ChevronRight, Zap, AlertTriangle, ArrowRight, Network, Cpu, Code2, BookOpen, Calculator } from 'lucide-react';
import { conceptsApi, type SubjectResponse } from '../api/concepts';
import { progressApi, type StreakInfo, type WeakArea, type DailyStats } from '../api/progress';
import { badgesApi, type LevelInfo } from '../api/badges';
import { useAuthStore } from '../store/authStore';
import PageContainer from '../components/layout/PageContainer';
import Card from '../components/ui/Card';
import Mascot from '../components/ui/Mascot';
import StreakCounter from '../components/progress/StreakCounter';
import XPBar from '../components/progress/XPBar';
import Loading from '../components/ui/Loading';

const DEGREE_OPTIONS = [
  { value: 'B.Tech', label: 'B.Tech (CS/IT)', desc: 'Computer Science, GATE CS prep' },
  { value: 'B.Arch', label: 'B.Arch', desc: 'Architecture & Planning, GATE AR prep' },
  { value: 'M.Tech', label: 'M.Tech', desc: 'Postgrad Engineering' },
  { value: 'M.Arch', label: 'M.Arch', desc: 'Postgrad Architecture' },
];

function getSubjectIcon(name: string, size = 18) {
  const n = name.toLowerCase();
  const cls = "text-indigo-500";
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
          <Mascot
            size={56}
            mood={streak && streak.current_streak >= 3 ? 'celebrating' : streak?.today_completed ? 'happy' : 'waving'}
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
            <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-semibold bg-indigo-50 text-indigo-600 border border-indigo-100">
              <Zap size={12} strokeWidth={1.5} />
              <span className="tabular-nums">{(user?.total_xp || 0).toLocaleString()} XP</span>
            </div>
          </div>
          {streak && (
            <XPBar current={todayXP} goal={150} questionsToday={streak.questions_today} />
          )}
        </motion.div>

        {/* Level card */}
        {level && (
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1, duration: 0.2 }}
          >
            <Link to="/badges" className="block">
              <div className="flex items-center gap-3 bg-white border border-slate-200/60 rounded-2xl px-4 py-3 hover:shadow-sm hover:border-slate-300 transition-all duration-200">
                <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-indigo-600 rounded-xl flex items-center justify-center text-white font-bold text-sm shadow-sm shadow-indigo-500/20">
                  {level.level}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-semibold text-slate-800">{level.title}</p>
                  <div className="flex items-center gap-2 mt-1">
                    <div className="flex-1 bg-slate-100 rounded-full h-1.5 overflow-hidden">
                      <div
                        className="bg-indigo-500 h-full rounded-full transition-all duration-500"
                        style={{ width: `${level.progress * 100}%` }}
                      />
                    </div>
                    <span className="text-[10px] text-slate-400 tabular-nums">{level.current_xp}/{level.xp_for_next}</span>
                  </div>
                </div>
                <ChevronRight size={16} strokeWidth={1.5} className="text-slate-300 flex-shrink-0" />
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
            {subjects.map((subject, i) => (
              <motion.div
                key={subject.id}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 + i * 0.04, duration: 0.2 }}
              >
                <Card hover onClick={() => navigate(`/topics?subject=${subject.id}`)}>
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-indigo-50 rounded-xl flex items-center justify-center flex-shrink-0">
                      {getSubjectIcon(subject.name)}
                    </div>
                    <div className="flex-1 min-w-0">
                      <h3 className="text-sm font-semibold text-slate-900">{subject.name}</h3>
                      <p className="text-xs text-slate-400 truncate mt-0.5">{subject.description}</p>
                      <div className="flex items-center gap-2 mt-2">
                        <div className="flex-1 bg-slate-100 rounded-full h-1.5 overflow-hidden">
                          <motion.div
                            className="bg-indigo-500 h-full rounded-full"
                            initial={{ width: 0 }}
                            animate={{ width: `${Math.min(subject.progress_percent, 100)}%` }}
                            transition={{ delay: 0.15 + i * 0.04, duration: 0.5 }}
                          />
                        </div>
                        <span className="text-[10px] text-slate-400 tabular-nums w-8 text-right">{Math.round(subject.progress_percent)}%</span>
                      </div>
                      <div className="flex items-center gap-3 mt-1">
                        <span className="text-[10px] text-slate-400">{subject.topic_count} topics</span>
                        <button
                          onClick={(e) => { e.stopPropagation(); navigate(`/progress?subject=${subject.id}`); }}
                          className="text-[10px] text-indigo-500 hover:text-indigo-700 font-medium transition-colors ml-auto"
                        >
                          View Stats
                        </button>
                      </div>
                    </div>
                    <ChevronRight size={16} strokeWidth={1.5} className="text-slate-300 flex-shrink-0" />
                  </div>
                </Card>
              </motion.div>
            ))}
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
                  className="w-full flex items-center gap-3 px-4 py-3 bg-white rounded-2xl border border-slate-200/60 hover:border-amber-200 hover:shadow-sm transition-all duration-200 text-left"
                >
                  <div className="w-8 h-8 bg-amber-50 rounded-xl flex items-center justify-center flex-shrink-0">
                    <AlertTriangle size={14} strokeWidth={1.5} className="text-amber-500" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-slate-800 truncate">{area.concept_name}</p>
                    <p className="text-[11px] text-slate-400">
                      {area.subject_name ? `${area.subject_name} · ` : ''}{area.topic_name} · {Math.round(area.accuracy)}% accuracy
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
              className="flex items-center justify-center gap-2 w-full py-3 bg-indigo-600 text-white text-center text-sm font-medium rounded-2xl hover:bg-indigo-700 transition-all duration-200 shadow-sm shadow-indigo-600/10"
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
