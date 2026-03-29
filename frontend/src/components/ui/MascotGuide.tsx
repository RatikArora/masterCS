import { useMemo } from 'react';
import Mascot, { type MascotMood } from './Mascot';

type Context =
  | 'dashboard'
  | 'learning'
  | 'progress'
  | 'topics'
  | 'feedback-correct'
  | 'feedback-wrong';

interface UserStats {
  accuracy?: number;
  streak?: number;
  todayQuestions?: number;
  totalXP?: number;
  level?: number;
  weakAreas?: number;
  conceptsStarted?: number;
  totalConcepts?: number;
  todayCompleted?: boolean;
  hotStreak?: number;
}

interface MascotGuideProps {
  context: Context;
  stats?: UserStats;
  size?: number;
  className?: string;
  subjectName?: string;
  userName?: string;
  showBubble?: boolean;
}

function getTimeGreeting(): string {
  const h = new Date().getHours();
  if (h < 6) return 'Burning the midnight oil?';
  if (h < 12) return 'Morning study session!';
  if (h < 17) return 'Afternoon focus time';
  if (h < 21) return 'Evening revision mode';
  return 'Late night grind!';
}

function pickRandom<T>(arr: T[]): T {
  return arr[Math.floor(Math.random() * arr.length)];
}

function decideMoodAndMessage(
  context: Context,
  stats: UserStats,
  userName?: string,
  subjectName?: string,
): { mood: MascotMood; message: string } {
  const name = userName?.split(' ')[0] || 'there';
  const acc = stats.accuracy ?? 0;
  const streak = stats.streak ?? 0;
  const todayQ = stats.todayQuestions ?? 0;
  const hot = stats.hotStreak ?? 0;

  switch (context) {
    case 'dashboard': {
      if (streak >= 7) return { mood: 'celebrating', message: `${streak}-day streak! Legendary, ${name}!` };
      if (streak >= 3) return { mood: 'happy', message: `${streak} days straight — keep building!` };
      if (stats.todayCompleted) return { mood: 'happy', message: pickRandom([
        'Great work today!',
        'You crushed it today!',
        `Solid session, ${name}!`,
      ])};
      if (todayQ === 0) return { mood: 'waving', message: pickRandom([
        `Hey ${name}! ${getTimeGreeting()}`,
        `Ready to learn, ${name}?`,
        `Welcome back, ${name}!`,
      ])};
      return { mood: 'encouraging', message: pickRandom([
        'Keep going — you\'re building momentum!',
        `${todayQ} questions in, nice!`,
        'Every question makes you sharper',
      ])};
    }

    case 'learning': {
      if (hot >= 7) return { mood: 'impressed', message: 'You\'re on another level!' };
      if (hot >= 3) return { mood: 'celebrating', message: pickRandom([
        'Unstoppable!',
        'You\'re in the zone!',
        'Keep this streak alive!',
      ])};
      if (acc >= 80) return { mood: 'focused', message: pickRandom([
        'High accuracy — try harder ones',
        'You\'re mastering this topic',
        'Ready for a challenge?',
      ])};
      if (acc >= 50) return { mood: 'thinking', message: pickRandom([
        'Take your time with each one',
        'Read all options carefully',
        'Think about the concept first',
      ])};
      if (acc > 0 && acc < 50) return { mood: 'encouraging', message: pickRandom([
        'Every mistake is a lesson',
        'Review the explanations carefully',
        'Focus on understanding, not speed',
      ])};
      return { mood: 'focused', message: pickRandom([
        'Read carefully before answering',
        'Take your time',
        'Focus on the concept',
      ])};
    }

    case 'progress': {
      if (acc >= 80) return { mood: 'impressed', message: pickRandom([
        `${Math.round(acc)}% accuracy — exceptional!`,
        'Your progress is remarkable',
        'You\'re excelling!',
      ])};
      if (acc >= 60) return { mood: 'happy', message: pickRandom([
        'Solid progress! Keep refining',
        `${Math.round(acc)}% — above average!`,
        'You\'re getting stronger',
      ])};
      if (stats.weakAreas && stats.weakAreas > 3) return { mood: 'thinking', message: pickRandom([
        `${stats.weakAreas} areas need attention`,
        'Focus on weak concepts first',
        'Targeted practice helps most',
      ])};
      if (todayQ > 50) return { mood: 'impressed', message: `${todayQ} questions today — impressive dedication!` };
      return { mood: 'encouraging', message: pickRandom([
        'Every concept mastered counts',
        'Consistent practice wins',
        'Track your weak spots here',
      ])};
    }

    case 'topics': {
      const pct = stats.totalConcepts ? Math.round(((stats.conceptsStarted ?? 0) / stats.totalConcepts) * 100) : 0;
      if (pct >= 80) return { mood: 'celebrating', message: pickRandom([
        `${pct}% covered in ${subjectName || 'this subject'}!`,
        'Almost complete! Finish strong',
      ])};
      if (pct >= 40) return { mood: 'happy', message: pickRandom([
        `Good coverage at ${pct}%`,
        'Keep exploring new concepts',
      ])};
      return { mood: 'waving', message: pickRandom([
        'Pick a topic to start learning',
        'Explore concepts at your pace',
        `${stats.totalConcepts ?? 0} concepts to explore`,
      ])};
    }

    case 'feedback-correct': {
      if (hot >= 7) return { mood: 'impressed', message: pickRandom(['Phenomenal!', 'You\'re a machine!', 'Absolutely brilliant!']) };
      if (hot >= 5) return { mood: 'celebrating', message: pickRandom(['Dominating!', 'Can\'t be stopped!', 'On fire!']) };
      if (hot >= 3) return { mood: 'celebrating', message: pickRandom(['Hat trick!', 'Rolling!', 'Crushing it!']) };
      return { mood: 'happy', message: '' };
    }

    case 'feedback-wrong': {
      return { mood: 'sad', message: '' };
    }

    default:
      return { mood: 'idle', message: '' };
  }
}

export default function MascotGuide({
  context, stats = {}, size = 64, className = '', subjectName, userName, showBubble = true,
}: MascotGuideProps) {
  const { mood, message } = useMemo(
    () => decideMoodAndMessage(context, stats, userName, subjectName),
    // Re-compute when key stats change, not on every render
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [context, stats.accuracy, stats.streak, stats.todayQuestions, stats.hotStreak, stats.todayCompleted, userName],
  );

  return (
    <Mascot
      mood={mood}
      size={size}
      message={message || undefined}
      showBubble={showBubble}
      className={className}
      level={stats.level}
    />
  );
}

export { type UserStats, type Context };
