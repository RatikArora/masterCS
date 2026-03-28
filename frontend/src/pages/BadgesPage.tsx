import { useEffect, useState, type ReactNode } from 'react';
import { motion } from 'framer-motion';
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

const CATEGORY_COLORS: Record<string, { bg: string; text: string }> = {
  xp: { bg: 'bg-amber-100', text: 'text-amber-600' },
  streak: { bg: 'bg-orange-100', text: 'text-orange-600' },
  volume: { bg: 'bg-primary-100', text: 'text-primary-600' },
  mastery: { bg: 'bg-purple-100', text: 'text-purple-600' },
  accuracy: { bg: 'bg-emerald-100', text: 'text-emerald-600' },
};

function CategoryIcon({ category }: { category: string }) {
  const colors = CATEGORY_COLORS[category] || { bg: 'bg-gray-100', text: 'text-gray-600' };
  const icon: Record<string, ReactNode> = {
    xp: (
      <svg className={`w-4 h-4 ${colors.text}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
      </svg>
    ),
    streak: (
      <svg className={`w-4 h-4 ${colors.text}`} fill="currentColor" viewBox="0 0 24 24">
        <path d="M12 23c-3.6 0-7-2.4-7-7 0-3.1 2.3-6.4 4.3-8.7.4-.5 1.1-.5 1.5-.1l1.3 1.3c.2.2.5.2.7 0C14.5 6 17 3 17 3s2 3.4 2 7c0 5.3-3.2 7.8-4.5 8.6-.3.2-.5.4-.5.7v.2c0 2-1 3.5-2 3.5zm-3.3-7c0 2.5 1.5 4 3.3 4 .3 0 .5-.6.5-1.2 0-.7.3-1.3.8-1.6C14.7 16.3 17 14.5 17 10c0-1.4-.3-2.8-.7-3.9-1.2 1.5-2.8 3.2-4.5 4.1-.8.4-1.7.2-2.3-.4L8.4 8.6C7.2 10.2 5.7 12.5 5.7 16h3z" />
      </svg>
    ),
    volume: (
      <svg className={`w-4 h-4 ${colors.text}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
      </svg>
    ),
    mastery: (
      <svg className={`w-4 h-4 ${colors.text}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
      </svg>
    ),
    accuracy: (
      <svg className={`w-4 h-4 ${colors.text}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <circle cx="12" cy="12" r="10" strokeWidth={2} />
        <circle cx="12" cy="12" r="6" strokeWidth={2} />
        <circle cx="12" cy="12" r="2" strokeWidth={2} />
      </svg>
    ),
  };
  return (
    <div className={`w-7 h-7 rounded-lg ${colors.bg} flex items-center justify-center flex-shrink-0`}>
      {icon[category] || (
        <svg className="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
        </svg>
      )}
    </div>
  );
}

const BADGE_ICON_COLORS: Record<string, { bg: string; text: string; glow: string; gradient: string }> = {
  zap: { bg: 'bg-amber-50', text: 'text-amber-500', glow: 'shadow-amber-200/50', gradient: 'from-amber-400 to-orange-500' },
  flame: { bg: 'bg-orange-50', text: 'text-orange-500', glow: 'shadow-orange-200/50', gradient: 'from-orange-400 to-red-500' },
  target: { bg: 'bg-primary-50', text: 'text-primary-500', glow: 'shadow-blue-200/50', gradient: 'from-blue-400 to-indigo-500' },
  award: { bg: 'bg-purple-50', text: 'text-purple-500', glow: 'shadow-purple-200/50', gradient: 'from-purple-400 to-pink-500' },
  crosshair: { bg: 'bg-emerald-50', text: 'text-emerald-500', glow: 'shadow-emerald-200/50', gradient: 'from-emerald-400 to-teal-500' },
};

function BadgeIcon({ icon, earned }: { icon: string; earned: boolean }) {
  const colors = earned
    ? (BADGE_ICON_COLORS[icon] || { bg: 'bg-gray-50', text: 'text-gray-500', glow: '', gradient: 'from-gray-400 to-gray-500' })
    : { bg: 'bg-gray-100', text: 'text-gray-400', glow: '', gradient: '' };

  const icons: Record<string, ReactNode> = {
    zap: (
      <svg className={`w-4.5 h-4.5 ${earned ? 'text-white' : colors.text}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
      </svg>
    ),
    flame: (
      <svg className={`w-4.5 h-4.5 ${earned ? 'text-white' : colors.text}`} fill="currentColor" viewBox="0 0 24 24">
        <path d="M12 23c-3.6 0-7-2.4-7-7 0-3.1 2.3-6.4 4.3-8.7.4-.5 1.1-.5 1.5-.1l1.3 1.3c.2.2.5.2.7 0C14.5 6 17 3 17 3s2 3.4 2 7c0 5.3-3.2 7.8-4.5 8.6-.3.2-.5.4-.5.7v.2c0 2-1 3.5-2 3.5zm-3.3-7c0 2.5 1.5 4 3.3 4 .3 0 .5-.6.5-1.2 0-.7.3-1.3.8-1.6C14.7 16.3 17 14.5 17 10c0-1.4-.3-2.8-.7-3.9-1.2 1.5-2.8 3.2-4.5 4.1-.8.4-1.7.2-2.3-.4L8.4 8.6C7.2 10.2 5.7 12.5 5.7 16h3z" />
      </svg>
    ),
    target: (
      <svg className={`w-4.5 h-4.5 ${earned ? 'text-white' : colors.text}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
      </svg>
    ),
    award: (
      <svg className={`w-4.5 h-4.5 ${earned ? 'text-white' : colors.text}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
      </svg>
    ),
    crosshair: (
      <svg className={`w-4.5 h-4.5 ${earned ? 'text-white' : colors.text}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <circle cx="12" cy="12" r="10" strokeWidth={2} />
        <circle cx="12" cy="12" r="6" strokeWidth={2} />
        <circle cx="12" cy="12" r="2" strokeWidth={2} />
      </svg>
    ),
  };

  return (
    <div className={`w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0 ${
      earned
        ? `bg-gradient-to-br ${colors.gradient} shadow-lg ${colors.glow}`
        : `${colors.bg} border border-gray-200`
    }`}>
      {icons[icon] || (
        <svg className={`w-4.5 h-4.5 ${earned ? 'text-white' : colors.text}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
        </svg>
      )}
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
          <div className="w-8 h-8 border-3 border-primary-500 border-t-transparent rounded-full animate-spin" />
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
              animate={{ width: `${data.level.progress * 100}%` }}
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
              <CategoryIcon category={cat} />
              <h3 className="text-sm font-semibold text-gray-700">{CATEGORY_LABELS[cat] || cat}</h3>
            </div>
            <div className="grid grid-cols-2 gap-3">
              {badges.map((badge, i) => (
                <motion.div
                  key={badge.id}
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.05 * i }}
                >
                  <Card
                    padding="sm"
                    onClick={() => badge.earned && sounds.badge()}
                    className={`cursor-pointer transition-all ${
                      badge.earned
                        ? 'border-primary-100 hover:border-primary-200 hover:shadow-lg bg-gradient-to-br from-white to-primary-50/30'
                        : '!bg-gray-50 !border-gray-100 opacity-60 grayscale'
                    }`}
                  >
                    <div className="flex items-center gap-2.5 mb-1.5">
                      <BadgeIcon icon={badge.icon} earned={badge.earned} />
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
                    <p className="text-[10px] text-gray-500 leading-tight mb-2">{badge.description}</p>
                    <div className="bg-gray-100 rounded-full h-1.5 overflow-hidden">
                      <div
                        className={`h-full rounded-full transition-all ${badge.earned ? 'bg-green-400' : 'bg-primary-300'}`}
                        style={{ width: `${Math.min(badge.progress * 100, 100)}%` }}
                      />
                    </div>
                    <p className="text-[10px] text-gray-400 mt-1 text-right">
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
