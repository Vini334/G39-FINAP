"""
WhatsApp Routes
API endpoints for WhatsApp webhook integration with Meta API.
Based on docs/API.md and docs/ARCHITECTURE.md
"""

import sys

# Fix Windows UTF-8 encoding for emojis
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

from fastapi import APIRouter, Request, Response, HTTPException, Query
from fastapi.responses import PlainTextResponse, JSONResponse
from typing import Optional, Dict, Any
from datetime import datetime

from services.whatsapp_service import WhatsAppService
from services.transaction_service import TransactionService
from models.transaction import Transaction, TransactionType, TransactionSource
from schemas.transaction import TransactionCreate
from core.database import get_firestore_client
from core.config import settings


router = APIRouter()
whatsapp_service = WhatsAppService()
transaction_service = TransactionService()


@router.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(alias="hub.mode"),
    hub_verify_token: str = Query(alias="hub.verify_token"),
    hub_challenge: str = Query(alias="hub.challenge")
):
    """
    Meta WhatsApp webhook verification endpoint (GET).
    A Meta faz uma requisição GET para verificar o webhook.

    Args:
        hub_mode: Deve ser 'subscribe'
        hub_verify_token: Token de verificação
        hub_challenge: Código de desafio a ser retornado

    Returns:
        Challenge string se verificado com sucesso
    """
    print(f"📞 Webhook verification request")
    print(f"Mode: {hub_mode}, Token: {hub_verify_token}")

    if hub_mode == "subscribe" and hub_verify_token == settings.META_WHATSAPP_VERIFY_TOKEN:
        print("✅ Webhook verified successfully")
        return int(hub_challenge)
    else:
        print("❌ Webhook verification failed")
        raise HTTPException(status_code=403, detail="Verification failed")


@router.post("/webhook")
async def whatsapp_webhook(request: Request) -> Dict[str, str]:
    """
    Meta WhatsApp webhook endpoint (POST).
    Receives messages from users and processes them.

    This endpoint receives POST requests from Meta when a user sends
    a WhatsApp message to the configured number.

    Returns:
        JSON response confirming receipt
    """
    try:
        # Parse incoming webhook data
        body = await request.json()
        print(f"📱 Webhook received: {body}")

        # Meta sends the webhook in this format
        if body.get("object") == "whatsapp_business_account":
            entries = body.get("entry", [])

            for entry in entries:
                changes = entry.get("changes", [])

                for change in changes:
                    value = change.get("value", {})

                    # Check if it's a message
                    messages = value.get("messages", [])

                    for message in messages:
                        message_id = message.get("id")
                        from_number = message.get("from")  # Número do remetente
                        message_type = message.get("type")

                        print(f"📨 Message from {from_number}, type: {message_type}")

                        # Processar apenas mensagens de texto
                        if message_type == "text":
                            text_body = message.get("text", {}).get("body", "")

                            print(f"💬 Text: {text_body}")

                            # Marcar mensagem como lida
                            try:
                                await whatsapp_service.mark_message_as_read(message_id)
                            except Exception as e:
                                print(f"⚠️ Could not mark as read: {e}")

                            # Processar a mensagem
                            parsed_data = await whatsapp_service.process_incoming_message(
                                from_number=from_number,
                                body=text_body
                            )

                            print(f"🔍 Parsed intent: {parsed_data.get('intent')}")

                            # Buscar usuário pelo telefone
                            user = await get_user_by_phone(from_number)

                            if not user:
                                # Usuário não encontrado
                                response_text = whatsapp_service.format_response('user_not_found', {})
                                await whatsapp_service.send_message(from_number, response_text)
                                continue

                            user_id = user['uid']

                            # Processar diferentes tipos de intent
                            intent = parsed_data.get('intent')

                            if intent == 'expense':
                                response_text = await handle_expense(
                                    user_id=user_id,
                                    amount=parsed_data['amount'],
                                    description=parsed_data['description'],
                                    category=parsed_data['category']
                                )

                            elif intent == 'income':
                                response_text = await handle_income(
                                    user_id=user_id,
                                    amount=parsed_data['amount'],
                                    description=parsed_data['description']
                                )

                            elif intent == 'balance':
                                response_text = await handle_balance(user_id=user_id)

                            elif intent == 'help':
                                response_text = whatsapp_service.format_response('help', {})

                            else:
                                response_text = whatsapp_service.format_response('error', {})

                            # Enviar resposta
                            await whatsapp_service.send_message(from_number, response_text)
                            print(f"✅ Response sent: {response_text[:50]}...")

        # Meta espera um 200 OK response
        return {"status": "ok"}

    except Exception as e:
        print(f"❌ Error processing webhook: {e}")
        import traceback
        traceback.print_exc()
        # Ainda retornar 200 para não causar retries da Meta
        return {"status": "error", "message": str(e)}


