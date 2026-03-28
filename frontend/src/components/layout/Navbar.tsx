import { Link, useLocation, useSearchParams } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';

const HomeIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
  </svg>
);

const LearnIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
  </svg>
);

const ProgressIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
  </svg>
);

const TopicsIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
  </svg>
);

const ProfileIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
  </svg>
);

const icons: Record<string, () => JSX.Element> = {
  '/dashboard': HomeIcon,
  '/topics': TopicsIcon,
  '/learn': LearnIcon,
  '/progress': ProgressIcon,
  '/profile': ProfileIcon,
};

const navItems = [
  { path: '/dashboard', label: 'Home' },
  { path: '/topics', label: 'Topics' },
  { path: '/learn', label: 'Learn' },
  { path: '/progress', label: 'Progress' },
  { path: '/profile', label: 'Profile' },
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

  return (
    <>
      {/* Desktop top nav */}
      <nav className="hidden md:flex items-center justify-between px-6 py-3 bg-white/80 backdrop-blur-lg border-b border-slate-200/60 sticky top-0 z-50">
        <Link to="/dashboard" className="flex items-center gap-2">
          <div className="w-8 h-8 bg-indigo-600 rounded-xl flex items-center justify-center">
            <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          </div>
          <span className="font-bold text-base text-slate-900">MasterCS</span>
        </Link>
        <div className="flex items-center gap-1">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={buildPath(item.path)}
              className={`px-4 py-2 rounded-xl text-sm font-medium transition-colors duration-200 ${
                location.pathname.startsWith(item.path)
                  ? 'bg-indigo-50 text-indigo-600'
                  : 'text-slate-500 hover:bg-slate-50 hover:text-slate-700'
              }`}
            >
              {item.label}
            </Link>
          ))}
        </div>
        <div className="flex items-center gap-3">
          <Link
            to="/profile"
            className={`flex items-center gap-2 px-3 py-1.5 rounded-xl transition-colors duration-200 ${
              location.pathname === '/profile' ? 'bg-indigo-50' : 'hover:bg-slate-50'
            }`}
          >
            <div className="w-7 h-7 bg-indigo-100 rounded-full flex items-center justify-center">
              <span className="text-xs font-bold text-indigo-600">
                {(user?.display_name || user?.username || 'U')[0].toUpperCase()}
              </span>
            </div>
            <span className="text-sm text-slate-600">{user?.display_name || user?.username}</span>
          </Link>
        </div>
      </nav>

      {/* Mobile bottom nav */}
      <nav className="md:hidden fixed bottom-0 left-0 right-0 bg-white/80 backdrop-blur-lg border-t border-slate-200/60 z-50 safe-area-bottom">
        <div className="flex items-center justify-around py-1.5">
          {navItems.map((item) => {
            const isActive = location.pathname.startsWith(item.path);
            const IconComponent = icons[item.path];
            return (
              <Link
                key={item.path}
                to={buildPath(item.path)}
                className={`flex flex-col items-center gap-0.5 px-3 py-1.5 rounded-xl transition-colors duration-200 ${
                  isActive ? 'text-indigo-600' : 'text-slate-400'
                }`}
              >
                {IconComponent && <IconComponent />}
                <span className={`text-[10px] ${isActive ? 'font-semibold' : 'font-medium'}`}>{item.label}</span>
              </Link>
            );
          })}
        </div>
      </nav>
    </>
  );
}
