import React, { useState, useEffect, useRef } from 'react';
import { Message } from '../types';
import { Send, RefreshCw, Sparkles } from 'lucide-react';
import { FimMascot } from '../components/FimMascot';
import { fimService, missionService } from '../services';
import { useToast } from '../components/Toast';
import { useAuth } from '../contexts/AuthContext';

const QUICK_PROMPTS = [
  { emoji: '🍔', text: "Como economizar em delivery?" },
  { emoji: '👟', text: "Quero comprar um tênis caro" },
  { emoji: '🎮', text: "Orçamento para jogos" },
  { emoji: '🆘', text: "Gastei demais! Socorro!" },
  { emoji: '📈', text: "Como investir com R$ 10?" },
];

export const Assistant: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    { id: '0', role: 'model', text: "E aí! Eu sou o FIM 🪙. Como posso te ajudar a economizar grana hoje?", timestamp: Date.now() }
  ]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { showToast, ToastComponent } = useToast();
  const { user } = useAuth();

  useEffect(() => {
    loadChatHistory();
  }, []);

  const loadChatHistory = async () => {
    try {
      const history = await fimService.getHistory();
      if (history && history.length > 0) {
        const formattedHistory: Message[] = history.map((msg: any, index: number) => ({
          id: index.toString(),
          role: msg.role,
          text: msg.content,
          timestamp: new Date(msg.timestamp).getTime()
        }));
        setMessages([...messages, ...formattedHistory]);
      }
    } catch (error: any) {
      console.error('Erro ao carregar histórico:', error);
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async (textOverride?: string) => {
    const textToSend = textOverride || inputText;
    if (!textToSend.trim() || isLoading) return;

    const userMsg: Message = {
      id: Date.now().toString(),
      role: 'user',
      text: textToSend,
      timestamp: Date.now()
    };

    setMessages(prev => [...prev, userMsg]);
    setInputText('');
    setIsLoading(true);

    try {
      const response = await fimService.chat(textToSend, true);

      const fimMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: 'model',
        text: response.response,
        timestamp: new Date(response.timestamp).getTime()
      };

      setMessages(prev => [...prev, fimMsg]);

      // Trigger CHAT_FIM mission
      if (user?.uid) {
        missionService.triggerChatFim(user.uid).catch(console.error);
      }
    } catch (error: any) {
      console.error('Erro ao enviar mensagem:', error);
      showToast(error.message || 'Erro ao enviar mensagem', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-80px)] bg-finap-bg"> {/* Match global bg */}
      {/* Header - Clean white */}
      <div className="bg-white border-b border-slate-100 p-4 flex items-center gap-3 sticky top-0 z-10 shadow-sm">
         <div className="bg-slate-50 border border-slate-100 p-1.5 rounded-full">
             <FimMascot size="sm" />
         </div>
         <div>
            <h1 className="font-bold text-finap-dark text-base">Assistente FIM</h1>
            <p className="text-[10px] text-finap-success font-bold flex items-center gap-1 uppercase tracking-wider">
               <span className="w-1.5 h-1.5 bg-finap-success rounded-full animate-pulse"></span> Online
            </p>
         </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg) => (
          <div key={msg.id} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[85%] rounded-2xl p-4 shadow-sm text-sm leading-relaxed ${
              msg.role === 'user' 
                ? 'bg-finap-primary text-white rounded-tr-none shadow-teal-500/10' 
                : 'bg-white text-slate-700 rounded-tl-none border border-slate-100'
            }`}>
              {msg.text}
            </div>
          </div>
        ))}
        {isLoading && (
           <div className="flex justify-start">
              <div className="bg-white p-4 rounded-2xl rounded-tl-none shadow-sm border border-slate-100 flex items-center gap-2">
                 <div className="w-2 h-2 bg-slate-300 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                 <div className="w-2 h-2 bg-slate-300 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                 <div className="w-2 h-2 bg-slate-300 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
              </div>
           </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Prompts Area */}
      <div className="bg-white/50 backdrop-blur-sm px-4 pt-2 pb-1 overflow-x-auto no-scrollbar border-t border-slate-100/50">
        <div className="flex gap-2 min-w-min">
          {QUICK_PROMPTS.map((prompt, index) => (
            <button
              key={index}
              onClick={() => handleSend(prompt.text)}
              disabled={isLoading}
              className="flex items-center gap-1.5 whitespace-nowrap bg-white border border-slate-200 rounded-full px-3 py-1.5 text-xs font-medium text-slate-600 shadow-sm hover:bg-finap-primary hover:text-white hover:border-finap-primary transition-colors active:scale-95"
            >
              <span>{prompt.emoji}</span>
              <span>{prompt.text}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Input Area */}
      <div className="bg-white p-3 pt-2 border-t border-slate-100">
         <div className="flex items-center gap-2 bg-slate-50 rounded-full px-4 py-2 border border-slate-200 focus-within:border-finap-primary focus-within:bg-white focus-within:shadow-lg focus-within:shadow-teal-500/5 transition-all duration-300">
            <input 
              type="text" 
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Pergunte ao FIM sobre economias..."
              className="flex-1 bg-transparent outline-none text-finap-dark placeholder-slate-400 text-sm py-1"
            />
            <button 
               onClick={() => handleSend()}
               disabled={isLoading || !inputText.trim()}
               className="p-2 bg-finap-primary rounded-full text-white disabled:opacity-50 disabled:cursor-not-allowed hover:bg-teal-600 transition-colors shadow-md"
            >
               {isLoading ? <RefreshCw size={16} className="animate-spin" /> : <Send size={16} />}
            </button>
         </div>
      </div>

      {/* Toast Notifications */}
      {ToastComponent}
    </div>
  );
};