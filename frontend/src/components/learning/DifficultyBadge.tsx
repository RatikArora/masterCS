import { motion } from 'framer-motion';

const diffColors = ['', 'bg-green-100 text-green-700', 'bg-amber-100 text-amber-700', 'bg-red-100 text-red-700'];
const diffLabels = ['', 'Easy', 'Medium', 'Hard'];

export default function DifficultyBadge({ level }: { level: number }) {
  const idx = Math.min(Math.max(level, 1), 3);
  return (
    <motion.span
      initial={{ scale: 0.8, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      className={`inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium ${diffColors[idx]}`}
    >
      {diffLabels[idx]}
    </motion.span>
  );
}
