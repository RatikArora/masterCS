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

// Shuffle dict options: randomize entries and reassign to A/B/C/D keys
function shuffleOptions(opts: Record<string, string>): { options: Record<string, string>; keyMap: Record<string, string> } {
  const entries = Object.entries(opts);
  const shuffled = shuffleArray(entries);
  const keys = ['A', 'B', 'C', 'D', 'E', 'F'];
  const newOpts: Record<string, string> = {};
  const keyMap: Record<string, string> = {}; // new key → original key
  shuffled.forEach(([origKey, value], i) => {
    const newKey = keys[i] || String.fromCharCode(65 + i);
    newOpts[newKey] = value;
    keyMap[newKey] = origKey;
  });
  return { options: newOpts, keyMap };
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
  optionKeyMap: Record<string, string> | null; // shuffled key → original key

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
  optionKeyMap: null,

  fetchNextQuestion: async (subjectId, conceptId, topicId) => {
    set({ isLoadingQuestion: true, error: null, result: null, showFeedback: false, currentConceptId: conceptId || null, currentTopicId: topicId || null, optionKeyMap: null });
    try {
      const { data } = await learningApi.getNextQuestion(subjectId, conceptId, topicId);
      // Shuffle options to randomize correct answer position
      if (data.question.options && Object.keys(data.question.options).length > 1) {
        const { options, keyMap } = shuffleOptions(data.question.options);
        data.question.options = options;
        set({ session: data, isLoadingQuestion: false, questionStartTime: Date.now(), optionKeyMap: keyMap });
      } else {
        set({ session: data, isLoadingQuestion: false, questionStartTime: Date.now(), optionKeyMap: null });
      }
    } catch (err: any) {
      const msg = err.response?.data?.detail || 'Failed to load question';
      set({ isLoadingQuestion: false, error: msg });
    }
  },

  submitAnswer: async (questionId, answer) => {
    const { questionStartTime, hotStreak, optionKeyMap } = get();
    const responseTime = Date.now() - questionStartTime;
    // Map the shuffled key back to the original key for backend comparison
    const originalKey = optionKeyMap ? (optionKeyMap[answer] || answer) : answer;
    set({ isSubmitting: true });
    try {
      const { data } = await learningApi.submitAnswer({
        question_id: questionId,
        selected_answer: originalKey,
        response_time_ms: responseTime,
      });
      // Map the correct_answer back to the shuffled key for UI highlighting
      if (optionKeyMap) {
        const reverseMap = Object.fromEntries(Object.entries(optionKeyMap).map(([k, v]) => [v, k]));
        data.correct_answer = reverseMap[data.correct_answer] || data.correct_answer;
      }
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
    optionKeyMap: null,
  }),
}));
