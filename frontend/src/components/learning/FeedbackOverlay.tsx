import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import type { AnswerResult } from '../../api/learning';
import Button from '../ui/Button';
import RichText from '../ui/RichText';
import { sounds } from '../../utils/sounds';

interface FeedbackOverlayProps {
  result: AnswerResult;
  onContinue: () => void;
  hotStreak?: number;
}

const HOT_STREAK_MESSAGES = [
  '', '', '',
  'Hat trick!',
  'On fire!',
  'Unstoppable!',
  'Dominating!',
  'Legendary!',
  'GODLIKE!',
  'Beyond Mortal!',
  'PERFECTION!',
];

function getStreakMessage(count: number): string {
  if (count < 3) return '';
  return HOT_STREAK_MESSAGES[Math.min(count, HOT_STREAK_MESSAGES.length - 1)];
}

export default function FeedbackOverlay({ result, onContinue, hotStreak = 0 }: FeedbackOverlayProps) {
  const [showLesson, setShowLesson] = useState(false);
  const streakMsg = getStreakMessage(hotStreak);

  useEffect(() => {
    if (result.is_correct) {
      if (hotStreak >= 5) {
        sounds.complete();
      } else if (hotStreak >= 3) {
        sounds.streak();
      } else {
        sounds.correct();
      }
      if (result.level_up) {
        setTimeout(() => sounds.levelUp(), 400);
      }
    } else {
      sounds.wrong();
    }
  }, [result, hotStreak]);

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
          <div className="flex-1">
            <p className={`font-semibold ${result.is_correct ? 'text-green-800' : 'text-red-800'}`}>
              {result.is_correct ? 'Correct!' : 'Not quite right'}
            </p>
            <p className="text-xs text-gray-600">
              +{result.xp_earned} XP · {result.next_review_message}
            </p>
          </div>
          {result.streak_count >= 3 && result.is_correct && (
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              className="flex items-center gap-1 bg-orange-100 text-orange-700 px-2 py-1 rounded-full text-xs font-bold"
            >
              <svg className="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
                <path d="M12.395 2.553a1 1 0 00-1.45-.385c-.345.23-.614.558-.822.88-.214.33-.403.713-.57 1.116-.334.804-.614 1.768-.84 2.734a31.365 31.365 0 00-.613 3.58 2.64 2.64 0 01-.945-1.067c-.328-.68-.398-1.534-.398-2.654A1 1 0 005.05 6.05 6.981 6.981 0 003 11a7 7 0 1011.95-4.95c-.592-.591-.98-.985-1.348-1.467-.363-.476-.724-1.063-1.207-2.03zM12.12 15.12A3 3 0 017 13s.879.5 2.5.5c0-1 .5-4 1.25-4.5.5 1 .786 1.293 1.371 1.879A2.99 2.99 0 0113 13a2.99 2.99 0 01-.879 2.121z"/>
              </svg>
              {result.streak_count}x
            </motion.div>
          )}
        </div>

        {/* Level up celebration */}
        {result.level_up && (
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 0.3, type: 'spring' }}
            className="mb-3 p-3 bg-gradient-to-r from-purple-100 to-indigo-100 rounded-xl border border-purple-200 text-center"
          >
            <p className="text-lg font-bold text-purple-700">Level Up!</p>
            <p className="text-xs text-purple-500">Keep going — you're getting stronger!</p>
          </motion.div>
        )}

        {/* Hot streak celebration (3+ correct in a row) */}
        {hotStreak >= 3 && result.is_correct && streakMsg && (
          <motion.div
            initial={{ scale: 0.5, opacity: 0, rotate: -5 }}
            animate={{ scale: 1, opacity: 1, rotate: 0 }}
            transition={{ type: 'spring', stiffness: 300, damping: 15 }}
            className={`mb-3 p-3 rounded-xl border text-center ${
              hotStreak >= 7
                ? 'bg-gradient-to-r from-amber-100 via-orange-100 to-red-100 border-orange-300'
                : hotStreak >= 5
                  ? 'bg-gradient-to-r from-orange-50 to-amber-50 border-amber-200'
                  : 'bg-gradient-to-r from-blue-50 to-cyan-50 border-blue-200'
            }`}
          >
            <p className={`text-lg font-black ${
              hotStreak >= 7 ? 'text-orange-600' : hotStreak >= 5 ? 'text-amber-600' : 'text-blue-600'
            }`}>
              {streakMsg}
            </p>
            <p className="text-xs text-gray-500 mt-0.5">{hotStreak} correct in a row</p>
          </motion.div>
        )}

        {/* Correct answer (if wrong) */}
        {!result.is_correct && (
          <div className="mb-3 px-3 py-2 bg-white/70 rounded-lg border border-red-100">
            <p className="text-xs text-gray-500 mb-0.5">Correct answer:</p>
            <p className="text-sm font-medium text-gray-800">{result.correct_answer}</p>
          </div>
        )}

        {/* Explanation */}
        {result.explanation && (
          <div className="mb-3 px-3 py-2 bg-white/70 rounded-lg">
            <p className="text-xs text-gray-500 mb-0.5">Why?</p>
            <RichText content={result.explanation} className="text-sm text-gray-700 leading-relaxed" />
          </div>
        )}

        {/* Lesson card (for wrong answers) */}
        {result.lesson_card && !showLesson && (
          <button
            onClick={() => setShowLesson(true)}
            className="w-full mb-3 px-3 py-2.5 bg-blue-50 border border-blue-100 rounded-xl text-left hover:bg-blue-100 transition-colors"
          >
            <div className="flex items-center gap-2">
              <svg className="w-4 h-4 text-blue-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
              <span className="text-sm font-medium text-blue-700">{result.lesson_card.title}</span>
              <svg className="w-3 h-3 text-blue-400 ml-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </div>
          </button>
        )}

        <AnimatePresence>
          {showLesson && result.lesson_card && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="mb-3 overflow-hidden"
            >
              <div className="px-4 py-3 bg-blue-50 border border-blue-100 rounded-xl">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="text-sm font-semibold text-blue-800">{result.lesson_card.title}</h4>
                  <button onClick={() => setShowLesson(false)} className="text-blue-400 hover:text-blue-600">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7" />
                    </svg>
                  </button>
                </div>
                <RichText content={result.lesson_card.content} className="text-xs text-blue-700 leading-relaxed mb-2" />
                {result.lesson_card.key_points.length > 0 && (
                  <div className="space-y-1 mt-2 pt-2 border-t border-blue-200/50">
                    {result.lesson_card.key_points.map((pt, i) => (
                      <p key={i} className="text-xs text-blue-600 flex gap-1.5">
                        <span className="text-blue-400 flex-shrink-0">•</span>
                        <RichText content={pt} />
                      </p>
                    ))}
                  </div>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        <Button onClick={onContinue} size="lg" className="w-full">
          Continue
        </Button>
      </motion.div>
    </AnimatePresence>
  );
}
