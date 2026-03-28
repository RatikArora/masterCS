import { motion } from 'framer-motion';

export default function XPBar({ current, goal }: { current: number; goal: number }) {
  const percent = Math.min((current / Math.max(goal, 1)) * 100, 100);
  const isComplete = current >= goal;

  return (
    <div className="flex-1 min-w-0">
      <div className="flex items-center justify-between text-xs mb-1">
        <span className="flex items-center gap-1 text-slate-600">
          <svg className="w-3 h-3 text-indigo-500" fill="currentColor" viewBox="0 0 20 20">
            <path d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z"/>
          </svg>
          <span className="font-medium">{current}</span>
          <span className="text-slate-400">/ {goal}</span>
        </span>
        {isComplete && (
          <span className="text-emerald-500 font-medium text-[10px]">Done!</span>
        )}
      </div>
      <div className="h-1.5 bg-slate-100 rounded-full overflow-hidden">
        <motion.div
          className={`h-full rounded-full ${
            isComplete
              ? 'bg-emerald-500'
              : 'bg-indigo-500'
          }`}
          initial={{ width: 0 }}
          animate={{ width: `${percent}%` }}
          transition={{ duration: 0.6, ease: 'easeOut' }}
        />
      </div>
    </div>
  );
}
