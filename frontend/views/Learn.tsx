import React, { useState, useRef, useEffect } from 'react';
import { Card } from '../components/Card';
import { QUIZ_SAMPLE } from '../constants';
import { CheckCircle2, XCircle, BookOpen, Trophy, Heart, ArrowLeft, Lock, Star, Play, TrendingUp, PiggyBank, Wallet, Send, X, RefreshCw, ChevronRight, Sparkles } from 'lucide-react';
import { FimMascot } from '../components/FimMascot';
import { UserStats, Message } from '../types';
import { createChatSession, sendMessageToFim } from '../services/geminiService';
import { Chat as GeminiChat } from '@google/genai';

interface LearnProps {
    stats?: UserStats;
}

type ViewMode = 'COURSES' | 'TRAIL' | 'INTRO' | 'CONTENT' | 'QUIZ' | 'RESULT';

interface Course {
    id: number;
    title: string;
    description: string;
    icon: React.ElementType;
    color: string;
    progress: number;
    totalModules: number;
    gradient: string;
}

interface Module {
    id: number;
    title: string;
    description: string;
    status: 'locked' | 'current' | 'completed';
    topics: string[];
}

const COURSES: Course[] = [
    {
        id: 1,
        title: "Início Financeiro",
        description: "Domine o básico de dinheiro, economia e mentalidade.",
        icon: PiggyBank,
        color: "text-emerald-500",
        gradient: "from-emerald-400 to-teal-600",
        progress: 45,
        totalModules: 5
    },
    {
        id: 2,
        title: "Orçamento Inteligente",
        description: "Aprenda a controlar seus gastos sem sofrer.",
        icon: Wallet,
        color: "text-blue-500",
        gradient: "from-blue-400 to-indigo-600",
        progress: 0,
        totalModules: 4
    },
    {
        id: 3,
        title: "Investimentos 101",
        description: "Faça seu dinheiro trabalhar pra você. Ações, Cripto e mais.",
        icon: TrendingUp,
        color: "text-purple-500",
        gradient: "from-purple-400 to-violet-600",
        progress: 0,
        totalModules: 6
    }
];

const MODULES: Module[] = [
    {
        id: 1,
        title: "Mentalidade Financeira",
        description: "Aprenda por que dinheiro importa e como pensar como um investidor profissional.",
        status: 'completed',
        topics: ['Necessidades vs Desejos', 'Definição de Metas']
    },
    {
        id: 2,
        title: "Segredos da Economia",
        description: "Descubra a mágica dos juros compostos e fundos de emergência.",
        status: 'current',
        topics: ['Juros Compostos', 'Fundo de Emergência', 'Regra 50/30/20']
    },
    {
        id: 3,
        title: "Crédito & Dívidas",
        description: "Como usar cartões de crédito com sabedoria sem cair em armadilhas.",
        status: 'locked',
        topics: ['Taxas de Juros', 'Score de Crédito']
    },
    {
        id: 4,
        title: "Investimentos 101",
        description: "Ações, Títulos e Cripto. O que são?",
        status: 'locked',
        topics: ['Bolsa de Valores', 'Risco vs Retorno']
    }
];

