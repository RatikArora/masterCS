import api from './client';

export interface Badge {
  id: string;
  name: string;
  description: string;
  icon: string;
  category: string;
  earned: boolean;
  progress: number;
  current_value: number;
  target_value: number;
}

export interface LevelInfo {
  level: number;
  title: string;
  current_xp: number;
  xp_for_next: number;
  progress: number;
}

export interface BadgesResponse {
  level: LevelInfo;
  badges: Badge[];
  total_earned: number;
  total_available: number;
}

export const badgesApi = {
  getBadges: () => api.get<BadgesResponse>('/badges'),
};
