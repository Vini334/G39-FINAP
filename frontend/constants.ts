import { Mission, Transaction, UserStats, QuizQuestion, SplitEvent } from './types';

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

// ========== SPLIT BILL (Dividir Conta) MOCK DATA ==========

export const MOCK_SPLIT_EVENTS: SplitEvent[] = [
  {
    id: 'se1',
    title: 'Viagem de Juquehy 13/11',
    date: '13 Nov 2024',
    createdBy: 'u1',
    members: [
      { id: 'u1', name: 'Você', avatar: 'Alex', balance: 0 },
      { id: 'u2', name: 'Sarah', avatar: 'Sarah', balance: 0 },
      { id: 'u3', name: 'Mike', avatar: 'Mike', balance: 0 },
      { id: 'u4', name: 'Jess', avatar: 'Jess', balance: 0 },
    ],
    expenses: [
      {
        // Restaurante com divisão desigual (exemplo da cerveja)
        id: 'exp1',
        description: 'Restaurante Praia',
        amount: 280.00,
        paidBy: 'u1', // Você pagou
        date: '13 Nov 2024',
        splits: [
          { memberId: 'u1', amount: 80.00 }, // Você bebeu cerveja
          { memberId: 'u2', amount: 60.00 }, // Sarah não bebeu
          { memberId: 'u3', amount: 80.00 }, // Mike bebeu cerveja
          { memberId: 'u4', amount: 60.00 }, // Jess não bebeu
        ]
      },
      {
        // Uber dividido igualmente
        id: 'exp2',
        description: 'Uber para praia',
        amount: 48.00,
        paidBy: 'u2', // Sarah pagou
        date: '13 Nov 2024',
        splits: [
          { memberId: 'u1', amount: 12.00 },
          { memberId: 'u2', amount: 12.00 },
          { memberId: 'u3', amount: 12.00 },
          { memberId: 'u4', amount: 12.00 },
        ]
      },
      {
        // Airbnb pago por uma pessoa
        id: 'exp3',
        description: 'Airbnb (2 noites)',
        amount: 400.00,
        paidBy: 'u1', // Você pagou
        date: '12 Nov 2024',
        splits: [
          { memberId: 'u1', amount: 100.00 },
          { memberId: 'u2', amount: 100.00 },
          { memberId: 'u3', amount: 100.00 },
          { memberId: 'u4', amount: 100.00 },
        ]
      },
      {
        // Lanche no posto
        id: 'exp4',
        description: 'Lanche posto',
        amount: 52.00,
        paidBy: 'u3', // Mike pagou
        date: '13 Nov 2024',
        splits: [
          { memberId: 'u1', amount: 13.00 },
          { memberId: 'u2', amount: 13.00 },
          { memberId: 'u3', amount: 13.00 },
          { memberId: 'u4', amount: 13.00 },
        ]
      }
    ]
  }
];

// Membros disponíveis para convidar (mock de amigos)
export const AVAILABLE_FRIENDS = [
  { id: 'u2', name: 'Sarah', avatar: 'Sarah' },
  { id: 'u3', name: 'Mike', avatar: 'Mike' },
  { id: 'u4', name: 'Jess', avatar: 'Jess' },
  { id: 'u5', name: 'Lucas', avatar: 'Lucas' },
  { id: 'u6', name: 'Ana', avatar: 'Ana' },
];