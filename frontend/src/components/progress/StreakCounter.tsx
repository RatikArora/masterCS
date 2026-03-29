import { motion } from 'framer-motion';

export default function StreakCounter({ count, isActive }: { count: number; isActive?: boolean }) {
  return (
    <motion.div
      className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-xl text-xs font-bold tracking-wide ${
        count > 0
          ? 'bg-gradient-to-r from-orange-50 to-amber-50 text-orange-600 border border-orange-200/70 shadow-sm'
          : 'bg-slate-50 text-slate-400 border border-slate-200/60'
      }`}
      animate={isActive && count > 0 ? { scale: [1, 1.06, 1] } : undefined}
      transition={{ duration: 0.3, type: 'spring' }}
    >
      {count > 0 ? (
        <motion.svg
          className="w-4 h-4"
          viewBox="0 0 20 20"
          fill="currentColor"
          animate={isActive ? { rotate: [-5, 5, -5] } : undefined}
          transition={{ repeat: Infinity, duration: 1.5, ease: 'easeInOut' }}
        >
          <path d="M12.395 2.553a1 1 0 00-1.45-.385c-.345.23-.614.558-.822.88-.214.33-.403.713-.57 1.116-.334.804-.614 1.768-.84 2.734a31.365 31.365 0 00-.613 3.58 2.64 2.64 0 01-.945-1.067c-.328-.68-.398-1.534-.398-2.654A1 1 0 005.05 6.05 6.981 6.981 0 003 11a7 7 0 1011.95-4.95c-.592-.591-.98-.985-1.348-1.467-.363-.476-.724-1.063-1.207-2.03zM12.12 15.12A3 3 0 017 13s.879.5 2.5.5c0-1 .5-4 1.25-4.5.5 1 .786 1.293 1.371 1.879A2.99 2.99 0 0113 13a2.99 2.99 0 01-.879 2.121z"/>
        </motion.svg>
      ) : (
        <svg className="w-4 h-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      )}
      <span>{count > 0 ? `${count} day${count !== 1 ? 's' : ''}` : 'No streak'}</span>
      {isActive && count > 0 && (
        <span className="w-1.5 h-1.5 rounded-full bg-orange-400 animate-pulse" />
      )}
    </motion.div>
  );
}
