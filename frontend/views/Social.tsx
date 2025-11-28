import React, { useState } from 'react';
import { createPortal } from 'react-dom';
import { Card } from '../components/Card';
import {
  Users, Target, Share2, Trophy, Plus, LogIn, ArrowLeft, Calendar, MapPin,
  Info, CheckCircle, AlertCircle, DollarSign, X, Check, Minus, ChevronDown,
  ChevronUp, UserPlus, Receipt, LogOut, Edit3
} from 'lucide-react';
import { SplitEvent, SplitMember, SplitExpense, ExpenseSplit, DebtDetail } from '../types';
import { MOCK_SPLIT_EVENTS, AVAILABLE_FRIENDS } from '../constants';
import {
  calculateMemberBalances,
  calculateDetailedDebts,
  calculateTotalSpent,
  getUserBalance,
  splitEqually
} from '../utils/splitBillCalculator';

// --- Squad Types ---
interface SquadMember {
  id: string;
  name: string;
  avatar: string;
  savedTotal: number;
  savedThisMonth: number;
  monthlyTarget: number;
  status: 'on-track' | 'late';
}

interface SquadGoal {
  id: string;
  title: string;
  type: string;
  totalSaved: number;
  totalTarget: number;
  date: string;
  location: string;
  description: string;
  monthlyPayment: number;
  members: SquadMember[];
}

// --- Mock Data ---
const MOCK_GOAL: SquadGoal = {
  id: 'g1',
  title: 'Viagem de Verão',
  type: 'Viagem',
  totalSaved: 1450,
  totalTarget: 3000,
  date: '15 Dez 2023',
  location: 'Florianópolis, BR',
  description: 'Nossa viagem de formatura! Praia, surf e açaí. Precisamos economizar para passagens aéreas e o Airbnb.',
  monthlyPayment: 200,
  members: [
    { id: 'u1', name: 'Você', avatar: 'Alex', savedTotal: 450, savedThisMonth: 200, monthlyTarget: 200, status: 'on-track' },
    { id: 'u2', name: 'Sarah', avatar: 'Sarah', savedTotal: 400, savedThisMonth: 200, monthlyTarget: 200, status: 'on-track' },
    { id: 'u3', name: 'Mike', avatar: 'Mike', savedTotal: 300, savedThisMonth: 50, monthlyTarget: 200, status: 'late' },
    { id: 'u4', name: 'Jess', avatar: 'Jess', savedTotal: 300, savedThisMonth: 0, monthlyTarget: 200, status: 'late' },
  ]
};

const CURRENT_USER_ID = 'u1';

