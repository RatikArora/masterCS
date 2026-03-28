import { motion } from 'framer-motion';

const diffColors = ['', 'bg-emerald-50 text-emerald-600', 'bg-amber-50 text-amber-600', 'bg-rose-50 text-rose-600'];
const diffLabels = ['', 'Easy', 'Medium', 'Hard'];

export default function DifficultyBadge({ level }: { level: number }) {
  const idx = Math.min(Math.max(level, 1), 3);
  return (
    <motion.span
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ duration: 0.12 }}
      className={`inline-flex items-center px-2 py-0.5 rounded-lg text-[10px] font-medium ${diffColors[idx]}`}
    >
      {diffLabels[idx]}
    </motion.span>
  );
}
