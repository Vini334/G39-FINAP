"""
User Model
Defines the structure for user documents in Firestore.
"""

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


class UserProfile(BaseModel):
    """User profile information"""
    age: Optional[int] = None
    monthly_income: Optional[float] = None
    monthly_budget: Optional[float] = 3000.0  # Default monthly budget R$ 3000
    savings_goal: Optional[float] = None  # Monthly savings goal
    financial_goals: List[str] = []
    avatar_url: Optional[str] = None


class UserGamification(BaseModel):
    """User gamification data"""
    level: int = 1
    xp: int = 0
    coins: int = 100
    lives: int = 5
    badges: List[str] = []
    current_streak: int = 0
    longest_streak: int = 0
    last_login: datetime = datetime.now()


class User(BaseModel):
    """
    User model representing a FINAP user.
    Maps to Firestore users collection.
    """
    uid: str
    email: EmailStr
    name: str
    phone: Optional[str] = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    profile: UserProfile = UserProfile()
    gamification: UserGamification = UserGamification()
    is_active: bool = True
    is_premium: bool = False

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
