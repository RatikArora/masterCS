import { useEffect, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { conceptsApi, type TopicResponse, type ConceptResponse } from '../api/concepts';
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

  useEffect(() => {
    if (!subjectId) return;
    conceptsApi.getTopics(subjectId)
      .then((r) => setTopics(r.data))
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
        setConcepts((prev) => ({ ...prev, [topicId]: data }));
      } finally {
        setLoadingConcepts(null);
      }
    }
  };

  if (!subjectId) {
    return (
      <PageContainer>
        <div className="text-center py-12">
          <p className="text-gray-500">No subject selected.</p>
          <button onClick={() => navigate('/dashboard')} className="mt-3 text-primary-600 font-medium text-sm">
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
      {/* Header */}
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mb-6">
        <button onClick={() => navigate('/dashboard')} className="text-sm text-gray-400 hover:text-gray-600 mb-2 flex items-center gap-1">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Dashboard
        </button>
        <h1 className="text-2xl font-bold text-gray-900">Topics</h1>
        <p className="text-sm text-gray-500 mt-1">
          {topics.length} topics · {totalConcepts} concepts · {avgMastery}% mastered
        </p>
      </motion.div>

      {/* Start Learning Button */}
      <motion.button
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.05 }}
        onClick={() => navigate(`/learn?subject=${subjectId}`)}
        className="w-full mb-6 py-3.5 bg-primary-600 text-white font-semibold rounded-xl hover:bg-primary-700 transition-colors shadow-lg shadow-primary-600/20"
      >
        Start Adaptive Learning
      </motion.button>

      {/* Topic List */}
      <div className="space-y-3">
        {topics.map((topic, i) => (
          <motion.div
            key={topic.id}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 + i * 0.04 }}
          >
            <Card>
              {/* Topic Header */}
              <button
                onClick={() => handleToggleTopic(topic.id)}
                className="w-full flex items-center gap-3 text-left"
              >
                {/* Mastery indicator */}
                <div className={`w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 ${
                  topic.mastery_percent >= 80 ? 'bg-green-100' :
                  topic.mastery_percent >= 40 ? 'bg-yellow-100' :
                  topic.mastery_percent > 0 ? 'bg-blue-100' : 'bg-gray-100'
                }`}>
                  <span className={`text-sm font-bold ${
                    topic.mastery_percent >= 80 ? 'text-green-600' :
                    topic.mastery_percent >= 40 ? 'text-yellow-600' :
                    topic.mastery_percent > 0 ? 'text-blue-600' : 'text-gray-400'
                  }`}>
                    {Math.round(topic.mastery_percent)}%
                  </span>
                </div>

                <div className="flex-1 min-w-0">
                  <h3 className="font-semibold text-gray-900 text-sm">{topic.name}</h3>
                  {topic.description && (
                    <p className="text-xs text-gray-500 truncate mt-0.5">{topic.description}</p>
                  )}
                  <p className="text-[11px] text-gray-400 mt-0.5">{topic.concept_count} concepts</p>
                </div>

                {/* Progress bar */}
                <div className="w-16 flex-shrink-0">
                  <div className="h-1.5 bg-gray-100 rounded-full overflow-hidden">
                    <motion.div
                      className={`h-full rounded-full ${
                        topic.mastery_percent >= 80 ? 'bg-green-500' :
                        topic.mastery_percent >= 40 ? 'bg-yellow-500' : 'bg-primary-500'
                      }`}
                      initial={{ width: 0 }}
                      animate={{ width: `${Math.min(topic.mastery_percent, 100)}%` }}
                      transition={{ delay: 0.2 + i * 0.04, duration: 0.6 }}
                    />
                  </div>
                </div>

                {/* Expand icon */}
                <motion.svg
                  animate={{ rotate: expandedTopic === topic.id ? 180 : 0 }}
                  className="w-4 h-4 text-gray-400 flex-shrink-0"
                  fill="none" stroke="currentColor" viewBox="0 0 24 24"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </motion.svg>
              </button>

              {/* Expanded Concepts */}
              <AnimatePresence>
                {expandedTopic === topic.id && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0.25 }}
                    className="overflow-hidden"
                  >
                    <div className="mt-3 pt-3 border-t border-gray-100 space-y-2">
                      {loadingConcepts === topic.id ? (
                        <p className="text-xs text-gray-400 text-center py-2">Loading concepts...</p>
                      ) : (
                        <>
                          {concepts[topic.id]?.map((concept) => (
                            <button
                              key={concept.id}
                              onClick={() => navigate(`/learn?subject=${subjectId}&concept=${concept.id}`)}
                              className="w-full flex items-center gap-2 px-2 py-2 rounded-lg hover:bg-primary-50 transition-colors text-left group"
                            >
                              <MasteryBadge level={concept.mastery_level} size="sm" />
                              <span className="text-sm text-gray-700 flex-1 group-hover:text-primary-700 transition-colors">{concept.name}</span>
                              <span className="text-[10px] text-gray-400 mr-1">
                                {Math.round(concept.confidence_score * 100)}%
                              </span>
                              <svg className="w-3.5 h-3.5 text-gray-300 group-hover:text-primary-400 transition-colors flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                              </svg>
                            </button>
                          ))}
                          <button
                            onClick={() => navigate(`/learn?subject=${subjectId}&topic=${topic.id}`)}
                            className="w-full mt-2 py-2 text-xs font-semibold text-primary-600 bg-primary-50 hover:bg-primary-100 rounded-lg transition-colors"
                          >
                            Practice All in {topic.name} →
                          </button>
                        </>
                      )}
                      )}
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </Card>
          </motion.div>
        ))}
      </div>
    </PageContainer>
  );
}
