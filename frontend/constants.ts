import { Mission, Transaction, UserStats, QuizQuestion } from './types';

export const INITIAL_USER_STATS: UserStats = {
  xp: 1250,
  level: 5,
  coins: 340,
  lives: 5,
  streak: 12
};

export const MOCK_TRANSACTIONS: Transaction[] = [
  { id: '1', description: 'Mesada', amount: 200, category: 'Outros', date: '2023-10-01', type: 'income' },
  { id: '2', description: 'Burger King', amount: 35.50, category: 'Alimentação', date: '2023-10-03', type: 'expense' },
  { id: '3', description: 'Uber pra Escola', amount: 15.00, category: 'Transporte', date: '2023-10-04', type: 'expense' },
  { id: '4', description: 'Ingresso Cinema', amount: 25.00, category: 'Lazer', date: '2023-10-05', type: 'expense' },
  { id: '5', description: 'Livraria', amount: 45.00, category: 'Educação', date: '2023-10-06', type: 'expense' },
];

export const DAILY_MISSIONS: Mission[] = [
  { id: 'm1', title: 'Conferir seu saldo', reward: 10, completed: true },
  { id: 'm2', title: 'Economizar R$ 5,00 hoje', reward: 50, completed: false },
  { id: 'm3', title: 'Ler uma dica financeira', reward: 20, completed: false },
];

export const QUIZ_SAMPLE: QuizQuestion[] = [
  {
    id: 1,
    question: "O que são juros compostos?",
    options: [
      "Juros apenas sobre o valor inicial",
      "Juros sobre o valor inicial mais os juros acumulados",
      "Uma taxa que o banco te paga de graça",
      "Dinheiro que você perde com o tempo"
    ],
    correctIndex: 1
  },
  {
    id: 2,
    question: "Qual é uma 'Necessidade' e não um 'Desejo'?",
    options: [
      "Videogame novo",
      "Tênis de marca",
      "Compras básicas de mercado",
      "Ingressos para show"
    ],
    correctIndex: 2
  },
  {
    id: 3,
    question: "Segundo a Regra 50/30/20, como você deve dividir seu dinheiro?",
    options: [
      "50% Diversão, 30% Poupança, 20% Necessidades",
      "50% Necessidades, 30% Desejos, 20% Poupança",
      "50% Poupança, 30% Necessidades, 20% Desejos",
      "50% Desejos, 30% Poupança, 20% Necessidades"
    ],
    correctIndex: 1
  }
];