export const Social: React.FC = () => {
  // View states
  const [view, setView] = useState<'LIST' | 'DETAIL' | 'SPLIT_DETAIL'>('LIST');
  const [activeGoal, setActiveGoal] = useState<SquadGoal | null>(null);

  // Split Bill states
  const [splitEvents, setSplitEvents] = useState<SplitEvent[]>(MOCK_SPLIT_EVENTS);
  const [activeSplitEvent, setActiveSplitEvent] = useState<SplitEvent | null>(null);
  const [expandedMemberId, setExpandedMemberId] = useState<string | null>(null);
  const [hiddenEvents, setHiddenEvents] = useState<string[]>([]);

  // Modal states
  const [isAddExpenseOpen, setIsAddExpenseOpen] = useState(false);
  const [isCreateEventOpen, setIsCreateEventOpen] = useState(false);

  // Add Expense form states
  const [expenseDescription, setExpenseDescription] = useState('');
  const [expenseAmount, setExpenseAmount] = useState('');
  const [expensePaidBy, setExpensePaidBy] = useState(CURRENT_USER_ID);
  const [selectedMembers, setSelectedMembers] = useState<string[]>([]);
  const [splitAmounts, setSplitAmounts] = useState<Record<string, number>>({});

  // Create Event form states
  const [newEventTitle, setNewEventTitle] = useState('');
  const [newEventDate, setNewEventDate] = useState('');
  const [selectedFriends, setSelectedFriends] = useState<string[]>([]);

  // --- Handlers ---
  const handleOpenGoal = (goal: SquadGoal) => {
    setActiveGoal(goal);
    setView('DETAIL');
  };

  const handleOpenSplitEvent = (event: SplitEvent) => {
    setActiveSplitEvent(event);
    setExpandedMemberId(null);
    setView('SPLIT_DETAIL');
  };

  const handleHideEvent = (eventId: string) => {
    setHiddenEvents([...hiddenEvents, eventId]);
    setView('LIST');
    setActiveSplitEvent(null);
  };

  const resetExpenseForm = () => {
    setExpenseDescription('');
    setExpenseAmount('');
    setExpensePaidBy(CURRENT_USER_ID);
    setSelectedMembers([]);
    setSplitAmounts({});
  };

  const openAddExpenseModal = () => {
    if (activeSplitEvent) {
      const memberIds = activeSplitEvent.members.map(m => m.id);
      setSelectedMembers(memberIds);
      const amount = parseFloat(expenseAmount) || 0;
      setSplitAmounts(splitEqually(amount, memberIds));
    }
    setIsAddExpenseOpen(true);
  };

  const handleSelectAllMembers = () => {
    if (activeSplitEvent) {
      const allIds = activeSplitEvent.members.map(m => m.id);
      if (selectedMembers.length === allIds.length) {
        setSelectedMembers([]);
        setSplitAmounts({});
      } else {
        setSelectedMembers(allIds);
        const amount = parseFloat(expenseAmount) || 0;
        setSplitAmounts(splitEqually(amount, allIds));
      }
    }
  };

  const handleToggleMember = (memberId: string) => {
    let newSelected: string[];
    if (selectedMembers.includes(memberId)) {
      newSelected = selectedMembers.filter(id => id !== memberId);
    } else {
      newSelected = [...selectedMembers, memberId];
    }
    setSelectedMembers(newSelected);
    const amount = parseFloat(expenseAmount) || 0;
    setSplitAmounts(splitEqually(amount, newSelected));
  };

  const handleAmountChange = (value: string) => {
    setExpenseAmount(value);
    const amount = parseFloat(value) || 0;
    setSplitAmounts(splitEqually(amount, selectedMembers));
  };

  const handleAdjustMemberAmount = (memberId: string, delta: number) => {
    const currentAmount = splitAmounts[memberId] || 0;
    const newAmount = Math.max(0, currentAmount + delta);
    const totalAmount = parseFloat(expenseAmount) || 0;

    // Calcula quanto sobra para os outros
    const otherMembers = selectedMembers.filter(id => id !== memberId);
    const remaining = totalAmount - newAmount;

    if (remaining < 0 || otherMembers.length === 0) return;

    const perOther = remaining / otherMembers.length;
    const newSplits: Record<string, number> = { [memberId]: newAmount };

    otherMembers.forEach((id, idx) => {
      const rounded = Math.floor(perOther * 100) / 100;
      const remainder = idx === 0 ? Math.round((remaining - (rounded * otherMembers.length)) * 100) / 100 : 0;
      newSplits[id] = rounded + remainder;
    });

    setSplitAmounts(newSplits);
  };

  const handleSaveExpense = () => {
    if (!activeSplitEvent || !expenseDescription || !expenseAmount || selectedMembers.length === 0) return;

    const newExpense: SplitExpense = {
      id: `exp${Date.now()}`,
      description: expenseDescription,
      amount: parseFloat(expenseAmount),
      paidBy: expensePaidBy,
      date: new Date().toLocaleDateString('pt-BR', { day: '2-digit', month: 'short', year: 'numeric' }),
      splits: selectedMembers.map(memberId => ({
        memberId,
        amount: splitAmounts[memberId] || 0
      }))
    };

    const updatedEvent = {
      ...activeSplitEvent,
      expenses: [...activeSplitEvent.expenses, newExpense]
    };

    setSplitEvents(splitEvents.map(e => e.id === updatedEvent.id ? updatedEvent : e));
    setActiveSplitEvent(updatedEvent);
    setIsAddExpenseOpen(false);
    resetExpenseForm();
  };

  const handleCreateEvent = () => {
    if (!newEventTitle || selectedFriends.length === 0) return;

    const newEvent: SplitEvent = {
      id: `se${Date.now()}`,
      title: newEventTitle,
      date: newEventDate || new Date().toLocaleDateString('pt-BR', { day: '2-digit', month: 'short', year: 'numeric' }),
      createdBy: CURRENT_USER_ID,
      members: [
        { id: CURRENT_USER_ID, name: 'Você', avatar: 'Alex', balance: 0 },
        ...selectedFriends.map(friendId => {
          const friend = AVAILABLE_FRIENDS.find(f => f.id === friendId);
          return { id: friendId, name: friend?.name || '', avatar: friend?.avatar || '', balance: 0 };
        })
      ],
      expenses: []
    };

    setSplitEvents([...splitEvents, newEvent]);
    setIsCreateEventOpen(false);
    setNewEventTitle('');
    setNewEventDate('');
    setSelectedFriends([]);
  };

  const getAvatar = (member: { name: string; avatar: string }) => {
    return member.name === 'Você'
      ? '/assets/profilePic.png'
      : `https://api.dicebear.com/9.x/avataaars/svg?seed=${member.avatar}`;
  };

  const getMemberName = (members: SplitMember[], memberId: string) => {
    return members.find(m => m.id === memberId)?.name || 'Desconhecido';
  };

  // Filter visible events
  const visibleEvents = splitEvents.filter(e => !hiddenEvents.includes(e.id));

  // --- SPLIT_DETAIL VIEW ---
  if (view === 'SPLIT_DETAIL' && activeSplitEvent) {
    const membersWithBalances = calculateMemberBalances(activeSplitEvent);
    const detailedDebts = calculateDetailedDebts(membersWithBalances);
    const totalSpent = calculateTotalSpent(activeSplitEvent);
    const isCreator = activeSplitEvent.createdBy === CURRENT_USER_ID;

    return (
      <div className="pb-24 px-4 pt-4 space-y-5 animate-fade-in min-h-screen bg-slate-50">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setView('LIST')}
              className="bg-white border border-slate-200 p-2 rounded-full shadow-sm hover:bg-slate-50"
            >
              <ArrowLeft size={20} className="text-slate-600" />
            </button>
            <h1 className="text-xl font-black text-slate-800 tracking-tight">{activeSplitEvent.title}</h1>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => handleHideEvent(activeSplitEvent.id)}
              className="bg-white border border-slate-200 p-2 rounded-full shadow-sm hover:bg-red-50 hover:border-red-200 hover:text-red-500 transition-colors"
              title="Sair do evento"
            >
              <LogOut size={18} className="text-slate-500" />
            </button>
            {isCreator && (
              <button
                className="bg-white border border-slate-200 p-2 rounded-full shadow-sm hover:bg-slate-50"
                title="Editar evento"
              >
                <Edit3 size={18} className="text-slate-500" />
              </button>
            )}
          </div>
        </div>

        {/* Hero Card - Total */}
        <Card className="bg-gradient-to-br from-finap-primary to-teal-700 border-none text-white relative overflow-hidden shadow-lg shadow-teal-500/20 mt-2">
          <div className="absolute top-0 right-0 w-40 h-40 bg-white/10 rounded-full blur-3xl -mr-10 -mt-10 pointer-events-none"></div>

          <div className="flex flex-col items-center py-4 relative z-10">
            <div className="bg-white/20 p-3 rounded-full mb-3 backdrop-blur-sm">
              <Receipt size={32} className="text-white" />
            </div>
            <p className="text-teal-100 font-medium text-sm mb-1">Total Gasto</p>
            <h2 className="text-3xl font-black">R$ {totalSpent.toFixed(2).replace('.', ',')}</h2>
            <p className="text-xs text-teal-200 mt-2">{activeSplitEvent.date} • {activeSplitEvent.members.length} participantes</p>
          </div>
        </Card>

        {/* Action Buttons */}
        <div className="flex gap-3">
          <button
            onClick={openAddExpenseModal}
            className="flex-1 bg-finap-primary text-white font-bold py-3 px-4 rounded-xl shadow-md shadow-teal-500/20 flex items-center justify-center gap-2 active:scale-95 transition-transform"
          >
            <Plus size={18} strokeWidth={3} /> Adicionar Despesa
          </button>
          <button className="bg-white text-finap-primary border border-finap-primary font-bold py-3 px-4 rounded-xl shadow-sm flex items-center justify-center gap-2 active:scale-95 transition-transform hover:bg-teal-50">
            <UserPlus size={18} strokeWidth={2.5} />
          </button>
        </div>

        {/* Members Balance List */}
        <div>
          <h3 className="font-bold text-slate-800 mb-3 px-1">Saldos</h3>
          <div className="space-y-3">
            {membersWithBalances.map((member) => {
              const isExpanded = expandedMemberId === member.id;
              const memberDebts = detailedDebts.filter(d => d.fromMemberId === member.id || d.toMemberId === member.id);
              const isCurrentUser = member.id === CURRENT_USER_ID;
              const isPositive = member.balance >= 0;

              return (
                <div key={member.id}>
                  <Card
                    className={`mb-0 py-3 px-4 cursor-pointer transition-all ${isExpanded ? 'ring-2 ring-finap-primary/30' : ''}`}
                    onClick={() => setExpandedMemberId(isExpanded ? null : member.id)}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className="relative">
                          <div className="w-10 h-10 rounded-full overflow-hidden bg-slate-100 border border-slate-200">
                            <img src={getAvatar(member)} alt={member.name} className="w-full h-full object-cover" />
                          </div>
                          <div className={`absolute -bottom-1 -right-1 w-4 h-4 rounded-full border-2 border-white flex items-center justify-center ${isPositive ? 'bg-emerald-500' : 'bg-red-500'}`}>
                            {isPositive ? <Check size={10} className="text-white" /> : <Minus size={10} className="text-white" />}
                          </div>
                        </div>
                        <div>
                          <p className="font-bold text-slate-800 text-sm">{member.name}</p>
                          <p className="text-xs text-slate-400">
                            {isPositive ? 'Tem a receber' : 'Deve'}
                          </p>
                        </div>
                      </div>

                      <div className="flex items-center gap-2">
                        <span className={`font-bold ${isPositive ? 'text-emerald-500' : 'text-red-500'}`}>
                          {isPositive ? '+' : '-'}R$ {Math.abs(member.balance).toFixed(2).replace('.', ',')}
                        </span>
                        {memberDebts.length > 0 && (
                          <div className={`p-1 rounded-full transition-colors ${isExpanded ? 'bg-finap-primary text-white' : 'bg-slate-100 text-slate-400'}`}>
                            {isExpanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                          </div>
                        )}
                      </div>
                    </div>
                  </Card>

                  {/* Expanded Debt Details */}
                  {isExpanded && memberDebts.length > 0 && (
                    <div className="ml-6 mt-2 space-y-2 animate-fade-in">
                      {memberDebts.map((debt, idx) => {
                        const isDebtor = debt.fromMemberId === member.id;
                        const otherMember = membersWithBalances.find(m =>
                          m.id === (isDebtor ? debt.toMemberId : debt.fromMemberId)
                        );

                        return (
                          <div key={idx} className="flex items-center gap-2 text-sm text-slate-600 bg-white p-2 rounded-lg border border-slate-100">
                            <div className="w-6 h-6 rounded-full overflow-hidden bg-slate-100">
                              <img src={getAvatar(otherMember!)} alt="" className="w-full h-full object-cover" />
                            </div>
                            {isDebtor ? (
                              <span>Deve <strong className="text-red-500">R$ {debt.amount.toFixed(2).replace('.', ',')}</strong> para <strong>{otherMember?.name}</strong></span>
                            ) : (
                              <span>Recebe <strong className="text-emerald-500">R$ {debt.amount.toFixed(2).replace('.', ',')}</strong> de <strong>{otherMember?.name}</strong></span>
                            )}
                          </div>
                        );
                      })}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* Expenses List */}
        <div>
          <h3 className="font-bold text-slate-800 mb-3 px-1">Despesas ({activeSplitEvent.expenses.length})</h3>
          {activeSplitEvent.expenses.length === 0 ? (
            <Card className="mb-0 text-center py-8">
              <Receipt className="mx-auto text-slate-300 mb-2" size={32} />
              <p className="text-sm text-slate-500">Nenhuma despesa ainda</p>
            </Card>
          ) : (
            <div className="space-y-2">
              {activeSplitEvent.expenses.map((expense) => {
                const payer = activeSplitEvent.members.find(m => m.id === expense.paidBy);
                return (
                  <Card key={expense.id} className="mb-0 py-3 px-4">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className="bg-slate-100 p-2 rounded-full">
                          <Receipt size={18} className="text-slate-500" />
                        </div>
                        <div>
                          <p className="font-bold text-slate-800 text-sm">{expense.description}</p>
                          <p className="text-xs text-slate-400">
                            Pago por {payer?.name || 'Desconhecido'} • {expense.date}
                          </p>
                        </div>
                      </div>
                      <span className="font-bold text-slate-700">
                        R$ {expense.amount.toFixed(2).replace('.', ',')}
                      </span>
                    </div>
                  </Card>
                );
              })}
            </div>
          )}
        </div>

        {/* Add Expense Modal - usando Portal */}
        {isAddExpenseOpen && createPortal(
          <div
            className="fixed inset-0 z-[9999] flex items-center justify-center bg-slate-900/50 backdrop-blur-sm animate-fade-in"
            onClick={() => { setIsAddExpenseOpen(false); resetExpenseForm(); }}
          >
            <div
              className="bg-white w-[calc(100%-2rem)] max-w-md rounded-3xl shadow-2xl p-6 animate-fade-in mx-4"
              style={{ maxHeight: 'calc(100dvh - 6rem)' }}
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-black text-slate-800">Nova Despesa</h2>
                <button
                  onClick={() => { setIsAddExpenseOpen(false); resetExpenseForm(); }}
                  className="p-2 hover:bg-slate-100 rounded-full transition-colors"
                >
                  <X size={20} className="text-slate-500" />
                </button>
              </div>

              <div className="space-y-5 overflow-y-auto" style={{ maxHeight: 'calc(100dvh - 14rem)' }}>
                {/* Description */}
                <div>
                  <label className="text-xs font-bold text-slate-500 uppercase ml-1 mb-1.5 block">Descrição</label>
                  <input
                    type="text"
                    value={expenseDescription}
                    onChange={(e) => setExpenseDescription(e.target.value)}
                    placeholder="Ex: Restaurante, Uber, etc."
                    className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-finap-primary focus:ring-2 focus:ring-finap-primary/20 outline-none transition-all"
                  />
                </div>

                {/* Amount */}
                <div>
                  <label className="text-xs font-bold text-slate-500 uppercase ml-1 mb-1.5 block">Valor Total</label>
                  <div className="relative">
                    <span className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 font-bold">R$</span>
                    <input
                      type="number"
                      value={expenseAmount}
                      onChange={(e) => handleAmountChange(e.target.value)}
                      placeholder="0,00"
                      className="w-full pl-12 pr-4 py-3 rounded-xl border border-slate-200 focus:border-finap-primary focus:ring-2 focus:ring-finap-primary/20 outline-none transition-all"
                    />
                  </div>
                </div>

                {/* Who Paid */}
                <div>
                  <label className="text-xs font-bold text-slate-500 uppercase ml-1 mb-1.5 block">Quem pagou?</label>
                  <select
                    value={expensePaidBy}
                    onChange={(e) => setExpensePaidBy(e.target.value)}
                    className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-finap-primary focus:ring-2 focus:ring-finap-primary/20 outline-none transition-all bg-white"
                  >
                    {activeSplitEvent.members.map(member => (
                      <option key={member.id} value={member.id}>{member.name}</option>
                    ))}
                  </select>
                </div>

                {/* Split Among */}
                <div>
                  <label className="text-xs font-bold text-slate-500 uppercase ml-1 mb-1.5 block">Dividir entre:</label>

                  {/* Select All */}
                  <div
                    onClick={handleSelectAllMembers}
                    className="flex items-center gap-3 p-3 bg-slate-50 rounded-xl cursor-pointer hover:bg-slate-100 transition-colors mb-2"
                  >
                    <div className={`w-5 h-5 rounded border-2 flex items-center justify-center transition-colors ${
                      selectedMembers.length === activeSplitEvent.members.length
                        ? 'bg-finap-primary border-finap-primary'
                        : 'border-slate-300'
                    }`}>
                      {selectedMembers.length === activeSplitEvent.members.length && <Check size={12} className="text-white" />}
                    </div>
                    <span className="font-bold text-sm text-slate-700">Selecionar Todos</span>
                  </div>

                  {/* Individual Members */}
                  <div className="space-y-2">
                    {activeSplitEvent.members.map(member => {
                      const isSelected = selectedMembers.includes(member.id);
                      const memberAmount = splitAmounts[member.id] || 0;

                      return (
                        <div key={member.id} className="flex items-center justify-between p-3 bg-slate-50 rounded-xl">
                          <div
                            onClick={() => handleToggleMember(member.id)}
                            className="flex items-center gap-3 cursor-pointer flex-1"
                          >
                            <div className={`w-5 h-5 rounded border-2 flex items-center justify-center transition-colors ${
                              isSelected ? 'bg-finap-primary border-finap-primary' : 'border-slate-300'
                            }`}>
                              {isSelected && <Check size={12} className="text-white" />}
                            </div>
                            <div className="w-8 h-8 rounded-full overflow-hidden bg-slate-200">
                              <img src={getAvatar(member)} alt={member.name} className="w-full h-full object-cover" />
                            </div>
                            <span className="font-medium text-sm text-slate-700">{member.name}</span>
                          </div>

                          {isSelected && (
                            <div className="flex items-center gap-2">
                              <button
                                onClick={() => handleAdjustMemberAmount(member.id, -5)}
                                className="w-7 h-7 rounded-full bg-slate-200 flex items-center justify-center text-slate-600 hover:bg-slate-300 active:scale-95 transition-all"
                              >
                                <Minus size={14} />
                              </button>
                              <span className="font-bold text-sm w-20 text-center">
                                R$ {memberAmount.toFixed(2).replace('.', ',')}
                              </span>
                              <button
                                onClick={() => handleAdjustMemberAmount(member.id, 5)}
                                className="w-7 h-7 rounded-full bg-slate-200 flex items-center justify-center text-slate-600 hover:bg-slate-300 active:scale-95 transition-all"
                              >
                                <Plus size={14} />
                              </button>
                            </div>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Save Button */}
                <button
                  onClick={handleSaveExpense}
                  disabled={!expenseDescription || !expenseAmount || selectedMembers.length === 0}
                  className="w-full bg-finap-primary text-white font-bold py-3.5 rounded-xl shadow-lg shadow-teal-500/20 flex items-center justify-center gap-2 active:scale-95 transition-transform disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Check size={20} /> Salvar Despesa
                </button>
              </div>
            </div>
          </div>,
          document.body
        )}
      </div>
    );
  }

  // --- SQUAD DETAIL VIEW ---
  if (view === 'DETAIL' && activeGoal) {
    const progressPercent = Math.round((activeGoal.totalSaved / activeGoal.totalTarget) * 100);

    return (
      <div className="pb-24 px-4 pt-4 space-y-5 animate-fade-in min-h-screen bg-slate-50">
        {/* Header */}
        <div className="flex items-center gap-3">
          <button
            onClick={() => setView('LIST')}
            className="bg-white border border-slate-200 p-2 rounded-full shadow-sm hover:bg-slate-50"
          >
            <ArrowLeft size={20} className="text-slate-600" />
          </button>
          <h1 className="text-xl font-black text-slate-800 tracking-tight">{activeGoal.title}</h1>
        </div>

        {/* Hero Card */}
        <Card className="bg-gradient-to-br from-finap-primary to-teal-700 border-none text-white relative overflow-hidden shadow-lg shadow-teal-500/20 mt-2">
          <div className="absolute top-0 right-0 w-40 h-40 bg-white/10 rounded-full blur-3xl -mr-10 -mt-10 pointer-events-none"></div>

          <div className="flex flex-col items-center py-4 relative z-10">
            <div className="bg-white/20 p-3 rounded-full mb-3 backdrop-blur-sm">
              <Target size={32} className="text-white" />
            </div>
            <h2 className="text-3xl font-black mb-1">R$ {activeGoal.totalSaved}</h2>
            <p className="text-teal-100 font-medium text-sm mb-6">de R$ {activeGoal.totalTarget} meta</p>

            <div className="w-full bg-black/20 rounded-full h-3 overflow-hidden backdrop-blur-sm mb-2">
              <div
                className="bg-finap-gold h-full rounded-full shadow-[0_0_15px_rgba(251,191,36,0.6)] relative transition-all duration-1000"
                style={{ width: `${progressPercent}%` }}
              >
                <div className="absolute top-0 left-0 w-full h-full bg-white/30 animate-pulse"></div>
              </div>
            </div>
            <p className="text-xs font-bold text-teal-50">{progressPercent}% Completo</p>
          </div>
        </Card>

        {/* Info Grid */}
        <div className="grid grid-cols-2 gap-3">
          <Card className="mb-0 py-3 px-3 flex items-center gap-3 border-none shadow-sm">
            <div className="bg-blue-50 p-2 rounded-lg text-blue-500"><Calendar size={18}/></div>
            <div>
              <p className="text-[10px] text-slate-400 font-bold uppercase">Prazo</p>
              <p className="text-xs font-bold text-slate-700">{activeGoal.date}</p>
            </div>
          </Card>
          <Card className="mb-0 py-3 px-3 flex items-center gap-3 border-none shadow-sm">
            <div className="bg-red-50 p-2 rounded-lg text-red-500"><MapPin size={18}/></div>
            <div>
              <p className="text-[10px] text-slate-400 font-bold uppercase">Local</p>
              <p className="text-xs font-bold text-slate-700 truncate">{activeGoal.location}</p>
            </div>
          </Card>
        </div>

        <Card className="mb-0">
          <div className="flex items-start gap-3">
            <Info className="text-slate-400 mt-0.5 shrink-0" size={18} />
            <p className="text-sm text-slate-600 leading-relaxed">{activeGoal.description}</p>
          </div>
        </Card>

        {/* Monthly Target Info */}
        <Card className="bg-slate-800 text-white border-none">
          <div className="flex justify-between items-center">
            <div>
              <p className="text-slate-400 text-xs font-medium mb-1">Contribuição Mensal</p>
              <p className="text-xl font-bold text-finap-secondary">R$ {activeGoal.monthlyPayment},00 <span className="text-xs text-slate-400 font-normal">/ pessoa</span></p>
            </div>
            <div className="bg-white/10 p-2 rounded-full">
              <DollarSign size={20} className="text-finap-gold" />
            </div>
          </div>
        </Card>

        {/* Members Status List */}
        <div>
          <h3 className="font-bold text-slate-800 mb-3 px-1">Status do Squad (Este Mês)</h3>
          <div className="space-y-3">
            {activeGoal.members.map((member) => {
              const isOnTrack = member.status === 'on-track';
              const isCurrentUser = member.name === 'Você';
              return (
                <Card key={member.id} className="mb-0 py-3 px-4 flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="relative">
                      <div className="w-10 h-10 rounded-full overflow-hidden bg-slate-100 border border-slate-200">
                        <img
                          src={isCurrentUser ? '/assets/profilePic.png' : `https://api.dicebear.com/9.x/avataaars/svg?seed=${member.avatar}`}
                          alt={member.name}
                          className="w-full h-full object-cover"
                        />
                      </div>
                      <div className={`absolute -bottom-1 -right-1 w-4 h-4 rounded-full border-2 border-white flex items-center justify-center ${isOnTrack ? 'bg-finap-success' : 'bg-red-500'}`}>
                        {isOnTrack ? <CheckCircle size={10} className="text-white" /> : <AlertCircle size={10} className="text-white" />}
                      </div>
                    </div>
                    <div>
                      <p className="font-bold text-slate-800 text-sm">{member.name}</p>
                      <p className="text-xs text-slate-500">Economizado: R$ {member.savedThisMonth} / {member.monthlyTarget}</p>
                    </div>
                  </div>

                  <div className={`px-2 py-1 rounded-md text-[10px] font-bold border ${
                    isOnTrack
                      ? 'bg-emerald-50 text-emerald-600 border-emerald-100'
                      : 'bg-red-50 text-red-600 border-red-100'
                  }`}>
                    {isOnTrack ? 'COMPLETO' : 'PENDENTE'}
                  </div>
                </Card>
              );
            })}
          </div>
        </div>
      </div>
    );
  }

  // --- LIST VIEW ---
  return (
    <div className="pb-24 px-4 pt-4 space-y-6 animate-fade-in">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-black text-slate-800 tracking-tight">FINAP Squad</h1>
        <button className="text-slate-400 hover:text-finap-primary transition-colors">
          <Share2 size={20} />
        </button>
      </div>

      {/* Action Buttons */}
      <div className="flex gap-3">
        <button className="flex-1 bg-finap-primary text-white font-bold py-3 px-4 rounded-xl shadow-md shadow-teal-500/20 flex items-center justify-center gap-2 active:scale-95 transition-transform">
          <Plus size={18} strokeWidth={3} /> Criar Objetivo
        </button>
        <button className="flex-1 bg-white text-finap-primary border border-finap-primary font-bold py-3 px-4 rounded-xl shadow-sm flex items-center justify-center gap-2 active:scale-95 transition-transform hover:bg-teal-50">
          <LogIn size={18} strokeWidth={3} /> Entrar
        </button>
      </div>

      {/* Active Squad Goal (Clickable) */}
      <div onClick={() => handleOpenGoal(MOCK_GOAL)} className="cursor-pointer group">
        <Card className="bg-gradient-to-br from-finap-primary to-teal-700 border-none text-white relative overflow-hidden transition-transform group-hover:scale-[1.02] group-active:scale-95">
          <div className="absolute top-0 right-0 w-32 h-32 bg-white/5 rounded-full blur-2xl -mr-10 -mt-10 pointer-events-none"></div>

          <div className="flex items-center gap-3 mb-6 relative z-10">
            <div className="bg-white/20 p-2.5 rounded-xl backdrop-blur-sm group-hover:bg-white/30 transition-colors">
              <Target className="text-white" size={24} />
            </div>
            <div>
              <h3 className="font-bold text-lg leading-tight">{MOCK_GOAL.title}</h3>
              <p className="text-xs text-teal-100 font-medium">Objetivo do Squad • {MOCK_GOAL.members.length} Membros</p>
            </div>
          </div>

          <div className="space-y-3 relative z-10">
            <div className="flex justify-between text-xs font-bold uppercase tracking-wide text-teal-100">
              <span>R$ {MOCK_GOAL.totalSaved} economizados</span>
              <span>Meta: R$ {MOCK_GOAL.totalTarget}</span>
            </div>
            <div className="w-full bg-black/20 rounded-full h-2.5 overflow-hidden backdrop-blur-sm">
              <div className="bg-finap-gold h-full rounded-full w-[48%] shadow-[0_0_12px_rgba(251,191,36,0.6)] relative">
                <div className="absolute top-0 left-0 w-full h-full bg-white/20 animate-pulse"></div>
              </div>
            </div>
            <div className="flex items-center justify-between pt-1">
              <div className="flex -space-x-2">
                {MOCK_GOAL.members.map((m, i) => {
                  const isCurrentUser = m.name === 'Você';
                  return (
                    <div key={i} className="w-8 h-8 rounded-full border-2 border-teal-600 bg-slate-200 overflow-hidden">
                      <img
                        src={isCurrentUser ? '/assets/profilePic.png' : `https://api.dicebear.com/9.x/avataaars/svg?seed=${m.avatar}`}
                        alt={m.name}
                        className="w-full h-full object-cover"
                      />
                    </div>
                  );
                })}
              </div>
              <span className="text-xs font-bold text-teal-200 bg-white/10 px-2 py-1 rounded-md">Toque para ver detalhes</span>
            </div>
          </div>
        </Card>
      </div>

      {/* Leaderboard Preview */}
      <div>
        <h2 className="font-bold text-slate-800 mb-4 flex items-center gap-2">
          <Trophy className="text-finap-gold fill-finap-gold" size={20} /> Ranking Semanal
        </h2>
        <div className="space-y-2">
          {[
            { name: 'Você', score: 1250, rank: 1 },
            { name: 'Sarah', score: 1100, rank: 2 },
            { name: 'Mike', score: 950, rank: 3 },
          ].map((user) => (
            <Card key={user.rank} className="py-3 px-4 mb-0 flex items-center justify-between hover:bg-slate-50 transition-colors group">
              <div className="flex items-center gap-4">
                <span className={`font-black text-lg w-6 text-center ${user.rank === 1 ? 'text-finap-gold' : 'text-slate-300 group-hover:text-finap-primary'}`}>
                  {user.rank}
                </span>
                <div className="font-bold text-finap-dark">{user.name}</div>
              </div>
              <div className="font-bold text-slate-500 text-sm group-hover:text-finap-primary transition-colors">{user.score} XP</div>
            </Card>
          ))}
        </div>
      </div>

      {/* Split Bill Section */}
      <Card
        title="Dividir Conta"
        action={
          <button
            onClick={() => setIsCreateEventOpen(true)}
            className="text-finap-primary text-xs font-bold bg-teal-50 px-2 py-1 rounded-md hover:bg-teal-100 transition-colors"
          >
            Novo
          </button>
        }
      >
        {visibleEvents.length === 0 ? (
          <div className="text-center py-6">
            <div className="bg-slate-50 w-14 h-14 rounded-full flex items-center justify-center mx-auto mb-3 border border-slate-100">
              <Users className="text-slate-300" />
            </div>
            <p className="text-sm text-slate-500 font-medium">Nenhuma divisão ativa. Sair com os amigos?</p>
          </div>
        ) : (
          <div className="space-y-3">
            {visibleEvents.map(event => {
              const userBalance = getUserBalance(event, CURRENT_USER_ID);
              const isPositive = userBalance >= 0;

              return (
                <div
                  key={event.id}
                  onClick={() => handleOpenSplitEvent(event)}
                  className="flex items-center justify-between p-3 bg-slate-50 rounded-xl cursor-pointer hover:bg-slate-100 transition-colors active:scale-[0.98]"
                >
                  <div className="flex items-center gap-3">
                    <div className={`p-2 rounded-full ${isPositive ? 'bg-emerald-100' : 'bg-red-100'}`}>
                      <Users size={20} className={isPositive ? 'text-emerald-600' : 'text-red-600'} />
                    </div>
                    <div>
                      <p className="font-bold text-slate-800 text-sm">{event.title}</p>
                      <p className="text-xs text-slate-400">{event.date} • {event.members.length} pessoas</p>
                    </div>
                  </div>
                  <span className={`font-bold text-sm ${isPositive ? 'text-emerald-500' : 'text-red-500'}`}>
                    {isPositive ? '+' : ''}R$ {userBalance.toFixed(2).replace('.', ',')}
                  </span>
                </div>
              );
            })}
          </div>
        )}
      </Card>

      {/* Create Event Modal - usando Portal */}
      {isCreateEventOpen && createPortal(
        <div
          className="fixed inset-0 z-[9999] flex items-center justify-center bg-slate-900/50 backdrop-blur-sm animate-fade-in"
          onClick={() => { setIsCreateEventOpen(false); setNewEventTitle(''); setNewEventDate(''); setSelectedFriends([]); }}
        >
          <div
            className="bg-white w-[calc(100%-2rem)] max-w-md rounded-3xl shadow-2xl p-6 animate-fade-in mx-4"
            style={{ maxHeight: 'calc(100dvh - 6rem)' }}
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-black text-slate-800">Novo Evento</h2>
              <button
                onClick={() => { setIsCreateEventOpen(false); setNewEventTitle(''); setNewEventDate(''); setSelectedFriends([]); }}
                className="p-2 hover:bg-slate-100 rounded-full transition-colors"
              >
                <X size={20} className="text-slate-500" />
              </button>
            </div>

            <div className="space-y-5 overflow-y-auto" style={{ maxHeight: 'calc(100dvh - 14rem)' }}>
              {/* Event Name */}
              <div>
                <label className="text-xs font-bold text-slate-500 uppercase ml-1 mb-1.5 block">Nome do Evento</label>
                <input
                  type="text"
                  value={newEventTitle}
                  onChange={(e) => setNewEventTitle(e.target.value)}
                  placeholder="Ex: Viagem de Juquey, Churrasco, etc."
                  className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-finap-primary focus:ring-2 focus:ring-finap-primary/20 outline-none transition-all"
                />
              </div>

              {/* Date */}
              <div>
                <label className="text-xs font-bold text-slate-500 uppercase ml-1 mb-1.5 block">Data</label>
                <input
                  type="date"
                  value={newEventDate}
                  onChange={(e) => setNewEventDate(e.target.value)}
                  className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-finap-primary focus:ring-2 focus:ring-finap-primary/20 outline-none transition-all"
                />
              </div>

              {/* Select Friends */}
              <div>
                <label className="text-xs font-bold text-slate-500 uppercase ml-1 mb-1.5 block">Convidar Amigos</label>
                <div className="space-y-2">
                  {AVAILABLE_FRIENDS.map(friend => {
                    const isSelected = selectedFriends.includes(friend.id);

                    return (
                      <div
                        key={friend.id}
                        onClick={() => {
                          if (isSelected) {
                            setSelectedFriends(selectedFriends.filter(id => id !== friend.id));
                          } else {
                            setSelectedFriends([...selectedFriends, friend.id]);
                          }
                        }}
                        className="flex items-center gap-3 p-3 bg-slate-50 rounded-xl cursor-pointer hover:bg-slate-100 transition-colors"
                      >
                        <div className={`w-5 h-5 rounded border-2 flex items-center justify-center transition-colors ${
                          isSelected ? 'bg-finap-primary border-finap-primary' : 'border-slate-300'
                        }`}>
                          {isSelected && <Check size={12} className="text-white" />}
                        </div>
                        <div className="w-8 h-8 rounded-full overflow-hidden bg-slate-200">
                          <img
                            src={`https://api.dicebear.com/9.x/avataaars/svg?seed=${friend.avatar}`}
                            alt={friend.name}
                            className="w-full h-full object-cover"
                          />
                        </div>
                        <span className="font-medium text-sm text-slate-700">{friend.name}</span>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Create Button */}
              <button
                onClick={handleCreateEvent}
                disabled={!newEventTitle || selectedFriends.length === 0}
                className="w-full bg-finap-primary text-white font-bold py-3.5 rounded-xl shadow-lg shadow-teal-500/20 flex items-center justify-center gap-2 active:scale-95 transition-transform disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Plus size={20} /> Criar Evento
              </button>
            </div>
          </div>
        </div>,
        document.body
      )}
    </div>
  );
};
