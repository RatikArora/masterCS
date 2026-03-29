import { motion } from 'framer-motion';
import { Zap, Check, Trophy } from 'lucide-react';

interface XPBarProps {
  current: number;
  goal: number;
  questionsToday?: number;
}

export default function XPBar({ current, goal, questionsToday }: XPBarProps) {
  const percent = Math.min((current / Math.max(goal, 1)) * 100, 100);
  const isComplete = current >= goal;
  const isDouble = current >= goal * 2;

  // Milestone markers
  const milestones = [
    { at: Math.round(goal * 0.33), label: '' },
    { at: Math.round(goal * 0.66), label: '' },
    { at: goal, label: `${goal}` },
  ];

  return (
    <div className="bg-white border border-slate-200/60 rounded-2xl px-4 py-3">
      <div className="flex items-center justify-between mb-2.5">
        <div className="flex items-center gap-2">
          <div className={`w-7 h-7 rounded-lg flex items-center justify-center ${
            isComplete ? 'bg-emerald-100' : 'bg-amber-50'
          }`}>
            {isComplete ? (
              <Trophy size={14} strokeWidth={1.5} className="text-emerald-600" />
            ) : (
              <Zap size={14} strokeWidth={1.5} className="text-amber-500" />
            )}
          </div>
          <div>
            <p className="text-xs font-semibold text-slate-800">
              {isComplete ? 'Daily Goal Reached!' : 'Daily Goal'}
            </p>
            <p className="text-[10px] text-slate-400">
              {questionsToday ? `${questionsToday} questions today` : 'Answer questions to earn XP'}
            </p>
          </div>
        </div>
        <div className="text-right">
          <p className={`text-sm font-bold tabular-nums ${isComplete ? 'text-emerald-600' : 'text-indigo-600'}`}>
            {current.toLocaleString()}
          </p>
          <p className="text-[9px] text-slate-400">/ {goal} XP</p>
        </div>
      </div>

      {/* Progress bar with milestones */}
      <div className="relative">
        <div className="h-2.5 bg-slate-100 rounded-full overflow-hidden">
          <motion.div
            className={`h-full rounded-full ${
              isDouble
                ? 'bg-gradient-to-r from-emerald-400 to-emerald-500'
                : isComplete
                  ? 'bg-gradient-to-r from-emerald-400 to-emerald-500'
                  : percent > 60
                    ? 'bg-gradient-to-r from-indigo-400 to-indigo-500'
                    : 'bg-indigo-400'
            }`}
            initial={{ width: 0 }}
            animate={{ width: `${percent}%` }}
            transition={{ duration: 0.8, ease: 'easeOut' }}
          />
        </div>

        {/* Milestone dots */}
        <div className="absolute top-0 left-0 right-0 h-2.5 pointer-events-none">
          {milestones.map((m) => {
            const pos = Math.min((m.at / Math.max(goal, 1)) * 100, 100);
            const reached = current >= m.at;
            return (
              <div
                key={m.at}
                className="absolute top-1/2 -translate-y-1/2"
                style={{ left: `${pos}%` }}
              >
                <div className={`w-2 h-2 rounded-full border-2 -ml-1 ${
                  reached
                    ? 'bg-white border-emerald-500'
                    : 'bg-white border-slate-300'
                }`} />
              </div>
            );
          })}
        </div>
      </div>

      {/* Completion badge */}
      {isComplete && (
        <motion.div
          initial={{ opacity: 0, y: 4 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="flex items-center gap-1.5 mt-2"
        >
          <Check size={12} strokeWidth={2} className="text-emerald-500" />
          <span className="text-[10px] text-emerald-600 font-medium">
            {isDouble ? 'Amazing! 2× daily goal!' : 'Goal complete — keep the momentum!'}
          </span>
        </motion.div>
      )}
    </div>
  );
}
