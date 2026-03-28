import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { conceptsApi, type SubjectResponse } from '../api/concepts';
import { progressApi, type StreakInfo, type WeakArea } from '../api/progress';
import { badgesApi, type LevelInfo } from '../api/badges';
import { useAuthStore } from '../store/authStore';
import PageContainer from '../components/layout/PageContainer';
import Card from '../components/ui/Card';
import StreakCounter from '../components/progress/StreakCounter';
import XPBar from '../components/progress/XPBar';
import Loading from '../components/ui/Loading';

const DEGREE_OPTIONS = [
  { value: 'B.Tech', label: 'B.Tech (CS/IT)', desc: 'Computer Science, GATE CS prep' },
  { value: 'B.Arch', label: 'B.Arch', desc: 'Architecture & Planning, GATE AR prep' },
  { value: 'M.Tech', label: 'M.Tech', desc: 'Postgrad Engineering' },
  { value: 'M.Arch', label: 'M.Arch', desc: 'Postgrad Architecture' },
];

export default function Dashboard() {
  const { user, updateProfile, refreshUser } = useAuthStore();
  const [subjects, setSubjects] = useState<SubjectResponse[]>([]);
  const [streak, setStreak] = useState<StreakInfo | null>(null);
  const [weakAreas, setWeakAreas] = useState<WeakArea[]>([]);
  const [level, setLevel] = useState<LevelInfo | null>(null);
  const [loading, setLoading] = useState(true);
  const [pickingDegree, setPickingDegree] = useState(false);
  const navigate = useNavigate();

  const loadData = () => {
    setLoading(true);
    Promise.all([
      conceptsApi.getSubjects().then((r) => setSubjects(r.data)),
      progressApi.getStreak().then((r) => setStreak(r.data)),
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
      progressApi.getWeakAreas(subjects[0].id)
        .then((r) => setWeakAreas((r.data.items || []).slice(0, 3)))
        .catch(() => {});
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
          <h1 className="text-xl font-bold text-slate-900 mb-1.5">Welcome to MasterCS!</h1>
          <p className="text-slate-500 text-sm mb-6">Select your degree to see relevant subjects.</p>
          <div className="space-y-2.5">
            {DEGREE_OPTIONS.map((opt) => (
              <button
                key={opt.value}
                onClick={() => handleDegreePick(opt.value)}
                className="w-full text-left p-4 bg-white rounded-2xl border border-slate-200/60 hover:border-indigo-300 hover:shadow-sm transition-all duration-200 group"
              >
                <p className="font-semibold text-sm text-slate-900 group-hover:text-indigo-600">{opt.label}</p>
                <p className="text-xs text-slate-400 mt-0.5">{opt.desc}</p>
              </button>
            ))}
          </div>
          <p className="text-[10px] text-slate-400 text-center mt-4">You can change this later in settings.</p>
        </motion.div>
      </PageContainer>
    );
  }

  if (loading) return <Loading text="Loading dashboard..." />;

  return (
    <PageContainer>
      <div className="space-y-5">
        {/* Greeting */}
        <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.2 }}>
          <h1 className="text-xl font-bold text-slate-900">
            Hey, {user?.display_name || user?.username}
          </h1>
          <p className="text-slate-500 text-sm mt-0.5">Ready to learn something new?</p>
        </motion.div>

        {/* Stats Row — compact pills + XP bar */}
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.05, duration: 0.2 }}
        >
          <div className="flex items-center gap-2 mb-2.5">
            <StreakCounter count={streak?.current_streak || 0} isActive={streak?.today_completed} />
            <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-xl text-xs font-semibold bg-indigo-50 text-indigo-600 border border-indigo-200/60">
              <svg className="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
                <path d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z"/>
              </svg>
              <span>{(user?.total_xp || 0).toLocaleString()} XP</span>
            </div>
          </div>
          {streak && (
            <XPBar current={streak.questions_today * 15} goal={150} />
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
              <div className="flex items-center gap-3 bg-white border border-slate-200/60 rounded-2xl px-4 py-3 hover:shadow-md hover:border-slate-300/60 transition-all duration-200">
                <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-indigo-600 rounded-xl flex items-center justify-center text-white font-bold text-sm shadow-sm">
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
                <svg className="w-4 h-4 text-slate-300 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </Link>
          </motion.div>
        )}

        {/* Subjects */}
        <div>
          <h2 className="text-base font-semibold text-slate-800 mb-3">Your Subjects</h2>
          {subjects.length === 0 && (
            <Card padding="lg">
              <p className="text-slate-500 text-sm text-center">No subjects available yet. Seed the database first!</p>
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
                <Card hover className="cursor-pointer" onClick={() => navigate(`/topics?subject=${subject.id}`)}>
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-indigo-50 rounded-xl flex items-center justify-center flex-shrink-0">
                      {subject.name.toLowerCase().includes('architecture') ? (
                        <svg className="w-5 h-5 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                        </svg>
                      ) : (
                        <svg className="w-5 h-5 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                        </svg>
                      )}
                    </div>
                    <div className="flex-1 min-w-0">
                      <h3 className="text-sm font-semibold text-slate-900">{subject.name}</h3>
                      <p className="text-xs text-slate-500 truncate">{subject.description}</p>
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
                          Stats →
                        </button>
                      </div>
                    </div>
                    <svg className="w-4 h-4 text-slate-300 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5l7 7-7 7" />
                    </svg>
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
            <h2 className="text-base font-semibold text-slate-800 mb-3">Needs Practice</h2>
            <div className="space-y-2">
              {weakAreas.map((area) => (
                <div key={area.concept_id} className="flex items-center gap-3 px-4 py-3 bg-white rounded-2xl border border-slate-200/60">
                  <div className="w-8 h-8 bg-indigo-50 rounded-xl flex items-center justify-center flex-shrink-0">
                    <svg className="w-4 h-4 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
                    </svg>
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-slate-800 truncate">{area.concept_name}</p>
                    <p className="text-[11px] text-slate-400">{area.topic_name} · {Math.round(area.accuracy)}% accuracy</p>
                  </div>
                  <span className="text-[10px] text-indigo-500 font-medium flex-shrink-0">{area.recommended_action}</span>
                </div>
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
              className="block w-full py-3 bg-indigo-600 text-white text-center text-sm font-medium rounded-2xl hover:bg-indigo-700 transition-colors duration-200 shadow-sm"
            >
              Start Learning →
            </Link>
          </motion.div>
        )}
      </div>
    </PageContainer>
  );
}
