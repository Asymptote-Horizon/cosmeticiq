import { create } from 'zustand';

interface User {
  id: number;
  email: string;
  username: string;
  full_name?: string;
  is_admin: boolean;
}

interface UserProfile {
  skin_type: string;
  age: number;
  climate: string;
  city: string;
  budget_min: number;
  budget_max: number;
  allergies: string[];
  concerns: string[];
  is_pregnant: boolean;
  is_vegan: boolean;
  is_cruelty_free: boolean;
}

interface AppState {
  user: User | null;
  profile: UserProfile | null;
  token: string | null;
  isLoading: boolean;
  
  setUser: (user: User | null) => void;
  setProfile: (profile: UserProfile | null) => void;
  setToken: (token: string | null) => void;
  setLoading: (loading: boolean) => void;
  logout: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  user: null,
  profile: null,
  token: typeof window !== 'undefined' ? localStorage.getItem('token') : null,
  isLoading: false,
  
  setUser: (user) => set({ user }),
  setProfile: (profile) => set({ profile }),
  setToken: (token) => {
    if (typeof window !== 'undefined') {
      if (token) {
        localStorage.setItem('token', token);
      } else {
        localStorage.removeItem('token');
      }
    }
    set({ token });
  },
  setLoading: (isLoading) => set({ isLoading }),
  logout: () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token');
    }
    set({ user: null, profile: null, token: null });
  },
}));
