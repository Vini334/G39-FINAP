import React, { useState, useEffect } from 'react';
import { Card } from '../components/Card';
import { FimMascot } from '../components/FimMascot';
import { UserStats, Mission, ViewState } from '../types';
import { LearningProgress } from '../types/api';
import { Zap, Heart, Coins, Flame, PlayCircle, ArrowRight, Loader } from 'lucide-react';
import { dashboardService } from '../services';
import { useToast } from '../components/Toast';
import { useAuth } from '../contexts/AuthContext';
import { useGamification } from '../contexts/GamificationContext';

interface OverviewProps {
  onNavigate: (view: ViewState) => void;
}

interface OverviewData {
  stats: UserStats;
  missions: Mission[];
  balance: {
    current: number;
    spent_this_month: number;
    monthly_budget: number;
    budget_percentage: number;
  };
  budget_alert: {
    show: boolean;
    percentage: number;
    message: string;
  };
  learning_progress?: LearningProgress;
}

export const Overview: React.FC<OverviewProps> = ({ onNavigate }) => {
  const [data, setData] = useState<OverviewData | null>(null);
  const [loading, setLoading] = useState(true);
  const [userName, setUserName] = useState<string>('');
  const { showToast, ToastComponent } = useToast();
  const { user } = useAuth();
  const { stats: gamificationStats, refreshStats } = useGamification();

  useEffect(() => {
    if (user) {
      loadOverviewData();
    }

    // Reload data when window/tab gets focus (user returns to the tab)
    const handleFocus = () => {
      if (user) {
        loadOverviewData();
      }
    };

    window.addEventListener('focus', handleFocus);

    return () => {
      window.removeEventListener('focus', handleFocus);
    };
  }, [user?.uid]);

  const loadOverviewData = async () => {
    try {
      setLoading(true);

      if (!user) {
        showToast('Usuário não autenticado', 'error');
        onNavigate(ViewState.LOGIN);
        return;
      }

      const overview = await dashboardService.getOverview(user.uid);

      setData({
        stats: overview.stats,
        missions: overview.missions,
        balance: overview.balance,
        budget_alert: overview.budget_alert,
        learning_progress: overview.learning_progress
      });

      // Get user's first name
      const firstName = user.name?.split(' ')[0] || 'Usuário';
      setUserName(firstName);
    } catch (error: any) {
      console.error('Erro ao carregar overview:', error);
      showToast(error.message || 'Erro ao carregar dados', 'error');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <Loader className="w-12 h-12 text-finap-primary animate-spin mx-auto mb-4" />
          <p className="text-gray-600">Carregando...</p>
        </div>
      </div>
    );
  }

  if (!data) {
    return null;
  }

  const { missions, balance, budget_alert, learning_progress } = data;
  // Use gamification stats from context for consistency across the app
  const stats = gamificationStats;
  const spendingPercentage = balance && balance.monthly_budget > 0
    ? (balance.spent_this_month / balance.monthly_budget) * 100
    : 0;

  // Handle continue course navigation
  const handleContinueCourse = () => {
    // Store the module_id to open directly in Learn view
    if (learning_progress?.module_id) {
      sessionStorage.setItem('openModuleId', learning_progress.module_id);
    }
    onNavigate(ViewState.LEARN);
  };

  return (
    <div className="pb-24 px-4 pt-4 animate-fade-in space-y-5">

      {/* Top Stats Bar - Clean white pill */}
      <div className="flex justify-between items-center bg-white border border-slate-200 p-2 rounded-full shadow-sm mb-4">
        <div className="flex items-center gap-1 px-3">
           <Heart className="text-red-500 fill-red-500" size={18} />
           <span className="font-bold text-slate-700 text-sm">{stats.lives}</span>
        </div>
        <div className="flex items-center gap-1 px-3 border-l border-r border-slate-100">
           <Flame className="text-orange-500 fill-orange-500" size={18} />
           <span className="font-bold text-slate-700 text-sm">{stats.streak}</span>
        </div>
        <div className="flex items-center gap-1 px-3">
           <Coins className="text-finap-gold fill-finap-gold" size={18} />
           <span className="font-bold text-slate-700 text-sm">{stats.coins}</span>
        </div>
      </div>

      {/* Welcome / Profile Header */}
      <div className="flex items-center justify-between mb-6">
         <div>
            <h1 className="text-2xl font-black text-slate-800 tracking-tight">E aí, {userName}! 👋</h1>
            <div className="flex items-center gap-3 mt-2">
               <div className="h-2 w-32 bg-slate-200 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-finap-primary shadow-md transition-all duration-300"
                    style={{ width: `${stats.xp % 100}%` }}
                  ></div>
               </div>
               <span className="text-xs font-bold text-finap-primary">Lvl {stats.level}</span>
               <span className="text-[10px] text-slate-400">{stats.xp % 100}/100 XP</span>
            </div>
         </div>

         {/* Profile Button */}
         <button
           onClick={() => onNavigate(ViewState.PROFILE)}
           className="relative group"
         >
            <div className="w-14 h-14 rounded-full border-2 border-white shadow-md overflow-hidden bg-indigo-100 relative z-10 group-active:scale-95 transition-transform">
               <img
                  src={user?.profile?.avatar_url || '/assets/profilePic.png'}
                  alt="Profile"
                  className="w-full h-full object-cover"
               />
            </div>
            <div className="absolute -bottom-1 -right-1 bg-finap-primary text-white text-[10px] font-bold px-1.5 py-0.5 rounded-full z-20 border border-white">
               ME
            </div>
         </button>
      </div>

      {/* Alert Card - Always visible for MVP demo */}
      <Card className="border-l-4 border-l-finap-alert bg-orange-50/50">
        <div className="flex gap-4 items-start">
           <FimMascot size="sm" emotion="worried" />
           <div>
              <h3 className="font-bold text-finap-alert mb-1 text-base">Alerta de Orçamento</h3>
              <p className="text-sm text-slate-600 leading-relaxed">
                {budget_alert?.message || "Você já gastou 35% do seu saldo em Alimentação! Tá na hora de dar uma segurada nos gastos, mano."}
              </p>
           </div>
        </div>
      </Card>

      {/* Balance Card */}
      <Card title="Saldo Atual">
         <div className="flex flex-col items-center py-2">
            <div className="text-4xl font-black text-finap-dark mb-2 tracking-tight">
              R$ {balance ? balance.current.toFixed(2).replace('.', ',') : '0,00'}
            </div>
            <p className="text-xs font-medium text-slate-400 uppercase tracking-wide mb-5">Saldo Restante</p>

            {/* Visual Progress - Barra mostra quanto foi gasto do limite */}
            <div className="w-full bg-slate-100 rounded-full h-4 relative overflow-hidden">
               <div
                 className={`absolute top-0 left-0 h-full flex items-center justify-center transition-all ${
                   spendingPercentage >= 100 ? 'bg-red-500' :
                   spendingPercentage >= 80 ? 'bg-orange-500' :
                   'bg-finap-primary'
                 }`}
                 style={{ width: `${Math.min(spendingPercentage, 100)}%` }}
               >
               </div>
            </div>
            <div className="flex justify-between w-full text-xs mt-3 font-medium text-slate-500">
               <span>Gasto: <span className="text-slate-800">R$ {balance ? balance.spent_this_month.toFixed(2).replace('.', ',') : '0,00'}</span></span>
               <span>Limite: <span className="text-slate-800">R$ {balance ? balance.monthly_budget.toFixed(2).replace('.', ',') : '0,00'}</span></span>
            </div>
         </div>
      </Card>

      {/* Continue Learning - Gradient Card */}
      <Card className="bg-gradient-to-br from-finap-primary to-teal-700 border-none text-white relative overflow-hidden p-0 shadow-lg shadow-teal-500/20">
         {/* Background decorations */}
         <div className="absolute top-0 right-0 w-40 h-40 bg-white/10 rounded-full blur-2xl -mr-10 -mt-10 pointer-events-none"></div>
         <div className="absolute bottom-0 left-0 w-20 h-20 bg-white/10 rounded-full blur-xl -ml-5 -mb-5 pointer-events-none"></div>

         <div className="p-5 relative z-10">
            <div className="flex justify-between items-start mb-4">
               <div>
                  <span className="text-xs font-bold text-teal-100 uppercase tracking-wider mb-1 block">Em Progresso</span>
                  <h3 className="font-bold text-lg leading-tight">
                    {learning_progress?.module_title || 'Mentalidade Financeira'}
                  </h3>
               </div>
               <div className="bg-white/20 p-2 rounded-full backdrop-blur-md">
                  <PlayCircle className="text-white" size={24} fill="rgba(255,255,255,0.2)" />
               </div>
            </div>

            <div className="space-y-2">
               <div className="flex justify-between text-xs font-medium text-teal-100">
                  <span>Fase {learning_progress?.current_phase ?? 0}/{learning_progress?.total_phases ?? 4}</span>
                  <span className="font-bold text-white">{learning_progress?.progress_percentage ?? 0}%</span>
               </div>
               <div className="w-full bg-black/20 rounded-full h-2 overflow-hidden backdrop-blur-sm">
                  <div
                    className="bg-finap-gold h-full rounded-full shadow-[0_0_10px_rgba(251,191,36,0.5)] relative transition-all duration-500"
                    style={{ width: `${learning_progress?.progress_percentage ?? 0}%` }}
                  >
                     <div className="absolute top-0 left-0 w-full h-full bg-white/30 animate-pulse"></div>
                  </div>
               </div>
            </div>
         </div>
         <div
           onClick={handleContinueCourse}
           className="bg-black/10 px-5 py-2 flex justify-between items-center cursor-pointer hover:bg-black/20 transition-colors"
         >
            <span className="text-xs font-bold text-teal-50">
              {learning_progress?.progress_percentage === 0 ? 'Começar Curso' : 'Continuar Curso'}
            </span>
            <ArrowRight size={14} className="text-white" />
         </div>
      </Card>

      {/* Daily Missions */}
      <div>
        <h2 className="text-lg font-bold text-slate-800 mb-3 flex items-center gap-2">
          <Zap size={20} className="text-finap-gold fill-finap-gold" /> Missões Diárias
        </h2>
        {missions.map((mission) => {
          const hasProgress = mission.target && mission.target > 1;
          const progressPercent = hasProgress && mission.progress !== undefined
            ? Math.min((mission.progress / mission.target) * 100, 100)
            : 0;
          const rewardAmount = mission.coins_reward || mission.reward || 0;

          return (
            <Card key={mission.id} className={`py-4 px-4 mb-3 ${mission.completed ? 'opacity-70 bg-slate-50' : ''}`}>
               <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3 flex-1">
                     <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center transition-colors flex-shrink-0 ${mission.completed ? 'bg-finap-success border-finap-success' : 'border-slate-300'}`}>
                        {mission.completed && <div className="w-2 h-2 bg-white rounded-full" />}
                     </div>
                     <div className="flex-1 min-w-0">
                        <span className={`font-medium text-sm block ${mission.completed ? 'line-through text-slate-400' : 'text-slate-700'}`}>
                          {mission.title}
                        </span>
                        {/* Progress bar for multi-step missions */}
                        {hasProgress && !mission.completed && (
                          <div className="mt-2">
                            <div className="flex justify-between text-[10px] font-medium text-slate-400 mb-1">
                              <span>Progresso</span>
                              <span>{mission.progress || 0}/{mission.target}</span>
                            </div>
                            <div className="w-full bg-slate-100 rounded-full h-1.5 overflow-hidden">
                              <div
                                className="h-full bg-finap-primary rounded-full transition-all duration-300"
                                style={{ width: `${progressPercent}%` }}
                              />
                            </div>
                          </div>
                        )}
                     </div>
                  </div>
                  <div className="flex items-center gap-2 ml-3 flex-shrink-0">
                     {mission.xp_reward && mission.xp_reward > 0 && (
                       <div className="flex items-center gap-1 bg-purple-50 px-2 py-1 rounded-md border border-purple-100">
                          <span className="text-xs font-bold text-purple-700">+{mission.xp_reward}</span>
                          <span className="text-[10px] font-bold text-purple-500">XP</span>
                       </div>
                     )}
                     <div className="flex items-center gap-1 bg-yellow-50 px-2 py-1 rounded-md border border-yellow-100">
                        <span className="text-xs font-bold text-yellow-700">+{rewardAmount}</span>
                        <Coins size={12} className="text-yellow-700" />
                     </div>
                  </div>
               </div>
            </Card>
          );
        })}
      </div>

      {/* Toast Notifications */}
      {ToastComponent}
    </div>
  );
};