// Conteúdo educacional por módulo
const MODULE_CONTENT: { [key: number]: { title: string; content: string }[] } = {
    2: [ // Módulo 2: Segredos da Economia
        {
            title: "A Mágica dos Juros Compostos",
            content: `Os juros compostos são considerados a **oitava maravilha do mundo** por Albert Einstein! Mas o que são exatamente?

**O Básico:**
Juros compostos são juros calculados sobre o valor inicial MAIS os juros já acumulados. É como uma bola de neve que cresce cada vez mais rápido!

**Exemplo Prático:**
Imagine que você guardou R$ 100 com juros de 10% ao ano:
• Ano 1: R$ 100 + R$ 10 = R$ 110
• Ano 2: R$ 110 + R$ 11 = R$ 121
• Ano 3: R$ 121 + R$ 12,10 = R$ 133,10

Percebe como os juros aumentam a cada ano? No ano 2, você ganhou R$ 11 em vez de R$ 10!

**Por que isso importa?**
Quanto mais cedo você começar a economizar, mais tempo seus juros têm para crescer. Um jovem que começa aos 15 anos pode ter muito mais dinheiro aos 30 do que alguém que começou aos 25, mesmo investindo menos!

**Dica de Ouro:**
Comece pequeno, mas comece agora! Mesmo R$ 10 por mês podem se transformar em milhares com o tempo.`
        },
        {
            title: "Fundo de Emergência & Regra 50/30/20",
            content: `Todo mundo precisa de um **colchão financeiro** para imprevistos. Vamos aprender como construir o seu!

**O que é um Fundo de Emergência?**
É uma reserva de dinheiro guardada especialmente para emergências: celular quebrou, problema de saúde, ou até perda de renda. Serve para você não entrar em pânico quando algo inesperado acontecer.

**Quanto guardar?**
Para adolescentes: tente juntar o equivalente a 3 meses de suas despesas mensais.
Para adultos: idealmente de 6 a 12 meses de despesas.

**A Regra 50/30/20:**
Uma forma simples de organizar seu dinheiro:

💰 **50% - Necessidades**
Coisas essenciais: transporte, alimentação, contas básicas.

🎮 **30% - Desejos**
Diversão e entretenimento: jogos, cinema, lanches, roupas da moda.

🏦 **20% - Poupança**
Seu fundo de emergência, investimentos e objetivos futuros.

**Exemplo com mesada de R$ 200:**
• R$ 100 para necessidades
• R$ 60 para diversão
• R$ 40 para poupar (vai direto pro fundo!)

**Desafio:**
Tente aplicar essa regra na sua próxima mesada ou salário. Você vai se surpreender com quanto consegue economizar!`
        }
    ]
};

