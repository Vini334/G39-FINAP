
import React, { useState, useEffect } from 'react';
import { Card } from '../components/Card';
import { UserStats, ViewState } from '../types';
import { ArrowLeft, Settings, ShoppingBag, Palette, Bell, Shield, UserPlus, UserMinus, X, Star, Zap, Award, LogOut, HelpCircle, Loader } from 'lucide-react';
import { FimMascot } from '../components/FimMascot';
import { authService } from '../services';
import { useToast } from '../components/Toast';

interface ProfileProps {
  stats: UserStats;
  onBack: () => void;
  onNavigate: (view: ViewState) => void;
}

interface Friend {
    id: string;
    name: string;
    avatarSeed: string;
    online: boolean;
}

export const Profile: React.FC<ProfileProps> = ({ stats, onBack, onNavigate }) => {
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [userData, setUserData] = useState<any>(null);
  const { showToast, ToastComponent } = useToast();
  const [friends, setFriends] = useState<Friend[]>([
      { id: '1', name: 'Sarah', avatarSeed: 'Sarah', online: true },
      { id: '2', name: 'Mike', avatarSeed: 'Mike', online: false },
      { id: '3', name: 'Jess', avatarSeed: 'Jess', online: true },
  ]);

  useEffect(() => {
    loadUserData();
  }, []);

  const loadUserData = async () => {
    try {
      setLoading(true);
      const user = authService.getUser();

      if (!user) {
        showToast('Usuário não autenticado', 'error');
        onNavigate(ViewState.LOGIN);
        return;
      }

      setUserData(user);
    } catch (error: any) {
      console.error('Erro ao carregar dados do usuário:', error);
      showToast(error.message || 'Erro ao carregar perfil', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    try {
      await authService.logout();
      showToast('Logout realizado com sucesso!', 'success');
      onNavigate(ViewState.ONBOARDING);
    } catch (error: any) {
      console.error('Erro ao fazer logout:', error);
      showToast(error.message || 'Erro ao fazer logout', 'error');
    }
  };

  const removeFriend = (id: string) => {
      setFriends(prev => prev.filter(f => f.id !== id));
  };

  const addFriend = () => {
      const newFriend: Friend = {
          id: Date.now().toString(),
          name: 'New User',
          avatarSeed: `User${Date.now()}`,
          online: true
      };
      setFriends(prev => [...prev, newFriend]);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-slate-50">
        <div className="text-center">
          <Loader className="w-12 h-12 text-finap-primary animate-spin mx-auto mb-4" />
          <p className="text-gray-600">Carregando perfil...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="pb-24 bg-slate-50 min-h-screen animate-fade-in relative overflow-x-hidden">

      {/* Header Background */}
      <div className="h-48 bg-finap-primary rounded-b-[3rem] relative overflow-hidden">
         <div className="absolute top-0 left-0 w-full h-full opacity-10 bg-[radial-gradient(circle_at_50%_120%,rgba(255,255,255,0.8),transparent)]"></div>
         <div className="absolute top-4 left-4 z-10">
            <button onClick={onBack} className="bg-white/20 backdrop-blur-md p-2 rounded-full text-white hover:bg-white/30 transition-colors">
               <ArrowLeft size={24} />
            </button>
         </div>
         <div className="absolute top-4 right-4 z-10">
            <button 
                onClick={() => setIsSettingsOpen(true)}
                className="bg-white/20 backdrop-blur-md p-2 rounded-full text-white hover:bg-white/30 transition-colors"
            >
               <Settings size={24} />
            </button>
         </div>
      </div>

      {/* Avatar & Badges */}
      <div className="-mt-20 px-6 mb-6 flex flex-col items-center relative z-0">
         <div className="relative mb-3 group">
             {/* Main Avatar */}
             <div className="w-32 h-32 rounded-full border-4 border-white shadow-lg overflow-hidden bg-indigo-100 relative z-10">
                <img
                   src="/assets/profilePic.png"
                   alt="Profile"
                   className="w-full h-full object-cover"
                />
             </div>
             
             {/* Badges Display (Floating near avatar) */}
             <div className="absolute -right-2 bottom-2 flex flex-col gap-1 z-20">
                 <div className="bg-finap-gold border-2 border-white rounded-full p-1.5 shadow-sm transform hover:scale-110 transition-transform cursor-pointer" title="Premium Member">
                    <Award size={14} className="text-white fill-white" />
                 </div>
                 <div className="bg-purple-500 border-2 border-white rounded-full p-1.5 shadow-sm transform hover:scale-110 transition-transform cursor-pointer -mt-2 ml-4" title="Top Saver">
                    <Zap size={14} className="text-white fill-white" />
                 </div>
                 <div className="bg-emerald-500 border-2 border-white rounded-full p-1.5 shadow-sm transform hover:scale-110 transition-transform cursor-pointer -mt-2" title="Streak Master">
                    <Star size={14} className="text-white fill-white" />
                 </div>
             </div>
         </div>
         <h1 className="text-2xl font-black text-slate-800">{userData?.name || 'Carregando...'}</h1>
         <p className="text-slate-500 font-medium text-sm">{userData?.email || ''}</p>
      </div>

      <div className="px-4 space-y-6">
          {/* Stats Grid */}
          <div className="grid grid-cols-3 gap-3">
             <Card className="flex flex-col items-center justify-center py-4 gap-1 mb-0 border-none shadow-sm">
                <span className="text-2xl font-black text-slate-800">{stats.level}</span>
                <span className="text-[10px] uppercase font-bold text-slate-400 tracking-widest">Nível</span>
             </Card>
             <Card className="flex flex-col items-center justify-center py-4 gap-1 mb-0 border-none shadow-sm">
                <span className="text-2xl font-black text-finap-gold">{stats.coins}</span>
                <span className="text-[10px] uppercase font-bold text-slate-400 tracking-widest">Moedas</span>
             </Card>
             <Card className="flex flex-col items-center justify-center py-4 gap-1 mb-0 border-none shadow-sm">
                <span className="text-2xl font-black text-finap-primary">{stats.xp}</span>
                <span className="text-[10px] uppercase font-bold text-slate-400 tracking-widest">XP Total</span>
             </Card>
          </div>

          {/* Friends Section */}
          <div>
              <div className="flex justify-between items-center mb-3 px-1">
                <h2 className="font-bold text-slate-800 flex items-center gap-2">
                   <UserPlus size={20} className="text-finap-primary" /> Amigos ({friends.length})
                </h2>
             </div>
             <div className="bg-white p-4 rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
                 <div className="flex gap-4 overflow-x-auto no-scrollbar items-center">
                     {/* Add Button */}
                     <button 
                        onClick={addFriend}
                        className="flex-shrink-0 w-14 h-14 rounded-full border-2 border-dashed border-slate-300 flex items-center justify-center text-slate-400 hover:border-finap-primary hover:text-finap-primary hover:bg-teal-50 transition-all"
                     >
                         <UserPlus size={20} />
                     </button>

                     {/* Friends List */}
                     {friends.map(friend => (
                         <div key={friend.id} className="relative group flex-shrink-0 flex flex-col items-center gap-1">
                             <div className="w-14 h-14 rounded-full bg-slate-100 overflow-hidden border border-slate-200 relative">
                                 <img src={`https://api.dicebear.com/9.x/avataaars/svg?seed=${friend.avatarSeed}`} alt={friend.name} />
                                 {friend.online && (
                                     <div className="absolute bottom-0 right-0 w-3 h-3 bg-finap-success border-2 border-white rounded-full"></div>
                                 )}
                             </div>
                             <span className="text-[10px] font-bold text-slate-600 truncate max-w-[60px]">{friend.name}</span>
                             
                             {/* Remove Button (Visible on Hover/Focus) */}
                             <button 
                                onClick={() => removeFriend(friend.id)}
                                className="absolute -top-1 -right-1 bg-red-100 text-red-500 rounded-full p-0.5 opacity-0 group-hover:opacity-100 transition-opacity shadow-sm"
                             >
                                 <UserMinus size={12} />
                             </button>
                         </div>
                     ))}
                 </div>
             </div>
          </div>

          {/* Shop / Customization */}
          <div>
             <div className="flex justify-between items-center mb-3 px-1">
                <h2 className="font-bold text-slate-800 flex items-center gap-2">
                   <ShoppingBag size={20} className="text-finap-primary" /> Loja de Itens
                </h2>
                <span className="text-xs font-bold text-finap-primary cursor-pointer">Ver Tudo</span>
             </div>
             
             <div className="flex gap-4 overflow-x-auto no-scrollbar pb-2">
                {/* Shop Item 1 */}
                <div className="min-w-[140px] bg-white p-3 rounded-xl border border-slate-100 shadow-sm flex flex-col items-center gap-2 relative overflow-hidden">
                   <div className="absolute top-2 right-2 bg-finap-gold/10 text-finap-gold text-[10px] font-bold px-1.5 rounded-md border border-finap-gold/20">
                      NOVO
                   </div>
                   <div className="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mt-2">
                      <FimMascot size="sm" emotion="happy" />
                   </div>
                   <div className="text-center">
                      <p className="font-bold text-xs text-slate-700">FIM Dourado</p>
                      <p className="text-[10px] text-slate-400">Skin do Assistente</p>
                   </div>
                   <button className="w-full py-1.5 bg-slate-800 text-white text-xs font-bold rounded-lg mt-1 flex items-center justify-center gap-1">
                      500 <span className="w-2 h-2 bg-finap-gold rounded-full"></span>
                   </button>
                </div>

                {/* Shop Item 2 */}
                <div className="min-w-[140px] bg-white p-3 rounded-xl border border-slate-100 shadow-sm flex flex-col items-center gap-2">
                   <div className="w-16 h-16 bg-gradient-to-br from-pink-100 to-purple-100 rounded-full flex items-center justify-center mt-2 border-2 border-white shadow-inner">
                      <div className="w-full h-full rounded-full border-4 border-purple-400 opacity-50"></div>
                   </div>
                   <div className="text-center">
                      <p className="font-bold text-xs text-slate-700">Borda Neon</p>
                      <p className="text-[10px] text-slate-400">Moldura Avatar</p>
                   </div>
                   <button className="w-full py-1.5 bg-slate-100 text-slate-400 text-xs font-bold rounded-lg mt-1 flex items-center justify-center gap-1 cursor-not-allowed">
                      Bloqueado
                   </button>
                </div>
                 {/* Shop Item 3 */}
                 <div className="min-w-[140px] bg-white p-3 rounded-xl border border-slate-100 shadow-sm flex flex-col items-center gap-2">
                   <div className="w-16 h-16 bg-blue-50 rounded-full flex items-center justify-center mt-2">
                       <Palette size={24} className="text-blue-400"/>
                   </div>
                   <div className="text-center">
                      <p className="font-bold text-xs text-slate-700">Tema Escuro</p>
                      <p className="text-[10px] text-slate-400">Tema do App</p>
                   </div>
                   <button className="w-full py-1.5 bg-slate-800 text-white text-xs font-bold rounded-lg mt-1 flex items-center justify-center gap-1">
                      1200 <span className="w-2 h-2 bg-finap-gold rounded-full"></span>
                   </button>
                </div>
             </div>
          </div>
      </div>

      {/* Settings Side Menu (Drawer) */}
      {/* Backdrop */}
      {isSettingsOpen && (
          <div 
            className="fixed inset-0 bg-slate-900/50 z-40 animate-fade-in backdrop-blur-sm"
            onClick={() => setIsSettingsOpen(false)}
          ></div>
      )}
      
      {/* Drawer Content */}
      <div className={`fixed top-0 right-0 h-full w-3/4 max-w-xs bg-white shadow-2xl z-50 transform transition-transform duration-300 ease-out ${isSettingsOpen ? 'translate-x-0' : 'translate-x-full'}`}>
          <div className="p-5 flex flex-col h-full">
              <div className="flex justify-between items-center mb-8">
                  <h2 className="text-xl font-black text-slate-800">Configurações</h2>
                  <button onClick={() => setIsSettingsOpen(false)} className="p-2 rounded-full hover:bg-slate-100 text-slate-500">
                      <X size={24} />
                  </button>
              </div>

              <div className="space-y-2 flex-1">
                  {[
                    { icon: Palette, label: 'Aparência do App', sub: 'Modo Claro' },
                    { icon: Bell, label: 'Notificações', sub: 'Ativo' },
                    { icon: Shield, label: 'Privacidade & Segurança', sub: '' },
                    { icon: HelpCircle, label: 'Ajuda & Suporte', sub: '' },
                  ].map((item, idx) => (
                    <div key={idx} className="p-4 flex items-center justify-between rounded-xl hover:bg-slate-50 cursor-pointer group">
                        <div className="flex items-center gap-3">
                            <div className="bg-slate-100 p-2 rounded-lg text-slate-600 group-hover:bg-white group-hover:text-finap-primary transition-colors">
                                <item.icon size={20} />
                            </div>
                            <div>
                                <p className="font-bold text-sm text-slate-800">{item.label}</p>
                                {item.sub && <p className="text-xs text-slate-400">{item.sub}</p>}
                            </div>
                        </div>
                        <ArrowLeft size={16} className="rotate-180 text-slate-300" />
                    </div>
                  ))}
              </div>

              <button
                onClick={handleLogout}
                className="mt-auto w-full py-3 rounded-xl bg-red-50 text-red-500 font-bold flex items-center justify-center gap-2 hover:bg-red-100 transition-colors"
              >
                  <LogOut size={18} /> Sair
              </button>
              
              <div className="mt-4 text-center">
                  <p className="text-[10px] text-slate-300 font-bold">FINAP v1.0.2</p>
              </div>
          </div>
      </div>

      {/* Toast Notifications */}
      {ToastComponent}
    </div>
  );
};
