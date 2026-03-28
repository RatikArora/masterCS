import { useEffect, useState } from 'react';
import { useSearchParams, Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ClipboardList, Target, Flame, Zap, Timer, BookOpen, ChevronRight, Check } from 'lucide-react';
import { progressApi, type OverallProgress, type TopicProgress, type WeakArea, type DailyStats } from '../api/progress';
import { conceptsApi, type SubjectResponse } from '../api/concepts';
import { learningApi, type WrongQuestionItem } from '../api/learning';
import PageContainer from '../components/layout/PageContainer';
import Card from '../components/ui/Card';
import ProgressRing from '../components/progress/ProgressRing';
import MasteryBadge from '../components/progress/MasteryBadge';
import Loading from '../components/ui/Loading';
import RichText from '../components/ui/RichText';

const masteryColors: Record<string, string> = {
  novice: 'var(--color-gray-400, #9ca3af)',
  learning: 'var(--color-primary-500, #3b82f6)',
  familiar: 'var(--color-warning, #f59e0b)',
  proficient: 'var(--color-success, #22c55e)',
  mastered: '#8b5cf6',
};
const masteryLabels: Record<string, string> = {
  novice: 'Not Started', learning: 'Learning', familiar: 'Familiar', proficient: 'Proficient', mastered: 'Mastered',
};

const difficultyLabels: Record<number, string> = { 1: 'Easy', 2: 'Medium', 3: 'Hard' };
const difficultyColors: Record<number, string> = { 1: 'text-emerald-600', 2: 'text-amber-600', 3: 'text-rose-600' };

function MiniBar({ data }: { data: DailyStats[] }) {
  const maxQ = Math.max(...data.map((d) => d.questions_answered), 1);
  return (
    <div className="flex items-end gap-[3px] h-16">
      {data.map((d, i) => {
        const h = (d.questions_answered / maxQ) * 100;
        const isToday = i === data.length - 1;
        return (
          <div key={d.date} className="flex-1 flex flex-col items-center gap-0.5">
            <motion.div
              initial={{ height: 0 }}
              animate={{ height: `${Math.max(h, 4)}%` }}
              transition={{ duration: 0.5, delay: i * 0.03 }}
              className={`w-full rounded-t-sm ${d.questions_answered > 0 ? (isToday ? 'bg-indigo-500' : 'bg-indigo-300') : 'bg-slate-200'}`}
              title={`${d.date}: ${d.questions_answered} questions, ${d.accuracy}% accuracy`}
            />
          </div>
        );
      })}
    </div>
  );
}

const subjectPalette = ['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#22c55e', '#06b6d4'];

function DonutChart({ distribution, total }: { distribution: Record<string, number>; total: number }) {
  const size = 140;
  const sw = 24;
  const r = (size - sw) / 2;
  const C = 2 * Math.PI * r;
  let cum = 0;
  const segs = Object.entries(distribution)
    .filter(([, c]) => c > 0)
    .map(([level, count], i) => {
      const len = (count / Math.max(total, 1)) * C;
      const off = cum;
      cum += len;
      return { level, count, len, off, delay: i * 0.12 };
    });

  return (
    <div className="relative inline-flex items-center justify-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90">
        <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="#f3f4f6" strokeWidth={sw} />
        {segs.map((s) => (
          <motion.circle
            key={s.level}
            cx={size / 2} cy={size / 2} r={r}
            fill="none"
            stroke={masteryColors[s.level]}
            strokeWidth={sw}
            strokeLinecap="butt"
            strokeDasharray={`${s.len} ${C - s.len}`}
            strokeDashoffset={-s.off}
            initial={{ strokeDasharray: `0 ${C}` }}
            animate={{ strokeDasharray: `${s.len} ${C - s.len}` }}
            transition={{ duration: 0.8, delay: s.delay, ease: 'easeOut' }}
          />
        ))}
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-xl font-bold text-slate-900">{total}</span>
        <span className="text-[9px] text-slate-400">concepts</span>
      </div>
    </div>
  );
}

