export enum ViewState {
  LOGIN = 'LOGIN',
  REGISTER = 'REGISTER',
  OVERVIEW = 'OVERVIEW',
  EXTRACT = 'EXTRACT',
  LEARN = 'LEARN',
  SOCIAL = 'SOCIAL',
  ASSISTANT = 'ASSISTANT',
  PROFILE = 'PROFILE',
  ONBOARDING = 'ONBOARDING'
}

export interface Transaction {
  id: string;
  description: string;
  amount: number;
  category: 'Alimentação' | 'Transporte' | 'Lazer' | 'Educação' | 'Outros';
  date: string;
  type: 'expense' | 'income';
}

export interface Mission {
  id: string;
  type?: string;
  title: string;
  description?: string;
  xp_reward?: number;
  coins_reward?: number;
  reward?: number; // Legacy: coins_reward alias
  progress?: number;
  target?: number;
  completed: boolean;
  status?: 'pending' | 'completed' | 'expired';
}

export interface Message {
  id: string;
  role: 'user' | 'model';
  text: string;
  timestamp: number;
}

export interface QuizQuestion {
  id: number;
  question: string;
  options: string[];
  correctIndex: number;
}

export interface UserStats {
  xp: number;
  level: number;
  coins: number;
  lives: number;
  streak: number;
}

// ========== SPLIT BILL (Dividir Conta) TYPES ==========

export interface SplitEvent {
  id: string;
  title: string;
  date: string;
  createdBy: string;
  members: SplitMember[];
  expenses: SplitExpense[];
}

export interface SplitMember {
  id: string;
  name: string;
  avatar: string;
  balance: number; // positivo = recebe, negativo = deve
}

export interface SplitExpense {
  id: string;
  description: string;
  amount: number;
  paidBy: string;
  date: string;
  splits: ExpenseSplit[];
}

export interface ExpenseSplit {
  memberId: string;
  amount: number;
}

export interface DebtDetail {
  fromMemberId: string;
  toMemberId: string;
  amount: number;
}