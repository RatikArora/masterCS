import { useEffect, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { conceptsApi, type TopicResponse, type ConceptResponse } from '../api/concepts';
import { authApi } from '../api/auth';
import PageContainer from '../components/layout/PageContainer';
import Card from '../components/ui/Card';
import Loading from '../components/ui/Loading';
import MasteryBadge from '../components/progress/MasteryBadge';

export default function TopicBrowser() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const subjectId = searchParams.get('subject');

  const [topics, setTopics] = useState<TopicResponse[]>([]);
  const [expandedTopic, setExpandedTopic] = useState<string | null>(null);
  const [concepts, setConcepts] = useState<Record<string, ConceptResponse[]>>({});
  const [loadingConcepts, setLoadingConcepts] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [resettingTopic, setResettingTopic] = useState<string | null>(null);

  useEffect(() => {
    if (!subjectId) return;
    conceptsApi.getTopics(subjectId)
      .then((r) => setTopics(r.data.items))
      .finally(() => setLoading(false));
  }, [subjectId]);

  const handleToggleTopic = async (topicId: string) => {
    if (expandedTopic === topicId) {
      setExpandedTopic(null);
      return;
    }
    setExpandedTopic(topicId);
    if (!concepts[topicId]) {
      setLoadingConcepts(topicId);
      try {
        const { data } = await conceptsApi.getConcepts(topicId);
        setConcepts((prev) => ({ ...prev, [topicId]: data.items }));
      } finally {
        setLoadingConcepts(null);
      }
    }
  };

  const handleResetTopic = async (topicId: string, topicName: string) => {
    if (!confirm(`Reset progress for "${topicName}"?`)) return;
    setResettingTopic(topicId);
    try {
      await authApi.resetTopicProgress(topicId);
      const { data } = await conceptsApi.getTopics(subjectId!);
      setTopics(data.items);
      setConcepts((prev) => { const copy = { ...prev }; delete copy[topicId]; return copy; });
    } catch {
      alert('Failed to reset topic');
    } finally {
      setResettingTopic(null);
    }
  };

  if (!subjectId) {
    return (
      <PageContainer>
        <div className="text-center py-12">
          <p className="text-slate-500 text-sm">No subject selected.</p>
          <button onClick={() => navigate('/dashboard')} className="mt-3 text-indigo-600 font-medium text-sm">
            ← Back to Dashboard
          </button>
        </div>
      </PageContainer>
    );
  }

  if (loading) return <Loading text="Loading topics..." />;

  const totalConcepts = topics.reduce((sum, t) => sum + t.concept_count, 0);
  const avgMastery = topics.length > 0
    ? Math.round(topics.reduce((sum, t) => sum + t.mastery_percent, 0) / topics.length)
    : 0;

  return (
    <PageContainer>
      <div className="space-y-5">
        {/* Header */}
        <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.2 }}>
          <button onClick={() => navigate('/dashboard')} className="text-xs text-slate-400 hover:text-slate-600 mb-2 flex items-center gap-1 transition-colors">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 19l-7-7 7-7" />
            </svg>
            Dashboard
          </button>
          <h1 className="text-xl font-bold text-slate-900">Topics</h1>
          <p className="text-xs text-slate-400 mt-0.5">
            {topics.length} topics · {totalConcepts} concepts · {avgMastery}% mastered
          </p>
        </motion.div>

        {/* Start Learning Button */}
        <motion.button
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.05, duration: 0.2 }}
          onClick={() => navigate(`/learn?subject=${subjectId}`)}
          className="w-full py-3 bg-indigo-600 text-white text-sm font-medium rounded-2xl hover:bg-indigo-700 transition-colors duration-200 shadow-sm"
        >
          Start Adaptive Learning
        </motion.button>

        {/* Topic List */}
        <div className="space-y-2.5">
          {topics.map((topic, i) => (
            <motion.div
              key={topic.id}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.08 + i * 0.03, duration: 0.2 }}
            >
              <Card>
                {/* Topic Header */}
                <button
                  onClick={() => handleToggleTopic(topic.id)}
                  className="w-full flex items-center gap-3 text-left"
                >
                  <div className={`w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0 ${
                    topic.mastery_percent >= 80 ? 'bg-emerald-50' :
                    topic.mastery_percent >= 40 ? 'bg-amber-50' :
                    topic.mastery_percent > 0 ? 'bg-indigo-50' : 'bg-slate-50'
                  }`}>
                    <span className={`text-xs font-bold ${
                      topic.mastery_percent >= 80 ? 'text-emerald-600' :
                      topic.mastery_percent >= 40 ? 'text-amber-600' :
                      topic.mastery_percent > 0 ? 'text-indigo-600' : 'text-slate-400'
                    }`}>
                      {Math.round(topic.mastery_percent)}%
                    </span>
                  </div>

                  <div className="flex-1 min-w-0">
                    <h3 className="font-semibold text-slate-900 text-sm">{topic.name}</h3>
                    {topic.description && (
                      <p className="text-xs text-slate-400 truncate mt-0.5">{topic.description}</p>
                    )}
                    <p className="text-[10px] text-slate-400 mt-0.5">{topic.concept_count} concepts · {topic.question_count} questions</p>
                  </div>

                  <div className="w-14 flex-shrink-0">
                    <div className="h-1.5 bg-slate-100 rounded-full overflow-hidden">
                      <motion.div
                        className={`h-full rounded-full ${
                          topic.mastery_percent >= 80 ? 'bg-emerald-500' :
                          topic.mastery_percent >= 40 ? 'bg-amber-500' : 'bg-indigo-500'
                        }`}
                        initial={{ width: 0 }}
                        animate={{ width: `${Math.min(topic.mastery_percent, 100)}%` }}
                        transition={{ delay: 0.15 + i * 0.03, duration: 0.5 }}
                      />
                    </div>
                  </div>

                  <motion.svg
                    animate={{ rotate: expandedTopic === topic.id ? 180 : 0 }}
                    transition={{ duration: 0.15 }}
                    className="w-4 h-4 text-slate-300 flex-shrink-0"
                    fill="none" stroke="currentColor" viewBox="0 0 24 24"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19 9l-7 7-7-7" />
                  </motion.svg>
                </button>

                {/* Expanded Concepts */}
                <AnimatePresence>
                  {expandedTopic === topic.id && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.2 }}
                      className="overflow-hidden"
                    >
                      <div className="mt-3 pt-3 border-t border-slate-100 space-y-1.5">
                        {loadingConcepts === topic.id ? (
                          <p className="text-xs text-slate-400 text-center py-2">Loading concepts...</p>
                        ) : (
                          <>
                            {concepts[topic.id]?.map((concept) => (
                              <button
                                key={concept.id}
                                onClick={() => navigate(`/learn?subject=${subjectId}&concept=${concept.id}`)}
                                className="w-full flex items-center gap-2 px-2 py-2 rounded-xl hover:bg-indigo-50 transition-colors duration-200 text-left group"
                              >
                                <MasteryBadge level={concept.mastery_level} size="sm" />
                                <span className="text-sm text-slate-700 flex-1 group-hover:text-indigo-600 transition-colors">{concept.name}</span>
                                <span className="text-[10px] text-slate-400 mr-1 tabular-nums">
                                  {Math.round(concept.confidence_score * 100)}%
                                </span>
                                <svg className="w-3.5 h-3.5 text-slate-300 group-hover:text-indigo-400 transition-colors flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5l7 7-7 7" />
                                </svg>
                              </button>
                            ))}
                            <button
                              onClick={() => navigate(`/learn?subject=${subjectId}&topic=${topic.id}`)}
                              className="w-full mt-1.5 py-2 text-xs font-medium text-indigo-600 bg-indigo-50 hover:bg-indigo-100 rounded-xl transition-colors duration-200"
                            >
                              Practice All in {topic.name} →
                            </button>
                            <button
                              onClick={() => handleResetTopic(topic.id, topic.name)}
                              disabled={resettingTopic === topic.id}
                              className="w-full mt-1 py-2 text-xs font-medium text-rose-500 bg-rose-50 hover:bg-rose-100 rounded-xl transition-colors duration-200 disabled:opacity-50"
                            >
                              {resettingTopic === topic.id ? 'Resetting...' : 'Reset Progress'}
                            </button>
                          </>
                        )}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </PageContainer>
  );
}
