import api from './client';

export interface OverallProgress {
  total_concepts: number;
  concepts_started: number;
  concepts_mastered: number;
  total_questions_answered: number;
  overall_accuracy: number;
  current_streak: number;
  longest_streak: number;
  total_xp: number;
  mastery_distribution: Record<string, number>;
}

export interface TopicProgress {
  topic_id: string;
  topic_name: string;
  total_concepts: number;
  mastered_concepts: number;
  avg_confidence: number;
  mastery_percent: number;
}

export interface WeakArea {
  concept_id: string;
  concept_name: string;
  topic_name: string;
  confidence_score: number;
  error_streak: number;
  accuracy: number;
  recommended_action: string;
}

export interface DailyStats {
  date: string;
  questions_answered: number;
  correct_count: number;
  accuracy: number;
  xp_earned: number;
  time_spent_minutes: number;
}

export interface StreakInfo {
  current_streak: number;
  longest_streak: number;
  today_completed: boolean;
  daily_goal: number;
  questions_today: number;
  xp_today: number;
}

export const progressApi = {
  getOverview: (subjectId: string) =>
    api.get<OverallProgress>(`/progress/overview/${subjectId}`),

  getTopicProgress: (subjectId: string) =>
    api.get<TopicProgress[]>(`/progress/topics/${subjectId}`),

  getWeakAreas: (subjectId: string) =>
    api.get<{ items: WeakArea[]; total: number; page: number; page_size: number }>(`/progress/weak-areas/${subjectId}?page_size=100`),

  getDailyStats: (days = 30) =>
    api.get<{ items: DailyStats[]; total: number }>(`/progress/daily-stats?days=${days}`),

  getStreak: () =>
    api.get<StreakInfo>('/progress/streak'),
};
