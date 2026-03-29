import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Save, Check, Volume2, VolumeX, LogOut, RotateCcw, Award } from 'lucide-react';
import { useAuthStore } from '../store/authStore';
import { authApi } from '../api/auth';
import { conceptsApi, type SubjectResponse } from '../api/concepts';
import { badgesApi, type LevelInfo } from '../api/badges';
import { getSoundEnabled, setSoundEnabled } from '../utils/sounds';
import PageContainer from '../components/layout/PageContainer';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';

const DEGREES = ['B.Tech', 'B.Arch', 'M.Tech', 'M.Arch', 'B.Sc', 'M.Sc', 'BCA', 'MCA', 'Other'];
const COURSES: Record<string, string[]> = {
  'B.Tech': ['Computer Science', 'Information Technology', 'Electronics', 'Electrical', 'Mechanical', 'Civil'],
  'B.Arch': ['Architecture & Planning'],
  'M.Tech': ['Computer Science', 'Information Technology', 'Electronics', 'Electrical', 'Structural Engineering'],
  'M.Arch': ['Architecture & Planning', 'Urban Design', 'Landscape Architecture'],
  'B.Sc': ['Computer Science', 'Mathematics', 'Physics'],
  'M.Sc': ['Computer Science', 'Mathematics', 'Physics'],
  'BCA': ['Computer Applications'],
  'MCA': ['Computer Applications'],
  'Other': ['Computer Science', 'Architecture & Planning', 'Other'],
};

