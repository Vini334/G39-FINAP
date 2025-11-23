/**
 * FIM Service
 * Handles communication with FIM AI Assistant
 */

import { createChatSession, sendMessageToFim } from './geminiService';
import type { Chat } from '@google/genai';
import type { ChatResponse, ConversationMessage } from '../types/api';

class FIMService {
  private chatSession: Chat | null = null;
  private conversationHistory: ConversationMessage[] = [];

  /**
   * Initialize or get existing chat session
   */
  private getChatSession(): Chat {
    if (!this.chatSession) {
      this.chatSession = createChatSession();
    }
    return this.chatSession;
  }

  /**
   * Send a message to FIM
   */
  async chat(message: string, includeContext: boolean = true): Promise<ChatResponse> {
    try {
      const chat = this.getChatSession();
      const response = await sendMessageToFim(chat, message);

      // Save to conversation history
      const timestamp = new Date().toISOString();
      this.conversationHistory.push(
        {
          role: 'user',
          content: message,
          timestamp,
        },
        {
          role: 'assistant',
          content: response,
          timestamp,
        }
      );

      // Generate suggestions based on message content
      const suggestions = this._generateSuggestions(message);

      return {
        response,
        suggestions,
        timestamp,
      };
    } catch (error) {
      throw new Error('Erro ao enviar mensagem para o FIM. Tente novamente.');
    }
  }

  /**
   * Generate quick reply suggestions
   */
  private _generateSuggestions(userMessage: string): string[] {
    const message_lower = userMessage.toLowerCase();

    if (
      message_lower.includes('economizar') ||
      message_lower.includes('poupar') ||
      message_lower.includes('guardar')
    ) {
      return [
        'Como criar um fundo de emergência?',
        'Regra 50-30-20',
        'Apps de desconto',
      ];
    }

    if (
      message_lower.includes('gastei') ||
      message_lower.includes('comprei') ||
      message_lower.includes('paguei')
    ) {
      return [
        'Foi necessário esse gasto?',
        'Como evitar gastos impulsivos?',
        'Ver orçamento do mês',
      ];
    }

    if (
      message_lower.includes('investir') ||
      message_lower.includes('investimento') ||
      message_lower.includes('aplicar')
    ) {
      return [
        'O que é Tesouro Direto?',
        'Diferença entre poupança e CDB',
        'Como começar a investir?',
      ];
    }

    if (
      message_lower.includes('cartão') ||
      message_lower.includes('crédito') ||
      message_lower.includes('débito')
    ) {
      return [
        'Como usar cartão com segurança?',
        'Evitar dívidas no cartão',
        'Cartão ou dinheiro?',
      ];
    }

    return ['Como economizar mais?', 'Ver meus gastos', 'Dicas do dia'];
  }

  /**
   * Get conversation history
   */
  async getHistory(limit: number = 20): Promise<ConversationMessage[]> {
    const start = Math.max(0, this.conversationHistory.length - limit);
    return this.conversationHistory.slice(start);
  }

  /**
   * Clear conversation history
   */
  async clearHistory(): Promise<void> {
    this.conversationHistory = [];
    this.chatSession = null; // Reset chat session
  }

  /**
   * Get suggested questions
   */
  async getSuggestions(): Promise<Record<string, string[]>> {
    return {
      'Economia': [
        'Como economizar dinheiro?',
        'O que é um fundo de emergência?',
        'Regra 50-30-20',
      ],
      'Gastos': [
        'Como controlar meus gastos?',
        'Como evitar compras por impulso?',
        'Ver meu orçamento',
      ],
      'Investimentos': [
        'Como começar a investir?',
        'O que é Tesouro Direto?',
        'Diferença entre poupança e CDB',
      ],
      'Cartões': [
        'Como usar cartão de crédito?',
        'Como evitar dívidas no cartão?',
        'Cartão ou dinheiro?',
      ],
    };
  }

  /**
   * Get spending analysis from FIM
   */
  async analyzeSpending(): Promise<{ analysis: string; suggestions: string[] }> {
    try {
      const chat = this.getChatSession();
      const analysisPrompt =
        'Pode me dar uma análise dos meus gastos recentes e sugestões de como economizar?';
      const response = await sendMessageToFim(chat, analysisPrompt);

      return {
        analysis: response,
        suggestions: [
          'Como criar um orçamento?',
          'Dicas para economizar',
          'Ver meu progresso',
        ],
      };
    } catch (error) {
      throw new Error('Erro ao analisar gastos. Tente novamente.');
    }
  }
}

// Export singleton instance
export const fimService = new FIMService();
export default fimService;
