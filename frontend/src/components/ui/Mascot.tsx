import { motion, useMotionValue, useTransform, type Variants } from 'framer-motion';
import { useEffect, useRef, useState } from 'react';

export type MascotMood =
  | 'idle' | 'happy' | 'thinking' | 'celebrating' | 'sad' | 'waving'
  | 'impressed' | 'encouraging' | 'focused' | 'sleepy';

interface MascotProps {
  mood?: MascotMood;
  size?: number;
  message?: string;
  className?: string;
  showBubble?: boolean;
  level?: number;
  onClick?: () => void;
}

const moodConfig: Record<MascotMood, { primary: string; glow: string; cheek: string }> = {
  idle:         { primary: '#6366f1', glow: '#818cf8', cheek: '#f9a8d4' },
  happy:        { primary: '#6366f1', glow: '#a5b4fc', cheek: '#fca5a5' },
  thinking:     { primary: '#6366f1', glow: '#a5b4fc', cheek: '#fde68a' },
  celebrating:  { primary: '#7c3aed', glow: '#c4b5fd', cheek: '#fca5a5' },
  sad:          { primary: '#6366f1', glow: '#818cf8', cheek: '#c4b5fd' },
  waving:       { primary: '#6366f1', glow: '#a5b4fc', cheek: '#f9a8d4' },
  impressed:    { primary: '#6366f1', glow: '#c4b5fd', cheek: '#fda4af' },
  encouraging:  { primary: '#4f46e5', glow: '#818cf8', cheek: '#fdba74' },
  focused:      { primary: '#4338ca', glow: '#6366f1', cheek: '#e2e8f0' },
  sleepy:       { primary: '#6366f1', glow: '#818cf8', cheek: '#e2e8f0' },
};

const levelBadge = (lvl: number) => {
  if (lvl >= 20) return { color: '#f59e0b', label: '★' };
  if (lvl >= 10) return { color: '#a78bfa', label: '◆' };
  if (lvl >= 5)  return { color: '#60a5fa', label: '●' };
  return null;
};

