import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Flame, BookOpen, ChevronDown, ChevronUp, ArrowRight, RefreshCw, Timer } from 'lucide-react';
import type { AnswerResult } from '../../api/learning';
import Button from '../ui/Button';
import MascotGuide from '../ui/MascotGuide';
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

function formatCooldown(seconds: number): string {
  if (seconds < 60) return `${seconds}s`;
  const mins = Math.ceil(seconds / 60);
  if (mins < 60) return `${mins} min`;
  const hrs = Math.floor(mins / 60);
  const remMins = mins % 60;
  return remMins > 0 ? `${hrs}h ${remMins}m` : `${hrs}h`;
}

export default function FeedbackOverlay({ result, onContinue, hotStreak = 0 }: FeedbackOverlayProps) {
  const [showLesson, setShowLesson] = useState(false);
  const [cooldownRemaining, setCooldownRemaining] = useState(result.cooldown_seconds || 0);
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

  // Live cooldown timer
  useEffect(() => {
    if (!result.cooldown_seconds || result.cooldown_seconds <= 0) return;
    setCooldownRemaining(result.cooldown_seconds);
    const interval = setInterval(() => {
      setCooldownRemaining(prev => {
        if (prev <= 1) { clearInterval(interval); return 0; }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(interval);
  }, [result.cooldown_seconds]);

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: 20 }}
        transition={{ duration: 0.2, ease: 'easeOut' }}
        className={`rounded-2xl border overflow-hidden ${
          result.is_correct
            ? 'bg-emerald-50/80 border-emerald-200/60'
            : 'bg-rose-50/80 border-rose-200/60'
        }`}
      >
        {/* Header */}
        <div className="px-5 pt-5 pb-4">
          <div className="flex items-center gap-3">
            <MascotGuide
              context={result.is_correct ? 'feedback-correct' : 'feedback-wrong'}
              size={36}
              stats={{ hotStreak: hotStreak }}
              showBubble={false}
            />
            <div className="flex-1 min-w-0">
              <p className={`text-sm font-semibold ${result.is_correct ? 'text-emerald-800' : 'text-rose-800'}`}>
                {result.is_correct ? 'Correct!' : 'Not quite right'}
              </p>
              <p className="text-xs text-slate-500 mt-0.5">
                {result.xp_earned > 0 ? `+${result.xp_earned} XP · ` : ''}{result.next_review_message}
              </p>
            </div>
            {result.streak_count >= 3 && result.is_correct && (
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                className="flex items-center gap-1 bg-orange-100 text-orange-600 px-2 py-1 rounded-lg text-xs font-bold"
              >
                <Flame size={12} strokeWidth={2} />
                {result.streak_count}x
              </motion.div>
            )}
          </div>
        </div>

        {/* Content area */}
        <div className="px-5 pb-5 space-y-3">
          {/* Level up */}
          {result.level_up && (
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.3, type: 'spring' }}
              className="p-3 bg-gradient-to-r from-violet-100 to-indigo-100 rounded-xl text-center"
            >
              <p className="text-sm font-bold text-violet-700">Level Up!</p>
              <p className="text-xs text-violet-500 mt-0.5">Keep going — you're getting stronger</p>
            </motion.div>
          )}

          {/* Hot streak */}
          {hotStreak >= 3 && result.is_correct && streakMsg && (
            <motion.div
              initial={{ scale: 0.5, opacity: 0, rotate: -3 }}
              animate={{ scale: 1, opacity: 1, rotate: 0 }}
              transition={{ type: 'spring', stiffness: 300, damping: 15 }}
              className={`p-3 rounded-xl text-center ${
                hotStreak >= 7
                  ? 'bg-gradient-to-r from-amber-50 to-orange-50 border border-orange-200/60'
                  : hotStreak >= 5
                    ? 'bg-gradient-to-r from-orange-50 to-amber-50 border border-amber-200/60'
                    : 'bg-gradient-to-r from-indigo-50 to-cyan-50 border border-indigo-200/60'
              }`}
            >
              <p className={`text-sm font-bold ${
                hotStreak >= 7 ? 'text-orange-600' : hotStreak >= 5 ? 'text-amber-600' : 'text-indigo-600'
              }`}>
                {streakMsg}
              </p>
              <p className="text-xs text-slate-500 mt-0.5">{hotStreak} correct in a row</p>
            </motion.div>
          )}

          {/* Correct answer (if wrong) */}
          {!result.is_correct && (
            <div className="px-3 py-2.5 bg-white/60 rounded-xl border border-rose-100/60">
              <p className="text-[10px] font-medium text-slate-400 uppercase tracking-wider mb-1">Correct answer</p>
              <p className="text-sm font-medium text-slate-800">
                <span className="text-indigo-600 font-bold mr-1.5">{result.correct_answer}.</span>
                {result.correct_answer_text || result.correct_answer}
              </p>
            </div>
          )}

          {/* Cooldown timer for wrong answers */}
          {!result.is_correct && cooldownRemaining > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 4 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="flex items-center gap-2.5 px-3 py-2.5 bg-slate-50/80 rounded-xl border border-slate-200/40"
            >
              <div className="w-7 h-7 rounded-lg bg-indigo-100 flex items-center justify-center flex-shrink-0">
                <Timer size={14} strokeWidth={1.5} className="text-indigo-500" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-xs font-medium text-slate-700">Respawning in {formatCooldown(cooldownRemaining)}</p>
                <p className="text-[10px] text-slate-400 mt-0.5">Practice other questions while you wait</p>
              </div>
              <RefreshCw size={12} strokeWidth={1.5} className="text-slate-300 animate-spin" style={{ animationDuration: '3s' }} />
            </motion.div>
          )}
          {!result.is_correct && cooldownRemaining === 0 && !result.cooldown_seconds && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.4 }}
              className="flex items-center gap-2 px-3 py-2 bg-white/50 rounded-xl"
            >
              <RefreshCw size={14} strokeWidth={1.5} className="text-slate-400" />
              <p className="text-xs text-slate-500">This question will return for practice soon</p>
            </motion.div>
          )}

          {/* Explanation */}
          {result.explanation && (
            <div className="px-3 py-2.5 bg-white/60 rounded-xl">
              <p className="text-[10px] font-medium text-slate-400 uppercase tracking-wider mb-1">Explanation</p>
              <RichText content={result.explanation} className="text-sm text-slate-600 leading-relaxed" />
            </div>
          )}

          {/* Lesson card toggle */}
          {result.lesson_card && !showLesson && (
            <button
              onClick={() => setShowLesson(true)}
              className="w-full px-3 py-2.5 bg-white/60 border border-indigo-100/60 rounded-xl text-left hover:bg-indigo-50/50 transition-all duration-200"
            >
              <div className="flex items-center gap-2.5">
                <BookOpen size={16} strokeWidth={1.5} className="text-indigo-500 flex-shrink-0" />
                <span className="text-sm font-medium text-indigo-700 flex-1">{result.lesson_card.title}</span>
                <ChevronDown size={14} strokeWidth={1.5} className="text-indigo-400" />
              </div>
            </button>
          )}

          <AnimatePresence>
            {showLesson && result.lesson_card && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className="overflow-hidden"
              >
                <div className="px-4 py-3 bg-white/60 border border-indigo-100/60 rounded-xl">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="text-sm font-semibold text-indigo-800">{result.lesson_card.title}</h4>
                    <button onClick={() => setShowLesson(false)} className="text-indigo-400 hover:text-indigo-600 transition-colors">
                      <ChevronUp size={16} strokeWidth={1.5} />
                    </button>
                  </div>
                  <RichText content={result.lesson_card.content} className="text-xs text-slate-600 leading-relaxed mb-2" />
                  {result.lesson_card.key_points.length > 0 && (
                    <div className="space-y-1 mt-2 pt-2 border-t border-indigo-100/60">
                      {result.lesson_card.key_points.map((pt, i) => (
                        <p key={i} className="text-xs text-slate-600 flex gap-1.5">
                          <span className="text-indigo-400 flex-shrink-0">•</span>
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
            <ArrowRight size={16} strokeWidth={1.5} />
          </Button>
        </div>
      </motion.div>
    </AnimatePresence>
  );
}
