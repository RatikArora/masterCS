import { motion } from 'framer-motion';
import { Flame, Clock } from 'lucide-react';

export default function StreakCounter({ count, isActive }: { count: number; isActive?: boolean }) {
  return (
    <motion.div
      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-semibold ${
        count > 0 ? 'bg-orange-50 text-orange-600 border border-orange-100' : 'bg-slate-50 text-slate-400 border border-slate-200/60'
      }`}
      animate={isActive ? { scale: [1, 1.05, 1] } : undefined}
      transition={{ duration: 0.2 }}
    >
      {count > 0 ? (
        <Flame size={14} strokeWidth={1.5} className="text-orange-500" />
      ) : (
        <Clock size={14} strokeWidth={1.5} className="text-slate-400" />
      )}
      <span>{count}d</span>
    </motion.div>
  );
}
