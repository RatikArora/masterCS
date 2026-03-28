import { create } from 'zustand';
import { authApi, type UserResponse, type ProfileUpdate } from '../api/auth';

interface AuthState {
  user: UserResponse | null;
  token: string | null;
  isLoading: boolean;
  isAuthenticated: boolean;

  login: (username: string, password: string) => Promise<void>;
  register: (username: string, email: string, password: string, displayName?: string) => Promise<void>;
  logout: () => void;
  loadFromStorage: () => void;
  updateProfile: (data: ProfileUpdate) => Promise<void>;
  refreshUser: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  token: null,
  isLoading: false,
  isAuthenticated: false,

  login: async (username, password) => {
    set({ isLoading: true });
    try {
      const { data } = await authApi.login({ username, password });
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('user', JSON.stringify(data.user));
      set({ user: data.user, token: data.access_token, isAuthenticated: true, isLoading: false });
    } catch {
      set({ isLoading: false });
      throw new Error('Invalid credentials');
    }
  },

  register: async (username, email, password, displayName) => {
    set({ isLoading: true });
    try {
      const { data } = await authApi.register({ username, email, password, display_name: displayName });
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('user', JSON.stringify(data.user));
      set({ user: data.user, token: data.access_token, isAuthenticated: true, isLoading: false });
    } catch {
      set({ isLoading: false });
      throw new Error('Registration failed');
    }
  },

  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    set({ user: null, token: null, isAuthenticated: false });
  },

  loadFromStorage: () => {
    const token = localStorage.getItem('token');
    const userStr = localStorage.getItem('user');
    if (token && userStr) {
      try {
        const user = JSON.parse(userStr);
        set({ user, token, isAuthenticated: true });
      } catch {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
      }
    }
  },

  updateProfile: async (data: ProfileUpdate) => {
    const { data: updated } = await authApi.updateProfile(data);
    localStorage.setItem('user', JSON.stringify(updated));
    set({ user: updated });
  },

  refreshUser: async () => {
    try {
      const { data: user } = await authApi.me();
      localStorage.setItem('user', JSON.stringify(user));
      set({ user });
    } catch {
      // silent fail
    }
  },
}));
