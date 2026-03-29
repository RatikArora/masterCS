import { motion } from 'framer-motion';
import { Check, X } from 'lucide-react';
import RichText from '../ui/RichText';

interface OptionButtonProps {
  label: string;
  index: number;
  isSelected: boolean;
  isCorrect?: boolean;
  isWrong?: boolean;
  showResult: boolean;
  disabled: boolean;
  onSelect: () => void;
}

const letters = ['A', 'B', 'C', 'D', 'E', 'F'];

export default function OptionButton({
  label, index, isSelected, isCorrect, isWrong, showResult, disabled, onSelect,
}: OptionButtonProps) {
  let borderColor = 'border-slate-200 hover:border-indigo-300';
  let bg = 'bg-white hover:bg-indigo-50/30';
  let letterBg = 'bg-slate-100 text-slate-500';

  if (showResult) {
    if (isCorrect) {
      borderColor = 'border-emerald-300';
      bg = 'bg-emerald-50';
      letterBg = 'bg-emerald-500 text-white';
    } else if (isWrong) {
      borderColor = 'border-rose-300';
      bg = 'bg-rose-50';
      letterBg = 'bg-rose-500 text-white';
    } else {
      borderColor = 'border-slate-100';
      bg = 'bg-slate-50/50';
      letterBg = 'bg-slate-100 text-slate-400';
    }
  } else if (isSelected) {
    borderColor = 'border-indigo-400';
    bg = 'bg-indigo-50';
    letterBg = 'bg-indigo-500 text-white';
  }

  return (
    <motion.button
      whileTap={disabled ? undefined : { scale: 0.98 }}
      initial={{ opacity: 0, x: -8 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: index * 0.04, duration: 0.15 }}
      onClick={onSelect}
      disabled={disabled}
      className={`w-full flex items-center gap-3.5 px-4 py-3.5 rounded-2xl border transition-all duration-200 text-left min-h-[3.5rem] ${borderColor} ${bg} ${disabled && !showResult ? 'opacity-40' : ''}`}
    >
      <span className={`flex-shrink-0 w-8 h-8 flex items-center justify-center rounded-xl text-xs font-semibold transition-all duration-200 ${letterBg}`}>
        {letters[index]}
      </span>
      <span className="text-sm text-slate-700 leading-snug flex-1">
        <RichText content={label} />
      </span>
      {showResult && isCorrect && (
        <div className="w-6 h-6 rounded-full bg-emerald-500 flex items-center justify-center flex-shrink-0">
          <Check size={14} strokeWidth={2.5} className="text-white" />
        </div>
      )}
      {showResult && isWrong && (
        <div className="w-6 h-6 rounded-full bg-rose-500 flex items-center justify-center flex-shrink-0">
          <X size={14} strokeWidth={2.5} className="text-white" />
        </div>
      )}
    </motion.button>
  );
}
