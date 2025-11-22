"""
WhatsApp Routes
API endpoints for WhatsApp webhook integration.
Based on docs/API.md and docs/ARCHITECTURE.md
"""

from fastapi import APIRouter, Request, Response, HTTPException, Form
from fastapi.responses import PlainTextResponse
from typing import Optional
from datetime import datetime

from services.whatsapp_service import WhatsAppService
from services.transaction_service import TransactionService
from models.transaction import Transaction, TransactionType, TransactionSource
from schemas.transaction import TransactionCreate
from core.database import get_firestore_client


router = APIRouter()
whatsapp_service = WhatsAppService()
transaction_service = TransactionService()


@router.post("/webhook")
async def whatsapp_webhook(
    Body: str = Form(...),
    From: str = Form(...),
    To: Optional[str] = Form(None),
    MessageSid: Optional[str] = Form(None)
) -> Response:
    """
    Twilio WhatsApp webhook endpoint.
    Receives messages from users and processes them.

    This endpoint receives POST requests from Twilio when a user sends
    a WhatsApp message to the configured number.

    Args:
        Body: Message text
        From: Sender phone number (e.g., 'whatsapp:+5511999999999')
        To: Recipient phone number (our WhatsApp number)
        MessageSid: Twilio message ID

    Returns:
        TwiML response to send back to user
    """
    try:
        # Extract phone number (remove 'whatsapp:' prefix)
        phone_number = From.replace('whatsapp:', '')

        print(f"📱 WhatsApp message received from {phone_number}: {Body}")

        # Process the message
        parsed_data = await whatsapp_service.process_incoming_message(
            from_number=phone_number,
            body=Body
        )

        print(f"🔍 Parsed intent: {parsed_data.get('intent')}")

        # Get user by phone number
        user = await get_user_by_phone(phone_number)

        if not user:
            # User not found - send registration message
            response_text = whatsapp_service.format_response(
                'user_not_found',
                {}
            )
            twiml = whatsapp_service.create_twiml_response(response_text)
            return PlainTextResponse(content=twiml, media_type="application/xml")

        user_id = user['uid']

        # Handle different intents
        intent = parsed_data.get('intent')

        if intent == 'expense':
            # Create expense transaction
            response_text = await handle_expense(
                user_id=user_id,
                amount=parsed_data['amount'],
                description=parsed_data['description'],
                category=parsed_data['category']
            )

        elif intent == 'income':
            # Create income transaction
            response_text = await handle_income(
                user_id=user_id,
                amount=parsed_data['amount'],
                description=parsed_data['description']
            )

        elif intent == 'balance':
            # Get balance summary
            response_text = await handle_balance(user_id=user_id)

        elif intent == 'help':
            # Send help message
            response_text = whatsapp_service.format_response('help', {})

        else:
            # Unknown intent - send error message
            response_text = whatsapp_service.format_response('error', {})

        # Create TwiML response
        twiml = whatsapp_service.create_twiml_response(response_text)

        print(f"✅ Response sent: {response_text[:50]}...")

        return PlainTextResponse(content=twiml, media_type="application/xml")

    except Exception as e:
        print(f"❌ Error processing WhatsApp message: {e}")
        # Send error message to user
        error_response = whatsapp_service.format_response('error', {})
        twiml = whatsapp_service.create_twiml_response(error_response)
        return PlainTextResponse(content=twiml, media_type="application/xml")


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
            "whatsapp_number": service.whatsapp_number
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"WhatsApp service configuration error: {str(e)}"
        }
