import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { conceptsApi, type SubjectResponse } from '../api/concepts';
import { progressApi, type StreakInfo, type WeakArea } from '../api/progress';
import { useAuthStore } from '../store/authStore';
import PageContainer from '../components/layout/PageContainer';
import Card from '../components/ui/Card';
import ProgressRing from '../components/progress/ProgressRing';
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
  const [loading, setLoading] = useState(true);
  const [pickingDegree, setPickingDegree] = useState(false);
  const navigate = useNavigate();

  const loadData = () => {
    setLoading(true);
    Promise.all([
      conceptsApi.getSubjects().then((r) => setSubjects(r.data)),
      progressApi.getStreak().then((r) => setStreak(r.data)),
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

  // Fetch weak areas once we have subjects
  useEffect(() => {
    if (subjects.length > 0) {
      progressApi.getWeakAreas(subjects[0].id)
        .then((r) => setWeakAreas(r.data.slice(0, 3)))
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
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="max-w-md mx-auto py-8">
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Welcome to MasterCS!</h1>
          <p className="text-gray-500 text-sm mb-6">Select your degree to see relevant subjects and courses.</p>
          <div className="space-y-3">
            {DEGREE_OPTIONS.map((opt) => (
              <button
                key={opt.value}
                onClick={() => handleDegreePick(opt.value)}
                className="w-full text-left p-4 bg-white rounded-xl border-2 border-gray-100 hover:border-primary-400 hover:bg-primary-50 transition-all duration-200 group"
              >
                <p className="font-semibold text-gray-900 group-hover:text-primary-700">{opt.label}</p>
                <p className="text-xs text-gray-400 mt-0.5">{opt.desc}</p>
              </button>
            ))}
          </div>
          <p className="text-[10px] text-gray-400 text-center mt-4">You can change this later in your profile settings.</p>
        </motion.div>
      </PageContainer>
    );
  }

  if (loading) return <Loading text="Loading dashboard..." />;

  return (
    <PageContainer>
      {/* Greeting */}
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">
          Hey, {user?.display_name || user?.username}
        </h1>
        <p className="text-gray-500 text-sm mt-1">Ready to learn something new?</p>
      </motion.div>

      {/* Stats Row */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="flex flex-wrap items-center gap-3 mb-6"
      >
        <StreakCounter count={streak?.current_streak || 0} isActive={streak?.today_completed} />
        <div className="text-sm">
          <span className="font-bold text-primary-600">{(user?.total_xp || 0).toLocaleString()}</span>
          <span className="text-gray-400 ml-1 text-xs">XP total</span>
        </div>
        <div className="w-px h-6 bg-gray-200 hidden sm:block" />
        {streak && (
          <XPBar current={streak.questions_today * 15} goal={150} />
        )}
      </motion.div>

      {/* Subjects */}
      <div className="space-y-3">
        <h2 className="text-lg font-semibold text-gray-800">Your Subjects</h2>
        {subjects.length === 0 && (
          <Card padding="lg">
            <p className="text-gray-500 text-center">No subjects available yet. Seed the database first!</p>
          </Card>
        )}
        {subjects.map((subject, i) => (
          <motion.div
            key={subject.id}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.15 + i * 0.05 }}
          >
             <Card hover className="cursor-pointer" onClick={() => navigate(`/topics?subject=${subject.id}`)}>
              <div className="flex items-center gap-4">
                <ProgressRing percent={subject.progress_percent} size={56} strokeWidth={5}>
                  <div className="w-8 h-8 bg-primary-100 rounded-lg flex items-center justify-center">
                    {subject.name.toLowerCase().includes('architecture') ? (
                      <svg className="w-4.5 h-4.5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                      </svg>
                    ) : (
                      <svg className="w-4.5 h-4.5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                      </svg>
                    )}
                  </div>
                </ProgressRing>
                <div className="flex-1 min-w-0">
                  <h3 className="font-semibold text-gray-900">{subject.name}</h3>
                  <p className="text-sm text-gray-500 truncate">{subject.description}</p>
                  <div className="flex items-center gap-3 mt-1.5">
                    <span className="text-xs text-gray-400">{subject.topic_count} topics</span>
                    <span className="text-xs text-gray-400">{Math.round(subject.progress_percent)}% complete</span>
                    <button
                      onClick={(e) => { e.stopPropagation(); navigate(`/progress?subject=${subject.id}`); }}
                      className="text-xs text-primary-500 hover:text-primary-700 font-medium transition-colors ml-auto"
                    >
                      Stats →
                    </button>
                  </div>
                </div>
                <svg className="w-5 h-5 text-gray-300 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Weak Areas Preview */}
      {weakAreas.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.35 }}
          className="mt-6"
        >
          <h2 className="text-lg font-semibold text-gray-800 mb-3">Needs Practice</h2>
          <div className="space-y-2">
            {weakAreas.map((area) => (
              <div key={area.concept_id} className="flex items-center gap-3 px-4 py-3 bg-amber-50 rounded-xl border border-amber-100">
                <svg className="w-4 h-4 text-amber-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-800 truncate">{area.concept_name}</p>
                  <p className="text-[11px] text-gray-500">{area.topic_name} · {Math.round(area.accuracy)}% accuracy</p>
                </div>
                <span className="text-[10px] text-amber-600 font-medium">{area.recommended_action}</span>
              </div>
            ))}
          </div>
        </motion.div>
      )}

      {/* Quick tip */}
      {subjects.length > 1 && (
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="mt-6 text-center text-xs text-gray-400"
        >
          Tap a subject to start learning
        </motion.p>
      )}
      {subjects.length === 1 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="mt-8"
        >
          <Link
            to={`/learn?subject=${subjects[0].id}`}
            className="block w-full py-4 bg-primary-600 text-white text-center font-semibold rounded-2xl hover:bg-primary-700 transition-colors shadow-lg shadow-primary-600/20"
          >
            Start Learning →
          </Link>
        </motion.div>
      )}
    </PageContainer>
  );
}
