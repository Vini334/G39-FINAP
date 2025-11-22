"""
FIM Assistant Schemas
Request and response models for FIM AI assistant endpoints.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class ChatRequest(BaseModel):
    """Request to send a message to FIM"""
    message: str = Field(..., min_length=1, max_length=1000, description="User's message")
    include_context: bool = Field(True, description="Include user's financial context in response")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Como posso economizar no supermercado?",
                "include_context": True
            }
        }


class ChatResponse(BaseModel):
    """Response from FIM"""
    response: str = Field(..., description="FIM's response message")
    suggestions: List[str] = Field(default=[], description="Quick reply suggestions")
    timestamp: str = Field(..., description="Response timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "response": "Ótima pergunta! 🛒 Vou te dar umas dicas massa...",
                "suggestions": [
                    "Como fazer lista de compras?",
                    "Apps de desconto",
                    "Planejar refeições da semana"
                ],
                "timestamp": "2024-11-22T10:30:00"
            }
        }


class ConversationMessage(BaseModel):
    """Single message in conversation history"""
    role: str = Field(..., description="Message role (user or assistant)")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(..., description="Message timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "role": "user",
                "content": "Como economizar?",
                "timestamp": "2024-11-22T10:30:00"
            }
        }


class ConversationHistoryResponse(BaseModel):
    """Conversation history response"""
    messages: List[Dict[str, Any]] = Field(default=[], description="List of messages")
    total: int = Field(..., description="Total number of messages")

    class Config:
        json_schema_extra = {
            "example": {
                "messages": [
                    {
                        "role": "user",
                        "content": "Como economizar?",
                        "timestamp": "2024-11-22T10:30:00"
                    },
                    {
                        "role": "assistant",
                        "content": "Vou te dar umas dicas...",
                        "timestamp": "2024-11-22T10:30:05"
                    }
                ],
                "total": 2
            }
        }


class SuggestionsResponse(BaseModel):
    """Suggested questions/topics response"""
    suggestions: List[str] = Field(..., description="List of suggested questions")
    category: str = Field(..., description="Suggestion category")

    class Config:
        json_schema_extra = {
            "example": {
                "suggestions": [
                    "Como criar um fundo de emergência?",
                    "O que é a regra 50-30-20?",
                    "Como começar a investir?"
                ],
                "category": "economia"
            }
        }
