import { useEffect, useState, useCallback } from 'react';
import { useSearchParams } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { Zap, Info, Flag, CheckCircle, AlertTriangle, BookOpen, ChevronRight, X as XIcon } from 'lucide-react';
import { useLearningStore } from '../store/learningStore';
import { learningApi, type ConceptNotes } from '../api/learning';
import OptionButton from '../components/learning/OptionButton';
import FeedbackOverlay from '../components/learning/FeedbackOverlay';
import DifficultyBadge from '../components/learning/DifficultyBadge';
import MasteryBadge from '../components/progress/MasteryBadge';
import Loading from '../components/ui/Loading';
import Button from '../components/ui/Button';
import RichText from '../components/ui/RichText';
import { sounds } from '../utils/sounds';

const REPORT_REASONS = ['Wrong Answer', 'Unclear Question', 'Duplicate', 'Outdated', 'Other'];

export default function LearnPage() {
  const [searchParams] = useSearchParams();
  const subjectId = searchParams.get('subject') || '';
  const conceptId = searchParams.get('concept') || undefined;
  const topicId = searchParams.get('topic') || undefined;
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [showNotes, setShowNotes] = useState(false);
  const [notes, setNotes] = useState<ConceptNotes | null>(null);
  const [loadingNotes, setLoadingNotes] = useState(false);
  const [showReportMenu, setShowReportMenu] = useState(false);
  const [reportReason, setReportReason] = useState<string | null>(null);
  const [reportDetails, setReportDetails] = useState('');
  const [reportSubmitting, setReportSubmitting] = useState(false);
  const [reportDone, setReportDone] = useState(false);

  const {
    session, result, isLoadingQuestion, isSubmitting, showFeedback, error, hotStreak,
    fetchNextQuestion, submitAnswer, dismissFeedback,
  } = useLearningStore();

  useEffect(() => {
    if (subjectId) fetchNextQuestion(subjectId, conceptId, topicId);
  }, [subjectId, conceptId, topicId]);

  const handleSelect = useCallback((option: string) => {
    if (showFeedback || isSubmitting || selectedOption) return;
    sounds.select();
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
    setShowReportMenu(false);
    setReportReason(null);
    setReportDetails('');
    setReportDone(false);
    dismissFeedback();
    if (subjectId) fetchNextQuestion(subjectId, conceptId, topicId);
  }, [subjectId, conceptId, topicId, dismissFeedback, fetchNextQuestion]);

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

  const handleReport = useCallback(async () => {
    if (!session || !reportReason) return;
    setReportSubmitting(true);
    try {
      await learningApi.reportQuestion({
        question_id: session.question.id,
        reason: reportReason,
        details: reportDetails || undefined,
      });
      setReportDone(true);
      setTimeout(() => {
        setShowReportMenu(false);
        setReportReason(null);
        setReportDetails('');
      }, 1500);
    } catch {
      // silently fail
    } finally {
      setReportSubmitting(false);
    }
  }, [session, reportReason, reportDetails]);

  if (!subjectId) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <p className="text-slate-400 text-sm">No subject selected. Go back to dashboard.</p>
      </div>
    );
  }

  if (isLoadingQuestion) return <Loading text="Finding the perfect question..." />;

  if (error) {
    const isComplete = error.includes('covered everything') || error.includes('No more questions');
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] gap-5 px-6">
        <div className={`w-14 h-14 rounded-2xl flex items-center justify-center ${isComplete ? 'bg-emerald-50' : 'bg-slate-100'}`}>
          {isComplete ? (
            <CheckCircle size={28} strokeWidth={1.5} className="text-emerald-500" />
          ) : (
            <AlertTriangle size={28} strokeWidth={1.5} className="text-slate-400" />
          )}
        </div>
        <div className="text-center">
          <h2 className="text-lg font-semibold text-slate-900 mb-1">
            {isComplete ? 'All Done!' : 'Something went wrong'}
          </h2>
          <p className="text-slate-500 text-sm max-w-xs">
            {isComplete
              ? "You've covered all available questions. Check back later for new content or try a different topic."
              : error}
          </p>
        </div>
        <div className="flex gap-3 mt-1">
          <Button onClick={() => window.location.href = `/topics?subject=${subjectId}`} variant="secondary" size="sm">
            Browse Topics
          </Button>
          <Button onClick={() => window.location.href = `/progress?subject=${subjectId}`} size="sm">
            View Progress
          </Button>
        </div>
      </div>
    );
  }

  if (!session) return null;

  const { question, session_stats, concept_progress } = session;

  return (
    <div className="bg-slate-50 min-h-screen">
      <div className="max-w-lg mx-auto px-4 pt-5 pb-28 md:pb-8">
        {/* Focus mode banner */}
        {(conceptId || topicId) && (
          <motion.div
            initial={{ opacity: 0, y: -4 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.15 }}
            className="mb-4 flex items-center gap-2 px-3 py-2 bg-indigo-50/80 border border-indigo-100 rounded-xl"
          >
            <Zap size={14} strokeWidth={1.5} className="text-indigo-500 flex-shrink-0" />
            <span className="text-xs font-medium text-indigo-600 flex-1 truncate">
              {conceptId ? `Concept: ${question.concept_name}` : `Topic: ${question.topic_name}`}
            </span>
            <button
              onClick={() => window.location.href = `/learn?subject=${subjectId}`}
              className="text-[10px] text-indigo-500 hover:text-indigo-700 font-medium transition-colors"
            >
              Exit
            </button>
          </motion.div>
        )}

        {/* Stats bar */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.15 }}
          className="flex items-center justify-between mb-6"
        >
          <div className="flex items-center gap-2">
            <MasteryBadge level={concept_progress.mastery_level} size="xs" />
            <span className="text-xs text-slate-400 truncate max-w-[120px]">{question.topic_name}</span>
          </div>
          <div className="flex items-center gap-3 text-xs text-slate-400">
            {session_stats.current_streak > 0 && (
              <span className="flex items-center gap-1 text-orange-500 font-medium">
                <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M12.395 2.553a1 1 0 00-1.45-.385c-.345.23-.614.558-.822.88-.214.33-.403.713-.57 1.116-.334.804-.614 1.768-.84 2.734a31.365 31.365 0 00-.613 3.58 2.64 2.64 0 01-.945-1.067c-.328-.68-.398-1.534-.398-2.654A1 1 0 005.05 6.05 6.981 6.981 0 003 11a7 7 0 1011.95-4.95c-.592-.591-.98-.985-1.348-1.467-.363-.476-.724-1.063-1.207-2.03zM12.12 15.12A3 3 0 017 13s.879.5 2.5.5c0-1 .5-4 1.25-4.5.5 1 .786 1.293 1.371 1.879A2.99 2.99 0 0113 13a2.99 2.99 0 01-.879 2.121z"/>
                </svg>
                {session_stats.current_streak}
              </span>
            )}
            <span className="tabular-nums font-medium">{session_stats.correct_today}/{session_stats.questions_answered_today}</span>
            <DifficultyBadge level={question.difficulty} />
          </div>
        </motion.div>

        {/* Concept + Actions row */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.15, delay: 0.05 }}
          className="mb-4 flex items-center gap-2 flex-wrap"
        >
          <span className="text-xs font-medium text-indigo-600 bg-indigo-50 px-2.5 py-1 rounded-lg border border-indigo-100">
            {question.concept_name}
          </span>
          {question.attempt_number > 0 && (
            <span className="text-[10px] font-medium text-amber-600 bg-amber-50 px-2 py-0.5 rounded-lg border border-amber-100">
              Attempt #{question.attempt_number + 1}
            </span>
          )}
          {session.selection_reason && (
            <span className="text-[10px] text-slate-400 italic truncate max-w-[200px]" title={session.selection_reason}>
              {session.selection_reason}
            </span>
          )}
          <div className="ml-auto flex items-center gap-1.5">
            <button
              onClick={handleShowNotes}
              className="flex items-center gap-1 text-xs font-medium text-slate-400 hover:text-indigo-600 transition-colors duration-200 px-2 py-1 rounded-lg hover:bg-indigo-50"
            >
              <Info size={14} strokeWidth={1.5} />
              {loadingNotes ? '...' : showNotes ? 'Hide' : 'Notes'}
            </button>
            <div className="relative">
              <button
                onClick={() => { setShowReportMenu(!showReportMenu); setReportDone(false); }}
                className="text-slate-300 hover:text-rose-500 transition-colors duration-200 p-1 rounded-lg hover:bg-rose-50"
                title="Report question"
              >
                <Flag size={14} strokeWidth={1.5} />
              </button>
              <AnimatePresence>
                {showReportMenu && (
                  <motion.div
                    initial={{ opacity: 0, scale: 0.95, y: -4 }}
                    animate={{ opacity: 1, scale: 1, y: 0 }}
                    exit={{ opacity: 0, scale: 0.95, y: -4 }}
                    transition={{ duration: 0.12 }}
                    className="absolute right-0 top-full mt-1 w-56 bg-white rounded-xl border border-slate-200/60 shadow-lg z-20 overflow-hidden"
                  >
                    {reportDone ? (
                      <div className="p-4 text-center">
                        <CheckCircle size={18} strokeWidth={1.5} className="text-emerald-500 mx-auto mb-1.5" />
                        <p className="text-xs font-medium text-slate-600">Report submitted</p>
                      </div>
                    ) : (
                      <div className="p-2">
                        <p className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider px-2 mb-1.5">Report Issue</p>
                        {REPORT_REASONS.map((reason) => (
                          <button
                            key={reason}
                            onClick={() => setReportReason(reportReason === reason ? null : reason)}
                            className={`w-full text-left text-xs px-2.5 py-1.5 rounded-lg transition-colors duration-200 ${
                              reportReason === reason ? 'bg-indigo-50 text-indigo-600 font-medium' : 'text-slate-600 hover:bg-slate-50'
                            }`}
                          >
                            {reason}
                          </button>
                        ))}
                        {reportReason && (
                          <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} className="overflow-hidden">
                            <textarea
                              value={reportDetails}
                              onChange={(e) => setReportDetails(e.target.value)}
                              placeholder="Details (optional)"
                              rows={2}
                              className="w-full mt-1.5 px-2.5 py-1.5 text-xs border border-slate-200 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-400 text-slate-600 placeholder:text-slate-300"
                            />
                            <button
                              onClick={handleReport}
                              disabled={reportSubmitting}
                              className="w-full mt-1.5 py-1.5 text-xs font-medium bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors duration-200 disabled:opacity-40"
                            >
                              {reportSubmitting ? 'Submitting...' : 'Submit Report'}
                            </button>
                          </motion.div>
                        )}
                      </div>
                    )}
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </div>
        </motion.div>

        {/* Concept Notes Panel */}
        <AnimatePresence>
          {showNotes && notes && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.2 }}
              className="mb-5 overflow-hidden"
            >
              <div className="bg-indigo-50/80 border border-indigo-100 rounded-2xl p-4">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <BookOpen size={14} strokeWidth={1.5} className="text-indigo-500" />
                    <h4 className="text-sm font-semibold text-slate-800">{notes.name}</h4>
                  </div>
                  <button onClick={() => setShowNotes(false)} className="text-slate-400 hover:text-slate-600 transition-colors">
                    <XIcon size={14} strokeWidth={1.5} />
                  </button>
                </div>
                {notes.explanation && (
                  <div className="text-xs text-slate-600 leading-relaxed mb-3"><RichText content={notes.explanation} /></div>
                )}
                {notes.key_points.length > 0 && (
                  <div className="space-y-1">
                    <p className="text-[10px] font-semibold text-indigo-500 uppercase tracking-wider">Key Points</p>
                    {notes.key_points.map((point, i) => (
                      <div key={i} className="text-xs text-slate-600 flex items-start gap-1.5">
                        <span className="text-indigo-400 mt-0.5 flex-shrink-0">•</span>
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
          initial={{ opacity: 0, y: 6 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.2 }}
          className="mb-6"
        >
          <div className="text-base font-semibold text-slate-900 leading-relaxed">
            <RichText content={question.question_text} />
          </div>
        </motion.div>

        {/* Options */}
        <div className="space-y-2.5 mb-6">
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
              className="flex justify-center py-3"
            >
              <div className="w-5 h-5 border-2 border-indigo-200 border-t-indigo-600 rounded-full animate-spin" />
            </motion.div>
          )}
        </AnimatePresence>

        {/* Feedback */}
        <AnimatePresence>
          {showFeedback && result && (
            <motion.div
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.2 }}
            >
              <FeedbackOverlay result={result} onContinue={handleContinue} hotStreak={hotStreak} />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