function WeeklyHeatmap({ data }: { data: DailyStats[] }) {
  const last7 = data.slice(-7);
  const maxQ = Math.max(...last7.map((d) => d.questions_answered), 1);
  const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  const intensity = (n: number) => {
    if (n === 0) return 'bg-slate-100';
    const ratio = n / maxQ;
    if (ratio <= 0.25) return 'bg-emerald-200';
    if (ratio <= 0.5) return 'bg-emerald-300';
    if (ratio <= 0.75) return 'bg-emerald-500';
    return 'bg-emerald-600';
  };

  return (
    <div className="flex gap-1.5">
      {last7.map((d, i) => {
        const dow = new Date(d.date + 'T12:00:00').getDay();
        return (
          <motion.div
            key={d.date}
            initial={{ scale: 0, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: i * 0.06 }}
            className="flex-1 flex flex-col items-center gap-1"
          >
            <span className="text-[9px] text-slate-400">{dayNames[dow]}</span>
            <div
              className={`w-full aspect-square rounded-xl ${intensity(d.questions_answered)} flex items-center justify-center`}
              title={`${d.date}: ${d.questions_answered} questions`}
            >
              {d.questions_answered > 0 && (
                <span className={`text-[10px] font-semibold ${d.questions_answered / maxQ > 0.5 ? 'text-white' : 'text-emerald-800'}`}>
                  {d.questions_answered}
                </span>
              )}
            </div>
          </motion.div>
        );
      })}
    </div>
  );
}

function AccuracyTrendLine({ data }: { data: DailyStats[] }) {
  const pts = data.filter((d) => d.questions_answered > 0).slice(-10);
  if (pts.length < 2) return <p className="text-xs text-slate-400 text-center py-6">Need more sessions for accuracy trend</p>;
  const W = 320, H = 140;
  const P = { t: 15, r: 15, b: 28, l: 35 };
  const cw = W - P.l - P.r, ch = H - P.t - P.b;
  const accs = pts.map((d) => d.accuracy);
  const lo = Math.max(0, Math.floor(Math.min(...accs) / 10) * 10 - 5);
  const hi = Math.min(100, Math.ceil(Math.max(...accs) / 10) * 10 + 5);
  const rng = hi - lo || 1;
  const coords = pts.map((d, i) => ({
    x: P.l + (i / (pts.length - 1)) * cw,
    y: P.t + ch - ((d.accuracy - lo) / rng) * ch,
    acc: d.accuracy, date: d.date,
  }));
  const line = coords.map((c, i) => `${i === 0 ? 'M' : 'L'}${c.x},${c.y}`).join(' ');
  const area = `${line} L${coords[coords.length - 1].x},${P.t + ch} L${coords[0].x},${P.t + ch} Z`;

  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="w-full" preserveAspectRatio="xMidYMid meet">
      <defs>
        <linearGradient id="trendFill" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#3b82f6" stopOpacity="0.15" />
          <stop offset="100%" stopColor="#3b82f6" stopOpacity="0.01" />
        </linearGradient>
      </defs>
      {[0, 0.5, 1].map((p) => {
        const y = P.t + ch * (1 - p);
        return (
          <g key={p}>
            <line x1={P.l} y1={y} x2={W - P.r} y2={y} stroke="#f3f4f6" strokeWidth="1" />
            <text x={P.l - 5} y={y + 3} textAnchor="end" fontSize="7" fill="#9ca3af">{Math.round(lo + rng * p)}%</text>
          </g>
        );
      })}
      <motion.path d={area} fill="url(#trendFill)" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.8 }} />
      <motion.path
        d={line} fill="none" stroke="#3b82f6" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
        initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ duration: 1, ease: 'easeOut' }}
      />
      {coords.map((c, i) => (
        <motion.circle
          key={i} cx={c.x} cy={c.y} r="3.5" fill="white" stroke="#3b82f6" strokeWidth="1.5"
          initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.6 + i * 0.06 }}
        >
          <title>{`${c.date}: ${Math.round(c.acc)}%`}</title>
        </motion.circle>
      ))}
      {coords.filter((_, i) => i === 0 || i === coords.length - 1).map((c) => (
        <text key={c.date} x={c.x} y={H - 6} textAnchor="middle" fontSize="7" fill="#9ca3af">{c.date.slice(5)}</text>
      ))}
    </svg>
  );
}

