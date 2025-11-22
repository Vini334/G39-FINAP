"""
Gamification Models
Defines structures for gamification elements (challenges, rewards, badges).
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict
from enum import Enum


class XPAction(str, Enum):
    """XP action types"""
    DAILY_LOGIN = "daily_login"
    ADD_TRANSACTION = "add_transaction"
    ADD_TRANSACTION_WHATSAPP = "add_transaction_whatsapp"
    COMPLETE_QUIZ = "complete_quiz"
    COMPLETE_QUIZ_PERFECT = "complete_quiz_perfect"
    COMPLETE_MODULE = "complete_module"
    COMPLETE_CHALLENGE = "complete_challenge"
    MAINTAIN_STREAK_7 = "maintain_streak_7"
    FIRST_TRANSACTION_DAY = "first_transaction_day"
    REVIEW_MONTHLY_REPORT = "review_monthly_report"


class XPReward(BaseModel):
    """XP reward configuration"""
    action: XPAction
    amount: int
    description: str


# XP Rewards Table (based on PROJECT_CONFIG.md)
XP_REWARDS = {
    XPAction.DAILY_LOGIN: XPReward(
        action=XPAction.DAILY_LOGIN,
        amount=10,
        description="Login diário"
    ),
    XPAction.ADD_TRANSACTION: XPReward(
        action=XPAction.ADD_TRANSACTION,
        amount=5,
        description="Registrar transação manualmente"
    ),
    XPAction.ADD_TRANSACTION_WHATSAPP: XPReward(
        action=XPAction.ADD_TRANSACTION_WHATSAPP,
        amount=10,
        description="Registrar transação via WhatsApp"
    ),
    XPAction.COMPLETE_QUIZ: XPReward(
        action=XPAction.COMPLETE_QUIZ,
        amount=30,
        description="Completar quiz (>70%)"
    ),
    XPAction.COMPLETE_QUIZ_PERFECT: XPReward(
        action=XPAction.COMPLETE_QUIZ_PERFECT,
        amount=50,
        description="Completar quiz (100%)"
    ),
    XPAction.COMPLETE_MODULE: XPReward(
        action=XPAction.COMPLETE_MODULE,
        amount=80,
        description="Completar módulo de aprendizado"
    ),
    XPAction.COMPLETE_CHALLENGE: XPReward(
        action=XPAction.COMPLETE_CHALLENGE,
        amount=100,
        description="Completar desafio semanal"
    ),
    XPAction.MAINTAIN_STREAK_7: XPReward(
        action=XPAction.MAINTAIN_STREAK_7,
        amount=70,
        description="Manter streak de 7 dias"
    ),
    XPAction.FIRST_TRANSACTION_DAY: XPReward(
        action=XPAction.FIRST_TRANSACTION_DAY,
        amount=15,
        description="Primeira transação do dia"
    ),
    XPAction.REVIEW_MONTHLY_REPORT: XPReward(
        action=XPAction.REVIEW_MONTHLY_REPORT,
        amount=25,
        description="Revisar relatório mensal"
    ),
}


class Level(BaseModel):
    """Level definition"""
    level: int
    min_xp: int
    max_xp: Optional[int]
    title: str


# Levels configuration (based on PROJECT_CONFIG.md)
LEVELS = [
    Level(level=1, min_xp=0, max_xp=99, title="Iniciante Financeiro"),
    Level(level=2, min_xp=100, max_xp=299, title="Aprendiz Econômico"),
    Level(level=3, min_xp=300, max_xp=599, title="Poupador Bronze"),
    Level(level=4, min_xp=600, max_xp=999, title="Poupador Prata"),
    Level(level=5, min_xp=1000, max_xp=1499, title="Poupador Ouro"),
    Level(level=6, min_xp=1500, max_xp=2499, title="Gestor Financeiro"),
    Level(level=7, min_xp=2500, max_xp=3999, title="Investidor Júnior"),
    Level(level=8, min_xp=4000, max_xp=5999, title="Investidor Pleno"),
    Level(level=9, min_xp=6000, max_xp=8999, title="Investidor Sênior"),
    Level(level=10, min_xp=9000, max_xp=None, title="Mestre das Finanças"),
]


class LivesConfig(BaseModel):
    """Lives system configuration"""
    max_lives: int = 5
    recharge_time_hours: int = 5
    cost_quiz_retry: int = 1
    cost_skip_challenge: int = 2
    cost_unlock_hint: int = 1


class CoinsReward(BaseModel):
    """Coins reward configuration"""
    action: str
    amount: int


# Coins rewards (based on PROJECT_CONFIG.md)
COINS_REWARDS = {
    "daily_login": CoinsReward(action="daily_login", amount=5),
    "complete_quiz": CoinsReward(action="complete_quiz", amount=20),
    "complete_challenge": CoinsReward(action="complete_challenge", amount=50),
    "perfect_week": CoinsReward(action="perfect_week", amount=100),
}


class Badge(BaseModel):
    """Badge model"""
    id: str
    name: str
    description: str
    icon: str
    requirement: str
    xp_reward: int = 0


class ChallengeStatus(str, Enum):
    """Challenge status"""
    ACTIVE = "active"
    COMPLETED = "completed"
    EXPIRED = "expired"
    FAILED = "failed"


class ChallengeType(str, Enum):
    """Challenge type"""
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    SPECIAL = "special"


class Challenge(BaseModel):
    """Challenge model"""
    id: Optional[str] = None
    user_id: str
    type: ChallengeType
    title: str
    description: str
    target: float  # Target value (e.g., save R$50)
    current: float = 0.0  # Current progress
    reward_xp: int = 100
    reward_coins: int = 50
    status: ChallengeStatus = ChallengeStatus.ACTIVE
    starts_at: datetime
    expires_at: datetime
    completed_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class XPTransaction(BaseModel):
    """XP transaction record"""
    id: Optional[str] = None
    user_id: str
    action: XPAction
    xp_amount: int
    description: str
    metadata: Dict = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class LivesRecharge(BaseModel):
    """Lives recharge calculation"""
    current_lives: int
    max_lives: int
    last_recharge: datetime
    next_recharge: datetime
    recharge_time_remaining_minutes: int


class MissionType(str, Enum):
    """Mission type"""
    DAILY_LOGIN = "daily_login"
    ADD_TRANSACTION = "add_transaction"
    COMPLETE_QUIZ = "complete_quiz"
    VIEW_REPORT = "view_report"
    CHAT_FIM = "chat_fim"
    LEARN_MODULE = "learn_module"


class MissionStatus(str, Enum):
    """Mission status"""
    PENDING = "pending"
    COMPLETED = "completed"
    EXPIRED = "expired"


class Mission(BaseModel):
    """Daily mission model"""
    id: Optional[str] = None
    user_id: str
    type: MissionType
    title: str
    description: str
    xp_reward: int
    coins_reward: int = 0
    status: MissionStatus = MissionStatus.PENDING
    progress: int = 0  # Current progress (0-100%)
    target: int = 1  # Target to complete (e.g., 1 login, 3 transactions)
    date: str  # Date in YYYY-MM-DD format (missions reset daily)
    completed_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
