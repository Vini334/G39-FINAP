import React, { useState } from 'react';
import { FimMascot } from '../components/FimMascot';
import { ArrowRight, ArrowLeft, Mail, Lock, User, DollarSign, Target, CheckCircle2, ChevronRight, Loader2, AlertCircle } from 'lucide-react';
import { authService } from '../services';

interface OnboardingProps {
  onComplete: () => void;
}

type Step = 'SPLASH' | 'AUTH' | 'NAME' | 'INCOME' | 'GOALS' | 'INTERESTS' | 'LOADING';

export const Onboarding: React.FC<OnboardingProps> = ({ onComplete }) => {
  const [step, setStep] = useState<Step>('SPLASH');
  const [authMode, setAuthMode] = useState<'LOGIN' | 'SIGNUP'>('SIGNUP');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Form Data State
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    monthlyIncome: 1000,
    savingsGoal: 100,
    interests: [] as string[]
  });

  const handleInterestToggle = (interest: string) => {
    setFormData(prev => {
      if (prev.interests.includes(interest)) {
        return { ...prev, interests: prev.interests.filter(i => i !== interest) };
      }
      return { ...prev, interests: [...prev.interests, interest] };
    });
  };

  // Password strength validation
  const getPasswordStrength = (password: string) => {
    const checks = {
      minLength: password.length >= 6,
      hasUpperCase: /[A-Z]/.test(password),
      hasNumber: /\d/.test(password),
    };

    const passedChecks = Object.values(checks).filter(Boolean).length;

    return {
      checks,
      strength: passedChecks === 0 ? 0 : passedChecks === 1 ? 1 : passedChecks === 2 ? 2 : 3,
      isValid: passedChecks === 3
    };
  };

  const passwordStrength = getPasswordStrength(formData.password);

  const handleAuth = async () => {
    setError(null);
    setLoading(true);

    try {
      if (authMode === 'LOGIN') {
        // Login
        const result = await authService.login({
          email: formData.email,
          password: formData.password
        });

        console.log('Login bem-sucedido:', result);

        // Apenas vai para LOADING se o login foi bem-sucedido
        setStep('LOADING');
        setTimeout(onComplete, 2000);
      } else {
        // Signup - valida senha antes de continuar
        if (!passwordStrength.isValid) {
          setError('Por favor, atenda todos os requisitos de senha');
          setLoading(false);
          return;
        }
        nextStep();
      }
    } catch (err: any) {
      // Melhorar mensagens de erro
      console.error('Erro no handleAuth:', err);
      const errorMessage = err.message || 'Erro ao autenticar';

      if (errorMessage.includes('Email ou senha')) {
        setError(errorMessage);
      } else if (errorMessage.includes('already') || errorMessage.includes('cadastrado')) {
        setError('Este email já está cadastrado. Tente fazer login.');
      } else if (errorMessage.includes('email')) {
        setError('Por favor, insira um email válido.');
      } else if (errorMessage.includes('password') || errorMessage.includes('senha')) {
        setError(errorMessage);
      } else if (errorMessage.includes('conexão') || errorMessage.includes('rede')) {
        setError('Erro de conexão. Verifique sua internet.');
      } else {
        setError(errorMessage);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleCompleteSignup = async () => {
    setError(null);
    setLoading(true);

    try {
      await authService.register({
        email: formData.email,
        password: formData.password,
        name: formData.name
      });
      setStep('LOADING');
      setTimeout(onComplete, 2000);
    } catch (err: any) {
      // Melhorar mensagens de erro do backend
      const errorMessage = err.message || 'Erro ao criar conta';

      if (errorMessage.includes('already')) {
        setError('Este email já está cadastrado. Tente fazer login.');
      } else if (errorMessage.includes('maiúscula') || errorMessage.includes('uppercase')) {
        setError('A senha deve conter pelo menos uma letra maiúscula');
      } else if (errorMessage.includes('número') || errorMessage.includes('number')) {
        setError('A senha deve conter pelo menos um número');
      } else if (errorMessage.includes('6 caracteres') || errorMessage.includes('6 characters')) {
        setError('A senha deve ter no mínimo 6 caracteres');
      } else {
        setError(errorMessage);
      }

      setLoading(false);
    }
  };

  const nextStep = () => {
    if (step === 'SPLASH') setStep('AUTH');
    else if (step === 'AUTH') setStep('NAME');
    else if (step === 'NAME') setStep('INCOME');
    else if (step === 'INCOME') setStep('GOALS');
    else if (step === 'GOALS') setStep('INTERESTS');
    else if (step === 'INTERESTS') {
        handleCompleteSignup();
    }
  };

  const prevStep = () => {
    if (step === 'NAME') setStep('AUTH');
    else if (step === 'INCOME') setStep('NAME');
    else if (step === 'GOALS') setStep('INCOME');
    else if (step === 'INTERESTS') setStep('GOALS');
  };

  // --- RENDER COMPONENTS ---

  if (step === 'SPLASH') {
    return (
      <div className="min-h-screen bg-finap-primary flex flex-col items-center justify-center p-6 text-white relative overflow-hidden animate-fade-in">
         {/* Background Decoration */}
         <div className="absolute top-0 left-0 w-full h-full opacity-20 bg-[radial-gradient(circle_at_50%_50%,white,transparent)]"></div>
         
         <div className="z-10 flex flex-col items-center text-center">
            <div className="w-32 h-32 bg-white rounded-full flex items-center justify-center shadow-2xl mb-8 animate-bounce">
                <FimMascot size="xl" emotion="happy" />
            </div>
            <h1 className="text-4xl font-black tracking-tighter mb-2">FINAP</h1>
            <p className="text-teal-100 text-lg font-medium mb-12">Domine seu dinheiro.<br/>Jogue o jogo.</p>

            <button
                onClick={nextStep}
                className="w-full max-w-xs bg-white text-finap-primary font-bold py-4 rounded-2xl shadow-xl hover:scale-105 transition-transform flex items-center justify-center gap-2"
            >
                Começar <ArrowRight size={20} />
            </button>

            <p className="mt-6 text-sm text-teal-200 font-medium">Já tem uma conta? <span className="text-white underline cursor-pointer" onClick={() => { setAuthMode('LOGIN'); setStep('AUTH'); }}>Entrar</span></p>
         </div>
      </div>
    );
  }

  if (step === 'AUTH') {
    return (
      <div className="min-h-screen bg-slate-50 flex flex-col p-6 animate-fade-in">
         <button onClick={() => setStep('SPLASH')} className="self-start text-slate-400 p-2 -ml-2"><ArrowLeft /></button>
         
         <div className="flex-1 flex flex-col justify-center">
             <div className="mb-8">
                 <h2 className="text-3xl font-black text-slate-800 mb-2">{authMode === 'SIGNUP' ? 'Criar Conta' : 'Bem-vindo de Volta'}</h2>
                 <p className="text-slate-500">{authMode === 'SIGNUP' ? 'Comece sua jornada financeira hoje.' : 'Vamos voltar aos ganhos.'}</p>
             </div>

             {error && (
                <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-4 rounded-lg flex items-start">
                  <AlertCircle className="w-5 h-5 text-red-500 mr-3 mt-0.5 flex-shrink-0" />
                  <p className="text-red-700 text-sm">{error}</p>
                </div>
             )}

             <div className="space-y-4">
                 {authMode === 'SIGNUP' && (
                    <div className="bg-white p-4 rounded-2xl border border-slate-200 flex items-center gap-3 focus-within:border-finap-primary focus-within:ring-2 focus-within:ring-teal-100 transition-all">
                        <User className="text-slate-400" size={20} />
                        <input
                            type="text"
                            placeholder="Nome Completo"
                            className="flex-1 outline-none text-slate-800 font-medium placeholder-slate-300 bg-transparent"
                            value={formData.name}
                            onChange={(e) => setFormData({...formData, name: e.target.value})}
                        />
                    </div>
                 )}
                 <div className="bg-white p-4 rounded-2xl border border-slate-200 flex items-center gap-3 focus-within:border-finap-primary focus-within:ring-2 focus-within:ring-teal-100 transition-all">
                     <Mail className="text-slate-400" size={20} />
                     <input
                        type="email"
                        placeholder="Endereço de Email"
                        className="flex-1 outline-none text-slate-800 font-medium placeholder-slate-300 bg-transparent"
                        value={formData.email}
                        onChange={(e) => setFormData({...formData, email: e.target.value})}
                     />
                 </div>
                 <div>
                   <div className="bg-white p-4 rounded-2xl border border-slate-200 flex items-center gap-3 focus-within:border-finap-primary focus-within:ring-2 focus-within:ring-teal-100 transition-all">
                       <Lock className="text-slate-400" size={20} />
                       <input
                          type="password"
                          placeholder="Senha"
                          className="flex-1 outline-none text-slate-800 font-medium placeholder-slate-300 bg-transparent"
                          value={formData.password}
                          onChange={(e) => setFormData({...formData, password: e.target.value})}
                       />
                   </div>

                   {authMode === 'SIGNUP' && formData.password.length > 0 && (
                     <div className="mt-3 space-y-2">
                       {/* Password Strength Bar */}
                       <div className="flex gap-1">
                         {[1, 2, 3].map((level) => (
                           <div
                             key={level}
                             className={`h-1.5 flex-1 rounded-full transition-all ${
                               level <= passwordStrength.strength
                                 ? passwordStrength.strength === 1
                                   ? 'bg-red-500'
                                   : passwordStrength.strength === 2
                                   ? 'bg-yellow-500'
                                   : 'bg-green-500'
                                 : 'bg-slate-200'
                             }`}
                           />
                         ))}
                       </div>

                       {/* Requirements Checklist */}
                       <div className="space-y-1 text-xs">
                         <div className={`flex items-center gap-2 ${passwordStrength.checks.minLength ? 'text-green-600' : 'text-slate-400'}`}>
                           <CheckCircle2 size={14} className={passwordStrength.checks.minLength ? 'opacity-100' : 'opacity-30'} />
                           <span>Mínimo 6 caracteres</span>
                         </div>
                         <div className={`flex items-center gap-2 ${passwordStrength.checks.hasUpperCase ? 'text-green-600' : 'text-slate-400'}`}>
                           <CheckCircle2 size={14} className={passwordStrength.checks.hasUpperCase ? 'opacity-100' : 'opacity-30'} />
                           <span>Uma letra maiúscula</span>
                         </div>
                         <div className={`flex items-center gap-2 ${passwordStrength.checks.hasNumber ? 'text-green-600' : 'text-slate-400'}`}>
                           <CheckCircle2 size={14} className={passwordStrength.checks.hasNumber ? 'opacity-100' : 'opacity-30'} />
                           <span>Um número</span>
                         </div>
                       </div>
                     </div>
                   )}
                 </div>
             </div>

             <button
                onClick={handleAuth}
                disabled={loading}
                className="mt-8 w-full bg-finap-primary text-white font-bold py-4 rounded-2xl shadow-lg shadow-teal-500/30 active:scale-95 transition-transform flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
             >
                {loading ? (
                  <Loader2 className="w-5 h-5 animate-spin" />
                ) : (
                  <>
                    {authMode === 'SIGNUP' ? 'Continuar' : 'Entrar'} <ArrowRight size={20} />
                  </>
                )}
             </button>

             <div className="mt-6 text-center">
                 <span className="text-slate-400 text-sm font-medium">
                    {authMode === 'SIGNUP' ? 'Já tem uma conta?' : 'Novo no FINAP?'}
                    <button
                        onClick={() => setAuthMode(authMode === 'SIGNUP' ? 'LOGIN' : 'SIGNUP')}
                        className="text-finap-primary font-bold ml-1 hover:underline"
                    >
                        {authMode === 'SIGNUP' ? 'Entrar' : 'Criar Conta'}
                    </button>
                 </span>
             </div>
         </div>
      </div>
    );
  }

  if (step === 'NAME') {
       // Specialized step just for Name if we want to make it chatty, 
       // but since we did it in Auth form, let's skip to financial questions (INCOME)
       // This block catches the flow if user clicked "Continue" on Signup.
       // We can use this intermediate step to have FIM introduce himself.
       return (
         <div className="min-h-screen bg-slate-50 flex flex-col p-6 animate-fade-in">
            <div className="flex-1 flex flex-col items-center justify-center text-center">
                <FimMascot size="lg" emotion="happy" className="mb-6" />
                <h2 className="text-2xl font-black text-slate-800 mb-2">Prazer em te conhecer, {formData.name.split(' ')[0]}!</h2>
                <p className="text-slate-500 mb-8 max-w-xs">Eu sou o FIM. Pra te ajudar a ganhar o jogo do dinheiro, preciso saber umas paradas sobre você.</p>
                <button
                    onClick={nextStep}
                    className="bg-finap-primary text-white font-bold py-3 px-8 rounded-full shadow-lg shadow-teal-500/30 hover:scale-105 transition-transform"
                >
                    Bora lá! 🚀
                </button>
            </div>
         </div>
       );
  }

  if (step === 'INCOME') {
    return (
      <div className="min-h-screen bg-slate-50 flex flex-col p-6 animate-fade-in">
        <div className="w-full bg-slate-200 h-1 rounded-full mb-8">
            <div className="bg-finap-primary h-1 rounded-full w-1/3 transition-all"></div>
        </div>
        
        <div className="flex-1">
            <button onClick={prevStep} className="text-slate-400 mb-6"><ArrowLeft /></button>
            <h2 className="text-3xl font-black text-slate-800 mb-4">Qual é sua renda mensal?</h2>
            <p className="text-slate-500 mb-10">Isso me ajuda a montar seu orçamento. Uma estimativa tá valendo!</p>

            <div className="bg-white p-8 rounded-3xl shadow-sm border border-slate-100 flex flex-col items-center mb-8">
                <span className="text-slate-400 text-sm font-bold uppercase tracking-widest mb-2">Renda Mensal</span>
                <div className="flex items-center text-4xl font-black text-finap-dark mb-6">
                    <span className="text-2xl mr-1 text-slate-400">R$</span>
                    {formData.monthlyIncome}
                </div>
                
                <input 
                    type="range" 
                    min="0" 
                    max="10000" 
                    step="50" 
                    value={formData.monthlyIncome}
                    onChange={(e) => setFormData({...formData, monthlyIncome: parseInt(e.target.value)})}
                    className="w-full h-2 bg-slate-100 rounded-lg appearance-none cursor-pointer accent-finap-primary"
                />
                <div className="flex justify-between w-full text-xs text-slate-400 font-bold mt-2">
                    <span>R$ 0</span>
                    <span>R$ 10k+</span>
                </div>
            </div>

            <div className="flex gap-2 bg-blue-50 p-4 rounded-xl border border-blue-100">
                 <div className="bg-blue-100 p-1 rounded-full h-fit"><DollarSign size={16} className="text-blue-500" /></div>
                 <p className="text-xs text-blue-600 font-medium leading-relaxed">
                     Dica: Inclua mesada, salário ou qualquer grana de trampos que você recebe regularmente.
                 </p>
            </div>
        </div>

        <button onClick={nextStep} className="w-full bg-slate-800 text-white font-bold py-4 rounded-2xl shadow-lg active:scale-95 transition-transform">
            Próximo Passo
        </button>
      </div>
    );
  }

  if (step === 'GOALS') {
    return (
      <div className="min-h-screen bg-slate-50 flex flex-col p-6 animate-fade-in">
        <div className="w-full bg-slate-200 h-1 rounded-full mb-8">
            <div className="bg-finap-primary h-1 rounded-full w-2/3 transition-all"></div>
        </div>
        
        <div className="flex-1">
            <button onClick={prevStep} className="text-slate-400 mb-6"><ArrowLeft /></button>
            <h2 className="text-3xl font-black text-slate-800 mb-4">Quanto você quer economizar?</h2>
            <p className="text-slate-500 mb-10">Defina um desafio mensal pra você.</p>

            <div className="bg-white p-8 rounded-3xl shadow-sm border border-slate-100 flex flex-col items-center mb-8">
                <div className="bg-finap-gold/10 p-3 rounded-full mb-4">
                    <Target size={32} className="text-finap-gold" />
                </div>
                <span className="text-slate-400 text-sm font-bold uppercase tracking-widest mb-2">Meta Mensal</span>
                <div className="flex items-center text-4xl font-black text-finap-dark mb-6">
                    <span className="text-2xl mr-1 text-slate-400">R$</span>
                    {formData.savingsGoal}
                </div>
                
                <div className="flex gap-4 w-full">
                    <button 
                        onClick={() => setFormData(p => ({...p, savingsGoal: Math.max(0, p.savingsGoal - 50)}))}
                        className="w-12 h-12 rounded-full border-2 border-slate-200 flex items-center justify-center text-slate-400 text-2xl font-bold hover:border-finap-primary hover:text-finap-primary transition-colors"
                    >-</button>
                    <div className="flex-1 h-12 bg-slate-50 rounded-full border border-slate-100 flex items-center justify-center font-bold text-slate-600">
                        {Math.round((formData.savingsGoal / formData.monthlyIncome) * 100)}% da renda
                    </div>
                    <button 
                        onClick={() => setFormData(p => ({...p, savingsGoal: p.savingsGoal + 50}))}
                        className="w-12 h-12 rounded-full border-2 border-slate-200 flex items-center justify-center text-slate-400 text-2xl font-bold hover:border-finap-primary hover:text-finap-primary transition-colors"
                    >+</button>
                </div>
            </div>
        </div>

        <button onClick={nextStep} className="w-full bg-slate-800 text-white font-bold py-4 rounded-2xl shadow-lg active:scale-95 transition-transform">
            Próximo Passo
        </button>
      </div>
    );
  }

  if (step === 'INTERESTS') {
    const options = [
        "💰 Investimentos", "📉 Lidar com Dívidas", "🎮 Orçamento para Diversão",
        "✈️ Economizar para Viagens", "🤑 Ganhar mais dinheiro", "💳 Cartões de Crédito"
    ];

    return (
      <div className="min-h-screen bg-slate-50 flex flex-col p-6 animate-fade-in">
        <div className="w-full bg-slate-200 h-1 rounded-full mb-8">
            <div className="bg-finap-primary h-1 rounded-full w-full transition-all"></div>
        </div>
        
        <div className="flex-1">
            <button onClick={prevStep} className="text-slate-400 mb-6"><ArrowLeft /></button>
            <h2 className="text-3xl font-black text-slate-800 mb-4">O que você quer aprender?</h2>
            <p className="text-slate-500 mb-8">Vou personalizar seu Caminho de Aprendizado baseado nisso.</p>

            <div className="grid grid-cols-1 gap-3">
                {options.map(opt => {
                    const isSelected = formData.interests.includes(opt);
                    return (
                        <button 
                            key={opt}
                            onClick={() => handleInterestToggle(opt)}
                            className={`p-4 rounded-xl border-2 text-left font-bold flex justify-between items-center transition-all active:scale-[0.98] ${
                                isSelected 
                                ? 'bg-teal-50 border-finap-primary text-teal-700' 
                                : 'bg-white border-slate-100 text-slate-600 hover:border-slate-300'
                            }`}
                        >
                            {opt}
                            {isSelected && <CheckCircle2 size={20} className="text-finap-success" />}
                        </button>
                    )
                })}
            </div>
        </div>

        <button
            onClick={nextStep}
            disabled={formData.interests.length === 0 || loading}
            className="w-full bg-finap-primary text-white font-bold py-4 rounded-2xl shadow-lg shadow-teal-500/30 active:scale-95 transition-transform disabled:opacity-50 disabled:scale-100 flex items-center justify-center gap-2"
        >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Criando conta...
              </>
            ) : (
              'Finalizar Configuração'
            )}
        </button>
      </div>
    );
  }

  if (step === 'LOADING') {
      return (
        <div className="min-h-screen bg-white flex flex-col items-center justify-center p-6 animate-fade-in text-center">
            <div className="relative">
                <div className="absolute inset-0 bg-finap-primary rounded-full opacity-20 animate-ping"></div>
                <div className="relative w-24 h-24 bg-white border-4 border-finap-primary rounded-full flex items-center justify-center mb-8">
                    <FimMascot size="md" emotion="happy" />
                </div>
            </div>
            <h2 className="text-2xl font-black text-slate-800 mb-2">Montando seu perfil...</h2>
            <p className="text-slate-500 mb-8">Criando missões personalizadas baseadas na sua renda de R$ {formData.monthlyIncome}.</p>

            <div className="flex gap-2 items-center text-finap-primary font-bold bg-teal-50 px-4 py-2 rounded-full">
                <Loader2 size={18} className="animate-spin" />
                <span>Quase lá!</span>
            </div>
        </div>
      );
  }

  return null;
};