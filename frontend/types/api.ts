/**
 * API Types
 * TypeScript interfaces for API requests and responses
 */

// ==================
// Authentication
// ==================

export interface RegisterRequest {
  email: string;
  password: string;
  name: string;
  phone?: string;
  monthly_income?: number;
  savings_goal?: number;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface UserGamification {
  level: number;
  xp: number;
  coins: number;
  lives: number;
  badges: string[];
  current_streak: number;
  longest_streak: number;
  last_login: string;
}

export interface UserProfile {
  age?: number;
  monthly_income?: number;
  monthly_budget?: number;
  savings_goal?: number;
  financial_goals?: string[];
  avatar_url?: string;
}

export interface UserData {
  uid: string;
  email: string;
  name: string;
  phone?: string;
  gamification: UserGamification;
  profile?: UserProfile;
}

export interface AuthResponse {
  user: UserData;
  tokens: AuthTokens;
}

// ==================
// FIM Assistant
// ==================

export interface ChatRequest {
  message: string;
  include_context?: boolean;
}

export interface ChatResponse {
  response: string;
  suggestions: string[];
  timestamp: string;
  error?: string;
}

export interface ConversationMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

// ==================
// Transactions
// ==================

export interface Transaction {
  id: string;
  user_id: string;
  type: 'income' | 'expense';
  amount: number;
  category: string;
  description?: string;
  date: string;
  source: 'app' | 'whatsapp';
  tags?: string[];
  is_recurrent?: boolean;
  created_at: string;
  updated_at: string;
}

export interface TransactionCreate {
  type: 'income' | 'expense';
  amount: number;
  category: string;
  description?: string;
  date?: string;
  tags?: string[];
  is_recurrent?: boolean;
}

export interface TransactionUpdate {
  amount?: number;
  category?: string;
  description?: string;
  date?: string;
  tags?: string[];
}

export interface TransactionListResponse {
  transactions: Transaction[];
  total: number;
  page: number;
  limit: number;
  total_pages: number;
}

// ==================
// Dashboard
// ==================

export interface DashboardStats {
  lives: number;
  max_lives: number;
  streak: number;
  coins: number;
  level: number;
  current_xp: number;
  next_level_xp: number;
  xp_percentage: number;
}

export interface BalanceInfo {
  current: number;
  spent_this_month: number;
  monthly_budget: number;
  budget_percentage: number;
}

export interface BudgetAlert {
  show: boolean;
  percentage: number;
  message: string;
}

export interface Mission {
  id: string;
  type: string;
  title: string;
  description: string;
  xp_reward: number;
  coins_reward: number;
  status: string;
  progress: number;
  target: number;
  completed: boolean;
  date: string;
}

export interface LearningProgress {
  course_id: string;
  course_title: string;
  module_id: string;
  module_title: string;
  current_phase: number;
  total_phases: number;
  progress_percentage: number;
  current_phase_id?: string;
}

export interface DashboardOverview {
  stats: DashboardStats;
  balance: BalanceInfo;
  budget_alert: BudgetAlert;
  missions: Mission[];
  learning_progress?: LearningProgress;
}

// ==================
// Categories
// ==================

export interface Category {
  id: string;
  name: string;
  icon: string;
  color: string;
  budget_suggestion?: number;
}

// ==================
// Gamification
// ==================

export interface Badge {
  id: string;
  name: string;
  description: string;
  icon: string;
  rarity: 'common' | 'uncommon' | 'rare' | 'epic' | 'legendary';
  earned: boolean;
  earned_at?: string;
  xp_reward: number;
}

export interface LeaderboardEntry {
  rank: number;
  user: {
    uid: string;
    name: string;
    avatar_url?: string;
  };
  xp: number;
  level: number;
  badges_count: number;
}

// ==================
// Learning
// ==================

export interface LearningModule {
  id: string;
  title: string;
  description: string;
  category: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  estimated_time: number;
  xp_reward: number;
  completed: boolean;
  progress: number;
}

export interface QuizQuestion {
  id: string;
  question: string;
  options: string[];
  correct_answer: number;
  explanation?: string;
}
