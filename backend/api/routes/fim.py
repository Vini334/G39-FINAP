"""
FIM Assistant Routes
API endpoints for interacting with FIM, the AI financial assistant.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from schemas.fim import ChatRequest, ChatResponse, ConversationHistoryResponse, SuggestionsResponse
from schemas.common import APIResponse, SuccessResponse
from services.fim_service import FIMService
from api.dependencies.auth import get_current_user, get_current_user_optional
from typing import Optional

router = APIRouter()
fim_service = FIMService()


@router.post("/chat", response_model=APIResponse)
async def chat_with_fim(
    request: ChatRequest,
    current_user_id: str = Depends(get_current_user)
):
    """
    Send a message to FIM and get a response.

    FIM is FINAP's AI financial assistant powered by Google Gemini.
    It provides personalized financial advice, tips, and motivation.

    **Headers:**
    - Authorization: Bearer {access_token}

    **Request Body:**
    - message: Your question or message to FIM
    - include_context: Whether to include your financial data for personalized response

    **Returns:**
    - FIM's response
    - Quick reply suggestions
    - Timestamp

    **Status Codes:**
    - 200: Success
    - 401: Invalid or missing token
    - 400: Invalid message
    """
    try:
        # Get conversation history
        history = await fim_service.get_conversation_history(current_user_id, limit=10)

        # Chat with FIM
        result = await fim_service.chat(
            user_id=current_user_id,
            message=request.message,
            conversation_history=history,
            include_context=request.include_context
        )

        return APIResponse(
            success=True,
            data=result,
            message="FIM responded successfully"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get FIM response: {str(e)}"
        )


@router.get("/history", response_model=APIResponse)
async def get_chat_history(
    limit: int = 20,
    current_user_id: str = Depends(get_current_user)
):
    """
    Get conversation history with FIM.

    **Headers:**
    - Authorization: Bearer {access_token}

    **Query Parameters:**
    - limit: Maximum number of messages to return (default: 20)

    **Returns:**
    - List of messages
    - Total count

    **Status Codes:**
    - 200: Success
    - 401: Invalid or missing token
    """
    try:
        messages = await fim_service.get_conversation_history(current_user_id, limit=limit)

        return APIResponse(
            success=True,
            data={
                "messages": messages,
                "total": len(messages)
            },
            message="Conversation history retrieved successfully"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete("/history", response_model=APIResponse)
async def clear_chat_history(current_user_id: str = Depends(get_current_user)):
    """
    Clear conversation history with FIM.

    This will delete all previous messages and start a fresh conversation.

    **Headers:**
    - Authorization: Bearer {access_token}

    **Returns:**
    - Success message

    **Status Codes:**
    - 200: History cleared successfully
    - 401: Invalid or missing token
    """
    try:
        cleared = await fim_service.clear_conversation(current_user_id)

        if not cleared:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to clear conversation history"
            )

        return APIResponse(
            success=True,
            data={},
            message="Conversation history cleared successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/suggestions", response_model=APIResponse)
async def get_suggestions(
    current_user_id: Optional[str] = Depends(get_current_user_optional)
):
    """
    Get suggested questions/topics to ask FIM.

    This endpoint works both with and without authentication.
    Authenticated users get personalized suggestions based on their data.

    **Headers (optional):**
    - Authorization: Bearer {access_token}

    **Returns:**
    - List of suggested questions
    - Category

    **Status Codes:**
    - 200: Success
    """
    try:
        # Default suggestions for new users or unauthenticated
        default_suggestions = {
            "economia": [
                "Como criar um fundo de emergência?",
                "O que é a regra 50-30-20?",
                "Dicas para economizar no dia a dia"
            ],
            "educacao": [
                "O que são juros compostos?",
                "Diferença entre renda fixa e variável",
                "Como começar a investir?"
            ],
            "habitos": [
                "Como evitar compras por impulso?",
                "Como usar cartão de crédito com segurança?",
                "Dicas para não estourar o orçamento"
            ],
            "metas": [
                "Como definir metas financeiras?",
                "Como economizar para uma viagem?",
                "Quanto guardar por mês?"
            ]
        }

        # If authenticated, could personalize suggestions based on user's context
        # For MVP, return default suggestions

        return APIResponse(
            success=True,
            data={
                "categories": default_suggestions
            },
            message="Suggestions retrieved successfully"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/analyze", response_model=APIResponse)
async def analyze_spending(current_user_id: str = Depends(get_current_user)):
    """
    Get FIM's analysis of your spending patterns.

    FIM will analyze your recent transactions and provide insights,
    tips, and recommendations.

    **Headers:**
    - Authorization: Bearer {access_token}

    **Returns:**
    - FIM's detailed analysis
    - Recommendations
    - Action items

    **Status Codes:**
    - 200: Success
    - 401: Invalid or missing token
    """
    try:
        # Generate analysis prompt
        analysis_message = """
Analisa meus gastos dos últimos 30 dias e me dá um feedback completo:
- O que tá indo bem
- Onde posso melhorar
- Dicas práticas pra economizar
- Metas que posso estabelecer

Quero uma análise honesta mas motivadora! 💪
"""

        # Get analysis from FIM
        result = await fim_service.chat(
            user_id=current_user_id,
            message=analysis_message,
            include_context=True
        )

        return APIResponse(
            success=True,
            data={
                "analysis": result['response'],
                "suggestions": result['suggestions']
            },
            message="Spending analysis completed successfully"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
