"""
Transaction Schemas
Request and response schemas for transaction endpoints.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from models.transaction import TransactionType, TransactionSource


class TransactionCreate(BaseModel):
    """Schema for creating a transaction"""
    type: TransactionType
    amount: float = Field(gt=0, description="Transaction amount (must be positive)")
    category: str = Field(min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=255)
    date: Optional[datetime] = None
    tags: List[str] = Field(default_factory=list)
    is_recurrent: bool = False
    recurrence_period: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "type": "expense",
                "amount": 45.50,
                "category": "alimentação",
                "description": "Almoço no restaurante",
                "date": "2024-11-20T12:30:00",
                "tags": ["restaurante", "almoço"],
                "is_recurrent": False
            }
        }


class TransactionUpdate(BaseModel):
    """Schema for updating a transaction"""
    amount: Optional[float] = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=255)
    date: Optional[datetime] = None
    tags: Optional[List[str]] = None
    is_recurrent: Optional[bool] = None
    recurrence_period: Optional[str] = None


class TransactionResponse(BaseModel):
    """Schema for transaction response"""
    id: str
    user_id: str
    type: TransactionType
    amount: float
    category: str
    description: Optional[str]
    date: datetime
    source: TransactionSource
    tags: List[str]
    is_recurrent: bool
    created_at: datetime
    updated_at: datetime


class TransactionListResponse(BaseModel):
    """Schema for transaction list response"""
    transactions: List[TransactionResponse]
    total: int
    page: int
    limit: int
    total_pages: int


class CategorySummary(BaseModel):
    """Summary by category"""
    category: str
    amount: float
    percentage: float
    count: int


class DashboardSummary(BaseModel):
    """Dashboard summary response"""
    period: str
    total_income: float
    total_expenses: float
    balance: float
    savings_rate: float
    categories: List[CategorySummary]
    transaction_count: int
    recent_transactions: List[TransactionResponse]


# Analytics Schemas

class CategoryBreakdown(BaseModel):
    """Category breakdown with color"""
    name: str
    amount: float
    percentage: float
    color: str


class SpendingBreakdownResponse(BaseModel):
    """Spending breakdown response"""
    time_range: str
    period_label: str
    start_date: str
    end_date: str
    total_expenses: float
    categories: List[CategoryBreakdown]
    transaction_count: int


class RecentTransactionsResponse(BaseModel):
    """Recent transactions response with pagination"""
    transactions: List[dict]
    total: int
    limit: int
    offset: int
    has_more: bool


class MonthlyTrend(BaseModel):
    """Monthly trend data"""
    month: str
    income: float
    expenses: float
    balance: float


class SpendingTrendsResponse(BaseModel):
    """Spending trends response"""
    months: int
    trends: List[MonthlyTrend]


class CategoryStatsResponse(BaseModel):
    """Category statistics response"""
    category: str
    time_range: str
    total: float
    count: int
    average: float
    max: float
    min: float
    color: str
