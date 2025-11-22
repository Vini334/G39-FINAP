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
  title: string;
  reward: number;
  completed: boolean;
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