import api from './client';

export interface UserResponse {
  id: string;
  username: string;
  email: string;
  display_name: string | null;
  avatar_url: string | null;
  degree: string | null;
  course: string | null;
  current_streak: number;
  longest_streak: number;
  total_xp: number;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  user: UserResponse;
}

export interface ProfileUpdate {
  display_name?: string;
  degree?: string;
  course?: string;
}

export const authApi = {
  register: (data: { username: string; email: string; password: string; display_name?: string }) =>
    api.post<TokenResponse>('/auth/register', data),

  login: (data: { username: string; password: string }) =>
    api.post<TokenResponse>('/auth/login', data),

  me: () => api.get<UserResponse>('/auth/me'),

  updateProfile: (data: ProfileUpdate) =>
    api.patch<UserResponse>('/auth/profile', data),

  resetSubjectProgress: (subjectId: string) =>
    api.post<{ message: string }>(`/auth/reset-progress/${subjectId}`),

  resetTopicProgress: (topicId: string) =>
    api.post<{ message: string }>(`/auth/reset-topic/${topicId}`),
};
