import { useEffect, useState } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { progressApi, type OverallProgress, type TopicProgress, type WeakArea } from '../api/progress';
import { conceptsApi, type SubjectResponse } from '../api/concepts';
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

const difficultyLabels: Record<number, string> = { 1: 'Easy', 2: 'Medium', 3: 'Hard' };
const difficultyColors: Record<number, string> = { 1: 'text-green-600', 2: 'text-amber-600', 3: 'text-red-600' };

export default function ProgressPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  let subjectId = searchParams.get('subject') || '';
  const [overview, setOverview] = useState<OverallProgress | null>(null);
  const [topics, setTopics] = useState<TopicProgress[]>([]);
  const [weakAreas, setWeakAreas] = useState<WeakArea[]>([]);
  const [wrongQuestions, setWrongQuestions] = useState<WrongQuestionItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'overview' | 'topics' | 'mistakes'>('overview');

  // Auto-detect subject if not provided
  useEffect(() => {
    if (subjectId) {
      loadData(subjectId);
    } else {
      conceptsApi.getSubjects().then((r) => {
        if (r.data.length > 0) {
          const firstId = r.data[0].id;
          setSearchParams({ subject: firstId }, { replace: true });
        } else {
          setLoading(false);
        }
      });
    }
  }, [subjectId]);

  const loadData = (sid: string) => {
    setLoading(true);
    Promise.all([
      progressApi.getOverview(sid).then((r) => setOverview(r.data)),
      progressApi.getTopicProgress(sid).then((r) => setTopics(r.data)),
      progressApi.getWeakAreas(sid).then((r) => setWeakAreas(r.data)),
      learningApi.getWrongQuestions(sid, 1, 20).then((r) => setWrongQuestions(r.data.items)),
    ]).finally(() => setLoading(false));
  };

  if (loading) return <Loading text="Loading progress..." />;
  if (!overview) return <p className="text-center text-gray-500 py-20">No data available yet. Start learning first!</p>;

  const dist = overview.mastery_distribution;
  const totalAnswered = overview.total_questions_answered;

  return (
    <PageContainer>
      <motion.h1 initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-2xl font-bold text-gray-900 mb-6">
        Your Progress
      </motion.h1>

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
              { label: 'Concepts', value: `${overview.concepts_started}/${overview.total_concepts}`, sub: 'started' },
              { label: 'Mastered', value: overview.concepts_mastered, sub: 'concepts' },
              { label: 'Accuracy', value: `${overview.overall_accuracy}%`, sub: `${totalAnswered} answers` },
              { label: 'Total XP', value: overview.total_xp.toLocaleString(), sub: 'earned' },
            ].map((stat, i) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.05 }}
              >
                <Card padding="sm" className="text-center">
                  <p className="text-xs text-gray-400 mb-1">{stat.label}</p>
                  <p className="text-xl font-bold text-gray-900">{stat.value}</p>
                  <p className="text-[10px] text-gray-400">{stat.sub}</p>
                </Card>
              </motion.div>
            ))}
          </div>

          {/* Mastery Distribution */}
          <Card className="mb-6">
            <h3 className="text-sm font-semibold text-gray-700 mb-3">Mastery Distribution</h3>
            <div className="flex gap-1 h-4 rounded-full overflow-hidden bg-gray-100">
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
            <div className="flex flex-wrap gap-3 mt-2">
              {Object.entries(dist).map(([level, count]) => (
                <span key={level} className="flex items-center gap-1 text-xs text-gray-500">
                  <span className="w-2 h-2 rounded-full" style={{ backgroundColor: masteryColors[level] }} />
                  {level}: {count}
                </span>
              ))}
            </div>
          </Card>

          {/* Weak Areas */}
          {weakAreas.length > 0 && (
            <>
              <h3 className="text-sm font-semibold text-gray-700 mb-3">Areas to Improve</h3>
              <div className="space-y-2 mb-6">
                {weakAreas.map((w) => (
                  <Card key={w.concept_id} padding="sm">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-gray-800">{w.concept_name}</p>
                        <p className="text-xs text-gray-400">{w.topic_name} · {w.accuracy}% accuracy</p>
                      </div>
                      <MasteryBadge level="learning" size="xs" />
                    </div>
                    <p className="text-xs text-orange-600 mt-1">{w.recommended_action}</p>
                  </Card>
                ))}
              </div>
            </>
          )}

          {/* Quick action */}
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
          {topics.map((t, i) => (
            <motion.div
              key={t.topic_id}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.03 }}
            >
              <Card padding="sm">
                <div className="flex items-center gap-3">
                  <ProgressRing percent={t.mastery_percent} size={40} strokeWidth={4}>
                    <span className="text-[10px] font-semibold">{Math.round(t.mastery_percent)}%</span>
                  </ProgressRing>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-800 truncate">{t.topic_name}</p>
                    <p className="text-xs text-gray-400">{t.mastered_concepts}/{t.total_concepts} concepts mastered</p>
                  </div>
                </div>
              </Card>
            </motion.div>
          ))}
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
                      <p className="text-xs text-gray-500 mt-2 leading-relaxed">{wq.explanation}</p>
                    )}
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
