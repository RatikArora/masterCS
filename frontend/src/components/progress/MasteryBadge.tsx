const colors: Record<string, { bg: string; text: string; label: string }> = {
  novice:     { bg: 'bg-slate-100',      text: 'text-slate-500',      label: 'Novice' },
  learning:   { bg: 'bg-indigo-50',      text: 'text-indigo-600',     label: 'Learning' },
  familiar:   { bg: 'bg-amber-50',       text: 'text-amber-600',      label: 'Familiar' },
  proficient: { bg: 'bg-emerald-50',     text: 'text-emerald-600',    label: 'Proficient' },
  mastered:   { bg: 'bg-violet-50',      text: 'text-violet-600',     label: 'Mastered' },
};

export default function MasteryBadge({ level, size = 'sm' }: { level: string; size?: 'xs' | 'sm' | 'md' }) {
  const config = colors[level] || colors.novice;
  const sizeClass = size === 'xs' ? 'px-1.5 py-0.5 text-[10px]' : size === 'sm' ? 'px-2 py-0.5 text-xs' : 'px-2.5 py-1 text-xs';

  return (
    <span className={`inline-flex items-center font-medium rounded-lg ${config.bg} ${config.text} ${sizeClass}`}>
      {config.label}
    </span>
  );
}
