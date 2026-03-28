import { create } from 'zustand';
import { learningApi, type LearningSession, type AnswerResult } from '../api/learning';

// Fisher-Yates shuffle
function shuffleArray<T>(arr: T[]): T[] {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

interface LearningState {
  session: LearningSession | null;
  result: AnswerResult | null;
  isLoadingQuestion: boolean;
  isSubmitting: boolean;
  showFeedback: boolean;
  questionStartTime: number;
  error: string | null;
  currentConceptId: string | null;
  currentTopicId: string | null;
  hotStreak: number; // consecutive correct in this session

  fetchNextQuestion: (subjectId: string, conceptId?: string, topicId?: string) => Promise<void>;
  submitAnswer: (questionId: string, answer: string) => Promise<void>;
  dismissFeedback: () => void;
  reset: () => void;
}

export const useLearningStore = create<LearningState>((set, get) => ({
  session: null,
  result: null,
  isLoadingQuestion: false,
  isSubmitting: false,
  showFeedback: false,
  questionStartTime: 0,
  error: null,
  currentConceptId: null,
  currentTopicId: null,
  hotStreak: 0,

  fetchNextQuestion: async (subjectId, conceptId, topicId) => {
    set({ isLoadingQuestion: true, error: null, result: null, showFeedback: false, currentConceptId: conceptId || null, currentTopicId: topicId || null });
    try {
      const { data } = await learningApi.getNextQuestion(subjectId, conceptId, topicId);
      // Shuffle options to randomize correct answer position
      if (data.question.options && data.question.options.length > 1) {
        data.question.options = shuffleArray(data.question.options);
      }
      set({ session: data, isLoadingQuestion: false, questionStartTime: Date.now() });
    } catch (err: any) {
      const msg = err.response?.data?.detail || 'Failed to load question';
      set({ isLoadingQuestion: false, error: msg });
    }
  },

  submitAnswer: async (questionId, answer) => {
    const { questionStartTime, hotStreak } = get();
    const responseTime = Date.now() - questionStartTime;
    set({ isSubmitting: true });
    try {
      const { data } = await learningApi.submitAnswer({
        question_id: questionId,
        selected_answer: answer,
        response_time_ms: responseTime,
      });
      const newHotStreak = data.is_correct ? hotStreak + 1 : 0;
      set({ result: data, isSubmitting: false, showFeedback: true, hotStreak: newHotStreak });
    } catch {
      set({ isSubmitting: false, error: 'Failed to submit answer' });
    }
  },

  dismissFeedback: () => set({ showFeedback: false }),

  reset: () => set({
    session: null, result: null, isLoadingQuestion: false,
    isSubmitting: false, showFeedback: false, error: null, hotStreak: 0,
  }),
}));
