import api from './client';

export interface SubjectResponse {
  id: string;
  name: string;
  description: string | null;
  icon: string | null;
  color: string | null;
  order_index: number;
  topic_count: number;
  progress_percent: number;
}

export interface TopicResponse {
  id: string;
  subject_id: string;
  name: string;
  description: string | null;
  icon: string | null;
  order_index: number;
  concept_count: number;
  question_count: number;
  mastery_percent: number;
  is_unlocked: boolean;
}

export interface ConceptResponse {
  id: string;
  topic_id: string;
  name: string;
  explanation: string | null;
  key_points: string[] | null;
  order_index: number;
  mastery_level: string;
  confidence_score: number;
}

export interface ConceptDetailResponse extends ConceptResponse {
  topic_name: string;
  subject_name: string;
  question_count: number;
  attempts_count: number;
  accuracy: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
  has_next: boolean;
  has_prev: boolean;
}

export const conceptsApi = {
  getSubjects: () =>
    api.get<SubjectResponse[]>('/concepts/subjects'),

  getTopics: (subjectId: string) =>
    api.get<PaginatedResponse<TopicResponse>>(`/concepts/subjects/${subjectId}/topics?page_size=100`),

  getConcepts: (topicId: string) =>
    api.get<PaginatedResponse<ConceptResponse>>(`/concepts/topics/${topicId}/concepts?page_size=100`),

  getConceptDetail: (conceptId: string) =>
    api.get<ConceptDetailResponse>(`/concepts/concept/${conceptId}`),
};
