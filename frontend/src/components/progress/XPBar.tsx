import { motion } from 'framer-motion';

export default function XPBar({ current, goal }: { current: number; goal: number }) {
  const percent = Math.min((current / Math.max(goal, 1)) * 100, 100);
  const isComplete = current >= goal;

  return (
    <div className="flex-1 min-w-[140px]">
      <div className="flex items-center justify-between text-[11px] text-gray-400 mb-1.5">
        <span className="flex items-center gap-1">
          <svg className="w-3 h-3 text-amber-400" fill="currentColor" viewBox="0 0 20 20">
            <path d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z"/>
          </svg>
          <span className="font-medium text-gray-600">{current} XP</span> today
        </span>
        <span className={isComplete ? 'text-green-500 font-medium' : ''}>
          {isComplete ? 'Goal reached!' : `Goal: ${goal}`}
        </span>
      </div>
      <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
        <motion.div
          className={`h-full rounded-full ${
            isComplete
              ? 'bg-gradient-to-r from-green-400 to-emerald-500'
              : 'bg-gradient-to-r from-primary-400 to-primary-500'
          }`}
          initial={{ width: 0 }}
          animate={{ width: `${percent}%` }}
          transition={{ duration: 0.8, ease: 'easeOut' }}
        />
      </div>
    </div>
  );
}
