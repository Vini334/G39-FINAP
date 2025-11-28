import React, { useState, useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';
import { Card } from '../components/Card';
import { Transaction } from '../types';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import { ArrowDownRight, ArrowUpRight, Filter, Plus, Trash2, X, Check, DollarSign, Loader } from 'lucide-react';
import { transactionService, missionService } from '../services';
import { useToast } from '../components/Toast';
import { useAuth } from '../contexts/AuthContext';

interface ExtractProps {}

// WhatsApp SVG Icon Component
const WhatsAppIcon = () => (
  <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" className="mr-2">
    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
  </svg>
);

export const Extract: React.FC<ExtractProps> = () => {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState('Este Mês');
  const [isDeleteMode, setIsDeleteMode] = useState(false);
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const { showToast, ToastComponent } = useToast();
  const { user } = useAuth();
  const viewReportTriggered = useRef(false);

  // New Transaction Form State
  const [newTx, setNewTx] = useState({
    desc: '',
    amount: '',
    type: 'expense' as 'expense' | 'income',
    category: 'Outros'
  });

  useEffect(() => {
    loadTransactions();

    // Trigger VIEW_REPORT mission on first mount
    if (user?.uid && !viewReportTriggered.current) {
      viewReportTriggered.current = true;
      missionService.triggerViewReport(user.uid).catch(console.error);
    }

    // Reload data when window/tab gets focus (user returns to the tab)
    const handleFocus = () => {
      loadTransactions();
    };

    window.addEventListener('focus', handleFocus);

    return () => {
      window.removeEventListener('focus', handleFocus);
    };
  }, [user?.uid]);

  const loadTransactions = async () => {
    try {
      setLoading(true);

      // Get transactions from last 30 days to match Overview period
      const now = new Date();
      const thirtyDaysAgo = new Date();
      thirtyDaysAgo.setDate(now.getDate() - 30);

      const data = await transactionService.getTransactions({
        limit: 50,
        offset: 0,
        start_date: thirtyDaysAgo.toISOString(),
        end_date: now.toISOString()
      });
      setTransactions(data.transactions);
    } catch (error: any) {
      console.error('Erro ao carregar transações:', error);
      showToast(error.message || 'Erro ao carregar transações', 'error');
    } finally {
      setLoading(false);
    }
  };

  // Update pie chart data based on current transactions
  const calculateChartData = () => {
    const expenses = transactions.filter(t => t.type === 'expense');
    const categories = ['Alimentação', 'Transporte', 'Lazer', 'Educação', 'Outros'];
    const colors = ['#F97316', '#14B8A6', '#2DD4BF', '#0D9488', '#94A3B8'];
    
    return categories.map((cat, index) => ({
      name: cat,
      value: expenses.filter(t => t.category === cat).reduce((acc, curr) => acc + curr.amount, 0),
      color: colors[index]
    })).filter(item => item.value > 0);
  };

  const [data, setData] = useState(calculateChartData());

  useEffect(() => {
    setData(calculateChartData());
  }, [transactions]);

  const handleAddTransaction = async () => {
    if (!newTx.desc || !newTx.amount) return;

    try {
      await transactionService.createTransaction({
        description: newTx.desc,
        amount: parseFloat(newTx.amount),
        category: newTx.category as any,
        date: new Date().toISOString(),
        type: newTx.type
      });

      // Trigger ADD_TRANSACTION mission
      if (user?.uid) {
        missionService.triggerAddTransaction(user.uid).catch(console.error);
      }

      // Reload all transactions from server to ensure consistency
      await loadTransactions();

      setIsAddModalOpen(false);
      setNewTx({ desc: '', amount: '', type: 'expense', category: 'Outros' });
      showToast('Transação criada com sucesso!', 'success');
    } catch (error: any) {
      console.error('Erro ao criar transação:', error);
      showToast(error.message || 'Erro ao criar transação', 'error');
    }
  };

  const handleDeleteTransaction = async (id: string) => {
    try {
      await transactionService.deleteTransaction(id);

      // Reload all transactions from server to ensure consistency
      await loadTransactions();

      showToast('Transação excluída com sucesso!', 'success');
    } catch (error: any) {
      console.error('Erro ao deletar transação:', error);
      showToast(error.message || 'Erro ao deletar transação', 'error');
    }
  };

  const totalSpent = transactions
    .filter(t => t.type === 'expense')
    .reduce((acc, curr) => acc + curr.amount, 0);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <Loader className="w-12 h-12 text-finap-primary animate-spin mx-auto mb-4" />
          <p className="text-gray-600">Carregando transações...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="pb-24 px-4 pt-4 space-y-4 animate-fade-in relative">

      {/* Header */}
      <div className="flex justify-between items-center mb-2">
        <h1 className="text-2xl font-black text-slate-800 tracking-tight">Análise</h1>
        <button className="bg-white border border-slate-200 p-2 rounded-full shadow-sm text-slate-600 hover:bg-slate-50 transition-colors">
           <Filter size={20} />
        </button>
      </div>

      {/* WhatsApp Integration Button */}
      <button className="w-full bg-[#25D366] text-white font-bold py-3 px-4 rounded-xl shadow-md shadow-green-500/20 flex items-center justify-center transition-transform active:scale-95 hover:bg-[#20bd5a]">
        <WhatsAppIcon />
        Conectar WhatsApp
      </button>

      {/* Chart Card */}
      <Card title="Divisão de Gastos">
        {data.length > 0 ? (
          <>
            <div className="h-64 w-full" style={{ minHeight: '256px', minWidth: '100%', position: 'relative' }}>
              <ResponsiveContainer width="100%" height={256} minWidth={300}>
                <PieChart>
                  <Pie
                    data={data}
                    cx="50%"
                    cy="50%"
                    innerRadius={65}
                    outerRadius={85}
                    paddingAngle={5}
                    dataKey="value"
                    stroke="none"
                    cornerRadius={4}
                  >
                    {data.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip contentStyle={{ borderRadius: '12px', border: '1px solid #e2e8f0', boxShadow: '0 4px 12px rgba(0,0,0,0.05)' }} />
                  <Legend verticalAlign="bottom" height={36} iconType="circle" />
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div className="text-center mt-2">
              <p className="text-xs text-slate-400 font-medium uppercase tracking-wider">Total Gasto</p>
              <p className="text-2xl font-black text-finap-dark">R$ {totalSpent.toFixed(2)}</p>
            </div>
          </>
        ) : (
          <div className="h-64 flex flex-col items-center justify-center text-center py-10">
            <p className="text-slate-400 font-medium mb-2">Nenhuma despesa ainda</p>
            <p className="text-xs text-slate-300">Adicione uma transação para ver o gráfico</p>
          </div>
        )}
      </Card>

      {/* Action Buttons (Insert / Delete) */}
      <div className="flex gap-3">
        <button 
          onClick={() => setIsAddModalOpen(true)}
          className="flex-1 bg-finap-primary text-white font-bold py-3 px-4 rounded-xl shadow-md shadow-teal-500/20 flex items-center justify-center gap-2 active:scale-95 transition-transform"
        >
          <Plus size={20} /> Inserir
        </button>
        
        <button 
          onClick={() => setIsDeleteMode(!isDeleteMode)}
          className={`flex-1 font-bold py-3 px-4 rounded-xl shadow-sm border flex items-center justify-center gap-2 active:scale-95 transition-all ${
            isDeleteMode 
              ? 'bg-red-500 text-white border-red-500' 
              : 'bg-white text-red-500 border-red-100 hover:bg-red-50'
          }`}
        >
          {isDeleteMode ? <Check size={20} /> : <Trash2 size={20} />}
          {isDeleteMode ? 'Concluir' : 'Excluir'}
        </button>
      </div>

      {/* Add Transaction Modal - usando Portal para renderizar fora do container */}
      {isAddModalOpen && createPortal(
        <div
          className="fixed inset-0 z-[9999] flex items-center justify-center bg-slate-900/50 backdrop-blur-sm animate-fade-in"
          onClick={() => setIsAddModalOpen(false)}
        >
          <div
            className="bg-white w-[calc(100%-2rem)] max-w-md rounded-3xl shadow-2xl p-6 animate-fade-in mx-4"
            style={{ maxHeight: 'calc(100dvh - 6rem)' }}
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xl font-black text-slate-800">Nova Transação</h3>
              <button onClick={() => setIsAddModalOpen(false)} className="p-2 rounded-full hover:bg-slate-100 text-slate-500">
                <X size={20} />
              </button>
            </div>

            <div className="space-y-4 overflow-y-auto" style={{ maxHeight: 'calc(100dvh - 14rem)' }}>
              {/* Type Toggle */}
              <div className="flex bg-slate-100 p-1 rounded-xl">
                <button
                  onClick={() => setNewTx({...newTx, type: 'expense'})}
                  className={`flex-1 py-2 rounded-lg text-sm font-bold transition-all ${newTx.type === 'expense' ? 'bg-white text-red-500 shadow-sm' : 'text-slate-500'}`}
                >
                  Despesa
                </button>
                <button
                  onClick={() => setNewTx({...newTx, type: 'income'})}
                  className={`flex-1 py-2 rounded-lg text-sm font-bold transition-all ${newTx.type === 'income' ? 'bg-white text-emerald-500 shadow-sm' : 'text-slate-500'}`}
                >
                  Receita
                </button>
              </div>

              <div>
                <label className="text-xs font-bold text-slate-500 uppercase ml-1">Descrição</label>
                <input
                  type="text"
                  value={newTx.desc}
                  onChange={(e) => setNewTx({...newTx, desc: e.target.value})}
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl p-3 mt-1 font-medium outline-none focus:border-finap-primary"
                  placeholder="ex: Burger King"
                />
              </div>

              <div>
                <label className="text-xs font-bold text-slate-500 uppercase ml-1">Valor (R$)</label>
                <div className="relative">
                  <DollarSign size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                  <input
                    type="number"
                    value={newTx.amount}
                    onChange={(e) => setNewTx({...newTx, amount: e.target.value})}
                    className="w-full bg-slate-50 border border-slate-200 rounded-xl p-3 pl-9 mt-1 font-medium outline-none focus:border-finap-primary"
                    placeholder="0.00"
                  />
                </div>
              </div>

              <div>
                <label className="text-xs font-bold text-slate-500 uppercase ml-1">Categoria</label>
                <select
                  value={newTx.category}
                  onChange={(e) => setNewTx({...newTx, category: e.target.value})}
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl p-3 mt-1 font-medium outline-none focus:border-finap-primary"
                >
                  <option value="Alimentação">Alimentação</option>
                  <option value="Transporte">Transporte</option>
                  <option value="Lazer">Lazer</option>
                  <option value="Educação">Educação</option>
                  <option value="Outros">Outros</option>
                </select>
              </div>

              <button
                onClick={handleAddTransaction}
                className="w-full bg-finap-primary text-white font-bold py-4 rounded-xl shadow-lg shadow-teal-500/20 mt-2 active:scale-95 transition-transform"
              >
                Salvar Transação
              </button>
            </div>
          </div>
        </div>,
        document.body
      )}

      {/* Transactions List */}
      <div>
         <div className="flex gap-2 mb-4 overflow-x-auto no-scrollbar">
            {['Este Mês', 'Últimos 6 Meses', 'Último Ano'].map(range => (
               <button 
                  key={range}
                  onClick={() => setTimeRange(range)}
                  className={`whitespace-nowrap px-4 py-2 rounded-full text-xs font-bold transition-all ${
                      timeRange === range 
                      ? 'bg-finap-primary text-white shadow-lg shadow-teal-500/20' 
                      : 'bg-white text-slate-500 hover:bg-slate-50 border border-slate-200'
                  }`}
               >
                  {range}
               </button>
            ))}
         </div>

         <div className="space-y-3">
            {transactions.map((t) => (
               <div key={t.id} className="relative group">
                 <Card className={`py-4 px-4 mb-0 flex justify-between items-center transition-all ${isDeleteMode ? 'border-red-200 bg-red-50 cursor-pointer' : 'hover:bg-slate-50'}`}
                   onClick={() => isDeleteMode && handleDeleteTransaction(t.id)}
                 >
                    <div className="flex items-center gap-4">
                       <div className={`p-2.5 rounded-full transition-colors ${
                         isDeleteMode 
                           ? 'bg-red-100 text-red-500' 
                           : (t.type === 'expense' ? 'bg-red-50 text-red-500' : 'bg-emerald-50 text-emerald-500')
                       }`}>
                          {isDeleteMode ? <Trash2 size={20} /> : (t.type === 'expense' ? <ArrowDownRight size={20} /> : <ArrowUpRight size={20} />)}
                       </div>
                       <div>
                          <p className={`font-bold text-sm ${isDeleteMode ? 'text-red-700' : 'text-finap-dark'}`}>{t.description}</p>
                          <p className={`text-xs font-medium ${isDeleteMode ? 'text-red-400' : 'text-slate-400'}`}>{t.category} • {t.date}</p>
                       </div>
                    </div>
                    <span className={`font-bold ${isDeleteMode ? 'text-red-500 decoration-red-500 line-through' : (t.type === 'expense' ? 'text-red-500' : 'text-emerald-500')}`}>
                       {t.type === 'expense' ? '-' : '+'} R$ {t.amount.toFixed(2)}
                    </span>
                 </Card>
               </div>
            ))}
            
            {transactions.length === 0 && (
               <div className="text-center py-10 opacity-50">
                  <p className="text-slate-400 font-medium">Nenhuma transação encontrada.</p>
               </div>
            )}
         </div>
      </div>

      {/* Toast Notifications */}
      {ToastComponent}
    </div>
  );
};