function SubjectComparisonBars({ subjects, overviews }: { subjects: SubjectResponse[]; overviews: Record<string, OverallProgress> }) {
  const items = subjects
    .filter((s) => overviews[s.id])
    .map((s, i) => {
      const ov = overviews[s.id];
      return {
        name: s.name,
        color: s.color || subjectPalette[i % subjectPalette.length],
        accuracy: Math.round(ov.overall_accuracy),
        questions: ov.total_questions_answered,
        masteryPct: ov.total_concepts > 0 ? Math.round((ov.concepts_mastered / ov.total_concepts) * 100) : 0,
      };
    });

  if (items.length === 0) return <p className="text-xs text-slate-400 text-center py-6">No subject data available</p>;

  const maxQ = Math.max(...items.map((d) => d.questions), 1);
  const metrics: { label: string; key: 'accuracy' | 'questions' | 'masteryPct'; max: number; suffix: string }[] = [
    { label: 'Accuracy', key: 'accuracy', max: 100, suffix: '%' },
    { label: 'Questions Attempted', key: 'questions', max: maxQ, suffix: '' },
    { label: 'Mastery', key: 'masteryPct', max: 100, suffix: '%' },
  ];

  return (
    <div className="space-y-5">
      <div className="flex flex-wrap gap-3">
        {items.map((d) => (
          <div key={d.name} className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded-full flex-shrink-0" style={{ backgroundColor: d.color }} />
            <span className="text-xs text-slate-600">{d.name}</span>
          </div>
        ))}
      </div>
      {metrics.map((m) => (
        <div key={m.label}>
          <p className="text-xs text-slate-500 mb-2">{m.label}</p>
          <div className="space-y-2">
            {items.map((d, i) => {
              const val = d[m.key];
              const pct = (val / m.max) * 100;
              return (
                <motion.div
                  key={d.name}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.06 }}
                  className="flex items-center gap-2"
                >
                  <span className="text-[10px] text-slate-500 w-16 truncate">{d.name}</span>
                  <div className="flex-1 h-7 bg-slate-100 rounded-xl overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${Math.max(pct, 3)}%` }}
                      transition={{ duration: 0.8, ease: 'easeOut' }}
                      className="h-full rounded-xl flex items-center justify-end pr-2"
                      style={{ backgroundColor: d.color }}
                    >
                      {pct > 15 && (
                        <span className="text-[10px] font-semibold text-white drop-shadow-sm">
                          {val}{m.suffix}
                        </span>
                      )}
                    </motion.div>
                  </div>
                  {pct <= 15 && (
                    <span className="text-[10px] font-semibold text-slate-500">{val}{m.suffix}</span>
                  )}
                </motion.div>
              );
            })}
          </div>
        </div>
      ))}
    </div>
  );
}

