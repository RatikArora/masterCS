import { motion } from 'framer-motion';
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
  let borderColor = 'border-gray-200 hover:border-primary-300';
  let bg = 'bg-white hover:bg-primary-50/50';
  let letterBg = 'bg-gray-100 text-gray-600';

  if (showResult) {
    if (isCorrect) {
      borderColor = 'border-green-400';
      bg = 'bg-green-50';
      letterBg = 'bg-green-500 text-white';
    } else if (isWrong) {
      borderColor = 'border-red-400';
      bg = 'bg-red-50';
      letterBg = 'bg-red-500 text-white';
    } else {
      borderColor = 'border-gray-100';
      bg = 'bg-gray-50/50';
    }
  } else if (isSelected) {
    borderColor = 'border-primary-400';
    bg = 'bg-primary-50';
    letterBg = 'bg-primary-500 text-white';
  }

  return (
    <motion.button
      whileTap={disabled ? undefined : { scale: 0.98 }}
      initial={{ opacity: 0, x: -10 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: index * 0.05 }}
      onClick={onSelect}
      disabled={disabled}
      className={`w-full flex items-center gap-3 px-4 py-3.5 rounded-xl border-2 transition-colors text-left ${borderColor} ${bg} ${disabled && !showResult ? 'opacity-50' : ''}`}
    >
      <span className={`flex-shrink-0 w-8 h-8 flex items-center justify-center rounded-lg text-sm font-semibold transition-colors ${letterBg}`}>
        {letters[index]}
      </span>
      <span className="text-sm text-gray-800 leading-snug flex-1">
        <RichText content={label} />
      </span>
      {showResult && isCorrect && (
        <svg className="w-5 h-5 text-green-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
        </svg>
      )}
      {showResult && isWrong && (
        <svg className="w-5 h-5 text-red-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M6 18L18 6M6 6l12 12" />
        </svg>
      )}
    </motion.button>
  );
}