export default function ProfilePage() {
  const { user, updateProfile, logout, refreshUser } = useAuthStore();
  const navigate = useNavigate();
  const [displayName, setDisplayName] = useState(user?.display_name || '');
  const [degree, setDegree] = useState(user?.degree || '');
  const [course, setCourse] = useState(user?.course || '');
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [subjects, setSubjects] = useState<SubjectResponse[]>([]);
  const [resetting, setResetting] = useState<string | null>(null);
  const [level, setLevel] = useState<LevelInfo | null>(null);
  const [soundOn, setSoundOn] = useState(getSoundEnabled());

  useEffect(() => {
    conceptsApi.getSubjects().then((r) => setSubjects(r.data)).catch(() => {});
    badgesApi.getBadges().then((r) => setLevel(r.data.level)).catch(() => {});
    refreshUser();
  }, []);

  useEffect(() => {
    if (user) {
      setDisplayName(user.display_name || '');
      setDegree(user.degree || '');
      setCourse(user.course || '');
    }
  }, [user]);

  const handleSave = async () => {
    setSaving(true);
    try {
      await updateProfile({ display_name: displayName, degree, course });
      setSaved(true);
      setTimeout(() => setSaved(false), 2000);
    } catch {
      // silent
    } finally {
      setSaving(false);
    }
  };

  const handleResetSubject = async (subjectId: string, subjectName: string) => {
    if (!confirm(`Reset all progress for "${subjectName}"? This cannot be undone.`)) return;
    setResetting(subjectId);
    try {
      await authApi.resetSubjectProgress(subjectId);
      await refreshUser();
      setSubjects((prev) => prev.map((s) => s.id === subjectId ? { ...s, progress_percent: 0 } : s));
    } catch {
      alert('Failed to reset progress');
    } finally {
      setResetting(null);
    }
  };

  const availableCourses = COURSES[degree] || [];

  return (
    <PageContainer>
      <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.2 }}>
        <div className="space-y-6">
          <h1 className="text-xl font-semibold text-slate-900">Profile</h1>

          {/* User Info */}
          <Card>
            <div className="flex items-center gap-3 mb-5">
              <div className="w-12 h-12 bg-indigo-50 rounded-2xl flex items-center justify-center">
                <span className="text-lg font-bold text-indigo-600">
                  {(user?.display_name || user?.username || 'U')[0].toUpperCase()}
                </span>
              </div>
              <div>
                <p className="text-sm font-semibold text-slate-900">{user?.username}</p>
                <p className="text-xs text-slate-400">{user?.email}</p>
                <p className="text-[10px] text-slate-400 mt-0.5">Member since {new Date(user?.created_at || '').toLocaleDateString()}</p>
              </div>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-3 gap-2 mb-5">
              <div className="text-center p-2.5 bg-slate-50 rounded-xl">
                <p className="text-base font-bold text-indigo-600 tabular-nums">{user?.total_xp?.toLocaleString() || 0}</p>
                <p className="text-[10px] text-slate-400 mt-0.5">Total XP</p>
              </div>
              <div className="text-center p-2.5 bg-slate-50 rounded-xl">
                <p className="text-base font-bold text-orange-500 tabular-nums">{user?.current_streak || 0}</p>
                <p className="text-[10px] text-slate-400 mt-0.5">Streak</p>
              </div>
              <div className="text-center p-2.5 bg-slate-50 rounded-xl">
                <p className="text-base font-bold text-indigo-500 tabular-nums">{user?.longest_streak || 0}</p>
                <p className="text-[10px] text-slate-400 mt-0.5">Best Streak</p>
              </div>
            </div>

            {/* Level & Badges link */}
            {level && (
              <Link to="/badges" className="block">
                <div className="flex items-center gap-3 p-3 bg-slate-50 rounded-xl hover:bg-slate-100 transition-all duration-200">
                  <div className="w-9 h-9 bg-gradient-to-br from-indigo-500 to-indigo-600 rounded-lg flex items-center justify-center text-white font-bold text-sm shadow-sm shadow-indigo-500/20">
                    {level.level}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-semibold text-slate-800">{level.title}</p>
                    <div className="flex items-center gap-2 mt-0.5">
                      <div className="flex-1 bg-slate-200 rounded-full h-1.5 overflow-hidden">
                        <div className="bg-indigo-500 h-full rounded-full" style={{ width: `${level.progress * 100}%` }} />
                      </div>
                      <span className="text-[10px] text-slate-400 tabular-nums">{level.current_xp}/{level.xp_for_next}</span>
                    </div>
                  </div>
                  <div className="flex items-center gap-1 text-xs text-indigo-500 font-medium">
                    <Award size={14} strokeWidth={1.5} />
                    Badges
                  </div>
                </div>
              </Link>
            )}
          </Card>

          {/* Edit Profile */}
          <Card>
            <h3 className="text-sm font-semibold text-slate-800 mb-4">Edit Profile</h3>
            <div className="space-y-3">
              <div>
                <label className="block text-xs font-medium text-slate-500 mb-1.5">Display Name</label>
                <input
                  type="text"
                  value={displayName}
                  onChange={(e) => setDisplayName(e.target.value)}
                  className="w-full px-3 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-400 text-slate-900 transition-all duration-200"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-500 mb-1.5">Degree</label>
                <select
                  value={degree}
                  onChange={(e) => { setDegree(e.target.value); setCourse(''); }}
                  className="w-full px-3 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-400 bg-white text-slate-900 transition-all duration-200"
                >
                  <option value="">Select your degree</option>
                  {DEGREES.map((d) => (
                    <option key={d} value={d}>{d}</option>
                  ))}
                </select>
              </div>
              {degree && availableCourses.length > 0 && (
                <div>
                  <label className="block text-xs font-medium text-slate-500 mb-1.5">Course / Branch</label>
                  <select
                    value={course}
                    onChange={(e) => setCourse(e.target.value)}
                    className="w-full px-3 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-400 bg-white text-slate-900 transition-all duration-200"
                  >
                    <option value="">Select your course</option>
                    {availableCourses.map((c) => (
                      <option key={c} value={c}>{c}</option>
                    ))}
                  </select>
                </div>
              )}
              <Button onClick={handleSave} disabled={saving} isLoading={saving} className="w-full">
                {saving ? 'Saving...' : saved ? (
                  <span className="inline-flex items-center gap-1.5">
                    <Check size={16} strokeWidth={1.5} />
                    Saved
                  </span>
                ) : (
                  <span className="inline-flex items-center gap-1.5">
                    <Save size={16} strokeWidth={1.5} />
                    Save Profile
                  </span>
                )}
              </Button>
            </div>
          </Card>

          {/* Settings */}
          <Card>
            <h3 className="text-sm font-semibold text-slate-800 mb-4">Settings</h3>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                {soundOn ? (
                  <Volume2 size={18} strokeWidth={1.5} className="text-slate-500" />
                ) : (
                  <VolumeX size={18} strokeWidth={1.5} className="text-slate-400" />
                )}
                <div>
                  <p className="text-sm font-medium text-slate-800">Sound Effects</p>
                  <p className="text-xs text-slate-400">Feedback sounds on answers</p>
                </div>
              </div>
              <button
                onClick={() => {
                  const next = !soundOn;
                  setSoundOn(next);
                  setSoundEnabled(next);
                }}
                className={`relative w-11 h-6 rounded-full transition-colors duration-200 ${soundOn ? 'bg-indigo-500' : 'bg-slate-300'}`}
              >
                <span
                  className={`absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full shadow-sm transition-transform duration-200 ${soundOn ? 'translate-x-5' : ''}`}
                />
              </button>
            </div>
          </Card>

          {/* Reset Progress */}
          <Card>
            <h3 className="text-sm font-semibold text-slate-800 mb-1">Reset Progress</h3>
            <p className="text-xs text-slate-400 mb-4">Start fresh on any subject. This clears all attempts and mastery data.</p>
            <div className="space-y-2">
              {subjects.map((s) => (
                <div key={s.id} className="flex items-center justify-between px-3 py-2.5 bg-slate-50 rounded-xl">
                  <div>
                    <p className="text-sm font-medium text-slate-800">{s.name}</p>
                    <p className="text-xs text-slate-400">{Math.round(s.progress_percent)}% complete</p>
                  </div>
                  <button
                    onClick={() => handleResetSubject(s.id, s.name)}
                    disabled={resetting === s.id}
                    className="flex items-center gap-1 text-xs font-medium text-rose-500 hover:text-rose-700 bg-rose-50 hover:bg-rose-100 px-3 py-1.5 rounded-lg transition-all duration-200 disabled:opacity-40"
                  >
                    <RotateCcw size={12} strokeWidth={1.5} />
                    {resetting === s.id ? 'Resetting...' : 'Reset'}
                  </button>
                </div>
              ))}
            </div>
          </Card>

          {/* Logout */}
          <Button
            variant="danger"
            onClick={() => { logout(); navigate('/login'); }}
            className="w-full"
          >
            <LogOut size={16} strokeWidth={1.5} />
            Log Out
          </Button>
        </div>
      </motion.div>
    </PageContainer>
  );
}
