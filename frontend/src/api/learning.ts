import api from './client';

export interface QuestionResponse {
  id: string;
  question_text: string;
  question_type: string;
  options: string[] | null;
  difficulty: number;
  concept_id: string;
  concept_name: string;
  topic_name: string;
  time_estimate_seconds: number;
  attempt_number: number;
}

export interface SessionStats {
  questions_answered_today: number;
  correct_today: number;
  current_streak: number;
  xp_today: number;
}

export interface ConceptProgressBrief {
  concept_id: string;
  concept_name: string;
  mastery_level: string;
  confidence_score: number;
  exposure_count: number;
}

export interface CooldownItem {
  question_id: string;
  expires_in_seconds: number;
}

export interface LearningSession {
  question: QuestionResponse;
  session_stats: SessionStats;
  concept_progress: ConceptProgressBrief;
  cooldown_questions: CooldownItem[];
}

export interface LessonCard {
  title: string;
  content: string;
  key_points: string[];
  type: 'intro' | 'review' | 'mistake_fix';
}

export interface AnswerResult {
  is_correct: boolean;
  correct_answer: string;
  explanation: string | null;
  xp_earned: number;
  confidence_change: number;
  mastery_level: string;
  streak_count: number;
  next_review_message: string;
  level_up: boolean;
  new_badges: string[];
  lesson_card: LessonCard | null;
  cooldown_seconds: number | null;
}

export interface WrongQuestionItem {
  question_id: string;
  question_text: string;
  correct_answer: string;
  selected_answer: string;
  explanation: string | null;
  concept_id: string;
  concept_name: string;
  topic_name: string;
  difficulty: number;
  attempt_count: number;
  last_attempted: string;
}

export interface ConceptNotes {
  id: string;
  name: string;
  topic_name: string;
  explanation: string;
  key_points: string[];
}

export const learningApi = {
  getNextQuestion: (subjectId: string, conceptId?: string, topicId?: string) => {
    const params = new URLSearchParams();
    if (conceptId) params.set('concept_id', conceptId);
    if (topicId) params.set('topic_id', topicId);
    const qs = params.toString();
    return api.get<LearningSession>(`/learn/next-question/${subjectId}${qs ? `?${qs}` : ''}`);
  },

  submitAnswer: (data: { question_id: string; selected_answer: string; response_time_ms: number }) =>
    api.post<AnswerResult>('/learn/submit-answer', data),

  getWrongQuestions: (subjectId: string, page = 1, pageSize = 20) =>
    api.get<{ items: WrongQuestionItem[]; total: number; page: number; total_pages: number; has_next: boolean }>(
      `/learn/wrong-questions/${subjectId}?page=${page}&page_size=${pageSize}`
    ),

  getConceptNotes: (conceptId: string) =>
    api.get<ConceptNotes>(`/learn/concept-notes/${conceptId}`),

  reportQuestion: (data: { question_id: string; reason: string; details?: string }) =>
    api.post<{ message: string; report_count: number }>('/learn/report-question', data),

  getQuestionReports: (questionId: string) =>
    api.get<{ report_count: number; user_reported: boolean }>(`/learn/question-reports/${questionId}`),
};
