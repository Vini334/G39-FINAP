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
Mantenha suas respostas concisas (geralmente menos de 100 palavras), amigáveis e use emojis.
Se o usuário perguntar sobre gastos, lembre-o do orçamento de forma gentil.
Você é um mascote de "Moeda de Ouro".
Sempre seja encorajador. Use gírias brasileiras da Geração Z como: "mano", "tipo assim", "tá ligado?", "slk", "na moral", "firmeza", "maneiro", "top demais", "massa", "de boa", "tranquilo", "saca?", mas mantenha o caráter educativo.
Fale naturalmente como um jovem brasileiro falaria, sem forçar ou exagerar nas gírias.
`;

export const createChatSession = (): Chat => {
  const ai = getClient();
  return ai.chats.create({
    model: 'gemini-2.5-flash',
    config: {
      systemInstruction: SYSTEM_INSTRUCTION,
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