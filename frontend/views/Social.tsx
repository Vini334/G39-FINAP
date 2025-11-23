import React, { useState } from 'react';
import { Card } from '../components/Card';
import { Users, Target, Share2, Trophy, Plus, LogIn, ArrowLeft, Calendar, MapPin, Info, CheckCircle, AlertCircle, DollarSign } from 'lucide-react';

// --- Types ---
interface SquadMember {
  id: string;
  name: string;
  avatar: string;
  savedTotal: number;
  savedThisMonth: number;
  monthlyTarget: number;
  status: 'on-track' | 'late'; // Green vs Red
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
    {
      id: 'u1', name: 'Você', avatar: 'Alex',
      savedTotal: 450, savedThisMonth: 200, monthlyTarget: 200, status: 'on-track'
    },
    {
      id: 'u2', name: 'Sarah', avatar: 'Sarah',
      savedTotal: 400, savedThisMonth: 200, monthlyTarget: 200, status: 'on-track'
    },
    {
      id: 'u3', name: 'Mike', avatar: 'Mike',
      savedTotal: 300, savedThisMonth: 50, monthlyTarget: 200, status: 'late'
    },
    {
      id: 'u4', name: 'Jess', avatar: 'Jess',
      savedTotal: 300, savedThisMonth: 0, monthlyTarget: 200, status: 'late'
    },
  ]
};

export const Social: React.FC = () => {
  const [view, setView] = useState<'LIST' | 'DETAIL'>('LIST');
  const [activeGoal, setActiveGoal] = useState<SquadGoal | null>(null);

  const handleOpenGoal = (goal: SquadGoal) => {
    setActiveGoal(goal);
    setView('DETAIL');
  };

  // --- DETAIL VIEW ---
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
      
      {/* Split Bill Placeholder */}
      <Card title="Dividir Conta" action={<button className="text-finap-primary text-xs font-bold bg-teal-50 px-2 py-1 rounded-md">Novo</button>}>
         <div className="text-center py-6">
            <div className="bg-slate-50 w-14 h-14 rounded-full flex items-center justify-center mx-auto mb-3 border border-slate-100">
               <Users className="text-slate-300" />
            </div>
            <p className="text-sm text-slate-500 font-medium">Nenhuma divisão ativa. Sair com os amigos?</p>
         </div>
      </Card>
    </div>
  );
};
