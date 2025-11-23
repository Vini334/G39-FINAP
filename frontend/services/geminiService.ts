import { GoogleGenAI, Chat, GenerateContentResponse } from "@google/genai";

const API_KEY = process.env.API_KEY || '';

// Debug: Log to verify API key is loaded
if (!API_KEY) {
  console.error('❌ GEMINI API KEY NOT FOUND! Check .env.local');
} else {
  console.log('✅ Gemini API Key loaded:', API_KEY.substring(0, 10) + '...');
}

let aiClient: GoogleGenAI | null = null;

const getClient = (): GoogleGenAI => {
  if (!aiClient) {
    console.log('🤖 Initializing Gemini AI client...');
    aiClient = new GoogleGenAI({ apiKey: API_KEY });
  }
  return aiClient;
};

const SYSTEM_INSTRUCTION = `Você é o FIM, um assistente financeiro divertido, animado e educativo para adolescentes e jovens adultos que usam o app FINAP.

Seu objetivo é ajudá-los a gerenciar dinheiro, economizar para metas e entender conceitos financeiros de forma simples e gamificada.

FORMATAÇÃO IMPORTANTE:
- NUNCA use markdown (**, *, _, etc.) nas respostas
- Use quebras de linha para separar tópicos e parágrafos
- Para listar itens, use apenas números ou símbolos simples (1., 2., •, →)
- Mantenha o texto limpo e bem organizado visualmente

ESTILO DE COMUNICAÇÃO:
- Adapte o tamanho da resposta à complexidade da pergunta
- Para perguntas simples: respostas concisas (50-100 palavras)
- Para perguntas complexas ou educativas: respostas detalhadas (150-300 palavras) com explicações completas
- Use emojis com moderação para deixar as mensagens mais animadas
- Seja amigável e encorajador
- Use ocasionalmente gírias brasileiras como "mano", "tipo", "tá ligado?", mas com moderação (máximo 1-2 por resposta)
- Fale de forma natural e acessível, sem forçar linguagem jovem

PAPEL:
- Você é um mascote de "Moeda de Ouro"
- Sempre seja encorajador e positivo
- Se o usuário perguntar sobre gastos, lembre-o do orçamento de forma gentil
- Mantenha sempre o caráter educativo
`;

export const createChatSession = (): Chat => {
  const ai = getClient();
  return ai.chats.create({
    model: 'gemini-2.5-flash',
    config: {
      systemInstruction: SYSTEM_INSTRUCTION,
      maxOutputTokens: 1024, // Permite respostas mais detalhadas (anteriormente ~150 tokens)
      temperature: 0.8, // Mantém criatividade e naturalidade
    },
  });
};

export const sendMessageToFim = async (chat: Chat, message: string): Promise<string> => {
  try {
    const response: GenerateContentResponse = await chat.sendMessage({ message });
    return response.text || "Opa! Meu cérebro de moeda travou. Tenta de novo?";
  } catch (error) {
    console.error("Error communicating with FIM:", error);
    return "Tô com problema pra conectar na rede financeira agora. Tenta mais tarde! 🪙";
  }
};