async def get_user_by_phone(phone_number: str) -> Optional[dict]:
    """
    Get user from Firestore by phone number.

    Args:
        phone_number: User phone number

    Returns:
        User dict or None if not found
    """
    try:
        db = get_firestore_client()
        users_ref = db.collection('users')

        # Query for user with this phone number
        query = users_ref.where('phone', '==', phone_number).limit(1)
        docs = query.stream()

        for doc in docs:
            user_data = doc.to_dict()
            user_data['uid'] = doc.id
            return user_data

        return None
    except Exception as e:
        print(f"⚠️ Error getting user by phone: {e}")
        return None


async def handle_expense(
    user_id: str,
    amount: float,
    description: str,
    category: str
) -> str:
    """
    Handle expense transaction creation.

    Args:
        user_id: User ID
        amount: Transaction amount
        description: Transaction description
        category: Auto-categorized category

    Returns:
        Formatted response message
    """
    try:
        # Create transaction
        transaction_data = TransactionCreate(
            type=TransactionType.EXPENSE,
            amount=amount,
            category=category,
            description=description,
            date=datetime.now(),
            tags=[],
            is_recurrent=False
        )

        # Save transaction (source will be set to WHATSAPP)
        transaction = await transaction_service.create_transaction(
            transaction_data=transaction_data,
            user_id=user_id
        )

        # Update source to WhatsApp
        db = get_firestore_client()
        db.collection('transactions').document(transaction.id).update({
            'source': TransactionSource.WHATSAPP.value
        })

        # Get current balance
        summary = await transaction_service.get_summary(user_id=user_id)
        balance = summary['balance']

        # Format response
        response_text = whatsapp_service.format_response(
            'expense_created',
            {
                'amount': amount,
                'category': category,
                'balance': balance
            }
        )

        # TODO: Award XP for WhatsApp transaction (10 XP)
        # await gamification_service.award_xp(user_id, 10, 'whatsapp_transaction')

        return response_text

    except Exception as e:
        print(f"❌ Error creating expense: {e}")
        return whatsapp_service.format_response('error', {})


async def handle_income(
    user_id: str,
    amount: float,
    description: str
) -> str:
    """
    Handle income transaction creation.

    Args:
        user_id: User ID
        amount: Transaction amount
        description: Transaction description

    Returns:
        Formatted response message
    """
    try:
        # Create transaction
        transaction_data = TransactionCreate(
            type=TransactionType.INCOME,
            amount=amount,
            category='receita',
            description=description,
            date=datetime.now(),
            tags=[],
            is_recurrent=False
        )

        # Save transaction
        transaction = await transaction_service.create_transaction(
            transaction_data=transaction_data,
            user_id=user_id
        )

        # Update source to WhatsApp
        db = get_firestore_client()
        db.collection('transactions').document(transaction.id).update({
            'source': TransactionSource.WHATSAPP.value
        })

        # Get current balance
        summary = await transaction_service.get_summary(user_id=user_id)
        balance = summary['balance']

        # Format response
        response_text = whatsapp_service.format_response(
            'income_created',
            {
                'amount': amount,
                'description': description,
                'balance': balance
            }
        )

        # TODO: Award XP for WhatsApp transaction (10 XP)
        # await gamification_service.award_xp(user_id, 10, 'whatsapp_transaction')

        return response_text

    except Exception as e:
        print(f"❌ Error creating income: {e}")
        return whatsapp_service.format_response('error', {})


async def handle_balance(user_id: str) -> str:
    """
    Handle balance query.

    Args:
        user_id: User ID

    Returns:
        Formatted balance summary message
    """
    try:
        # Get summary for current month
        summary = await transaction_service.get_summary(user_id=user_id)

        # Format top expenses
        top_expenses_lines = []
        for i, cat_summary in enumerate(summary['categories'][:3], 1):
            top_expenses_lines.append(
                f"{i}. {cat_summary.category}: R$ {cat_summary.amount:.2f}"
            )

        top_expenses_text = '\n'.join(top_expenses_lines) if top_expenses_lines else "Nenhum gasto registrado"

        # Format response
        response_text = whatsapp_service.format_response(
            'balance',
            {
                'balance': summary['balance'],
                'income': summary['total_income'],
                'expenses': summary['total_expenses'],
                'top_expenses': top_expenses_text
            }
        )

        return response_text

    except Exception as e:
        print(f"❌ Error getting balance: {e}")
        return whatsapp_service.format_response('error', {})


@router.get("/test")
async def test_whatsapp():
    """
    Test endpoint to verify WhatsApp service is configured.
    """
    try:
        # Try to initialize WhatsApp service
        service = WhatsAppService()

        return {
            "success": True,
            "message": "WhatsApp service is configured",
            "phone_id": service.phone_number_id,
            "api_version": service.api_version
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"WhatsApp service configuration error: {str(e)}"
        }
