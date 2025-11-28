import React, { useState, useRef, useEffect } from 'react';
import { Card } from '../components/Card';
import { CheckCircle2, XCircle, BookOpen, Trophy, Heart, ArrowLeft, Lock, Star, Play, TrendingUp, PiggyBank, Wallet, Send, X, RefreshCw, ChevronRight, Sparkles, Loader2, Rocket } from 'lucide-react';
import { FimMascot } from '../components/FimMascot';
import { Message } from '../types';
import { createChatSession, sendMessageToFim } from '../services/geminiService';
import { Chat as GeminiChat } from '@google/genai';
import { useAuth } from '../contexts/AuthContext';
import { useGamification, GamificationStats } from '../contexts/GamificationContext';
import { learningService, Course as APICourse, ModuleWithPhases, Phase, PhaseQuizResult } from '../services/learningService';
import { missionService } from '../services';

interface LearnProps {
    stats?: GamificationStats;
}

type ViewMode = 'COURSES' | 'TRAIL' | 'INTRO' | 'CONTENT' | 'QUIZ' | 'RESULT';

// Local interface for display (mapped from API)
interface DisplayCourse {
    id: string;
    title: string;
    description: string;
    icon: React.ElementType;
    color: string;
    progress: number;
    totalModules: number;
    completedModules: number;
    gradient: string;
    locked?: boolean;
    lockedMessage?: string;
}

// Phase status type
type PhaseStatus = 'locked' | 'current' | 'completed';

// Icon mapping for courses from API
const COURSE_ICONS: { [key: string]: React.ElementType } = {
    'Wallet': Wallet,
    'PiggyBank': PiggyBank,
    'TrendingUp': TrendingUp,
    'BookOpen': BookOpen,
    'Rocket': Rocket,
};

// Map API course to display course
const mapApiCourseToDisplay = (course: APICourse): DisplayCourse => ({
    id: course.id,
    title: course.title,
    description: course.description,
    icon: COURSE_ICONS[course.icon] || PiggyBank,
    color: course.color || "text-emerald-500",
    gradient: course.gradient || "from-emerald-400 to-teal-600",
    progress: course.progress_percentage || 0,
    totalModules: course.total_modules || 0,
    completedModules: course.modules_completed || 0,
    locked: (course as any).locked || false,
    lockedMessage: (course as any).locked_message || '',
});

