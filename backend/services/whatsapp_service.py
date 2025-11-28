"""
WhatsApp Service
Business logic for WhatsApp integration using Meta WhatsApp Business API.
Based on docs/PROJECT_CONFIG.md and docs/ARCHITECTURE.md
"""

from core.config import settings
from typing import Dict, Optional
import re
import httpx
import json


class WhatsAppService:
    """Service for WhatsApp message processing and integration"""

    def __init__(self):
        """Initialize Meta WhatsApp Business API client"""
        self.api_token = settings.META_WHATSAPP_TOKEN
        self.phone_number_id = settings.META_WHATSAPP_PHONE_ID
        self.api_version = settings.META_WHATSAPP_API_VERSION
        self.base_url = f"https://graph.facebook.com/{self.api_version}/{self.phone_number_id}"

    async def send_message(
        self,
        to: str,
        body: str,
        media_url: Optional[str] = None
    ) -> Dict:
        """
        Send message via WhatsApp using Meta API.

        Args:
            to: Recipient phone number (e.g., '5511999999999' - without + or whatsapp:)
            body: Message text
            media_url: Optional media URL to attach

        Returns:
            Response dict with message_id
        """
        # Remove caracteres não numéricos do número
        clean_number = re.sub(r'[^\d]', '', to)

        url = f"{self.base_url}/messages"
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

        # Payload básico para mensagem de texto
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": clean_number,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": body
            }
        }

        # Se houver mídia, muda o tipo da mensagem
        if media_url:
            payload["type"] = "image"
            payload["image"] = {
                "link": media_url
            }
            # Remove o campo text quando enviar imagem
            del payload["text"]

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()

        return result

    async def process_incoming_message(
        self,
        from_number: str,
        body: str
    ) -> Dict:
        """
        Process incoming WhatsApp message and extract information.

        Args:
            from_number: Sender phone number
            body: Message text

        Returns:
            Dictionary with parsed intent and data
        """
        # Normalize text
        text = body.lower().strip()

        # Try to match patterns
        result = self._parse_message(text)

        return result

    def _parse_message(self, text: str) -> Dict:
        """
        Parse message text and extract intent and data.

        Supported patterns (from docs/PROJECT_CONFIG.md):
        - Expense: "gastei {valor} no/na/em {descrição}"
        - Income: "recebi {valor} de/do/da {descrição}"
        - Balance: "saldo", "extrato", "resumo"
        - Help: "ajuda", "help", "comandos"

        Args:
            text: Normalized message text (lowercase)

        Returns:
            Dictionary with intent, amount, description, category
        """
        # Patterns for extracting information
        patterns = {
            'expense': [
                r'gastei?\s+(?:r\$)?\s*(\d+(?:[.,]\d{1,2})?)\s+(?:no|na|em|de|do|da)?\s*(.+)',
                r'paguei?\s+(?:r\$)?\s*(\d+(?:[.,]\d{1,2})?)\s+(?:no|na|em|de|do|da)?\s*(.+)',
                r'comprei?\s+(.+?)\s+(?:por|p/)?\s*(?:r\$)?\s*(\d+(?:[.,]\d{1,2})?)'
            ],
            'income': [
                r'recebi?\s+(?:r\$)?\s*(\d+(?:[.,]\d{1,2})?)\s+(?:de|do|da)?\s*(.+)',
                r'ganhei?\s+(?:r\$)?\s*(\d+(?:[.,]\d{1,2})?)\s+(?:com|de|do|da)?\s*(.+)'
            ],
            'balance': [
                r'^(?:saldo|extrato|resumo)$'
            ],
            'help': [
                r'^(?:ajuda|help|comandos|\?)$'
            ]
        }

        # Try expense patterns
        for pattern in patterns['expense']:
            match = re.search(pattern, text)
            if match:
                # Handle different group orders
                groups = match.groups()
                if pattern.startswith(r'comprei'):
                    # "comprei X por Y" - description first, then amount
                    description = groups[0].strip()
                    amount_str = groups[1]
                else:
                    # "gastei Y em X" - amount first, then description
                    amount_str = groups[0]
                    description = groups[1].strip() if len(groups) > 1 else ""

                amount = float(amount_str.replace(',', '.'))
                return {
                    'intent': 'expense',
                    'amount': amount,
                    'description': description,
                    'category': self._infer_category(description)
                }

        # Try income patterns
        for pattern in patterns['income']:
            match = re.search(pattern, text)
            if match:
                amount = float(match.group(1).replace(',', '.'))
                description = match.group(2).strip() if len(match.groups()) > 1 else ""
                return {
                    'intent': 'income',
                    'amount': amount,
                    'description': description,
                    'category': 'receita'
                }

        # Try balance pattern
        for pattern in patterns['balance']:
            if re.search(pattern, text):
                return {'intent': 'balance'}

        # Try help pattern
        for pattern in patterns['help']:
            if re.search(pattern, text):
                return {'intent': 'help'}

        # Unknown intent
        return {
            'intent': 'unknown',
            'text': text
        }

    def _infer_category(self, description: str) -> str:
        """
        Infer transaction category based on description keywords.
        Based on category keywords from docs/PROJECT_CONFIG.md

        Args:
            description: Transaction description

        Returns:
            Category name
        """
        # Category keywords (from PROJECT_CONFIG.md)
        categories = {
            'alimentação': [
                'mercado', 'supermercado', 'açougue', 'feira',
                'restaurante', 'lanche', 'almoço', 'jantar',
                'café', 'padaria', 'ifood', 'delivery', 'pizza',
                'hamburger', 'comida', 'bebida', 'bar'
            ],
            'transporte': [
                'uber', '99', 'taxi', 'ônibus', 'metrô', 'metro',
                'gasolina', 'álcool', 'alcool', 'combustível', 'combustivel',
                'estacionamento', 'pedágio', 'pedagio'
            ],
            'moradia': [
                'aluguel', 'condomínio', 'condominio', 'luz', 'energia',
                'água', 'agua', 'gás', 'gas', 'internet', 'telefone'
            ],
            'lazer': [
                'cinema', 'teatro', 'show', 'festa', 'bar', 'balada',
                'netflix', 'spotify', 'amazon', 'prime',
                'jogos', 'jogo', 'livro'
            ],
            'saúde': [
                'farmácia', 'farmacia', 'remédio', 'remedio',
                'médico', 'medico', 'consulta', 'exame',
                'dentista', 'psicólogo', 'psicologo', 'terapia'
            ],
            'educação': [
                'curso', 'faculdade', 'escola', 'livro',
                'apostila', 'material', 'mensalidade', 'aula'
            ],
            'compras': [
                'roupa', 'sapato', 'presente', 'shopping',
                'loja', 'calça', 'calca', 'camisa', 'tênis', 'tenis'
            ]
        }

        description_lower = description.lower()

        # Check each category
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in description_lower:
                    return category

        # Default category
        return 'outros'

    def format_response(self, response_type: str, data: Dict) -> str:
        """
        Format response message for WhatsApp.
        Based on templates from docs/PROJECT_CONFIG.md

        Args:
            response_type: Type of response
            data: Data to format into template

        Returns:
            Formatted message text
        """
        templates = {
            'expense_created': """✅ Registrado!
💸 Débito: R$ {amount:.2f}
📁 Categoria: {category}
💰 Saldo atual: R$ {balance:.2f}""",

            'income_created': """💰 Boa! Dinheiro entrando!
➕ Receita: R$ {amount:.2f}
📝 {description}
💵 Saldo atual: R$ {balance:.2f}""",

            'balance': """📊 Seu resumo financeiro:

💰 Saldo: R$ {balance:.2f}
📈 Receitas do mês: R$ {income:.2f}
📉 Gastos do mês: R$ {expenses:.2f}

*Top 3 Gastos:*
{top_expenses}

Use "ajuda" para ver mais comandos! 😊""",

            'help': """🤖 *Comandos Disponíveis:*

💸 *Registrar gasto:*
"Gastei 50 no mercado"

💰 *Registrar receita:*
"Recebi 1000 de salário"

📊 *Ver saldo:*
"Saldo" ou "Extrato"

❓ *Ajuda:*
"Ajuda" ou "?"

Estou sempre aqui para ajudar! 😊""",

            'error': """🤔 Não entendi sua mensagem...

Tente algo como:
• "Gastei 30 no almoço"
• "Recebi 1000 de salário"
• "Saldo" para ver resumo

Digite "ajuda" para ver todos os comandos! 💡""",

            'user_not_found': """👋 Olá! Parece que você ainda não tem uma conta no FINAP.

Por favor, crie sua conta no app primeiro para começar a usar o WhatsApp! 📱

Baixe o app em: [link do app]"""
        }

        template = templates.get(response_type, templates['error'])

        try:
            return template.format(**data)
        except KeyError:
            # If data is missing keys, return error message
            return templates['error']

    async def mark_message_as_read(self, message_id: str) -> Dict:
        """
        Mark message as read in Meta WhatsApp API.

        Args:
            message_id: ID of the message to mark as read

        Returns:
            API response
        """
        url = f"{self.base_url}/messages"
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
