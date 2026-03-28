import { create } from 'zustand';
import { learningApi, type LearningSession, type AnswerResult } from '../api/learning';

interface LearningState {
  session: LearningSession | null;
  result: AnswerResult | null;
  isLoadingQuestion: boolean;
  isSubmitting: boolean;
  showFeedback: boolean;
  questionStartTime: number;
  error: string | null;
  currentConceptId: string | null;

  fetchNextQuestion: (subjectId: string, conceptId?: string) => Promise<void>;
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

  fetchNextQuestion: async (subjectId, conceptId) => {
    set({ isLoadingQuestion: true, error: null, result: null, showFeedback: false, currentConceptId: conceptId || null });
    try {
      const { data } = await learningApi.getNextQuestion(subjectId, conceptId);
      set({ session: data, isLoadingQuestion: false, questionStartTime: Date.now() });
    } catch (err: any) {
      const msg = err.response?.data?.detail || 'Failed to load question';
      set({ isLoadingQuestion: false, error: msg });
    }
  },

  submitAnswer: async (questionId, answer) => {
    const { questionStartTime } = get();
    const responseTime = Date.now() - questionStartTime;
    set({ isSubmitting: true });
    try {
      const { data } = await learningApi.submitAnswer({
        question_id: questionId,
        selected_answer: answer,
        response_time_ms: responseTime,
      });
      set({ result: data, isSubmitting: false, showFeedback: true });
    } catch {
      set({ isSubmitting: false, error: 'Failed to submit answer' });
    }
  },

  dismissFeedback: () => set({ showFeedback: false }),

  reset: () => set({
    session: null, result: null, isLoadingQuestion: false,
    isSubmitting: false, showFeedback: false, error: null,
  }),
}));