export default function ProgressPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();
  const subjectId = searchParams.get('subject') || '';
  const [overview, setOverview] = useState<OverallProgress | null>(null);
  const [topics, setTopics] = useState<TopicProgress[]>([]);
  const [weakAreas, setWeakAreas] = useState<WeakArea[]>([]);
  const [wrongQuestions, setWrongQuestions] = useState<WrongQuestionItem[]>([]);
  const [dailyStats, setDailyStats] = useState<DailyStats[]>([]);
  const [allSubjects, setAllSubjects] = useState<SubjectResponse[]>([]);
  const [allOverviews, setAllOverviews] = useState<Record<string, OverallProgress>>({});
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'overview' | 'topics' | 'analytics' | 'mistakes'>('overview');

  useEffect(() => {
    if (subjectId) {
      loadData(subjectId);
    } else {
      conceptsApi.getSubjects().then((r) => {
        if (r.data.length > 0) {
          setSearchParams({ subject: r.data[0].id }, { replace: true });
        } else {
          setLoading(false);
        }
      });
    }
  }, [subjectId]);

  const loadData = (sid: string) => {
    setLoading(true);
    const subjectsPromise = conceptsApi.getSubjects().then((r) => {
      setAllSubjects(r.data);
      return Promise.all(
        r.data.map((s) =>
          progressApi.getOverview(s.id).then((res) => [s.id, res.data] as const).catch(() => null)
        )
      ).then((results) => {
        const map: Record<string, OverallProgress> = {};
        for (const r of results) if (r) map[r[0]] = r[1];
        setAllOverviews(map);
      });
    }).catch(() => {});
    Promise.all([
      progressApi.getOverview(sid).then((r) => setOverview(r.data)).catch(() => {}),
      progressApi.getTopicProgress(sid).then((r) => setTopics(r.data)).catch(() => {}),
      progressApi.getWeakAreas(sid).then((r) => setWeakAreas(r.data.items)).catch(() => {}),
      learningApi.getWrongQuestions(sid, 1, 20).then((r) => setWrongQuestions(r.data.items)).catch(() => {}),
      progressApi.getDailyStats(30).then((r) => setDailyStats(r.data.items)).catch(() => {}),
      subjectsPromise,
    ]).finally(() => setLoading(false));
  };

  if (loading) return <Loading text="Loading progress..." />;
  if (!overview) return <p className="text-center text-slate-500 py-20">No data available yet. Start learning first!</p>;

  const dist = overview.mastery_distribution;
  const totalAnswered = overview.total_questions_answered;
  const completionPct = overview.total_concepts > 0
    ? Math.round((overview.concepts_mastered / overview.total_concepts) * 100)
    : 0;

  const totalDailyQuestions = dailyStats.reduce((a, d) => a + d.questions_answered, 0);
  const totalTimeMinutes = dailyStats.reduce((a, d) => a + d.time_spent_minutes, 0);
  const avgSpeedSeconds = totalDailyQuestions > 0 ? Math.round((totalTimeMinutes * 60) / totalDailyQuestions) : 0;
  const subjectsCovered = allSubjects.filter((s) => allOverviews[s.id] && allOverviews[s.id].total_questions_answered > 0).length;

  return (
    <PageContainer>
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
        {/* Header with completion ring */}
        <div className="flex items-center gap-4 mb-6">
          <ProgressRing percent={completionPct} size={72} strokeWidth={6}>
            <span className="text-lg font-bold text-slate-900">{completionPct}%</span>
          </ProgressRing>
          <div>
            <h1 className="text-xl font-bold text-slate-900">Your Progress</h1>
            <p className="text-sm text-slate-500">
              {overview.concepts_mastered} of {overview.total_concepts} concepts mastered
            </p>
          </div>
        </div>
      </motion.div>

      {/* Tab Switcher */}
      <div className="flex gap-1 bg-slate-100 rounded-lg p-1 mb-6">
        {(['overview', 'topics', 'analytics', 'mistakes'] as const).map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`flex-1 py-2 text-sm font-medium rounded-lg transition-all duration-200 ${
              activeTab === tab
                ? 'bg-white text-slate-900 shadow-sm'
                : 'text-slate-500 hover:text-slate-700'
            }`}
          >
            {tab === 'overview' ? 'Overview' : tab === 'topics' ? 'Topics' : tab === 'analytics' ? 'Analytics' : `Mistakes${wrongQuestions.length > 0 ? ` (${wrongQuestions.length})` : ''}`}
          </button>
        ))}
      </div>

      {/* Overview Tab */}
      {activeTab === 'overview' && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
          {/* Stats Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-6">
            {[
              { label: 'Total Questions', value: totalAnswered.toLocaleString(), sub: 'answered', color: 'text-indigo-600', icon: <ClipboardList size={18} strokeWidth={1.5} /> },
              { label: 'Accuracy', value: `${Math.round(overview.overall_accuracy)}%`, sub: `${totalAnswered > 0 ? Math.round((overview.overall_accuracy / 100) * totalAnswered) : 0} correct`, color: 'text-emerald-600', icon: <Target size={18} strokeWidth={1.5} /> },
              { label: 'Best Streak', value: overview.longest_streak, sub: `current: ${overview.current_streak}`, color: 'text-orange-600', icon: <Flame size={18} strokeWidth={1.5} /> },
              { label: 'Total XP', value: overview.total_xp.toLocaleString(), sub: 'earned', color: 'text-amber-600', icon: <Zap size={18} strokeWidth={1.5} /> },
              { label: 'Avg Speed', value: avgSpeedSeconds > 0 ? `${avgSpeedSeconds}s` : '—', sub: 'per question', color: 'text-purple-600', icon: <Timer size={18} strokeWidth={1.5} /> },
              { label: 'Subjects', value: subjectsCovered || allSubjects.length, sub: 'covered', color: 'text-cyan-600', icon: <BookOpen size={18} strokeWidth={1.5} /> },
            ].map((stat, i) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.05 }}
              >
                <Card padding="sm" className="text-center">
                  <p className="text-xs text-slate-400 mb-1 flex items-center justify-center gap-1">{stat.icon} {stat.label}</p>
                  <p className={`text-xl font-bold ${stat.color}`}>{stat.value}</p>
                  <p className="text-[10px] text-slate-400">{stat.sub}</p>
                </Card>
              </motion.div>
            ))}
          </div>

          {/* Daily Activity */}
          {dailyStats.length > 0 && (
            <Card className="mb-6">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-semibold text-slate-700">Last 14 Days</h3>
                <p className="text-xs text-slate-400">
                  {dailyStats.reduce((a, d) => a + d.questions_answered, 0)} questions total
                </p>
              </div>
              <MiniBar data={dailyStats.slice(-14)} />
              <div className="flex justify-between mt-1 text-[9px] text-slate-400">
                <span>{dailyStats[0]?.date.slice(5)}</span>
                <span>Today</span>
              </div>
            </Card>
          )}

          {/* Mastery Distribution */}
          <Card className="mb-6">
            <h3 className="text-sm font-semibold text-slate-700 mb-3">Mastery Distribution</h3>
            <div className="flex flex-col sm:flex-row items-center gap-4">
              <DonutChart distribution={dist} total={overview.total_concepts} />
              <div className="grid grid-cols-3 sm:grid-cols-1 gap-2 flex-1 w-full sm:w-auto">
                {Object.entries(dist).map(([level, count]) => {
                  const pct = overview.total_concepts > 0 ? Math.round((count / overview.total_concepts) * 100) : 0;
                  return (
                    <div key={level} className="flex items-center gap-2 p-2 bg-slate-50 rounded-xl">
                      <span className="w-3 h-3 rounded-full flex-shrink-0" style={{ backgroundColor: masteryColors[level] }} />
                      <div className="flex-1 min-w-0">
                        <div className="flex items-baseline gap-1">
                          <span className="text-sm font-semibold text-slate-700">{count}</span>
                          <span className="text-[9px] text-slate-400">({pct}%)</span>
                        </div>
                        <p className="text-[9px] text-slate-400 truncate">{masteryLabels[level] || level}</p>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </Card>

          {/* Weekly Activity Heatmap */}
          {dailyStats.length >= 7 && (
            <Card className="mb-6">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-sm font-semibold text-slate-700">This Week</h3>
                <div className="flex items-center gap-1 text-[9px] text-slate-400">
                  <span>Less</span>
                  <span className="w-3 h-3 rounded bg-slate-100" />
                  <span className="w-3 h-3 rounded bg-emerald-200" />
                  <span className="w-3 h-3 rounded bg-emerald-400" />
                  <span className="w-3 h-3 rounded bg-emerald-600" />
                  <span>More</span>
                </div>
              </div>
              <WeeklyHeatmap data={dailyStats} />
            </Card>
          )}

          {/* Streak & Performance */}
          <div className="grid grid-cols-2 gap-3 mb-6">
            <Card padding="sm" className="text-center">
              <p className="text-xl font-bold text-orange-500">{overview.current_streak}</p>
              <p className="text-[10px] text-slate-400">Day Streak</p>
              <p className="text-[9px] text-slate-300 mt-0.5">Best: {overview.longest_streak}</p>
            </Card>
            <Card padding="sm" className="text-center">
              <p className="text-xl font-bold text-emerald-500">
                {totalAnswered > 0 ? Math.round(overview.overall_accuracy) : 0}%
              </p>
              <p className="text-[10px] text-slate-400">Overall Accuracy</p>
              <p className="text-[9px] text-slate-300 mt-0.5">{totalAnswered} questions</p>
            </Card>
          </div>

          {/* Topic-wise Breakdown */}
          {topics.length > 0 && (
            <Card className="mb-6">
              <h3 className="text-sm font-semibold text-slate-700 mb-3">Topic Breakdown</h3>
              <div className="space-y-3">
                {topics.map((t) => {
                  const pct = Math.round(t.mastery_percent);
                  const conf = Math.round(t.avg_confidence * 100);
                  return (
                    <div key={t.topic_id}>
                      <div className="flex items-center justify-between mb-1">
                        <p className="text-xs font-medium text-slate-700 truncate flex-1">{t.topic_name}</p>
                        <div className="flex items-center gap-2">
                          <span className="text-[10px] text-slate-400">{t.mastered_concepts}/{t.total_concepts}</span>
                          <span className="text-[10px] font-semibold text-slate-600">{pct}%</span>
                        </div>
                      </div>
                      <div className="flex gap-1 h-2 rounded-full overflow-hidden bg-slate-100">
                        <motion.div
                          initial={{ width: 0 }}
                          animate={{ width: `${pct}%` }}
                          transition={{ duration: 0.6, ease: 'easeOut' }}
                          className={`h-full rounded-full ${
                            pct >= 80 ? 'bg-emerald-400' : pct >= 50 ? 'bg-amber-400' : pct >= 20 ? 'bg-indigo-400' : 'bg-slate-300'
                          }`}
                        />
                      </div>
                      <div className="flex items-center gap-2 mt-0.5">
                        <span className="text-[9px] text-slate-400">{conf}% confidence</span>
                      </div>
                    </div>
                  );
                })}
              </div>
            </Card>
          )}

          {/* Weak Areas */}
          {weakAreas.length > 0 && (
            <>
              <h3 className="text-sm font-semibold text-slate-700 mb-3">Areas to Improve</h3>
              <div className="space-y-2 mb-6">
                {weakAreas.map((w) => (
                  <Card
                    key={w.concept_id}
                    padding="sm"
                    className="cursor-pointer hover:border-indigo-200 transition-all duration-200"
                    onClick={() => navigate(`/learn?subject=${subjectId}&concept=${w.concept_id}`)}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-slate-800">{w.concept_name}</p>
                        <p className="text-xs text-slate-400">{w.topic_name} · {Math.round(w.accuracy)}% accuracy</p>
                      </div>
                      <div className="flex items-center gap-2">
                        <MasteryBadge level="learning" size="xs" />
                        <ChevronRight size={16} strokeWidth={1.5} className="text-slate-300" />
                      </div>
                    </div>
                    <p className="text-xs text-orange-600 mt-1">{w.recommended_action}</p>
                  </Card>
                ))}
              </div>
            </>
          )}

          {subjectId && (
            <Link
              to={`/learn?subject=${subjectId}`}
              className="block w-full py-3 bg-indigo-600 text-white text-center font-semibold rounded-xl hover:bg-indigo-700 transition-all duration-200 text-sm"
            >
              Continue Learning →
            </Link>
          )}
        </motion.div>
      )}

      {/* Analytics Tab */}
      {activeTab === 'analytics' && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
          {/* Subject Comparison */}
          <Card>
            <h3 className="text-sm font-semibold text-slate-700 mb-4">Subject Comparison</h3>
            <SubjectComparisonBars subjects={allSubjects} overviews={allOverviews} />
          </Card>

          {/* Accuracy Trend */}
          <Card>
            <h3 className="text-sm font-semibold text-slate-700 mb-3">Accuracy Trend</h3>
            <AccuracyTrendLine data={dailyStats} />
          </Card>

          {/* Per-Subject Stats */}
          {allSubjects.filter((s) => allOverviews[s.id]).length > 0 && (
            <Card>
              <h3 className="text-sm font-semibold text-slate-700 mb-3">Subject Details</h3>
              <div className="space-y-3">
                {allSubjects.filter((s) => allOverviews[s.id]).map((s, i) => {
                  const ov = allOverviews[s.id];
                  return (
                    <motion.div
                      key={s.id}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.08 }}
                      className="flex items-center gap-3 p-3 bg-slate-50 rounded-xl"
                    >
                      <span
                        className="w-3 h-3 rounded-full flex-shrink-0"
                        style={{ backgroundColor: s.color || subjectPalette[i % subjectPalette.length] }}
                      />
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-slate-800 truncate">{s.name}</p>
                        <div className="flex flex-wrap items-center gap-x-3 gap-y-0.5 mt-0.5 text-[10px] text-slate-400">
                          <span>{ov.total_questions_answered} questions</span>
                          <span>{Math.round(ov.overall_accuracy)}% accuracy</span>
                          <span>{ov.concepts_mastered}/{ov.total_concepts} mastered</span>
                        </div>
                      </div>
                      <div className="text-right flex-shrink-0">
                        <p className="text-sm font-bold text-amber-600">{ov.total_xp.toLocaleString()}</p>
                        <p className="text-[9px] text-slate-400">XP</p>
                      </div>
                    </motion.div>
                  );
                })}
              </div>
            </Card>
          )}
        </motion.div>
      )}

      {/* Topics Tab */}
      {activeTab === 'topics' && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-2">
          {topics.map((t, i) => {
            const pct = Math.round(t.mastery_percent);
            return (
              <motion.div
                key={t.topic_id}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.03 }}
              >
                <Card
                  padding="sm"
                  className="cursor-pointer hover:border-indigo-200 transition-all duration-200"
                  onClick={() => navigate(`/topics?subject=${subjectId}`)}
                >
                  <div className="flex items-center gap-3">
                    <ProgressRing percent={pct} size={44} strokeWidth={4}>
                      <span className="text-[10px] font-semibold">{pct}%</span>
                    </ProgressRing>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-slate-800 truncate">{t.topic_name}</p>
                      <div className="flex items-center gap-3 mt-0.5">
                        <span className="text-xs text-slate-400">
                          {t.mastered_concepts}/{t.total_concepts} mastered
                        </span>
                        <span className="text-xs text-slate-400">
                          {Math.round(t.avg_confidence * 100)}% confidence
                        </span>
                      </div>
                    </div>
                    <ChevronRight size={16} strokeWidth={1.5} className="text-slate-300 flex-shrink-0" />
                  </div>
                </Card>
              </motion.div>
            );
          })}
        </motion.div>
      )}

      {/* Mistakes Tab */}
      {activeTab === 'mistakes' && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
          {wrongQuestions.length === 0 ? (
            <div className="text-center py-12">
              <div className="w-12 h-12 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-3">
                <Check size={24} strokeWidth={1.5} className="text-emerald-600" />
              </div>
              <p className="text-slate-500 text-sm">No wrong answers yet. Keep learning!</p>
            </div>
          ) : (
            <div className="space-y-3">
              {wrongQuestions.map((wq, i) => (
                <motion.div
                  key={wq.question_id}
                  initial={{ opacity: 0, y: 5 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.03 }}
                >
                  <Card padding="sm">
                    <div className="flex items-start justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <span className="text-[10px] font-medium text-slate-400 bg-slate-100 px-2 py-0.5 rounded">
                          {wq.concept_name}
                        </span>
                        <span className={`text-[10px] font-medium ${difficultyColors[wq.difficulty]}`}>
                          {difficultyLabels[wq.difficulty]}
                        </span>
                      </div>
                      <span className="text-[10px] text-amber-600 bg-amber-50 px-2 py-0.5 rounded font-medium">
                        {wq.attempt_count}× wrong
                      </span>
                    </div>
                    <div className="text-sm text-slate-800 mb-2 leading-relaxed"><RichText content={wq.question_text} /></div>
                    <div className="grid grid-cols-2 gap-2 text-xs">
                      <div className="bg-rose-50 rounded-xl px-2.5 py-1.5">
                        <p className="text-[10px] text-rose-400 mb-0.5">Your answer</p>
                        <p className="text-rose-700 font-medium">{wq.selected_answer}</p>
                      </div>
                      <div className="bg-emerald-50 rounded-xl px-2.5 py-1.5">
                        <p className="text-[10px] text-emerald-400 mb-0.5">Correct answer</p>
                        <p className="text-emerald-700 font-medium">{wq.correct_answer}</p>
                      </div>
                    </div>
                    {wq.explanation && (
                      <div className="text-xs text-slate-500 mt-2 leading-relaxed">
                        <RichText content={wq.explanation} />
                      </div>
                    )}
                    <button
                      onClick={() => navigate(`/learn?subject=${subjectId}&concept=${wq.concept_id}`)}
                      className="mt-2 w-full py-1.5 text-xs font-medium text-indigo-600 bg-indigo-50 rounded-xl hover:bg-indigo-100 transition-colors"
                    >
                      Practice this concept →
                    </button>
                  </Card>
                </motion.div>
              ))}
            </div>
          )}
        </motion.div>
      )}
    </PageContainer>
  );
}
