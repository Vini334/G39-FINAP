"""
Transaction Model
Defines the structure for transaction documents in Firestore.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum


class TransactionType(str, Enum):
    """Transaction type enum"""
    INCOME = "income"
    EXPENSE = "expense"


class TransactionSource(str, Enum):
    """Transaction source enum"""
    APP = "app"
    WHATSAPP = "whatsapp"
    IMPORT = "import"


class Transaction(BaseModel):
    """
    Transaction model representing a financial transaction.
    Maps to Firestore transactions collection.
    """
    id: Optional[str] = None
    user_id: str
    type: TransactionType
    amount: float = Field(gt=0, description="Transaction amount (must be positive)")
    category: str
    description: Optional[str] = None
    date: datetime
    source: TransactionSource = TransactionSource.APP
    tags: List[str] = Field(default_factory=list)
    is_recurrent: bool = False
    recurrence_period: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class TransactionSummary(BaseModel):
    """Summary of transactions for a period"""
    total_income: float = 0.0
    total_expenses: float = 0.0
    balance: float = 0.0
    transaction_count: int = 0
    expense_count: int = 0
    income_count: int = 0
