import { motion } from 'framer-motion';
import { Zap } from 'lucide-react';

export default function XPBar({ current, goal }: { current: number; goal: number }) {
  const percent = Math.min((current / Math.max(goal, 1)) * 100, 100);
  const isComplete = current >= goal;

  return (
    <div className="flex-1 min-w-0">
      <div className="flex items-center justify-between text-xs mb-1.5">
        <span className="flex items-center gap-1.5 text-slate-600">
          <Zap size={12} strokeWidth={1.5} className="text-indigo-500" />
          <span className="font-medium tabular-nums">{current}</span>
          <span className="text-slate-400">/ {goal}</span>
        </span>
        {isComplete && (
          <span className="text-emerald-500 font-medium text-[10px]">Complete</span>
        )}
      </div>
      <div className="h-1.5 bg-slate-100 rounded-full overflow-hidden">
        <motion.div
          className={`h-full rounded-full ${isComplete ? 'bg-emerald-500' : 'bg-indigo-500'}`}
          initial={{ width: 0 }}
          animate={{ width: `${percent}%` }}
          transition={{ duration: 0.6, ease: 'easeOut' }}
        />
      </div>
    </div>
  );
}
