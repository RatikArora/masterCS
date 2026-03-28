import { motion, AnimatePresence } from 'framer-motion';
import type { AnswerResult } from '../../api/learning';
import Button from '../ui/Button';
import RichText from '../ui/RichText';

interface FeedbackOverlayProps {
  result: AnswerResult;
  onContinue: () => void;
}

export default function FeedbackOverlay({ result, onContinue }: FeedbackOverlayProps) {
  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: 40 }}
        className={`rounded-2xl p-5 border-2 ${
          result.is_correct
            ? 'bg-green-50 border-green-200'
            : 'bg-red-50 border-red-200'
        }`}
      >
        {/* Header */}
        <div className="flex items-center gap-3 mb-3">
          <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
            result.is_correct ? 'bg-green-200' : 'bg-red-200'
          }`}>
            {result.is_correct ? (
              <svg className="w-5 h-5 text-green-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
              </svg>
            ) : (
              <svg className="w-5 h-5 text-red-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M6 18L18 6M6 6l12 12" />
              </svg>
            )}
          </div>
          <div>
            <p className={`font-semibold ${result.is_correct ? 'text-green-800' : 'text-red-800'}`}>
              {result.is_correct ? 'Correct!' : 'Not quite right'}
            </p>
            <p className="text-xs text-gray-600">
              +{result.xp_earned} XP · {result.next_review_message}
            </p>
          </div>
        </div>

        {/* Correct answer (if wrong) */}
        {!result.is_correct && (
          <div className="mb-3 px-3 py-2 bg-white/70 rounded-lg border border-red-100">
            <p className="text-xs text-gray-500 mb-0.5">Correct answer:</p>
            <p className="text-sm font-medium text-gray-800">{result.correct_answer}</p>
          </div>
        )}

        {/* Explanation */}
        {result.explanation && (
          <div className="mb-4 px-3 py-2 bg-white/70 rounded-lg">
            <p className="text-xs text-gray-500 mb-0.5">Why?</p>
            <RichText content={result.explanation} className="text-sm text-gray-700 leading-relaxed" />
          </div>
        )}

        <Button onClick={onContinue} size="lg" className="w-full">
          Continue
        </Button>
      </motion.div>
    </AnimatePresence>
  );
}
