import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useAuthStore } from '../store/authStore';
import { authApi } from '../api/auth';
import { conceptsApi, type SubjectResponse } from '../api/concepts';
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

  useEffect(() => {
    conceptsApi.getSubjects().then((r) => setSubjects(r.data)).catch(() => {});
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
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Profile</h1>

        {/* User Info */}
        <Card className="mb-4">
          <div className="flex items-center gap-4 mb-4">
            <div className="w-14 h-14 bg-primary-100 rounded-full flex items-center justify-center">
              <span className="text-xl font-bold text-primary-600">
                {(user?.display_name || user?.username || 'U')[0].toUpperCase()}
              </span>
            </div>
            <div>
              <p className="font-semibold text-gray-900">{user?.username}</p>
              <p className="text-xs text-gray-400">{user?.email}</p>
              <p className="text-xs text-gray-400">Member since {new Date(user?.created_at || '').toLocaleDateString()}</p>
            </div>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-3 gap-3 mb-4">
            <div className="text-center p-2 bg-gray-50 rounded-lg">
              <p className="text-lg font-bold text-primary-600">{user?.total_xp?.toLocaleString() || 0}</p>
              <p className="text-[10px] text-gray-400">Total XP</p>
            </div>
            <div className="text-center p-2 bg-gray-50 rounded-lg">
              <p className="text-lg font-bold text-orange-500">{user?.current_streak || 0}</p>
              <p className="text-[10px] text-gray-400">Streak</p>
            </div>
            <div className="text-center p-2 bg-gray-50 rounded-lg">
              <p className="text-lg font-bold text-purple-500">{user?.longest_streak || 0}</p>
              <p className="text-[10px] text-gray-400">Best Streak</p>
            </div>
          </div>
        </Card>

        {/* Edit Profile */}
        <Card className="mb-4">
          <h3 className="text-sm font-semibold text-gray-700 mb-3">Edit Profile</h3>
          <div className="space-y-3">
            <div>
              <label className="block text-xs font-medium text-gray-500 mb-1">Display Name</label>
              <input
                type="text"
                value={displayName}
                onChange={(e) => setDisplayName(e.target.value)}
                className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-500 mb-1">Degree</label>
              <select
                value={degree}
                onChange={(e) => { setDegree(e.target.value); setCourse(''); }}
                className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white"
              >
                <option value="">Select your degree</option>
                {DEGREES.map((d) => (
                  <option key={d} value={d}>{d}</option>
                ))}
              </select>
            </div>
            {degree && availableCourses.length > 0 && (
              <div>
                <label className="block text-xs font-medium text-gray-500 mb-1">Course / Branch</label>
                <select
                  value={course}
                  onChange={(e) => setCourse(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white"
                >
                  <option value="">Select your course</option>
                  {availableCourses.map((c) => (
                    <option key={c} value={c}>{c}</option>
                  ))}
                </select>
              </div>
            )}
            <Button onClick={handleSave} disabled={saving} className="w-full">
              {saving ? 'Saving...' : saved ? '✓ Saved!' : 'Save Profile'}
            </Button>
          </div>
        </Card>

        {/* Reset Progress */}
        <Card className="mb-4">
          <h3 className="text-sm font-semibold text-gray-700 mb-1">Reset Progress</h3>
          <p className="text-xs text-gray-400 mb-3">Start fresh on any subject. This clears all attempts and mastery data.</p>
          <div className="space-y-2">
            {subjects.map((s) => (
              <div key={s.id} className="flex items-center justify-between px-3 py-2.5 bg-gray-50 rounded-lg">
                <div>
                  <p className="text-sm font-medium text-gray-800">{s.name}</p>
                  <p className="text-xs text-gray-400">{Math.round(s.progress_percent)}% complete</p>
                </div>
                <button
                  onClick={() => handleResetSubject(s.id, s.name)}
                  disabled={resetting === s.id}
                  className="text-xs font-medium text-red-500 hover:text-red-700 bg-red-50 hover:bg-red-100 px-3 py-1.5 rounded-lg transition-colors disabled:opacity-50"
                >
                  {resetting === s.id ? 'Resetting...' : 'Reset'}
                </button>
              </div>
            ))}
          </div>
        </Card>

        {/* Logout */}
        <button
          onClick={() => { logout(); navigate('/login'); }}
          className="w-full py-3 text-sm font-medium text-red-600 bg-red-50 hover:bg-red-100 rounded-xl transition-colors"
        >
          Log Out
        </button>
      </motion.div>
    </PageContainer>
  );
}
