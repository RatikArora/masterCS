import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import PageContainer from '../components/layout/PageContainer';
import { badgesApi, type Badge, type BadgesResponse } from '../api/badges';
import { sounds } from '../utils/sounds';

const CATEGORY_LABELS: Record<string, string> = {
  xp: 'Experience',
  streak: 'Streaks',
  volume: 'Practice',
  mastery: 'Mastery',
  accuracy: 'Precision',
};

const CATEGORY_ICONS: Record<string, string> = {
  xp: '⚡',
  streak: '🔥',
  volume: '📚',
  mastery: '🏆',
  accuracy: '🎯',
};

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
          <div className="w-8 h-8 border-3 border-blue-500 border-t-transparent rounded-full animate-spin" />
        </div>
      </PageContainer>
    );
  }

  if (!data) return <PageContainer><p className="text-center text-gray-500 py-12">Failed to load badges</p></PageContainer>;

  const grouped = data.badges.reduce((acc, b) => {
    (acc[b.category] ??= []).push(b);
    return acc;
  }, {} as Record<string, Badge[]>);

  return (
    <PageContainer>
      <div className="max-w-xl mx-auto space-y-6 pb-8">
        {/* Level header */}
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-2xl p-5 text-white text-center"
        >
          <p className="text-xs uppercase tracking-wide opacity-80 mb-0.5">Level {data.level.level}</p>
          <p className="text-2xl font-bold">{data.level.title}</p>
          <div className="mt-3 bg-white/20 rounded-full h-2.5 overflow-hidden">
            <motion.div
              className="bg-white h-full rounded-full"
              initial={{ width: 0 }}
              animate={{ width: `${data.level.progress}%` }}
              transition={{ delay: 0.3, duration: 0.8 }}
            />
          </div>
          <p className="text-xs mt-1.5 opacity-80">
            {data.level.current_xp} / {data.level.xp_for_next} XP
          </p>
        </motion.div>

        {/* Earned count */}
        <div className="flex items-center justify-between px-1">
          <h2 className="text-lg font-bold text-gray-800">Achievements</h2>
          <span className="text-sm text-gray-500">{data.total_earned}/{data.total_available} earned</span>
        </div>

        {/* Badge categories */}
        {Object.entries(grouped).map(([cat, badges]) => (
          <div key={cat}>
            <div className="flex items-center gap-2 mb-2">
              <span className="text-base">{CATEGORY_ICONS[cat] || '🏅'}</span>
              <h3 className="text-sm font-semibold text-gray-700">{CATEGORY_LABELS[cat] || cat}</h3>
            </div>
            <div className="grid grid-cols-2 gap-2">
              {badges.map((badge, i) => (
                <motion.div
                  key={badge.id}
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.05 * i }}
                  onClick={() => badge.earned && sounds.badge()}
                  className={`relative p-3 rounded-xl border transition-all cursor-pointer ${
                    badge.earned
                      ? 'bg-white border-indigo-200 shadow-sm hover:shadow-md'
                      : 'bg-gray-50 border-gray-100 opacity-50'
                  }`}
                >
                  <div className="flex items-center gap-2 mb-1.5">
                    <span className="text-xl">{badge.icon}</span>
                    <div className="flex-1 min-w-0">
                      <p className={`text-xs font-semibold truncate ${badge.earned ? 'text-gray-800' : 'text-gray-400'}`}>
                        {badge.name}
                      </p>
                    </div>
                    {badge.earned && (
                      <svg className="w-4 h-4 text-green-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                      </svg>
                    )}
                  </div>
                  <p className="text-[10px] text-gray-500 leading-tight mb-1.5">{badge.description}</p>
                  {/* Progress bar */}
                  <div className="bg-gray-200 rounded-full h-1.5 overflow-hidden">
                    <div
                      className={`h-full rounded-full transition-all ${badge.earned ? 'bg-green-400' : 'bg-indigo-300'}`}
                      style={{ width: `${Math.min(badge.progress, 100)}%` }}
                    />
                  </div>
                  <p className="text-[10px] text-gray-400 mt-0.5 text-right">
                    {badge.current_value}/{badge.target_value}
                  </p>
                </motion.div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </PageContainer>
  );
}
