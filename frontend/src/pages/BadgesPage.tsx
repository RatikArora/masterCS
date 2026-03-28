import { useEffect, useState, type ReactNode } from 'react';
import { motion } from 'framer-motion';
import { Zap, Flame, ClipboardCheck, Sparkles, Target, CheckCircle } from 'lucide-react';
import PageContainer from '../components/layout/PageContainer';
import Card from '../components/ui/Card';
import { badgesApi, type Badge, type BadgesResponse } from '../api/badges';
import { sounds } from '../utils/sounds';

const CATEGORY_LABELS: Record<string, string> = {
  xp: 'Experience',
  streak: 'Streaks',
  volume: 'Practice',
  mastery: 'Mastery',
  accuracy: 'Precision',
};

const CATEGORY_ICONS: Record<string, { icon: ReactNode; bg: string }> = {
  xp: { icon: <Zap size={14} strokeWidth={1.5} className="text-amber-600" />, bg: 'bg-amber-50' },
  streak: { icon: <Flame size={14} strokeWidth={1.5} className="text-orange-600" />, bg: 'bg-orange-50' },
  volume: { icon: <ClipboardCheck size={14} strokeWidth={1.5} className="text-indigo-600" />, bg: 'bg-indigo-50' },
  mastery: { icon: <Sparkles size={14} strokeWidth={1.5} className="text-violet-600" />, bg: 'bg-violet-50' },
  accuracy: { icon: <Target size={14} strokeWidth={1.5} className="text-emerald-600" />, bg: 'bg-emerald-50' },
};

function CategoryIcon({ category }: { category: string }) {
  const config = CATEGORY_ICONS[category] || { icon: <Sparkles size={14} strokeWidth={1.5} className="text-slate-500" />, bg: 'bg-slate-50' };
  return (
    <div className={`w-7 h-7 rounded-lg ${config.bg} flex items-center justify-center flex-shrink-0`}>
      {config.icon}
    </div>
  );
}

const BADGE_GRADIENTS: Record<string, string> = {
  zap: 'from-amber-400 to-orange-500',
  flame: 'from-orange-400 to-red-500',
  target: 'from-indigo-400 to-indigo-600',
  award: 'from-violet-400 to-violet-600',
  crosshair: 'from-emerald-400 to-teal-500',
};

function BadgeIcon({ icon, earned }: { icon: string; earned: boolean }) {
  const gradient = BADGE_GRADIENTS[icon] || 'from-slate-400 to-slate-500';

  const icons: Record<string, ReactNode> = {
    zap: <Zap size={14} strokeWidth={1.5} className={earned ? 'text-white' : 'text-slate-400'} />,
    flame: <Flame size={14} strokeWidth={1.5} className={earned ? 'text-white' : 'text-slate-400'} />,
    target: <ClipboardCheck size={14} strokeWidth={1.5} className={earned ? 'text-white' : 'text-slate-400'} />,
    award: <Sparkles size={14} strokeWidth={1.5} className={earned ? 'text-white' : 'text-slate-400'} />,
    crosshair: <Target size={14} strokeWidth={1.5} className={earned ? 'text-white' : 'text-slate-400'} />,
  };

  return (
    <div className={`w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 ${
      earned
        ? `bg-gradient-to-br ${gradient} shadow-sm`
        : 'bg-slate-100 border border-slate-200/60'
    }`}>
      {icons[icon] || <Sparkles size={14} strokeWidth={1.5} className={earned ? 'text-white' : 'text-slate-400'} />}
    </div>
  );
}

export default function BadgesPage() {
  const [data, setData] = useState<BadgesResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    badgesApi.getBadges().then(r => {
      setData(r.data);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <PageContainer>
        <div className="flex items-center justify-center min-h-[60vh]">
          <div className="w-6 h-6 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
        </div>
      </PageContainer>
    );
  }

  if (!data) return <PageContainer><p className="text-center text-slate-400 text-sm py-12">Failed to load badges</p></PageContainer>;

  const grouped = data.badges.reduce((acc, b) => {
    (acc[b.category] ??= []).push(b);
    return acc;
  }, {} as Record<string, Badge[]>);

  return (
    <PageContainer>
      <div className="space-y-6">
        {/* Level header */}
        <motion.div
          initial={{ opacity: 0, y: -8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.2 }}
          className="bg-gradient-to-br from-indigo-600 to-indigo-700 rounded-2xl p-6 text-white text-center"
        >
          <p className="text-[10px] uppercase tracking-widest opacity-60 mb-1">Level {data.level.level}</p>
          <p className="text-xl font-semibold">{data.level.title}</p>
          <div className="mt-4 bg-white/20 rounded-full h-2 overflow-hidden">
            <motion.div
              className="bg-white h-full rounded-full"
              initial={{ width: 0 }}
              animate={{ width: `${data.level.progress * 100}%` }}
              transition={{ delay: 0.15, duration: 0.6 }}
            />
          </div>
          <p className="text-xs mt-2 opacity-60 tabular-nums">
            {data.level.current_xp} / {data.level.xp_for_next} XP
          </p>
        </motion.div>

        {/* Earned count */}
        <div className="flex items-center justify-between px-1">
          <h2 className="text-sm font-semibold text-slate-500 uppercase tracking-wider">Achievements</h2>
          <span className="text-xs text-slate-400 tabular-nums">{data.total_earned}/{data.total_available} earned</span>
        </div>

        {/* Badge categories */}
        {Object.entries(grouped).map(([cat, badges]) => (
          <div key={cat}>
            <div className="flex items-center gap-2 mb-3">
              <CategoryIcon category={cat} />
              <h3 className="text-sm font-semibold text-slate-700">{CATEGORY_LABELS[cat] || cat}</h3>
            </div>
            <div className="grid grid-cols-2 gap-2.5">
              {badges.map((badge, i) => (
                <motion.div
                  key={badge.id}
                  initial={{ opacity: 0, scale: 0.97 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.03 * i, duration: 0.15 }}
                >
                  <Card
                    padding="sm"
                    onClick={() => badge.earned && sounds.badge()}
                    className={`cursor-pointer transition-all duration-200 ${
                      badge.earned
                        ? 'border-indigo-100 hover:border-indigo-200 hover:shadow-md'
                        : '!bg-slate-50 !border-slate-200/60 opacity-50 grayscale'
                    }`}
                  >
                    <div className="flex items-center gap-2 mb-2">
                      <BadgeIcon icon={badge.icon} earned={badge.earned} />
                      <div className="flex-1 min-w-0">
                        <p className={`text-xs font-semibold truncate ${badge.earned ? 'text-slate-800' : 'text-slate-400'}`}>
                          {badge.name}
                        </p>
                      </div>
                      {badge.earned && (
                        <CheckCircle size={16} strokeWidth={1.5} className="text-emerald-500 flex-shrink-0" />
                      )}
                    </div>
                    <p className="text-[10px] text-slate-500 leading-tight mb-2.5">{badge.description}</p>
                    <div className="bg-slate-100 rounded-full h-1.5 overflow-hidden">
                      <div
                        className={`h-full rounded-full transition-all ${badge.earned ? 'bg-emerald-500' : 'bg-indigo-400'}`}
                        style={{ width: `${Math.min(badge.progress * 100, 100)}%` }}
                      />
                    </div>
                    <p className="text-[10px] text-slate-400 mt-1 text-right tabular-nums">
                      {badge.current_value}/{badge.target_value}
                    </p>
                  </Card>
                </motion.div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </PageContainer>
  );
}
