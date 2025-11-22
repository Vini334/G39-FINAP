"""
FIM Service - AI Assistant Service
Handles conversation with FIM (FINAP's AI assistant) using Google Gemini.
"""

import google.generativeai as genai
from core.config import settings
from core.database import get_firestore_client
from typing import List, Dict, Any, Optional
from datetime import datetime


class FIMService:
    """Service for FIM AI assistant interactions"""

    def __init__(self):
        # Configure Gemini API
        genai.configure(api_key=settings.GEMINI_API_KEY)

        # Model name for text generation (using older SDK version)
        self.model_name = 'models/text-bison-001'

        self.db = None

        # FIM's system prompt (personalidade)
        self.system_prompt = """
Você é o FIM, o assistente financeiro virtual do FINAP!

PERSONALIDADE:
- Você é jovem, descontraído e animado
- Fala português brasileiro com gírias da Geração Z
- Use emojis com moderação (1-2 por mensagem)
- Seja amigável, encorajador e motivador
- Nunca julgue as decisões financeiras do usuário

GÍRIAS BRASILEIRAS QUE VOCÊ USA:
- "mano", "tipo assim", "tá ligado?", "slk", "na moral", "firmeza", "maneiro"
- "massa", "top", "show", "da hora", "de boa", "tranquilo"
- Mas não exagere! Use naturalmente.

OBJETIVOS:
1. Ajudar o usuário a gerenciar suas finanças
2. Educar sobre conceitos financeiros de forma simples
3. Motivar a atingir metas financeiras
4. Sugerir melhorias nos hábitos de consumo
5. Celebrar conquistas e progresso

REGRAS IMPORTANTES:
- SEMPRE dê dicas práticas e acionáveis
- NUNCA dê conselhos de investimento específicos (ações, criptomoedas, etc)
- NUNCA use termos técnicos complexos sem explicar
- Mantenha respostas curtas e diretas (2-4 frases no máximo)
- Use bullet points quando listar várias coisas
- Se o usuário estiver desanimado, seja extra encorajador

EXEMPLOS DE COMO RESPONDER:

Usuário: "Gastei muito esse mês"
FIM: "Relaxa mano! 😊 O importante é você tá percebendo isso agora. Vamos analisar onde rolaram os maiores gastos e ver como economizar no próximo mês. Tá ligado?"

Usuário: "Como faço pra economizar?"
FIM: "Massa que você quer economizar! 💰 Aqui vão umas dicas:\n\n• Anota TODOS os gastos (até o cafézinho)\n• Define uma meta de economia mensal\n• Separa o dinheiro assim que recebe\n• Evita compras por impulso (espera 24h antes)\n\nBora começar?"

Usuário: "O que é juros compostos?"
FIM: "Show que você quer aprender! 📚 Juros compostos é tipo assim: você ganha juros sobre os juros. É o famoso 'dinheiro que trabalha pra você'. Por exemplo, se você investe R$100 e rende 10% ao mês, no primeiro mês você tem R$110. No segundo, os 10% são sobre R$110, então você ganha R$11 (e não R$10). Sacou? É o segredo pra multiplicar grana no longo prazo! 🚀"

CONTEXTO DO USUÁRIO:
Você terá acesso a informações sobre os gastos, metas e progresso do usuário.
Use essas informações para dar dicas personalizadas e relevantes.
"""

    def _get_db(self):
        """Lazy load Firestore client"""
        if self.db is None:
            self.db = get_firestore_client()
        return self.db

    async def get_user_context(self, user_id: str) -> Dict[str, Any]:
        """
        Get user's financial context for personalized responses.

        Args:
            user_id: User ID

        Returns:
            Dictionary with user's financial data
        """
        db = self._get_db()

        # Get user profile
        user_doc = db.collection('users').document(user_id).get()
        user_data = user_doc.to_dict() if user_doc.exists else {}

        # Get recent transactions (last 30 days)
        from services.transaction_service import TransactionService
        transaction_service = TransactionService()

        from datetime import timedelta
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)

        summary = await transaction_service.get_summary(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date
        )

        # Build context
        context = {
            "user_name": user_data.get('name', 'amigo'),
            "level": user_data.get('gamification', {}).get('level', 1),
            "xp": user_data.get('gamification', {}).get('xp', 0),
            "coins": user_data.get('gamification', {}).get('coins', 0),
            "total_income_30d": summary.get('total_income', 0),
            "total_expenses_30d": summary.get('total_expenses', 0),
            "balance_30d": summary.get('balance', 0),
            "savings_rate": summary.get('savings_rate', 0),
            "top_categories": [
                {"category": cat.category, "amount": cat.amount, "percentage": cat.percentage}
                for cat in summary.get('categories', [])[:3]
            ]
        }

        return context

    async def chat(
        self,
        user_id: str,
        message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        include_context: bool = True
    ) -> Dict[str, Any]:
        """
        Send a message to FIM and get a response.

        Args:
            user_id: User ID
            message: User's message
            conversation_history: Previous messages (optional)
            include_context: Whether to include user's financial context

        Returns:
            Dictionary with FIM's response and suggestions
        """
        # Get user context if requested
        context_info = ""
        if include_context:
            context = await self.get_user_context(user_id)
            context_info = f"""
INFORMAÇÕES DO USUÁRIO:
- Nome: {context['user_name']}
- Nível: {context['level']} | XP: {context['xp']} | Moedas: {context['coins']}
- Últimos 30 dias:
  * Receitas: R$ {context['total_income_30d']:.2f}
  * Despesas: R$ {context['total_expenses_30d']:.2f}
  * Saldo: R$ {context['balance_30d']:.2f}
  * Taxa de economia: {context['savings_rate']:.1f}%
"""
            if context['top_categories']:
                context_info += "\n- Top categorias de gasto:\n"
                for cat in context['top_categories']:
                    context_info += f"  * {cat['category']}: R$ {cat['amount']:.2f} ({cat['percentage']:.1f}%)\n"

        # Build full prompt
        full_prompt = f"{self.system_prompt}\n\n{context_info}\n\nMENSAGEM DO USUÁRIO:\n{message}"

        # Add conversation history if provided
        if conversation_history:
            history_text = "\n\nHISTÓRICO DA CONVERSA:\n"
            for msg in conversation_history[-5:]:  # Last 5 messages
                role = "USUÁRIO" if msg['role'] == 'user' else "FIM"
                history_text += f"{role}: {msg['content']}\n"
            full_prompt = f"{self.system_prompt}\n\n{context_info}\n\n{history_text}\n\nMENSAGEM ATUAL DO USUÁRIO:\n{message}"

        try:
            # Generate response using older SDK
            response = genai.generate_text(
                model=self.model_name,
                prompt=full_prompt,
                temperature=0.7,
                max_output_tokens=500
            )
            fim_message = response.result if response.result else "Desculpa, não consegui processar sua mensagem. 😅"

            # Generate quick reply suggestions based on context
            suggestions = self._generate_suggestions(message, context if include_context else None)

            # Save conversation to Firestore
            await self._save_message(user_id, message, fim_message)

            return {
                "response": fim_message,
                "suggestions": suggestions,
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            # Fallback response if API fails
            return {
                "response": "Opa, deu um problema aqui! 😅 Tenta de novo em alguns segundos, tá?",
                "suggestions": ["Ver meus gastos", "Dicas de economia", "Como funciona o FINAP?"],
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

    def _generate_suggestions(self, user_message: str, context: Optional[Dict] = None) -> List[str]:
        """
        Generate quick reply suggestions based on user's message.

        Args:
            user_message: User's last message
            context: User's financial context

        Returns:
            List of suggestion strings
        """
        # Default suggestions
        default_suggestions = [
            "Como economizar mais?",
            "Ver meus gastos",
            "Dicas do dia"
        ]

        # Context-aware suggestions
        message_lower = user_message.lower()

        if any(word in message_lower for word in ['economizar', 'poupar', 'guardar']):
            return [
                "Como criar um fundo de emergência?",
                "Regra 50-30-20",
                "Apps de desconto"
            ]

        if any(word in message_lower for word in ['gastei', 'comprei', 'paguei']):
            return [
                "Foi necessário esse gasto?",
                "Como evitar gastos impulsivos?",
                "Ver orçamento do mês"
            ]

        if any(word in message_lower for word in ['investir', 'investimento', 'aplicar']):
            return [
                "O que é Tesouro Direto?",
                "Diferença entre poupança e CDB",
                "Como começar a investir?"
            ]

        if any(word in message_lower for word in ['cartão', 'crédito', 'débito']):
            return [
                "Como usar cartão com segurança?",
                "Evitar dívidas no cartão",
                "Cartão ou dinheiro?"
            ]

        # If we have context, suggest based on spending patterns
        if context and context.get('top_categories'):
            top_cat = context['top_categories'][0]['category']
            return [
                f"Como economizar em {top_cat}?",
                "Analisar meus gastos",
                "Criar meta de economia"
            ]

        return default_suggestions

    async def _save_message(self, user_id: str, user_message: str, fim_response: str):
        """
        Save conversation to Firestore.

        Args:
            user_id: User ID
            user_message: User's message
            fim_response: FIM's response
        """
        db = self._get_db()

        conversation_ref = db.collection('fim_conversations').document(user_id)

        # Check if conversation exists
        conv_doc = conversation_ref.get()

        now = datetime.utcnow()

        if not conv_doc.exists:
            # Create new conversation
            conversation_ref.set({
                'user_id': user_id,
                'created_at': now,
                'updated_at': now,
                'messages': [
                    {
                        'role': 'user',
                        'content': user_message,
                        'timestamp': now
                    },
                    {
                        'role': 'assistant',
                        'content': fim_response,
                        'timestamp': now
                    }
                ]
            })
        else:
            # Append to existing conversation
            from google.cloud.firestore import ArrayUnion
            conversation_ref.update({
                'updated_at': now,
                'messages': ArrayUnion([
                    {
                        'role': 'user',
                        'content': user_message,
                        'timestamp': now
                    },
                    {
                        'role': 'assistant',
                        'content': fim_response,
                        'timestamp': now
                    }
                ])
            })

    async def get_conversation_history(self, user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Get user's conversation history with FIM.

        Args:
            user_id: User ID
            limit: Maximum number of messages to return

        Returns:
            List of messages
        """
        db = self._get_db()

        conversation_ref = db.collection('fim_conversations').document(user_id)
        conv_doc = conversation_ref.get()

        if not conv_doc.exists:
            return []

        messages = conv_doc.to_dict().get('messages', [])

        # Return last N messages
        return messages[-limit:] if len(messages) > limit else messages

    async def clear_conversation(self, user_id: str) -> bool:
        """
        Clear user's conversation history.

        Args:
            user_id: User ID

        Returns:
            True if cleared successfully
        """
        db = self._get_db()

        try:
            db.collection('fim_conversations').document(user_id).delete()
            return True
        except Exception:
            return False
