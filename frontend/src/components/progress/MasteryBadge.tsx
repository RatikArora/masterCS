const colors: Record<string, { bg: string; text: string; label: string }> = {
  novice:     { bg: 'bg-gray-100',       text: 'text-gray-600',       label: 'Novice' },
  learning:   { bg: 'bg-blue-100',       text: 'text-blue-700',       label: 'Learning' },
  familiar:   { bg: 'bg-amber-100',      text: 'text-amber-700',      label: 'Familiar' },
  proficient: { bg: 'bg-emerald-100',    text: 'text-emerald-700',    label: 'Proficient' },
  mastered:   { bg: 'bg-purple-100',     text: 'text-purple-700',     label: 'Mastered' },
};

export default function MasteryBadge({ level, size = 'sm' }: { level: string; size?: 'xs' | 'sm' | 'md' }) {
  const config = colors[level] || colors.novice;
  const sizeClass = size === 'xs' ? 'px-1.5 py-0.5 text-[10px]' : size === 'sm' ? 'px-2 py-0.5 text-xs' : 'px-3 py-1 text-sm';

  return (
    <span className={`inline-flex items-center font-medium rounded-full ${config.bg} ${config.text} ${sizeClass}`}>
      {config.label}
    </span>
  );
}
