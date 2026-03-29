import { motion } from 'framer-motion';

type MascotMood = 'idle' | 'happy' | 'thinking' | 'celebrating' | 'sad' | 'waving';

interface MascotProps {
  mood?: MascotMood;
  size?: number;
  message?: string;
  className?: string;
}

const moodColors: Record<MascotMood, { body: string; cheek: string }> = {
  idle: { body: '#6366f1', cheek: '#f9a8d4' },
  happy: { body: '#6366f1', cheek: '#fca5a5' },
  thinking: { body: '#6366f1', cheek: '#fde68a' },
  celebrating: { body: '#8b5cf6', cheek: '#fca5a5' },
  sad: { body: '#6366f1', cheek: '#c4b5fd' },
  waving: { body: '#6366f1', cheek: '#f9a8d4' },
};

export default function Mascot({ mood = 'idle', size = 80, message, className = '' }: MascotProps) {
  const colors = moodColors[mood];
  const s = size;

  // Eye animation based on mood
  const eyeVariants = {
    idle: { scaleY: 1 },
    happy: { scaleY: [1, 0.1, 1], transition: { repeat: Infinity, repeatDelay: 3, duration: 0.3 } },
    thinking: { x: 2 },
    celebrating: { scaleY: [1, 0.1, 1], transition: { repeat: Infinity, repeatDelay: 1.5, duration: 0.2 } },
    sad: { scaleY: 0.7, y: 1 },
    waving: { scaleY: 1 },
  };

  // Body bounce
  const bodyVariants = {
    idle: { y: [0, -2, 0], transition: { repeat: Infinity, duration: 3, ease: 'easeInOut' } },
    happy: { y: [0, -4, 0], transition: { repeat: Infinity, duration: 0.8, ease: 'easeInOut' } },
    thinking: { rotate: [-2, 2, -2], transition: { repeat: Infinity, duration: 2, ease: 'easeInOut' } },
    celebrating: { y: [0, -8, 0], scale: [1, 1.05, 1], transition: { repeat: Infinity, duration: 0.6 } },
    sad: { y: 0, rotate: -3 },
    waving: { y: [0, -2, 0], transition: { repeat: Infinity, duration: 2, ease: 'easeInOut' } },
  };

  return (
    <div className={`flex flex-col items-center gap-2 ${className}`}>
      <motion.svg
        viewBox="0 0 100 110"
        width={s}
        height={s * 1.1}
        variants={bodyVariants}
        animate={mood}
        style={{ overflow: 'visible' }}
      >
        {/* Shadow */}
        <ellipse cx="50" cy="105" rx="22" ry="4" fill="#e2e8f0" opacity="0.6" />

        {/* Body */}
        <ellipse cx="50" cy="60" rx="28" ry="32" fill={colors.body} />
        <ellipse cx="50" cy="62" rx="22" ry="24" fill="#818cf8" />
        {/* Belly */}
        <ellipse cx="50" cy="70" rx="16" ry="14" fill="#e0e7ff" />

        {/* Graduation cap */}
        <g>
          <polygon points="50,18 25,30 50,38 75,30" fill="#1e1b4b" />
          <rect x="46" y="28" width="8" height="4" fill="#1e1b4b" rx="1" />
          <line x1="70" y1="30" x2="74" y2="42" stroke="#1e1b4b" strokeWidth="1.5" />
          <circle cx="74" cy="43" r="2" fill="#fbbf24" />
        </g>

        {/* Face */}
        {/* Eyes */}
        <motion.g variants={eyeVariants} animate={mood}>
          <ellipse cx="40" cy="52" rx="5" ry="5.5" fill="white" />
          <ellipse cx="60" cy="52" rx="5" ry="5.5" fill="white" />
          <circle cx="41" cy="52" r="2.5" fill="#1e1b4b" />
          <circle cx="61" cy="52" r="2.5" fill="#1e1b4b" />
          <circle cx="42" cy="51" r="0.8" fill="white" />
          <circle cx="62" cy="51" r="0.8" fill="white" />
        </motion.g>

        {/* Cheeks */}
        <circle cx="33" cy="58" r="4" fill={colors.cheek} opacity="0.4" />
        <circle cx="67" cy="58" r="4" fill={colors.cheek} opacity="0.4" />

        {/* Mouth */}
        {mood === 'happy' || mood === 'celebrating' ? (
          <path d="M44 62 Q50 68 56 62" fill="none" stroke="#1e1b4b" strokeWidth="1.5" strokeLinecap="round" />
        ) : mood === 'sad' ? (
          <path d="M44 64 Q50 60 56 64" fill="none" stroke="#1e1b4b" strokeWidth="1.5" strokeLinecap="round" />
        ) : mood === 'thinking' ? (
          <circle cx="52" cy="63" r="2" fill="#1e1b4b" />
        ) : (
          <path d="M45 62 Q50 65 55 62" fill="none" stroke="#1e1b4b" strokeWidth="1.2" strokeLinecap="round" />
        )}

        {/* Arms */}
        {mood === 'waving' || mood === 'celebrating' ? (
          <motion.g
            animate={{ rotate: [0, -15, 15, -15, 0] }}
            transition={{ repeat: Infinity, duration: 1, ease: 'easeInOut' }}
            style={{ transformOrigin: '24px 60px' }}
          >
            <path d="M24 60 Q14 48 18 40" fill="none" stroke={colors.body} strokeWidth="5" strokeLinecap="round" />
          </motion.g>
        ) : (
          <path d="M24 60 Q18 68 20 76" fill="none" stroke={colors.body} strokeWidth="5" strokeLinecap="round" />
        )}
        <path d="M76 60 Q82 68 80 76" fill="none" stroke={colors.body} strokeWidth="5" strokeLinecap="round" />

        {/* Feet */}
        <ellipse cx="40" cy="92" rx="8" ry="4" fill="#4f46e5" />
        <ellipse cx="60" cy="92" rx="8" ry="4" fill="#4f46e5" />

        {/* Stars for celebrating */}
        {mood === 'celebrating' && (
          <>
            <motion.text
              x="12" y="36" fontSize="10"
              animate={{ y: [36, 28, 36], opacity: [0.4, 1, 0.4] }}
              transition={{ repeat: Infinity, duration: 1.2 }}
            >&#9733;</motion.text>
            <motion.text
              x="80" y="28" fontSize="8" fill="#fbbf24"
              animate={{ y: [28, 20, 28], opacity: [0.4, 1, 0.4] }}
              transition={{ repeat: Infinity, duration: 1, delay: 0.3 }}
            >&#9733;</motion.text>
          </>
        )}
      </motion.svg>

      {/* Speech bubble */}
      {message && (
        <motion.div
          initial={{ opacity: 0, y: 4 }}
          animate={{ opacity: 1, y: 0 }}
          className="relative bg-white border border-slate-200 rounded-xl px-3 py-1.5 text-xs text-slate-600 font-medium shadow-sm max-w-[180px] text-center"
        >
          <div className="absolute -top-1.5 left-1/2 -translate-x-1/2 w-3 h-3 bg-white border-l border-t border-slate-200 rotate-45" />
          <span className="relative z-10">{message}</span>
        </motion.div>
      )}
    </div>
  );
}
