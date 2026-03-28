import { useEffect, useState } from 'react';
import { useSearchParams, Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { progressApi, type OverallProgress, type TopicProgress, type WeakArea, type DailyStats } from '../api/progress';
import { conceptsApi } from '../api/concepts';
import { learningApi, type WrongQuestionItem } from '../api/learning';
import PageContainer from '../components/layout/PageContainer';
import Card from '../components/ui/Card';
import ProgressRing from '../components/progress/ProgressRing';
import MasteryBadge from '../components/progress/MasteryBadge';
import Loading from '../components/ui/Loading';
import RichText from '../components/ui/RichText';

const masteryColors: Record<string, string> = {
  novice: '#9ca3af', learning: '#3b82f6', familiar: '#f59e0b', proficient: '#22c55e', mastered: '#8b5cf6',
};
const masteryLabels: Record<string, string> = {
  novice: 'Not Started', learning: 'Learning', familiar: 'Familiar', proficient: 'Proficient', mastered: 'Mastered',
};

const difficultyLabels: Record<number, string> = { 1: 'Easy', 2: 'Medium', 3: 'Hard' };
const difficultyColors: Record<number, string> = { 1: 'text-green-600', 2: 'text-amber-600', 3: 'text-red-600' };

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
              className={`w-full rounded-t-sm ${d.questions_answered > 0 ? (isToday ? 'bg-primary-500' : 'bg-primary-300') : 'bg-gray-200'}`}
              title={`${d.date}: ${d.questions_answered} questions, ${d.accuracy}% accuracy`}
            />
          </div>
        );
      })}
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
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'overview' | 'topics' | 'mistakes'>('overview');

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
    Promise.all([
      progressApi.getOverview(sid).then((r) => setOverview(r.data)).catch(() => {}),
      progressApi.getTopicProgress(sid).then((r) => setTopics(r.data)).catch(() => {}),
      progressApi.getWeakAreas(sid).then((r) => setWeakAreas(r.data)).catch(() => {}),
      learningApi.getWrongQuestions(sid, 1, 20).then((r) => setWrongQuestions(r.data.items)).catch(() => {}),
      progressApi.getDailyStats(14).then((r) => setDailyStats(r.data.items)).catch(() => {}),
    ]).finally(() => setLoading(false));
  };

  if (loading) return <Loading text="Loading progress..." />;
  if (!overview) return <p className="text-center text-gray-500 py-20">No data available yet. Start learning first!</p>;

  const dist = overview.mastery_distribution;
  const totalAnswered = overview.total_questions_answered;
  const completionPct = overview.total_concepts > 0
    ? Math.round((overview.concepts_mastered / overview.total_concepts) * 100)
    : 0;

  return (
    <PageContainer>
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
        {/* Header with completion ring */}
        <div className="flex items-center gap-4 mb-6">
          <ProgressRing percent={completionPct} size={72} strokeWidth={6}>
            <span className="text-lg font-bold text-gray-900">{completionPct}%</span>
          </ProgressRing>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Your Progress</h1>
            <p className="text-sm text-gray-500">
              {overview.concepts_mastered} of {overview.total_concepts} concepts mastered
            </p>
          </div>
        </div>
      </motion.div>

      {/* Tab Switcher */}
      <div className="flex gap-1 bg-gray-100 rounded-xl p-1 mb-6">
        {(['overview', 'topics', 'mistakes'] as const).map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`flex-1 py-2 text-sm font-medium rounded-lg transition-all ${
              activeTab === tab
                ? 'bg-white text-gray-900 shadow-sm'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            {tab === 'overview' ? 'Overview' : tab === 'topics' ? 'Topics' : `Mistakes${wrongQuestions.length > 0 ? ` (${wrongQuestions.length})` : ''}`}
          </button>
        ))}
      </div>

      {/* Overview Tab */}
      {activeTab === 'overview' && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
          {/* Stats Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
            {[
              { label: 'Concepts', value: `${overview.concepts_started}/${overview.total_concepts}`, sub: 'started', color: 'text-blue-600' },
              { label: 'Mastered', value: overview.concepts_mastered, sub: 'concepts', color: 'text-purple-600' },
              { label: 'Accuracy', value: `${overview.overall_accuracy}%`, sub: `${totalAnswered} answered`, color: 'text-green-600' },
              { label: 'Total XP', value: overview.total_xp.toLocaleString(), sub: 'earned', color: 'text-amber-600' },
            ].map((stat, i) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.05 }}
              >
                <Card padding="sm" className="text-center">
                  <p className="text-xs text-gray-400 mb-1">{stat.label}</p>
                  <p className={`text-xl font-bold ${stat.color}`}>{stat.value}</p>
                  <p className="text-[10px] text-gray-400">{stat.sub}</p>
                </Card>
              </motion.div>
            ))}
          </div>

          {/* Daily Activity */}
          {dailyStats.length > 0 && (
            <Card className="mb-6">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-semibold text-gray-700">Last 14 Days</h3>
                <p className="text-xs text-gray-400">
                  {dailyStats.reduce((a, d) => a + d.questions_answered, 0)} questions total
                </p>
              </div>
              <MiniBar data={dailyStats} />
              <div className="flex justify-between mt-1 text-[9px] text-gray-400">
                <span>{dailyStats[0]?.date.slice(5)}</span>
                <span>Today</span>
              </div>
            </Card>
          )}

          {/* Mastery Distribution */}
          <Card className="mb-6">
            <h3 className="text-sm font-semibold text-gray-700 mb-3">Mastery Distribution</h3>
            <div className="flex gap-1 h-5 rounded-full overflow-hidden bg-gray-100">
              {Object.entries(dist).map(([level, count]) => {
                const pct = overview.total_concepts > 0 ? (count / overview.total_concepts) * 100 : 0;
                if (pct === 0) return null;
                return (
                  <motion.div
                    key={level}
                    initial={{ width: 0 }}
                    animate={{ width: `${pct}%` }}
                    transition={{ duration: 0.8, ease: 'easeOut' }}
                    className="h-full"
                    style={{ backgroundColor: masteryColors[level] }}
                    title={`${level}: ${count}`}
                  />
                );
              })}
            </div>
            <div className="grid grid-cols-3 sm:grid-cols-5 gap-2 mt-3">
              {Object.entries(dist).map(([level, count]) => (
                <div key={level} className="text-center p-1.5 bg-gray-50 rounded-lg">
                  <span className="w-2.5 h-2.5 rounded-full inline-block mb-1" style={{ backgroundColor: masteryColors[level] }} />
                  <p className="text-xs font-semibold text-gray-700">{count}</p>
                  <p className="text-[9px] text-gray-400">{masteryLabels[level] || level}</p>
                </div>
              ))}
            </div>
          </Card>

          {/* Streak & Performance */}
          <div className="grid grid-cols-2 gap-3 mb-6">
            <Card padding="sm" className="text-center">
              <p className="text-2xl font-bold text-orange-500">{overview.current_streak}</p>
              <p className="text-[10px] text-gray-400">Day Streak</p>
              <p className="text-[9px] text-gray-300 mt-0.5">Best: {overview.longest_streak}</p>
            </Card>
            <Card padding="sm" className="text-center">
              <p className="text-2xl font-bold text-green-500">
                {totalAnswered > 0 ? Math.round(overview.overall_accuracy) : 0}%
              </p>
              <p className="text-[10px] text-gray-400">Overall Accuracy</p>
              <p className="text-[9px] text-gray-300 mt-0.5">{totalAnswered} questions</p>
            </Card>
          </div>

          {/* Weak Areas */}
          {weakAreas.length > 0 && (
            <>
              <h3 className="text-sm font-semibold text-gray-700 mb-3">Areas to Improve</h3>
              <div className="space-y-2 mb-6">
                {weakAreas.map((w) => (
                  <Card
                    key={w.concept_id}
                    padding="sm"
                    className="cursor-pointer hover:border-primary-200 transition-colors"
                    onClick={() => navigate(`/learn?subject=${subjectId}&concept=${w.concept_id}`)}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-gray-800">{w.concept_name}</p>
                        <p className="text-xs text-gray-400">{w.topic_name} · {Math.round(w.accuracy)}% accuracy</p>
                      </div>
                      <div className="flex items-center gap-2">
                        <MasteryBadge level="learning" size="xs" />
                        <svg className="w-4 h-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                        </svg>
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
              className="block w-full py-3 bg-primary-600 text-white text-center font-semibold rounded-xl hover:bg-primary-700 transition-colors text-sm"
            >
              Continue Learning →
            </Link>
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
                  className="cursor-pointer hover:border-primary-200 transition-colors"
                  onClick={() => navigate(`/topics?subject=${subjectId}`)}
                >
                  <div className="flex items-center gap-3">
                    <ProgressRing percent={pct} size={44} strokeWidth={4}>
                      <span className="text-[10px] font-semibold">{pct}%</span>
                    </ProgressRing>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-800 truncate">{t.topic_name}</p>
                      <div className="flex items-center gap-3 mt-0.5">
                        <span className="text-xs text-gray-400">
                          {t.mastered_concepts}/{t.total_concepts} mastered
                        </span>
                        <span className="text-xs text-gray-400">
                          {Math.round(t.avg_confidence * 100)}% confidence
                        </span>
                      </div>
                    </div>
                    <svg className="w-4 h-4 text-gray-300 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
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
              <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-3">
                <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <p className="text-gray-500 text-sm">No wrong answers yet. Keep learning!</p>
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
                        <span className="text-[10px] font-medium text-gray-400 bg-gray-100 px-2 py-0.5 rounded">
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
                    <div className="text-sm text-gray-800 mb-2 leading-relaxed"><RichText content={wq.question_text} /></div>
                    <div className="grid grid-cols-2 gap-2 text-xs">
                      <div className="bg-red-50 rounded-lg px-2.5 py-1.5">
                        <p className="text-[10px] text-red-400 mb-0.5">Your answer</p>
                        <p className="text-red-700 font-medium">{wq.selected_answer}</p>
                      </div>
                      <div className="bg-green-50 rounded-lg px-2.5 py-1.5">
                        <p className="text-[10px] text-green-400 mb-0.5">Correct answer</p>
                        <p className="text-green-700 font-medium">{wq.correct_answer}</p>
                      </div>
                    </div>
                    {wq.explanation && (
                      <div className="text-xs text-gray-500 mt-2 leading-relaxed">
                        <RichText content={wq.explanation} />
                      </div>
                    )}
                    <button
                      onClick={() => navigate(`/learn?subject=${subjectId}&concept=${wq.concept_id}`)}
                      className="mt-2 w-full py-1.5 text-xs font-medium text-primary-600 bg-primary-50 rounded-lg hover:bg-primary-100 transition-colors"
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