export const Learn: React.FC<LearnProps> = ({ stats }) => {
  const [viewMode, setViewMode] = useState<ViewMode>('COURSES');
  const [activeCourse, setActiveCourse] = useState<Course | null>(null);
  const [activeModule, setActiveModule] = useState<Module | null>(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [score, setScore] = useState(0);
  const [selectedOption, setSelectedOption] = useState<number | null>(null);
  const [isAnswerChecked, setIsAnswerChecked] = useState(false);
  const [lives, setLives] = useState(stats?.lives || 5);
  const [currentContentPage, setCurrentContentPage] = useState(0);

  // FIM Mini Chat State
  const [showFimChat, setShowFimChat] = useState(false);
  const [fimMessages, setFimMessages] = useState<Message[]>([]);
  const [fimInput, setFimInput] = useState('');
  const [isFimLoading, setIsFimLoading] = useState(false);
  const fimChatSessionRef = useRef<GeminiChat | null>(null);
  const fimMessagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (showFimChat && !fimChatSessionRef.current) {
        fimChatSessionRef.current = createChatSession();
        setFimMessages([{
            id: 'init',
            role: 'model',
            text: `E aí! Travou em ${activeCourse?.title || 'algum curso'}? Me pergunta qualquer coisa! 🤓`,
            timestamp: Date.now()
        }]);
    }
  }, [showFimChat, activeCourse]);

  useEffect(() => {
      fimMessagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [fimMessages]);

  const handleFimSend = async () => {
      if (!fimInput.trim() || isFimLoading) return;
      
      const userMsg: Message = { id: Date.now().toString(), role: 'user', text: fimInput, timestamp: Date.now() };
      setFimMessages(prev => [...prev, userMsg]);
      setFimInput('');
      setIsFimLoading(true);

      try {
          if (fimChatSessionRef.current) {
            const response = await sendMessageToFim(fimChatSessionRef.current, userMsg.text);
            setFimMessages(prev => [...prev, { id: (Date.now()+1).toString(), role: 'model', text: response, timestamp: Date.now() }]);
          }
      } catch (e) {
          console.error(e);
      } finally {
          setIsFimLoading(false);
      }
  };

  const handleCourseClick = (course: Course) => {
      setActiveCourse(course);
      setViewMode('TRAIL');
      setShowFimChat(false); // Reset chat when entering trail
  };

  const handleModuleClick = (mod: Module) => {
      if (mod.status === 'locked') return;
      setActiveModule(mod);
      setViewMode('INTRO');
  };

  const startLesson = () => {
    setCurrentContentPage(0);
    setViewMode('CONTENT');
  };

  const startQuiz = () => {
    setCurrentQuestionIndex(0);
    setScore(0);
    setViewMode('QUIZ');
    setSelectedOption(null);
    setIsAnswerChecked(false);
  };

  const handleAnswer = (index: number) => {
    if (isAnswerChecked) return;
    setSelectedOption(index);
    setIsAnswerChecked(true);

    const isCorrect = index === QUIZ_SAMPLE[currentQuestionIndex].correctIndex;

    if (isCorrect) {
       setScore(prev => prev + 1);
    } else {
        // Wrong answer logic
        setLives(prev => Math.max(0, prev - 1));
    }

    setTimeout(() => {
       if (currentQuestionIndex < QUIZ_SAMPLE.length - 1 && lives > 0) {
          setCurrentQuestionIndex(prev => prev + 1);
          setSelectedOption(null);
          setIsAnswerChecked(false);
       } else {
          setViewMode('RESULT');
       }
    }, 1500);
  };

  // --- Render: Courses List (Overview) ---
  if (viewMode === 'COURSES') {
      return (
          <div className="pb-24 px-4 pt-4 animate-fade-in space-y-6">
              <div className="flex justify-between items-center">
                  <h1 className="text-2xl font-black text-slate-800 tracking-tight">Academia</h1>
                  <div className="bg-white px-3 py-1 rounded-full border border-slate-200 shadow-sm flex items-center gap-1">
                      <Trophy size={14} className="text-finap-gold fill-finap-gold"/>
                      <span className="text-xs font-bold text-slate-600">Nível {stats?.level || 1}</span>
                  </div>
              </div>

              <div className="space-y-4">
                  {COURSES.map((course) => (
                      <div 
                        key={course.id}
                        onClick={() => handleCourseClick(course)}
                        className="group relative bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden cursor-pointer transition-all hover:-translate-y-1 hover:shadow-md"
                      >
                          {/* Course Card Header / Background */}
                          <div className={`h-24 bg-gradient-to-r ${course.gradient} relative overflow-hidden`}>
                             <div className="absolute -right-4 -bottom-8 w-32 h-32 bg-white/20 rounded-full blur-2xl"></div>
                             <div className="absolute top-4 left-4 bg-white/20 backdrop-blur-md p-2 rounded-xl">
                                 <course.icon className="text-white" size={24} />
                             </div>
                          </div>
                          
                          {/* Content */}
                          <div className="p-5">
                              <div className="flex justify-between items-start mb-2">
                                  <h3 className="font-bold text-lg text-slate-800 leading-tight">{course.title}</h3>
                              </div>
                              <p className="text-sm text-slate-500 mb-4 leading-relaxed">{course.description}</p>
                              
                              {/* Progress Bar */}
                              <div className="space-y-1.5">
                                  <div className="flex justify-between text-xs font-bold text-slate-400 uppercase tracking-wide">
                                      <span>{course.progress}% Completo</span>
                                      <span>{Math.ceil((course.progress / 100) * course.totalModules)}/{course.totalModules} Mods</span>
                                  </div>
                                  <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                                      <div 
                                        className={`h-full rounded-full bg-gradient-to-r ${course.gradient}`} 
                                        style={{ width: `${course.progress}%` }}
                                      ></div>
                                  </div>
                              </div>
                          </div>
                      </div>
                  ))}
              </div>
          </div>
      );
  }

  // --- Render: Result Screen ---
  if (viewMode === 'RESULT') {
       return (
          <div className="h-full flex flex-col items-center justify-center px-6 pb-24 pt-10 animate-fade-in">
             <div className="bg-white p-6 rounded-full mb-6 border border-slate-100 shadow-sm">
                 <FimMascot emotion={lives > 0 ? "happy" : "worried"} size="xl" />
             </div>
             <h2 className="text-3xl font-black text-slate-800 mb-2 tracking-tight">
                 {lives > 0 ? "Mandou bem!" : "Não desiste!"}
             </h2>
             <p className="text-slate-500 mb-8 text-center font-medium">
                 {lives > 0 ? `Você acertou ${score} de ${QUIZ_SAMPLE.length}` : "Você ficou sem vidas. Revise os tópicos e tente de novo!"}
             </p>
             
             {lives > 0 && (
                <Card className="w-full mb-6 flex flex-col items-center py-8">
                    <Trophy className="text-finap-gold fill-finap-gold mb-2" size={48} />
                    <p className="font-black text-2xl text-finap-dark">+{score * 50} XP</p>
                    <p className="text-xs text-slate-400 uppercase font-bold tracking-wider mt-1">Recompensa Ganha</p>
                </Card>
             )}

             <button 
               onClick={() => {
                   setViewMode('TRAIL');
                   setLives(stats?.lives || 5); // Reset lives for demo
               }}
               className="w-full bg-finap-primary text-white font-bold py-4 rounded-xl shadow-lg shadow-teal-500/30 active:scale-95 transition-transform"
             >
               Voltar pro Caminho
             </button>
          </div>
       );
  }

  // --- Render: Content Screen (Apostila) ---
  if (viewMode === 'CONTENT' && activeModule) {
      const contentPages = MODULE_CONTENT[activeModule.id] || [];
      const currentPage = contentPages[currentContentPage];
      const isLastPage = currentContentPage === contentPages.length - 1;

      if (!currentPage) {
          // Fallback if no content exists
          return (
              <div className="pb-24 px-4 pt-4 h-full flex flex-col items-center justify-center">
                  <p className="text-slate-500 mb-4">Conteúdo não disponível para este módulo.</p>
                  <button
                      onClick={() => setViewMode('INTRO')}
                      className="bg-finap-primary text-white font-bold py-3 px-6 rounded-xl"
                  >
                      Voltar
                  </button>
              </div>
          );
      }

      return (
          <div className="pb-24 h-full flex flex-col animate-fade-in bg-gradient-to-b from-teal-50 to-white">
              {/* Header */}
              <div className="bg-white p-4 border-b border-slate-200 flex items-center justify-between sticky top-0 z-20 shadow-sm">
                  <button
                      onClick={() => setViewMode('INTRO')}
                      className="p-2 hover:bg-slate-100 rounded-full transition-colors"
                  >
                      <ArrowLeft size={24} className="text-slate-600" />
                  </button>

                  <div className="flex items-center gap-2">
                      <BookOpen size={20} className="text-finap-primary" />
                      <span className="font-bold text-slate-700 text-sm">
                          Página {currentContentPage + 1} de {contentPages.length}
                      </span>
                  </div>

                  <div className="w-10"></div> {/* Spacer */}
              </div>

              {/* Progress Dots */}
              <div className="flex justify-center gap-2 py-3 bg-white border-b border-slate-100">
                  {contentPages.map((_, idx) => (
                      <div
                          key={idx}
                          className={`h-2 rounded-full transition-all ${
                              idx === currentContentPage
                                  ? 'w-8 bg-finap-primary'
                                  : 'w-2 bg-slate-200'
                          }`}
                      />
                  ))}
              </div>

              {/* Content Area */}
              <div className="flex-1 overflow-y-auto px-4 pt-6 pb-6">
                  <div className="max-w-2xl mx-auto">
                      {/* Title with Icon */}
                      <div className="flex items-start gap-3 mb-6">
                          <div className="bg-finap-primary/10 p-3 rounded-xl">
                              <Sparkles className="text-finap-primary" size={28} />
                          </div>
                          <div className="flex-1">
                              <h1 className="text-2xl font-black text-slate-800 leading-tight">
                                  {currentPage.title}
                              </h1>
                          </div>
                      </div>

                      {/* Content Card */}
                      <Card className="bg-white shadow-sm border-slate-200 mb-6">
                          <div className="prose prose-slate max-w-none">
                              {currentPage.content.split('\n\n').map((paragraph, idx) => {
                                  // Check if paragraph is a heading (starts with **)
                                  if (paragraph.trim().startsWith('**') && paragraph.trim().endsWith('**')) {
                                      const text = paragraph.replace(/\*\*/g, '');
                                      return (
                                          <h3 key={idx} className="text-lg font-bold text-finap-dark mt-4 mb-2">
                                              {text}
                                          </h3>
                                      );
                                  }

                                  // Check if it's a list item
                                  if (paragraph.trim().startsWith('•') || paragraph.trim().startsWith('💰') || paragraph.trim().startsWith('🎮') || paragraph.trim().startsWith('🏦')) {
                                      return (
                                          <p key={idx} className="text-slate-700 leading-relaxed ml-2 mb-2">
                                              {paragraph.split('**').map((part, i) =>
                                                  i % 2 === 0 ? part : <strong key={i} className="font-bold text-slate-900">{part}</strong>
                                              )}
                                          </p>
                                      );
                                  }

                                  // Regular paragraph
                                  return (
                                      <p key={idx} className="text-slate-700 leading-relaxed mb-4">
                                          {paragraph.split('**').map((part, i) =>
                                              i % 2 === 0 ? part : <strong key={i} className="font-bold text-slate-900">{part}</strong>
                                          )}
                                      </p>
                                  );
                              })}
                          </div>
                      </Card>

                      {/* FIM Mascot Tip */}
                      <div className="bg-teal-50 border-2 border-teal-200 rounded-2xl p-4 flex gap-3 items-start">
                          <div className="flex-shrink-0">
                              <FimMascot size="sm" emotion="happy" />
                          </div>
                          <div className="flex-1">
                              <p className="text-sm font-bold text-teal-900 mb-1">Dica do FIM:</p>
                              <p className="text-sm text-teal-800 leading-relaxed">
                                  {isLastPage
                                      ? "Agora que você leu tudo, está pronto pro quiz! Boa sorte, mano! 🚀"
                                      : "Leia com calma, essas dicas vão te ajudar no quiz! 📚"
                                  }
                              </p>
                          </div>
                      </div>
                  </div>
              </div>

              {/* Navigation Buttons */}
              <div className="bg-white border-t border-slate-200 p-4 flex gap-3">
                  {currentContentPage > 0 && (
                      <button
                          onClick={() => setCurrentContentPage(prev => prev - 1)}
                          className="flex-1 bg-slate-100 text-slate-700 font-bold py-4 rounded-xl hover:bg-slate-200 transition-colors"
                      >
                          Anterior
                      </button>
                  )}

                  <button
                      onClick={() => {
                          if (isLastPage) {
                              setViewMode('QUIZ');
                              setCurrentQuestionIndex(0);
                              setScore(0);
                              setSelectedOption(null);
                              setIsAnswerChecked(false);
                          } else {
                              setCurrentContentPage(prev => prev + 1);
                          }
                      }}
                      className="flex-1 bg-finap-primary text-white font-bold py-4 rounded-xl shadow-lg shadow-teal-500/30 active:scale-95 transition-transform flex items-center justify-center gap-2"
                  >
                      {isLastPage ? (
                          <>
                              <Play size={20} fill="currentColor" /> Fazer Quiz
                          </>
                      ) : (
                          <>
                              Próxima <ChevronRight size={20} />
                          </>
                      )}
                  </button>
              </div>
          </div>
      );
  }

  // --- Render: Quiz Screen ---
  if (viewMode === 'QUIZ' && activeModule) {
    const question = QUIZ_SAMPLE[currentQuestionIndex];
    const progress = ((currentQuestionIndex) / QUIZ_SAMPLE.length) * 100;

    return (
      <div className="pb-24 h-full flex flex-col animate-fade-in bg-slate-50">
         {/* Quiz Header with Lives */}
         <div className="bg-white p-4 border-b border-slate-200 flex items-center justify-between sticky top-0 z-20">
             <button onClick={() => setViewMode('INTRO')} className="p-2 hover:bg-slate-100 rounded-full transition-colors">
                 <XCircle size={24} className="text-slate-400" />
             </button>
             
             <div className="flex items-center gap-2 bg-red-50 px-3 py-1 rounded-full border border-red-100">
                 <Heart className="text-red-500 fill-red-500 animate-pulse" size={20} />
                 <span className="font-black text-red-500 text-lg">{lives}</span>
             </div>
             
             <div className="w-10 h-10"></div> {/* Spacer */}
         </div>

         {/* Progress Bar */}
         <div className="w-full bg-slate-200 h-1.5">
            <div className="bg-finap-primary h-1.5 transition-all duration-300" style={{ width: `${progress}%` }}></div>
         </div>

         <div className="px-4 pt-6 flex-grow flex flex-col">
            <Card className="flex-grow flex flex-col justify-center min-h-[300px] shadow-md border-slate-200">
                {/* Feedback Mascot */}
                {isAnswerChecked && (
                    <div className="absolute -top-12 right-4">
                        <FimMascot 
                            size="sm" 
                            emotion={selectedOption === question.correctIndex ? "happy" : "worried"} 
                        />
                    </div>
                )}

                <h3 className="text-xl font-bold text-finap-dark mb-8 text-center leading-relaxed">{question.question}</h3>
                <div className="space-y-3">
                {question.options.map((opt, idx) => {
                    let btnClass = "w-full p-4 rounded-xl border-2 text-left font-bold transition-all transform active:scale-[0.98] ";
                    if (isAnswerChecked) {
                        if (idx === question.correctIndex) btnClass += "border-finap-success bg-emerald-50 text-emerald-700";
                        else if (idx === selectedOption) btnClass += "border-red-500 bg-red-50 text-red-700";
                        else btnClass += "border-slate-100 text-slate-300 opacity-50";
                    } else {
                        btnClass += selectedOption === idx ? "border-finap-primary bg-teal-50" : "border-slate-200 text-slate-600 hover:border-finap-primary hover:bg-slate-50 shadow-sm";
                    }

                    return (
                        <button 
                            key={idx} 
                            onClick={() => handleAnswer(idx)}
                            disabled={isAnswerChecked}
                            className={btnClass}
                        >
                            <div className="flex justify-between items-center">
                            {opt}
                            {isAnswerChecked && idx === question.correctIndex && <CheckCircle2 size={20} className="text-finap-success" />}
                            {isAnswerChecked && idx === selectedOption && idx !== question.correctIndex && <XCircle size={20} className="text-red-500" />}
                            </div>
                        </button>
                    )
                })}
                </div>
            </Card>
         </div>
      </div>
    );
  }

  // --- Render: Intro Screen (Module Details) ---
  if (viewMode === 'INTRO' && activeModule) {
      return (
        <div className="pb-24 px-4 pt-4 h-full flex flex-col animate-fade-in">
            <button onClick={() => setViewMode('TRAIL')} className="self-start mb-4 p-2 bg-white rounded-full border border-slate-200 text-slate-500">
                <ArrowLeft size={24} />
            </button>

            <div className="flex-1 flex flex-col items-center">
                <div className="w-24 h-24 bg-teal-100 rounded-full flex items-center justify-center mb-6 border-4 border-white shadow-lg">
                    <BookOpen size={40} className="text-finap-primary" />
                </div>

                <h1 className="text-2xl font-black text-slate-800 text-center mb-2">{activeModule.title}</h1>
                <p className="text-slate-500 text-center mb-8 px-4 leading-relaxed">{activeModule.description}</p>

                <Card className="w-full mb-6 bg-slate-50 border-slate-200">
                    <h3 className="font-bold text-slate-700 mb-4 uppercase text-xs tracking-widest">O que você vai aprender</h3>
                    <ul className="space-y-3">
                        {activeModule.topics.map((topic, i) => (
                            <li key={i} className="flex items-center gap-3">
                                <div className="w-6 h-6 rounded-full bg-finap-primary text-white flex items-center justify-center text-xs font-bold">
                                    {i + 1}
                                </div>
                                <span className="text-slate-700 font-medium">{topic}</span>
                            </li>
                        ))}
                    </ul>
                </Card>
            </div>

            <button
                onClick={startLesson}
                className="w-full bg-finap-primary text-white font-bold py-4 rounded-xl shadow-lg shadow-teal-500/30 active:scale-95 transition-transform flex items-center justify-center gap-2"
            >
                <Play size={20} fill="currentColor" /> Começar Lição
            </button>
        </div>
      )
  }

  // --- Render: Trail View (Specific Course) ---
  return (
    <div className="pb-24 pt-6 animate-fade-in min-h-screen bg-finap-bg">
       {/* Back Button + Header */}
       <div className="px-4 mb-8 relative">
          <button 
            onClick={() => setViewMode('COURSES')}
            className="absolute left-4 top-1 p-2 bg-white border border-slate-200 rounded-full text-slate-500 hover:bg-slate-50"
          >
              <ArrowLeft size={20} />
          </button>
          <div className="text-center">
              <h1 className="text-2xl font-black text-slate-800 tracking-tight">{activeCourse?.title}</h1>
              <p className="text-slate-500 text-sm font-medium">Caminho de Aprendizado</p>
          </div>
       </div>

       <div className="relative flex flex-col items-center pb-10 px-4">
          {/* Winding Path Line Background */}
          <svg className="absolute top-0 left-0 w-full h-full -z-10 pointer-events-none" viewBox="0 0 100 1000" preserveAspectRatio="none">
              <path d="M 50 50 L 50 1000" stroke="#E2E8F0" strokeWidth="8" strokeLinecap="round" />
          </svg>

          {MODULES.map((mod, index) => {
              // Visual Logic for status
              const isLocked = mod.status === 'locked';
              const isCurrent = mod.status === 'current';
              const isCompleted = mod.status === 'completed';

              let circleColorClass = "";
              let icon = null;

              if (isLocked) {
                  // Orange for unavailable/locked modules
                  circleColorClass = "bg-orange-200 border-orange-300 text-orange-400";
                  icon = <Lock size={24} />;
              } else if (isCurrent) {
                  // Green/Success for current active module
                  circleColorClass = "bg-finap-success border-emerald-600 text-white shadow-[0_0_20px_rgba(16,185,129,0.4)] scale-110 z-10";
                  icon = <Play size={28} fill="currentColor" className="ml-1" />;
              } else {
                  // Teal for completed
                  circleColorClass = "bg-finap-primary border-teal-600 text-white";
                  icon = <Star size={24} fill="currentColor" />;
              }

              // Stagger the path slightly for "game" feel (Zig Zag)
              const alignmentClass = index % 2 === 0 ? "-translate-x-8" : "translate-x-8";

              return (
                  <div key={mod.id} className={`relative mb-12 ${alignmentClass} flex flex-col items-center group`}>
                      
                      {/* The Node Circle */}
                      <button 
                        onClick={() => handleModuleClick(mod)}
                        disabled={isLocked}
                        className={`
                            w-20 h-20 rounded-full border-b-4 flex items-center justify-center transition-all duration-300
                            ${circleColorClass}
                            ${isLocked ? 'cursor-not-allowed' : 'cursor-pointer active:scale-95 hover:-translate-y-1'}
                        `}
                      >
                          {icon}
                      </button>

                      {/* Star Rating for completed */}
                      {isCompleted && (
                          <div className="absolute -top-2 -right-2 flex gap-0.5">
                              <Star size={12} className="text-finap-gold fill-finap-gold" />
                              <Star size={12} className="text-finap-gold fill-finap-gold" />
                              <Star size={12} className="text-finap-gold fill-finap-gold" />
                          </div>
                      )}

                      {/* Current Pulse Effect */}
                      {isCurrent && (
                          <div className="absolute inset-0 bg-finap-success rounded-full animate-ping opacity-30 -z-10"></div>
                      )}

                      {/* Label Card */}
                      <div className={`
                          absolute top-full mt-3 bg-white px-3 py-2 rounded-xl shadow-sm border border-slate-100 whitespace-nowrap
                          ${isLocked ? 'opacity-60' : 'opacity-100'}
                      `}>
                          <p className={`text-xs font-bold ${isLocked ? 'text-slate-400' : 'text-slate-700'}`}>
                              Mod {mod.id}: {mod.title}
                          </p>
                      </div>
                  </div>
              );
          })}

          {/* FIM Assistant Button / Interaction */}
          <div className="mt-8 relative w-full max-w-xs flex flex-col items-center">
              
              {/* Chat Bubble Container (Conditional) */}
              {showFimChat && (
                  <div className="absolute bottom-24 w-72 bg-white rounded-2xl shadow-2xl border border-slate-100 p-0 flex flex-col overflow-hidden animate-fade-in z-30">
                      
                      {/* Header */}
                      <div className="bg-finap-primary p-3 flex justify-between items-center">
                          <div className="flex items-center gap-2">
                              <div className="w-2 h-2 bg-white rounded-full animate-pulse"></div>
                              <span className="text-white font-bold text-sm">Ajuda do FIM</span>
                          </div>
                          <button onClick={() => setShowFimChat(false)} className="text-white/80 hover:text-white">
                              <X size={16} />
                          </button>
                      </div>

                      {/* Messages */}
                      <div className="h-48 overflow-y-auto p-3 space-y-3 bg-slate-50">
                          {fimMessages.map(msg => (
                              <div key={msg.id} className={`text-xs p-2 rounded-lg max-w-[90%] ${msg.role === 'user' ? 'bg-finap-primary text-white ml-auto rounded-tr-none' : 'bg-white border border-slate-200 text-slate-700 mr-auto rounded-tl-none'}`}>
                                  {msg.text}
                              </div>
                          ))}
                          {isFimLoading && (
                              <div className="flex gap-1 ml-2">
                                  <span className="w-1 h-1 bg-slate-400 rounded-full animate-bounce"></span>
                                  <span className="w-1 h-1 bg-slate-400 rounded-full animate-bounce" style={{animationDelay: '100ms'}}></span>
                                  <span className="w-1 h-1 bg-slate-400 rounded-full animate-bounce" style={{animationDelay: '200ms'}}></span>
                              </div>
                          )}
                          <div ref={fimMessagesEndRef}></div>
                      </div>

                      {/* Input */}
                      <div className="p-2 bg-white border-t border-slate-100 flex gap-2">
                          <input 
                              type="text" 
                              value={fimInput}
                              onChange={(e) => setFimInput(e.target.value)}
                              onKeyDown={(e) => e.key === 'Enter' && handleFimSend()}
                              className="flex-1 text-xs bg-slate-50 rounded-full px-3 py-1 outline-none border border-transparent focus:border-finap-primary"
                              placeholder="Pergunte sobre o curso..."
                          />
                          <button 
                            onClick={handleFimSend}
                            disabled={isFimLoading || !fimInput.trim()}
                            className="bg-finap-primary p-1.5 rounded-full text-white hover:bg-teal-600 disabled:opacity-50"
                          >
                              <Send size={14} />
                          </button>
                      </div>
                      
                      {/* Triangle Pointer */}
                      <div className="absolute -bottom-2 left-1/2 -translate-x-1/2 w-4 h-4 bg-white rotate-45 border-b border-r border-slate-100"></div>
                  </div>
              )}

              <button 
                onClick={() => setShowFimChat(!showFimChat)}
                className="group relative flex flex-col items-center transition-transform active:scale-95"
              >
                  <div className={`${showFimChat ? 'scale-110' : 'animate-pulse'}`}>
                      <FimMascot size="md" emotion="happy" />
                  </div>
                  
                  <span className="mt-2 text-xs font-bold text-slate-400 bg-white/50 px-2 py-0.5 rounded-full backdrop-blur-sm">
                      {showFimChat ? 'Fechar Ajuda' : 'Toque pra Ajuda'}
                  </span>
              </button>
          </div>
       </div>
    </div>
  );
};