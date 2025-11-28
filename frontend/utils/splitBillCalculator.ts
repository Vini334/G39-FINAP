import { SplitEvent, SplitMember, DebtDetail } from '../types';

/**
 * Calcula o saldo de cada membro em um evento de divisão
 * Saldo positivo = pessoa deve receber dinheiro
 * Saldo negativo = pessoa deve dinheiro
 */
export function calculateMemberBalances(event: SplitEvent): SplitMember[] {
  const balances: Record<string, number> = {};

  // Inicializa saldos em 0
  event.members.forEach(member => {
    balances[member.id] = 0;
  });

  // Processa cada despesa
  event.expenses.forEach(expense => {
    // Quem pagou recebe crédito do valor total
    balances[expense.paidBy] += expense.amount;

    // Cada pessoa que participou tem seu valor debitado
    expense.splits.forEach(split => {
      balances[split.memberId] -= split.amount;
    });
  });

  // Retorna membros com saldos calculados
  return event.members.map(member => ({
    ...member,
    balance: Math.round(balances[member.id] * 100) / 100 // Arredonda para 2 decimais
  }));
}

/**
 * Calcula dívidas detalhadas: quem deve para quem
 * Usa algoritmo de simplificação para minimizar transações
 */
export function calculateDetailedDebts(members: SplitMember[]): DebtDetail[] {
  const debts: DebtDetail[] = [];

  // Separa credores (saldo positivo) e devedores (saldo negativo)
  const creditors = members
    .filter(m => m.balance > 0.01)
    .map(m => ({ id: m.id, amount: m.balance }))
    .sort((a, b) => b.amount - a.amount);

  const debtors = members
    .filter(m => m.balance < -0.01)
    .map(m => ({ id: m.id, amount: Math.abs(m.balance) }))
    .sort((a, b) => b.amount - a.amount);

  // Combina devedores com credores
  let creditorIdx = 0;
  let debtorIdx = 0;

  while (creditorIdx < creditors.length && debtorIdx < debtors.length) {
    const creditor = creditors[creditorIdx];
    const debtor = debtors[debtorIdx];

    const amount = Math.min(creditor.amount, debtor.amount);

    if (amount > 0.01) { // Só adiciona se valor significativo
      debts.push({
        fromMemberId: debtor.id,
        toMemberId: creditor.id,
        amount: Math.round(amount * 100) / 100
      });
    }

    creditor.amount -= amount;
    debtor.amount -= amount;

    if (creditor.amount < 0.01) creditorIdx++;
    if (debtor.amount < 0.01) debtorIdx++;
  }

  return debts;
}

/**
 * Calcula o total gasto em um evento
 */
export function calculateTotalSpent(event: SplitEvent): number {
  return event.expenses.reduce((sum, exp) => sum + exp.amount, 0);
}

/**
 * Retorna o saldo de um usuário específico no evento
 */
export function getUserBalance(event: SplitEvent, userId: string): number {
  const members = calculateMemberBalances(event);
  const user = members.find(m => m.id === userId);
  return user ? user.balance : 0;
}

/**
 * Divide valor igualmente entre membros selecionados
 */
export function splitEqually(
  totalAmount: number,
  memberIds: string[]
): Record<string, number> {
  if (memberIds.length === 0) return {};

  const perPerson = totalAmount / memberIds.length;
  const rounded = Math.floor(perPerson * 100) / 100;
  const remainder = Math.round((totalAmount - (rounded * memberIds.length)) * 100) / 100;

  const splits: Record<string, number> = {};
  memberIds.forEach((id, idx) => {
    // Dá o resto para a primeira pessoa
    splits[id] = idx === 0 ? rounded + remainder : rounded;
  });

  return splits;
}

/**
 * Recalcula splits quando um membro tem seu valor ajustado
 * O valor ajustado é fixo, o restante é redistribuído entre os outros
 */
export function redistributeSplits(
  totalAmount: number,
  currentSplits: Record<string, number>,
  fixedMemberId: string,
  fixedAmount: number,
  otherMemberIds: string[]
): Record<string, number> {
  const remaining = totalAmount - fixedAmount;
  const perOther = remaining / otherMemberIds.length;
  const rounded = Math.floor(perOther * 100) / 100;
  const remainder = Math.round((remaining - (rounded * otherMemberIds.length)) * 100) / 100;

  const newSplits: Record<string, number> = {
    [fixedMemberId]: fixedAmount
  };

  otherMemberIds.forEach((id, idx) => {
    newSplits[id] = idx === 0 ? rounded + remainder : rounded;
  });

  return newSplits;
}