export const Learn: React.FC<LearnProps> = ({ stats }) => {
  // Contexts
  const { user } = useAuth();
  const { addXP, addCoins, refreshStats } = useGamification();

  // View state
  const [viewMode, setViewMode] = useState<ViewMode>('COURSES');
  const [activeCourse, setActiveCourse] = useState<DisplayCourse | null>(null);

  // API data state
  const [courses, setCourses] = useState<DisplayCourse[]>([]);
  const [currentModule, setCurrentModule] = useState<ModuleWithPhases | null>(null);
  const [activePhase, setActivePhase] = useState<Phase | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Quiz state
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedOption, setSelectedOption] = useState<number | null>(null);
  const [isAnswerChecked, setIsAnswerChecked] = useState(false);
  const [quizAnswers, setQuizAnswers] = useState<Record<string, number>>({});
  const [quizResult, setQuizResult] = useState<PhaseQuizResult | null>(null);
  const [lives, setLives] = useState(stats?.lives || 5);

  // Content state
  const [currentContentPage, setCurrentContentPage] = useState(0);

  // FIM Mini Chat State
  const [showFimChat, setShowFimChat] = useState(false);
  const [fimMessages, setFimMessages] = useState<Message[]>([]);
  const [fimInput, setFimInput] = useState('');
  const [isFimLoading, setIsFimLoading] = useState(false);
  const fimChatSessionRef = useRef<GeminiChat | null>(null);
  const fimMessagesEndRef = useRef<HTMLDivElement>(null);

  // Ref for trail container to scroll to top
  const trailContainerRef = useRef<HTMLDivElement>(null);

  // Load courses on mount
  useEffect(() => {
    loadCourses();
  }, [user?.uid]);

  // Check for direct module navigation from Overview
  useEffect(() => {
    const openModuleId = sessionStorage.getItem('openModuleId');
    if (openModuleId && courses.length > 0) {
      // Clear the stored module ID
      sessionStorage.removeItem('openModuleId');

      // Find the course that contains this module and open it
      const course = courses.find(c => !c.locked);
      if (course) {
        setActiveCourse(course);
        loadModule(openModuleId);
        setViewMode('TRAIL');
      }
    }
  }, [courses]);

  const loadCourses = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const apiCourses = await learningService.getCourses(user?.uid);
      const displayCourses = apiCourses.map(mapApiCourseToDisplay);
      setCourses(displayCourses);
    } catch (err) {
      console.error('Failed to load courses:', err);
      setError('Erro ao carregar cursos');
    } finally {
      setIsLoading(false);
    }
  };

  const loadModule = async (moduleId: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const module = await learningService.getModuleWithPhases(moduleId, user?.uid);
      setCurrentModule(module);

      // Start module if not started
      if (user?.uid && module.status === 'not_started') {
        await learningService.startModuleV2(moduleId, user.uid);
      }
    } catch (err) {
      console.error('Failed to load module:', err);
      setError('Erro ao carregar módulo');
    } finally {
      setIsLoading(false);
    }
  };

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

            // Trigger CHAT_FIM mission
            if (user?.uid) {
              missionService.triggerChatFim(user.uid).catch(console.error);
            }
          }
      } catch (e) {
          console.error(e);
      } finally {
          setIsFimLoading(false);
      }
  };

  const handleCourseClick = async (course: DisplayCourse) => {
      // Don't allow clicking locked courses
      if (course.locked) return;

      setActiveCourse(course);
      // For MVP, we load the first module (Mentalidade Financeira)
      await loadModule('mod_mentalidade_financeira');
      setViewMode('TRAIL');
      setShowFimChat(false);

      // Scroll to top of trail view
      setTimeout(() => {
        trailContainerRef.current?.scrollTo({ top: 0, behavior: 'smooth' });
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }, 100);
  };

  const handlePhaseClick = (phase: Phase) => {
      if (phase.status === 'locked') return;
      setActivePhase(phase);
      setViewMode('INTRO');
      // Scroll to top when entering INTRO view
      window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const startLesson = () => {
    setCurrentContentPage(0);
    setViewMode('CONTENT');
    // Scroll to top when entering CONTENT view
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const startQuiz = () => {
    setCurrentQuestionIndex(0);
    setQuizAnswers({});
    setQuizResult(null);
    setViewMode('QUIZ');
    setSelectedOption(null);
    setIsAnswerChecked(false);
    // Scroll to top when entering QUIZ view
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleAnswer = async (index: number) => {
    if (isAnswerChecked || !activePhase) return;
    setSelectedOption(index);
    setIsAnswerChecked(true);

    const question = activePhase.quiz.questions[currentQuestionIndex];
    const newAnswers = { ...quizAnswers, [question.id]: index };
    setQuizAnswers(newAnswers);

    // Check if answer is correct
    const isCorrect = index === question.correct_answer;

    // Decrement lives if wrong
    if (!isCorrect) {
      setLives(prev => Math.max(0, prev - 1));
    }

    // Check if last question or out of lives
    const isLastQuestion = currentQuestionIndex >= activePhase.quiz.questions.length - 1;
    const newLives = isCorrect ? lives : lives - 1;

    setTimeout(async () => {
       if (!isLastQuestion && newLives > 0) {
          setCurrentQuestionIndex(prev => prev + 1);
          setSelectedOption(null);
          setIsAnswerChecked(false);
       } else {
          // Submit quiz to API
          if (user?.uid && currentModule) {
            try {
              console.log('Submitting quiz answers:', newAnswers);
              const result = await learningService.submitPhaseQuiz(
                user.uid,
                currentModule.id,
                activePhase.id,
                newAnswers
              );
              console.log('Quiz result:', result);
              setQuizResult(result);

              // Trigger COMPLETE_QUIZ mission
              if (result.passed) {
                missionService.triggerCompleteQuiz(user.uid).catch(console.error);
              }

              // Update local gamification state
              if (result.xp_earned > 0) {
                addXP(result.xp_earned);
              }
              if (result.coins_earned > 0) {
                addCoins(result.coins_earned);
              }

              // Refresh stats from server
              refreshStats();

              // Reload module to get updated progress
              await loadModule(currentModule.id);

              // Only go to RESULT after everything succeeded
              setViewMode('RESULT');
              window.scrollTo({ top: 0, behavior: 'smooth' });
            } catch (err) {
              console.error('Failed to submit quiz:', err);
              // Set a fallback result to show error state
              setQuizResult({
                phase_id: activePhase.id,
                quiz_id: activePhase.quiz?.id || '',
                score: 0,
                stars: 0,
                passed: false,
                correct_answers: 0,
                total_questions: activePhase.quiz?.questions?.length || 0,
                xp_earned: 0,
                coins_earned: 0,
                feedback: 'Erro ao enviar quiz. Tente novamente.',
                question_results: [],
                next_phase_unlocked: false,
                module_completed: false
              });
              setViewMode('RESULT');
              window.scrollTo({ top: 0, behavior: 'smooth' });
            }
          } else {
            // No user or module, still show result with empty state
            setQuizResult({
              phase_id: activePhase?.id || '',
              quiz_id: activePhase?.quiz?.id || '',
              score: 0,
              stars: 0,
              passed: false,
              correct_answers: 0,
              total_questions: activePhase?.quiz?.questions?.length || 0,
              xp_earned: 0,
              coins_earned: 0,
              feedback: 'Erro: usuário não autenticado.',
              question_results: [],
              next_phase_unlocked: false,
              module_completed: false
            });
            setViewMode('RESULT');
            window.scrollTo({ top: 0, behavior: 'smooth' });
          }
       }
    }, 1500);
  };

  const completeLesson = async (lessonId: string) => {
    if (!user?.uid || !currentModule || !activePhase) return;

    try {
      await learningService.completePhaseLesson(
        user.uid,
        currentModule.id,
        activePhase.id,
        lessonId
      );
    } catch (err) {
      console.error('Failed to complete lesson:', err);
    }
  };

  // --- Render: Courses List (Overview) ---
  if (viewMode === 'COURSES') {
      // Loading state
      if (isLoading) {
        return (
          <div className="pb-24 px-4 pt-4 animate-fade-in flex items-center justify-center min-h-[60vh]">
            <div className="text-center">
              <Loader2 className="w-8 h-8 animate-spin text-finap-primary mx-auto mb-2" />
              <p className="text-slate-500 text-sm">Carregando cursos...</p>
            </div>
          </div>
        );
      }

      // Error state
      if (error) {
        return (
          <div className="pb-24 px-4 pt-4 animate-fade-in flex items-center justify-center min-h-[60vh]">
            <div className="text-center">
              <p className="text-red-500 mb-4">{error}</p>
              <button
                onClick={loadCourses}
                className="bg-finap-primary text-white px-4 py-2 rounded-lg font-bold"
              >
                Tentar novamente
              </button>
            </div>
          </div>
        );
      }

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
                  {courses.map((course) => (
                      <div
                        key={course.id}
                        onClick={() => handleCourseClick(course)}
                        className={`group relative bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden transition-all ${
                          course.locked
                            ? 'cursor-not-allowed opacity-70'
                            : 'cursor-pointer hover:-translate-y-1 hover:shadow-md'
                        }`}
                      >
                          {/* Locked Overlay */}
                          {course.locked && (
                            <div className="absolute inset-0 z-10 flex items-center justify-center bg-white/60 backdrop-blur-[1px]">
                              <div className="text-center p-4">
                                <div className="bg-slate-200 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-2">
                                  <Lock size={24} className="text-slate-500" />
                                </div>
                                <p className="text-xs text-slate-500 font-medium max-w-[200px]">
                                  {course.lockedMessage || 'Em breve'}
                                </p>
                              </div>
                            </div>
                          )}

                          {/* Course Card Header / Background */}
                          <div className={`h-24 bg-gradient-to-r ${course.gradient} relative overflow-hidden ${course.locked ? 'grayscale' : ''}`}>
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
                                      <span>{course.completedModules}/{course.totalModules} Mods</span>
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
       const passed = quizResult?.passed ?? false;
       const stars = quizResult?.stars ?? 0;
       const xpEarned = quizResult?.xp_earned ?? 0;
       const coinsEarned = quizResult?.coins_earned ?? 0;
       const correctAnswers = quizResult?.correct_answers ?? 0;
       const totalQuestions = quizResult?.total_questions ?? 3;

       return (
          <div className="h-full flex flex-col items-center justify-center px-6 pb-24 pt-10 animate-fade-in">
             <div className="bg-white p-6 rounded-full mb-6 border border-slate-100 shadow-sm">
                 <FimMascot emotion={passed ? "happy" : "worried"} size="xl" />
             </div>
             <h2 className="text-3xl font-black text-slate-800 mb-2 tracking-tight">
                 {passed ? "Mandou bem!" : "Não desiste!"}
             </h2>
             <p className="text-slate-500 mb-4 text-center font-medium">
                 {passed
                   ? `Você acertou ${correctAnswers} de ${totalQuestions}`
                   : "Revise os tópicos e tente de novo!"}
             </p>

             {/* Stars Display */}
             {passed && (
               <div className="flex gap-2 mb-6">
                 {[1, 2, 3].map((s) => (
                   <Star
                     key={s}
                     size={32}
                     className={s <= stars ? "text-finap-gold fill-finap-gold" : "text-slate-200"}
                   />
                 ))}
               </div>
             )}

             {passed && (
                <Card className="w-full mb-6 flex flex-col items-center py-8">
                    <Trophy className="text-finap-gold fill-finap-gold mb-2" size={48} />
                    <p className="font-black text-2xl text-finap-dark">+{xpEarned} XP</p>
                    {coinsEarned > 0 && (
                      <p className="font-bold text-lg text-finap-gold">+{coinsEarned} Moedas</p>
                    )}
                    <p className="text-xs text-slate-400 uppercase font-bold tracking-wider mt-1">Recompensa Ganha</p>
                </Card>
             )}

             {/* Next phase indicator */}
             {quizResult?.next_phase_unlocked && (
               <p className="text-emerald-600 font-bold mb-4 text-center">
                 Nova fase desbloqueada!
               </p>
             )}

             {quizResult?.module_completed && (
               <p className="text-purple-600 font-bold mb-4 text-center">
                 Módulo completo! Parabéns!
               </p>
             )}

             <button
               onClick={() => {
                   setViewMode('TRAIL');
                   setLives(stats?.lives || 5);
                   setQuizResult(null);
                   // Scroll to top when returning to trail
                   setTimeout(() => {
                     trailContainerRef.current?.scrollTo({ top: 0, behavior: 'smooth' });
                     window.scrollTo({ top: 0, behavior: 'smooth' });
                   }, 100);
               }}
               className="w-full bg-finap-primary text-white font-bold py-4 rounded-xl shadow-lg shadow-teal-500/30 active:scale-95 transition-transform"
             >
               Voltar pro Caminho
             </button>
          </div>
       );
  }

  // --- Render: Content Screen (Apostila) ---
  if (viewMode === 'CONTENT' && activePhase) {
      const lessons = activePhase.lessons || [];
      const currentLesson = lessons[currentContentPage];
      const isLastPage = currentContentPage === lessons.length - 1;

      if (!currentLesson) {
          return (
              <div className="pb-24 px-4 pt-4 h-full flex flex-col items-center justify-center">
                  <p className="text-slate-500 mb-4">Conteúdo não disponível para esta fase.</p>
                  <button
                      onClick={() => { setViewMode('INTRO'); window.scrollTo({ top: 0, behavior: 'smooth' }); }}
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
                      onClick={() => { setViewMode('INTRO'); window.scrollTo({ top: 0, behavior: 'smooth' }); }}
                      className="p-2 hover:bg-slate-100 rounded-full transition-colors"
                  >
                      <ArrowLeft size={24} className="text-slate-600" />
                  </button>

                  <div className="flex items-center gap-2">
                      <BookOpen size={20} className="text-finap-primary" />
                      <span className="font-bold text-slate-700 text-sm">
                          Página {currentContentPage + 1} de {lessons.length}
                      </span>
                  </div>

                  <div className="w-10"></div>
              </div>

              {/* Progress Dots */}
              <div className="flex justify-center gap-2 py-3 bg-white border-b border-slate-100">
                  {lessons.map((_, idx) => (
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
                                  {currentLesson.title}
                              </h1>
                          </div>
                      </div>

                      {/* Content Card - Render markdown-like content */}
                      <Card className="bg-white shadow-sm border-slate-200 mb-6">
                          <div className="prose prose-slate max-w-none">
                              {currentLesson.content.split('\n\n').map((paragraph, idx) => {
                                  // Heading with #
                                  if (paragraph.trim().startsWith('# ')) {
                                      return (
                                          <h2 key={idx} className="text-xl font-black text-finap-dark mt-4 mb-3">
                                              {paragraph.replace(/^# /, '')}
                                          </h2>
                                      );
                                  }
                                  if (paragraph.trim().startsWith('## ')) {
                                      return (
                                          <h3 key={idx} className="text-lg font-bold text-finap-dark mt-4 mb-2">
                                              {paragraph.replace(/^## /, '')}
                                          </h3>
                                      );
                                  }
                                  if (paragraph.trim().startsWith('### ')) {
                                      return (
                                          <h4 key={idx} className="text-base font-bold text-slate-700 mt-3 mb-2">
                                              {paragraph.replace(/^### /, '')}
                                          </h4>
                                      );
                                  }

                                  // Blockquote
                                  if (paragraph.trim().startsWith('> ')) {
                                      return (
                                          <blockquote key={idx} className="border-l-4 border-finap-primary pl-4 py-2 my-4 bg-teal-50 rounded-r-lg">
                                              <p className="text-teal-800 font-medium italic">
                                                  {paragraph.replace(/^> /, '').split('**').map((part, i) =>
                                                      i % 2 === 0 ? part : <strong key={i} className="font-bold">{part}</strong>
                                                  )}
                                              </p>
                                          </blockquote>
                                      );
                                  }

                                  // List items
                                  if (paragraph.trim().startsWith('- ') || paragraph.trim().startsWith('• ')) {
                                      return (
                                          <p key={idx} className="text-slate-700 leading-relaxed ml-4 mb-2 flex items-start gap-2">
                                              <span className="text-finap-primary font-bold">•</span>
                                              <span>
                                                  {paragraph.replace(/^[-•] /, '').split('**').map((part, i) =>
                                                      i % 2 === 0 ? part : <strong key={i} className="font-bold text-slate-900">{part}</strong>
                                                  )}
                                              </span>
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
                                      ? "Agora que você leu tudo, está pronto pro quiz! Boa sorte, mano!"
                                      : "Leia com calma, essas dicas vão te ajudar no quiz!"}
                              </p>
                          </div>
                      </div>
                  </div>
              </div>

              {/* Navigation Buttons */}
              <div className="bg-white border-t border-slate-200 p-4 flex gap-3">
                  {currentContentPage > 0 && (
                      <button
                          onClick={() => {
                              setCurrentContentPage(prev => prev - 1);
                              window.scrollTo({ top: 0, behavior: 'smooth' });
                          }}
                          className="flex-1 bg-slate-100 text-slate-700 font-bold py-4 rounded-xl hover:bg-slate-200 transition-colors"
                      >
                          Anterior
                      </button>
                  )}

                  <button
                      onClick={async () => {
                          // Mark lesson as complete
                          await completeLesson(currentLesson.id);

                          if (isLastPage) {
                              startQuiz();
                          } else {
                              setCurrentContentPage(prev => prev + 1);
                              window.scrollTo({ top: 0, behavior: 'smooth' });
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
  if (viewMode === 'QUIZ' && activePhase) {
    const questions = activePhase.quiz?.questions || [];
    const question = questions[currentQuestionIndex];
    const totalQuestions = questions.length;
    const progress = ((currentQuestionIndex) / totalQuestions) * 100;

    if (!question) {
      return (
        <div className="pb-24 px-4 pt-4 h-full flex flex-col items-center justify-center">
          <p className="text-slate-500 mb-4">Quiz não disponível.</p>
          <button
            onClick={() => { setViewMode('INTRO'); window.scrollTo({ top: 0, behavior: 'smooth' }); }}
            className="bg-finap-primary text-white font-bold py-3 px-6 rounded-xl"
          >
            Voltar
          </button>
        </div>
      );
    }

    return (
      <div className="pb-24 h-full flex flex-col animate-fade-in bg-slate-50">
         {/* Quiz Header with Lives */}
         <div className="bg-white p-4 border-b border-slate-200 flex items-center justify-between sticky top-0 z-20">
             <button onClick={() => { setViewMode('INTRO'); window.scrollTo({ top: 0, behavior: 'smooth' }); }} className="p-2 hover:bg-slate-100 rounded-full transition-colors">
                 <XCircle size={24} className="text-slate-400" />
             </button>

             <div className="flex items-center gap-2 bg-red-50 px-3 py-1 rounded-full border border-red-100">
                 <Heart className="text-red-500 fill-red-500 animate-pulse" size={20} />
                 <span className="font-black text-red-500 text-lg">{lives}</span>
             </div>

             <div className="text-sm font-bold text-slate-500">
               {currentQuestionIndex + 1}/{totalQuestions}
             </div>
         </div>

         {/* Progress Bar */}
         <div className="w-full bg-slate-200 h-1.5">
            <div className="bg-finap-primary h-1.5 transition-all duration-300" style={{ width: `${progress}%` }}></div>
         </div>

         <div className="px-4 pt-6 flex-grow flex flex-col">
            <Card className="flex-grow flex flex-col justify-center min-h-[300px] shadow-md border-slate-200 relative">

                <h3 className="text-xl font-bold text-finap-dark mb-8 text-center leading-relaxed">{question.question}</h3>
                <div className="space-y-3">
                {question.options.map((opt, idx) => {
                    let btnClass = "w-full p-4 rounded-xl border-2 text-left font-bold transition-all transform active:scale-[0.98] ";
                    const isCorrectOption = idx === question.correct_answer;
                    const isSelectedOption = idx === selectedOption;

                    if (isAnswerChecked) {
                        // After answering: show correct/incorrect feedback
                        if (isCorrectOption) {
                            // Always highlight the correct answer in green
                            btnClass += "border-emerald-500 bg-emerald-50 text-emerald-700";
                        } else if (isSelectedOption) {
                            // User selected wrong answer - show in red
                            btnClass += "border-red-400 bg-red-50 text-red-700";
                        } else {
                            // Other options - fade out
                            btnClass += "border-slate-100 text-slate-300 opacity-50";
                        }
                    } else {
                        // Before answering: normal selection states
                        btnClass += selectedOption === idx ? "border-slate-400 bg-slate-100" : "border-slate-200 text-slate-600 hover:border-slate-400 hover:bg-slate-50 shadow-sm";
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
                            {isAnswerChecked && isCorrectOption && (
                              <CheckCircle2 size={20} className="text-emerald-500" />
                            )}
                            {isAnswerChecked && isSelectedOption && !isCorrectOption && (
                              <XCircle size={20} className="text-red-500" />
                            )}
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

  // --- Render: Intro Screen (Phase Details) ---
  if (viewMode === 'INTRO' && activePhase) {
      const lessonTitles = activePhase.lessons?.map(l => l.title) || [];
      const isCompleted = activePhase.status === 'completed';

      return (
        <div className="pb-24 px-4 pt-4 h-full flex flex-col animate-fade-in">
            <button onClick={() => { setViewMode('TRAIL'); window.scrollTo({ top: 0, behavior: 'smooth' }); }} className="self-start mb-4 p-2 bg-white rounded-full border border-slate-200 text-slate-500">
                <ArrowLeft size={24} />
            </button>

            <div className="flex-1 flex flex-col items-center">
                <div className={`w-24 h-24 rounded-full flex items-center justify-center mb-6 border-4 border-white shadow-lg ${isCompleted ? 'bg-emerald-100' : 'bg-teal-100'}`}>
                    {isCompleted ? (
                      <CheckCircle2 size={40} className="text-emerald-500" />
                    ) : (
                      <BookOpen size={40} className="text-finap-primary" />
                    )}
                </div>

                <h1 className="text-2xl font-black text-slate-800 text-center mb-2">{activePhase.title}</h1>
                <p className="text-slate-500 text-center mb-4 px-4 leading-relaxed">{activePhase.description}</p>

                {/* Stars earned */}
                {isCompleted && (
                  <div className="flex gap-1 mb-6">
                    {[1, 2, 3].map((s) => (
                      <Star
                        key={s}
                        size={24}
                        className={s <= activePhase.quiz_stars ? "text-finap-gold fill-finap-gold" : "text-slate-200"}
                      />
                    ))}
                  </div>
                )}

                {/* Rewards preview */}
                <div className="flex gap-4 mb-6">
                  <div className="bg-purple-50 px-3 py-1 rounded-full border border-purple-200">
                    <span className="text-sm font-bold text-purple-600">+{activePhase.xp_reward} XP</span>
                  </div>
                  <div className="bg-yellow-50 px-3 py-1 rounded-full border border-yellow-200">
                    <span className="text-sm font-bold text-yellow-600">+{activePhase.coins_reward} Moedas</span>
                  </div>
                </div>

                <Card className="w-full mb-6 bg-slate-50 border-slate-200">
                    <h3 className="font-bold text-slate-700 mb-4 uppercase text-xs tracking-widest">O que você vai aprender</h3>
                    <ul className="space-y-3">
                        {lessonTitles.map((title, i) => (
                            <li key={i} className="flex items-center gap-3">
                                <div className="w-6 h-6 rounded-full bg-finap-primary text-white flex items-center justify-center text-xs font-bold">
                                    {i + 1}
                                </div>
                                <span className="text-slate-700 font-medium">{title}</span>
                            </li>
                        ))}
                        <li className="flex items-center gap-3">
                            <div className="w-6 h-6 rounded-full bg-finap-gold text-white flex items-center justify-center text-xs font-bold">
                                <Star size={12} fill="currentColor" />
                            </div>
                            <span className="text-slate-700 font-medium">Quiz ({activePhase.quiz?.questions?.length || 3} perguntas)</span>
                        </li>
                    </ul>
                </Card>
            </div>

            <button
                onClick={startLesson}
                className="w-full bg-finap-primary text-white font-bold py-4 rounded-xl shadow-lg shadow-teal-500/30 active:scale-95 transition-transform flex items-center justify-center gap-2"
            >
                <Play size={20} fill="currentColor" /> {isCompleted ? 'Revisar Lição' : 'Começar Lição'}
            </button>
        </div>
      )
  }

  // --- Render: Trail View (Specific Course) ---
  // Loading state for module
  if (isLoading && viewMode === 'TRAIL') {
    return (
      <div className="pb-24 pt-6 animate-fade-in min-h-screen bg-finap-bg flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-8 h-8 animate-spin text-finap-primary mx-auto mb-2" />
          <p className="text-slate-500 text-sm">Carregando módulo...</p>
        </div>
      </div>
    );
  }

  // Get phases from current module
  const phases = currentModule?.phases || [];

  return (
    <div ref={trailContainerRef} className="pb-24 pt-6 animate-fade-in min-h-screen bg-finap-bg">
       {/* Back Button + Header */}
       <div className="px-4 mb-8 relative">
          <button
            onClick={() => {
              setViewMode('COURSES');
              setCurrentModule(null);
              window.scrollTo({ top: 0, behavior: 'smooth' });
            }}
            className="absolute left-4 top-1 p-2 bg-white border border-slate-200 rounded-full text-slate-500 hover:bg-slate-50"
          >
              <ArrowLeft size={20} />
          </button>
          <div className="text-center">
              <h1 className="text-2xl font-black text-slate-800 tracking-tight">{currentModule?.title || activeCourse?.title}</h1>
              <p className="text-slate-500 text-sm font-medium">
                {currentModule ? `${currentModule.phases_completed}/${currentModule.total_phases} fases completas` : 'Caminho de Aprendizado'}
              </p>
          </div>
       </div>

       <div className="relative flex flex-col items-center pb-10 px-4">
          {/* Winding Path Line Background */}
          <svg className="absolute top-0 left-0 w-full h-full -z-10 pointer-events-none" viewBox="0 0 100 1000" preserveAspectRatio="none">
              <path d="M 50 50 L 50 1000" stroke="#E2E8F0" strokeWidth="8" strokeLinecap="round" />
          </svg>

          {phases.map((phase, index) => {
              // Visual Logic for status
              const isLocked = phase.status === 'locked';
              const isCurrent = phase.status === 'current';
              const isCompleted = phase.status === 'completed';

              let circleColorClass = "";
              let icon = null;

              if (isLocked) {
                  circleColorClass = "bg-orange-200 border-orange-300 text-orange-400";
                  icon = <Lock size={24} />;
              } else if (isCurrent) {
                  circleColorClass = "bg-finap-success border-emerald-600 text-white shadow-[0_0_20px_rgba(16,185,129,0.4)] scale-110 z-10";
                  icon = <Play size={28} fill="currentColor" className="ml-1" />;
              } else {
                  circleColorClass = "bg-finap-primary border-teal-600 text-white";
                  icon = <Star size={24} fill="currentColor" />;
              }

              // Stagger the path slightly for "game" feel (Zig Zag)
              const alignmentClass = index % 2 === 0 ? "-translate-x-8" : "translate-x-8";

              return (
                  <div key={phase.id} className={`relative mb-12 ${alignmentClass} flex flex-col items-center group`}>

                      {/* The Node Circle */}
                      <button
                        onClick={() => handlePhaseClick(phase)}
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
                              {[1, 2, 3].map((s) => (
                                <Star
                                  key={s}
                                  size={12}
                                  className={s <= phase.quiz_stars ? "text-finap-gold fill-finap-gold" : "text-slate-300"}
                                />
                              ))}
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
                              Fase {index + 1}: {phase.title}
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