export default function Mascot({
  mood = 'idle', size = 80, message, className = '', showBubble = true, level, onClick,
}: MascotProps) {
  const cfg = moodConfig[mood];
  const s = size;
  const ref = useRef<HTMLDivElement>(null);
  const [blink, setBlink] = useState(false);
  const badge = level ? levelBadge(level) : null;
  const mouseX = useMotionValue(0);
  const mouseY = useMotionValue(0);
  const pupilX = useTransform(mouseX, [-300, 300], [-1.5, 1.5]);
  const pupilY = useTransform(mouseY, [-300, 300], [-1, 1]);

  // Natural blink cycle
  useEffect(() => {
    if (mood === 'sleepy') return;
    const interval = setInterval(() => {
      setBlink(true);
      setTimeout(() => setBlink(false), 150);
    }, 3000 + Math.random() * 2000);
    return () => clearInterval(interval);
  }, [mood]);

  // Track cursor for eye follow
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const handler = (e: MouseEvent) => {
      const r = el.getBoundingClientRect();
      const cx = r.left + r.width / 2;
      const cy = r.top + r.height / 2;
      mouseX.set(e.clientX - cx);
      mouseY.set(e.clientY - cy);
    };
    window.addEventListener('mousemove', handler, { passive: true });
    return () => window.removeEventListener('mousemove', handler);
  }, [mouseX, mouseY]);

  const bodyAnim: Variants = {
    idle:         { y: [0, -1.5, 0], transition: { repeat: Infinity, duration: 4, ease: 'easeInOut' } },
    happy:        { y: [0, -3, 0], transition: { repeat: Infinity, duration: 1.2, ease: 'easeInOut' } },
    thinking:     { rotate: [-1, 1, -1], transition: { repeat: Infinity, duration: 3, ease: 'easeInOut' } },
    celebrating:  { y: [0, -5, 0], scale: [1, 1.03, 1], transition: { repeat: Infinity, duration: 0.8, ease: 'easeInOut' } },
    sad:          { y: 0, rotate: -2 },
    waving:       { y: [0, -1, 0], transition: { repeat: Infinity, duration: 2.5, ease: 'easeInOut' } },
    impressed:    { scale: [1, 1.02, 1], transition: { repeat: Infinity, duration: 1.5, ease: 'easeInOut' } },
    encouraging:  { y: [0, -2, 0], transition: { repeat: Infinity, duration: 1.5, ease: 'easeInOut' } },
    focused:      { y: 0 },
    sleepy:       { rotate: [0, -3, 0], transition: { repeat: Infinity, duration: 5, ease: 'easeInOut' } },
  };

  const renderMouth = () => {
    switch (mood) {
      case 'happy': case 'celebrating': case 'impressed':
        return <path d="M43 63 Q50 70 57 63" fill="none" stroke="#1e1b4b" strokeWidth="1.5" strokeLinecap="round" />;
      case 'sad':
        return <path d="M44 66 Q50 62 56 66" fill="none" stroke="#1e1b4b" strokeWidth="1.5" strokeLinecap="round" />;
      case 'thinking': case 'focused':
        return <ellipse cx="52" cy="64" rx="2.5" ry="2" fill="#1e1b4b" />;
      case 'sleepy':
        return <path d="M45 64 L55 64" stroke="#1e1b4b" strokeWidth="1.2" strokeLinecap="round" />;
      case 'encouraging':
        return <path d="M43 62 Q50 69 57 62" fill="#1e1b4b" stroke="#1e1b4b" strokeWidth="0.5" />;
      default:
        return <path d="M45 63 Q50 66 55 63" fill="none" stroke="#1e1b4b" strokeWidth="1.2" strokeLinecap="round" />;
    }
  };

  const eyesClosed = blink || mood === 'sleepy';
  const showWavingArm = mood === 'waving' || mood === 'celebrating' || mood === 'encouraging';

  return (
    <div ref={ref} className={`flex flex-col items-center gap-1.5 ${className}`} onClick={onClick} style={onClick ? { cursor: 'pointer' } : undefined}>
      <motion.svg
        viewBox="0 0 100 110"
        width={s}
        height={s * 1.1}
        variants={bodyAnim}
        animate={mood}
        style={{ overflow: 'visible', filter: `drop-shadow(0 2px 4px ${cfg.primary}22)` }}
      >
        <defs>
          <radialGradient id={`bodyGrad-${mood}`} cx="45%" cy="35%" r="60%">
            <stop offset="0%" stopColor={cfg.glow} />
            <stop offset="100%" stopColor={cfg.primary} />
          </radialGradient>
          <radialGradient id="bellyGrad" cx="50%" cy="40%" r="55%">
            <stop offset="0%" stopColor="#eef2ff" />
            <stop offset="100%" stopColor="#e0e7ff" />
          </radialGradient>
        </defs>

        {/* Shadow */}
        <motion.ellipse
          cx="50" cy="105" rx="20" ry="3.5"
          fill="#94a3b8" opacity="0.15"
          animate={{ rx: mood === 'celebrating' ? [20, 18, 20] : 20 }}
          transition={{ repeat: Infinity, duration: 0.8 }}
        />

        {/* Body */}
        <ellipse cx="50" cy="62" rx="27" ry="30" fill={`url(#bodyGrad-${mood})`} />
        {/* Belly highlight */}
        <ellipse cx="50" cy="70" rx="15" ry="13" fill="url(#bellyGrad)" opacity="0.9" />

        {/* Graduation cap */}
        <g>
          <polygon points="50,22 27,33 50,40 73,33" fill="#1e1b4b" />
          <rect x="46" y="31" width="8" height="4" fill="#1e1b4b" rx="1" />
          <line x1="68" y1="33" x2="72" y2="43" stroke="#312e81" strokeWidth="1.5" />
          <circle cx="72" cy="44" r="2" fill="#fbbf24" />
          {/* Tassel swing */}
          <motion.line
            x1="72" y1="44" x2="76" y2="50"
            stroke="#fbbf24" strokeWidth="1"
            animate={{ x2: [76, 73, 76] }}
            transition={{ repeat: Infinity, duration: 2, ease: 'easeInOut' }}
          />
        </g>

        {/* Level badge on cap */}
        {badge && (
          <g>
            <circle cx="50" cy="26" r="5" fill={badge.color} opacity="0.9" />
            <text x="50" y="28.5" textAnchor="middle" fontSize="6" fill="white" fontWeight="bold">{badge.label}</text>
          </g>
        )}

        {/* Eyes */}
        <g>
          {/* Eye whites */}
          <ellipse cx="40" cy="54" rx="5.5" ry={eyesClosed ? 0.8 : 6} fill="white">
            {eyesClosed && <animate attributeName="ry" values="6;0.8;6" dur="0.15s" fill="freeze" />}
          </ellipse>
          <ellipse cx="60" cy="54" rx="5.5" ry={eyesClosed ? 0.8 : 6} fill="white">
            {eyesClosed && <animate attributeName="ry" values="6;0.8;6" dur="0.15s" fill="freeze" />}
          </ellipse>
          {/* Pupils — follow cursor */}
          {!eyesClosed && (
            <>
              <motion.circle cx="40" cy="54" r="2.8" fill="#1e1b4b" style={{ x: pupilX, y: pupilY }} />
              <motion.circle cx="60" cy="54" r="2.8" fill="#1e1b4b" style={{ x: pupilX, y: pupilY }} />
              {/* Catchlights */}
              <motion.circle cx="41.2" cy="52.5" r="1" fill="white" style={{ x: pupilX, y: pupilY }} />
              <motion.circle cx="61.2" cy="52.5" r="1" fill="white" style={{ x: pupilX, y: pupilY }} />
            </>
          )}
          {/* Impressed — wide eyes */}
          {mood === 'impressed' && !eyesClosed && (
            <>
              <ellipse cx="40" cy="54" rx="6" ry="6.5" fill="white" />
              <ellipse cx="60" cy="54" rx="6" ry="6.5" fill="white" />
              <motion.circle cx="40" cy="54" r="3" fill="#1e1b4b" style={{ x: pupilX, y: pupilY }} />
              <motion.circle cx="60" cy="54" r="3" fill="#1e1b4b" style={{ x: pupilX, y: pupilY }} />
              <motion.circle cx="41" cy="52" r="1.2" fill="white" style={{ x: pupilX, y: pupilY }} />
              <motion.circle cx="61" cy="52" r="1.2" fill="white" style={{ x: pupilX, y: pupilY }} />
            </>
          )}
        </g>

        {/* Glasses for focused/thinking */}
        {(mood === 'focused' || mood === 'thinking') && (
          <g opacity="0.7">
            <circle cx="40" cy="54" r="8" fill="none" stroke="#475569" strokeWidth="1" />
            <circle cx="60" cy="54" r="8" fill="none" stroke="#475569" strokeWidth="1" />
            <line x1="48" y1="54" x2="52" y2="54" stroke="#475569" strokeWidth="1" />
            <line x1="32" y1="53" x2="26" y2="51" stroke="#475569" strokeWidth="1" />
            <line x1="68" y1="53" x2="74" y2="51" stroke="#475569" strokeWidth="1" />
          </g>
        )}

        {/* Cheeks */}
        <circle cx="32" cy="60" r="4" fill={cfg.cheek} opacity="0.35" />
        <circle cx="68" cy="60" r="4" fill={cfg.cheek} opacity="0.35" />

        {/* Mouth */}
        {renderMouth()}

        {/* Arms */}
        {showWavingArm ? (
          <motion.g
            animate={{ rotate: [0, -20, 20, -20, 0] }}
            transition={{ repeat: Infinity, duration: 1.2, ease: 'easeInOut' }}
            style={{ transformOrigin: '24px 62px' }}
          >
            <path d="M24 62 Q14 48 18 38" fill="none" stroke={cfg.primary} strokeWidth="4.5" strokeLinecap="round" />
            <circle cx="18" cy="37" r="3" fill={cfg.primary} />
          </motion.g>
        ) : mood === 'focused' ? (
          <g>
            <path d="M24 60 Q20 55 24 48" fill="none" stroke={cfg.primary} strokeWidth="4.5" strokeLinecap="round" />
            <circle cx="24" cy="47" r="3" fill={cfg.primary} />
          </g>
        ) : (
          <path d="M24 62 Q19 70 22 78" fill="none" stroke={cfg.primary} strokeWidth="4.5" strokeLinecap="round" />
        )}
        <path d="M76 62 Q81 70 78 78" fill="none" stroke={cfg.primary} strokeWidth="4.5" strokeLinecap="round" />

        {/* Feet */}
        <ellipse cx="40" cy="92" rx="7" ry="3.5" fill="#4338ca" />
        <ellipse cx="60" cy="92" rx="7" ry="3.5" fill="#4338ca" />

        {/* Celebrating particles */}
        {mood === 'celebrating' && (
          <g>
            {[
              { x: 10, y: 30, d: 1.0, r: 1.5, c: '#fbbf24' },
              { x: 85, y: 25, d: 0.3, r: 1.2, c: '#f472b6' },
              { x: 15, y: 45, d: 0.6, r: 1, c: '#34d399' },
              { x: 82, y: 42, d: 0.8, r: 1.3, c: '#60a5fa' },
              { x: 50, y: 12, d: 0.5, r: 1.4, c: '#fbbf24' },
            ].map((p, i) => (
              <motion.circle
                key={i} cx={p.x} cy={p.y} r={p.r} fill={p.c}
                animate={{ y: [p.y, p.y - 10, p.y], opacity: [0.3, 1, 0.3], scale: [0.8, 1.2, 0.8] }}
                transition={{ repeat: Infinity, duration: 1.5, delay: p.d, ease: 'easeInOut' }}
              />
            ))}
          </g>
        )}

        {/* Zzz for sleepy */}
        {mood === 'sleepy' && (
          <g>
            <motion.text x="68" y="40" fontSize="8" fill="#94a3b8" fontWeight="bold"
              animate={{ y: [40, 34], opacity: [0, 1, 0] }}
              transition={{ repeat: Infinity, duration: 2.5 }}
            >z</motion.text>
            <motion.text x="75" y="32" fontSize="6" fill="#94a3b8" fontWeight="bold"
              animate={{ y: [32, 26], opacity: [0, 1, 0] }}
              transition={{ repeat: Infinity, duration: 2.5, delay: 0.8 }}
            >z</motion.text>
          </g>
        )}
      </motion.svg>

      {/* Speech bubble */}
      {message && showBubble && (
        <motion.div
          initial={{ opacity: 0, y: 6, scale: 0.95 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ type: 'spring', stiffness: 300, damping: 20 }}
          className="relative bg-white/90 backdrop-blur-sm border border-slate-200/80 rounded-2xl px-3.5 py-2 text-xs text-slate-700 font-medium shadow-lg shadow-slate-200/40 max-w-[200px] text-center"
        >
          <div className="absolute -top-[5px] left-1/2 -translate-x-1/2 w-2.5 h-2.5 bg-white/90 border-l border-t border-slate-200/80 rotate-45" />
          <span className="relative z-10 leading-relaxed">{message}</span>
        </motion.div>
      )}
    </div>
  );
}
