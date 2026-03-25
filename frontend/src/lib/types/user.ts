export type UserPlan = 'free' | 'pro' | 'team' | 'enterprise';

export interface User {
  id: string;
  email: string;
  fullName?: string;
  avatarUrl?: string;
  plan: UserPlan;
  isActive: boolean;
  emailVerified: boolean;
  onboardingCompleted: boolean;
  preferences: UserPreferences;
  createdAt: string;
  updatedAt: string;
}

export interface UserPreferences {
  theme: 'light' | 'dark' | 'system';
  defaultTimeRange: '1h' | '6h' | '24h' | '7d' | '30d';
  emailDigest: 'daily' | 'weekly' | 'none';
  favoriteCategories: string[];
}
