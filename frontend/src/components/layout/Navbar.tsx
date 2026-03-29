import { Link, useLocation, useSearchParams } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import { Home, BookOpen, GraduationCap, BarChart3, User } from 'lucide-react';

const navItems = [
  { path: '/dashboard', label: 'Home', icon: Home },
  { path: '/topics', label: 'Topics', icon: BookOpen },
  { path: '/learn', label: 'Learn', icon: GraduationCap },
  { path: '/progress', label: 'Progress', icon: BarChart3 },
  { path: '/profile', label: 'Profile', icon: User },
];

export default function Navbar() {
  const { isAuthenticated, user } = useAuthStore();
  const location = useLocation();
  const [searchParams] = useSearchParams();

  if (!isAuthenticated) return null;

  const subjectId = searchParams.get('subject') || '';
  const buildPath = (base: string) => {
    if (base === '/dashboard') return base;
    return subjectId ? `${base}?subject=${subjectId}` : base;
  };

  // Dynamic app name based on degree
  const degree = user?.degree || '';
  const appName = degree.toLowerCase().includes('arch') ? 'MasterAR' :
                  degree.toLowerCase().includes('tech') ? 'MasterCS' : 'MasterCS';

  return (
    <>
      {/* Desktop top nav */}
      <nav className="hidden md:flex items-center justify-between px-6 h-14 bg-white/80 backdrop-blur-xl border-b border-slate-200/60 sticky top-0 z-50">
        <Link to="/dashboard" className="flex items-center gap-2.5">
          <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center">
            <GraduationCap size={16} strokeWidth={1.5} className="text-white" />
          </div>
          <span className="font-semibold text-sm text-slate-900 tracking-tight">{appName}</span>
        </Link>
        <div className="flex items-center gap-0.5">
          {navItems.map((item) => {
            const isActive = location.pathname.startsWith(item.path);
            return (
              <Link
                key={item.path}
                to={buildPath(item.path)}
                className={`px-3.5 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                  isActive
                    ? 'bg-indigo-50 text-indigo-600'
                    : 'text-slate-500 hover:bg-slate-50 hover:text-slate-700'
                }`}
              >
                {item.label}
              </Link>
            );
          })}
        </div>
        <Link
          to="/profile"
          className={`flex items-center gap-2 px-2.5 py-1.5 rounded-lg transition-all duration-200 ${
            location.pathname === '/profile' ? 'bg-indigo-50' : 'hover:bg-slate-50'
          }`}
        >
          <div className="w-7 h-7 bg-indigo-100 rounded-full flex items-center justify-center">
            <span className="text-xs font-semibold text-indigo-600">
              {(user?.display_name || user?.username || 'U')[0].toUpperCase()}
            </span>
          </div>
          <span className="text-sm text-slate-600 font-medium">{user?.display_name || user?.username}</span>
        </Link>
      </nav>

      {/* Mobile bottom nav */}
      <nav className="md:hidden fixed bottom-0 left-0 right-0 bg-white/80 backdrop-blur-xl border-t border-slate-200/60 z-50 safe-area-bottom">
        <div className="flex items-center justify-around py-2 px-1">
          {navItems.map((item) => {
            const isActive = location.pathname.startsWith(item.path);
            const Icon = item.icon;
            return (
              <Link
                key={item.path}
                to={buildPath(item.path)}
                className={`flex flex-col items-center gap-0.5 px-3 py-1 rounded-xl transition-all duration-200 min-w-[48px] ${
                  isActive ? 'text-indigo-600' : 'text-slate-400'
                }`}
              >
                <Icon size={20} strokeWidth={isActive ? 2 : 1.5} />
                <span className={`text-[10px] ${isActive ? 'font-semibold' : 'font-medium'}`}>{item.label}</span>
              </Link>
            );
          })}
        </div>
      </nav>
    </>
  );
}
