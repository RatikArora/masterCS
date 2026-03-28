import { useEffect, useState, useCallback } from 'react';
import { useSearchParams } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { useLearningStore } from '../store/learningStore';
import { learningApi, type ConceptNotes } from '../api/learning';
import OptionButton from '../components/learning/OptionButton';
import FeedbackOverlay from '../components/learning/FeedbackOverlay';
import DifficultyBadge from '../components/learning/DifficultyBadge';
import MasteryBadge from '../components/progress/MasteryBadge';
import Loading from '../components/ui/Loading';
import Button from '../components/ui/Button';
import RichText from '../components/ui/RichText';

export default function LearnPage() {
  const [searchParams] = useSearchParams();
  const subjectId = searchParams.get('subject') || '';
  const conceptId = searchParams.get('concept') || undefined;
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [showNotes, setShowNotes] = useState(false);
  const [notes, setNotes] = useState<ConceptNotes | null>(null);
  const [loadingNotes, setLoadingNotes] = useState(false);

  const {
    session, result, isLoadingQuestion, isSubmitting, showFeedback, error,
    fetchNextQuestion, submitAnswer, dismissFeedback,
  } = useLearningStore();

  useEffect(() => {
    if (subjectId) fetchNextQuestion(subjectId, conceptId);
  }, [subjectId, conceptId]);

  const handleSelect = useCallback((option: string) => {
    if (showFeedback || isSubmitting || selectedOption) return;
    setSelectedOption(option);
    if (session) {
      setTimeout(() => {
        submitAnswer(session.question.id, option);
      }, 300);
    }
  }, [showFeedback, isSubmitting, selectedOption, session, submitAnswer]);

  const handleContinue = useCallback(() => {
    setSelectedOption(null);
    setShowNotes(false);
    setNotes(null);
    dismissFeedback();
    if (subjectId) fetchNextQuestion(subjectId, conceptId);
  }, [subjectId, conceptId, dismissFeedback, fetchNextQuestion]);

  const handleShowNotes = useCallback(async () => {
    if (!session) return;
    if (notes && notes.id === session.question.concept_id) {
      setShowNotes(!showNotes);
      return;
    }
    setLoadingNotes(true);
    try {
      const { data } = await learningApi.getConceptNotes(session.question.concept_id);
      setNotes(data);
      setShowNotes(true);
    } catch {
      // silently fail
    } finally {
      setLoadingNotes(false);
    }
  }, [session, notes, showNotes]);

  if (!subjectId) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <p className="text-gray-500">No subject selected. Go back to dashboard.</p>
      </div>
    );
  }

  if (isLoadingQuestion) return <Loading text="Finding the perfect question..." />;

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4 px-4">
        <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center">
          <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <p className="text-gray-600 text-center">{error}</p>
        <Button onClick={() => fetchNextQuestion(subjectId)} variant="secondary">Try Again</Button>
      </div>
    );
  }

  if (!session) return null;

  const { question, session_stats, concept_progress } = session;

  return (
    <div className="max-w-xl mx-auto px-4 py-6 pb-24 md:pb-8">
      {/* Concept focus banner */}
      {conceptId && (
        <motion.div
          initial={{ opacity: 0, y: -5 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-4 flex items-center gap-2 px-3 py-2 bg-primary-50 border border-primary-100 rounded-xl"
        >
          <svg className="w-4 h-4 text-primary-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          <span className="text-xs font-medium text-primary-700 flex-1 truncate">
            Focused: {question.concept_name}
          </span>
          <button
            onClick={() => window.location.href = `/learn?subject=${subjectId}`}
            className="text-[10px] text-primary-500 hover:text-primary-700 font-medium"
          >
            Exit Focus
          </button>
        </motion.div>
      )}

      {/* Top bar */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="flex items-center justify-between mb-6"
      >
        <div className="flex items-center gap-2">
          <MasteryBadge level={concept_progress.mastery_level} size="xs" />
          <span className="text-xs text-gray-400 truncate max-w-[140px]">{question.topic_name}</span>
        </div>
        <div className="flex items-center gap-3 text-xs text-gray-400">
          <span className="flex items-center gap-1">
            <svg className="w-3.5 h-3.5 text-orange-400" fill="currentColor" viewBox="0 0 20 20">
              <path d="M12.395 2.553a1 1 0 00-1.45-.385c-.345.23-.614.558-.822.88-.214.33-.403.713-.57 1.116-.334.804-.614 1.768-.84 2.734a31.365 31.365 0 00-.613 3.58 2.64 2.64 0 01-.945-1.067c-.328-.68-.398-1.534-.398-2.654A1 1 0 005.05 6.05 6.981 6.981 0 003 11a7 7 0 1011.95-4.95c-.592-.591-.98-.985-1.348-1.467-.363-.476-.724-1.063-1.207-2.03zM12.12 15.12A3 3 0 017 13s.879.5 2.5.5c0-1 .5-4 1.25-4.5.5 1 .786 1.293 1.371 1.879A2.99 2.99 0 0113 13a2.99 2.99 0 01-.879 2.121z"/>
            </svg>
            {session_stats.current_streak}
          </span>
          <span>{session_stats.correct_today}/{session_stats.questions_answered_today}</span>
          <DifficultyBadge level={question.difficulty} />
        </div>
      </motion.div>

      {/* Concept tag + attempt indicator */}
      <motion.div
        initial={{ opacity: 0, y: -5 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-3 flex items-center gap-2 flex-wrap"
      >
        <span className="text-xs font-medium text-primary-600 bg-primary-50 px-2.5 py-1 rounded-full">
          {question.concept_name}
        </span>
        {question.attempt_number > 0 && (
          <span className="text-[10px] font-medium text-amber-600 bg-amber-50 px-2 py-0.5 rounded-full">
            Attempt #{question.attempt_number + 1}
          </span>
        )}
        <button
          onClick={handleShowNotes}
          className="ml-auto text-[10px] font-medium text-gray-400 hover:text-primary-600 transition-colors flex items-center gap-1"
        >
          <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          {loadingNotes ? 'Loading...' : showNotes ? 'Hide Notes' : 'Show Notes'}
        </button>
      </motion.div>

      {/* Concept Notes Panel */}
      <AnimatePresence>
        {showNotes && notes && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="mb-4 overflow-hidden"
          >
            <div className="bg-blue-50 border border-blue-100 rounded-xl p-4">
              <h4 className="text-sm font-semibold text-blue-900 mb-2">{notes.name}</h4>
              {notes.explanation && (
                <div className="text-xs text-blue-800 leading-relaxed mb-3"><RichText content={notes.explanation} /></div>
              )}
              {notes.key_points.length > 0 && (
                <div className="space-y-1">
                  <p className="text-[10px] font-semibold text-blue-600 uppercase tracking-wider">Key Points</p>
                  {notes.key_points.map((point, i) => (
                    <div key={i} className="text-xs text-blue-700 flex items-start gap-1.5">
                      <span className="text-blue-400 mt-0.5 flex-shrink-0">•</span>
                      <RichText content={point} />
                    </div>
                  ))}
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Question */}
      <motion.div
        key={question.id}
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-6"
      >
        <h2 className="text-lg font-semibold text-gray-900 leading-relaxed">
          <RichText content={question.question_text} />
        </h2>
      </motion.div>

      {/* Options */}
      <div className="space-y-3 mb-6">
        {question.options?.map((option, idx) => (
          <OptionButton
            key={`${question.id}-${idx}`}
            label={option}
            index={idx}
            isSelected={selectedOption === option}
            isCorrect={showFeedback && result?.correct_answer === option}
            isWrong={showFeedback && selectedOption === option && !result?.is_correct}
            showResult={showFeedback}
            disabled={isSubmitting || showFeedback || (selectedOption !== null && selectedOption !== option)}
            onSelect={() => handleSelect(option)}
          />
        ))}
      </div>

      {/* Loading indicator during auto-submit */}
      <AnimatePresence>
        {isSubmitting && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="flex justify-center py-2"
          >
            <div className="w-5 h-5 border-2 border-primary-300 border-t-primary-600 rounded-full animate-spin" />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Feedback */}
      <AnimatePresence>
        {showFeedback && result && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-4"
          >
            <FeedbackOverlay result={result} onContinue={handleContinue} />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
