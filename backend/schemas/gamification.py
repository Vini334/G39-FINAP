"""
Gamification Schemas
Request and response schemas for gamification endpoints.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from models.gamification import XPAction, ChallengeStatus, ChallengeType


# Request Schemas

class AddXPRequest(BaseModel):
    """Request to add XP to user"""
    user_id: str
    action: XPAction
    metadata: dict = {}


class SpendLivesRequest(BaseModel):
    """Request to spend user lives"""
    user_id: str
    amount: int = 1
    reason: str


class AwardCoinsRequest(BaseModel):
    """Request to award coins to user"""
    user_id: str
    amount: int
    reason: str


class CreateChallengeRequest(BaseModel):
    """Request to create a new challenge"""
    user_id: str
    type: ChallengeType
    title: str
    description: str
    target: float
    reward_xp: int = 100
    reward_coins: int = 50
    duration_days: int = 7


class UpdateChallengeProgressRequest(BaseModel):
    """Request to update challenge progress"""
    challenge_id: str
    progress: float


class UpdateMissionProgressRequest(BaseModel):
    """Request to update mission progress by type"""
    user_id: str
    mission_type: str  # daily_login, add_transaction, complete_quiz, view_report, chat_fim


# Response Schemas

class LevelInfo(BaseModel):
    """Level information"""
    level: int
    title: str
    min_xp: int
    max_xp: Optional[int]
    current_xp: int
    xp_to_next_level: Optional[int]
    progress_percentage: int


class GamificationStats(BaseModel):
    """User gamification stats"""
    user_id: str
    level_info: LevelInfo
    total_xp: int
    coins: int
    lives: int
    max_lives: int
    badges: List[str]
    current_streak: int
    longest_streak: int
    next_life_recharge: Optional[datetime]

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class XPTransactionResponse(BaseModel):
    """Response after XP transaction"""
    success: bool
    xp_added: int
    total_xp: int
    level_up: bool = False
    new_level: Optional[int] = None
    level_info: LevelInfo
    message: str


class LivesResponse(BaseModel):
    """Response with lives information"""
    success: bool
    current_lives: int
    max_lives: int
    next_recharge: Optional[datetime]
    recharge_time_remaining_minutes: int
    message: str

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class CoinsResponse(BaseModel):
    """Response after coins transaction"""
    success: bool
    coins_added: int
    total_coins: int
    message: str


class ChallengeResponse(BaseModel):
    """Challenge response"""
    id: str
    user_id: str
    type: str
    title: str
    description: str
    target: float
    current: float
    progress_percentage: int
    reward_xp: int
    reward_coins: int
    status: ChallengeStatus
    starts_at: datetime
    expires_at: datetime
    completed_at: Optional[datetime] = None
    time_remaining_hours: Optional[int] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ChallengesListResponse(BaseModel):
    """List of challenges"""
    active_challenges: List[ChallengeResponse]
    completed_challenges: List[ChallengeResponse]
    expired_challenges: List[ChallengeResponse]


class LeaderboardEntry(BaseModel):
    """Leaderboard entry"""
    rank: int
    user_id: str
    user_name: str
    level: int
    total_xp: int
    avatar_url: Optional[str] = None


class LeaderboardResponse(BaseModel):
    """Leaderboard response"""
    period: str  # weekly, monthly, all_time
    entries: List[LeaderboardEntry]
    user_rank: Optional[int] = None


# Mission Schemas

class MissionResponse(BaseModel):
    """Mission response"""
    id: str
    type: str
    title: str
    description: str
    xp_reward: int
    coins_reward: int
    status: str
    progress: int
    target: int
    completed: bool
    date: str

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class CompleteMissionResponse(BaseModel):
    """Response after completing a mission"""
    success: bool
    mission_id: str
    xp_earned: int
    coins_earned: int
    total_xp: int
    total_coins: int
    level_up: bool = False
    new_level: Optional[int] = None
    message: str


class MissionProgressResponse(BaseModel):
    """Response after updating mission progress"""
    success: bool
    mission_id: str
    mission_type: str
    title: str
    progress: int
    target: int
    completed: bool
    xp_earned: int = 0
    coins_earned: int = 0
    total_xp: Optional[int] = None
    total_coins: Optional[int] = None
    level_up: bool = False
    new_level: Optional[int] = None
    message: str


# Dashboard Schemas

class BalanceInfo(BaseModel):
    """Balance information"""
    current: float
    spent_this_month: float
    monthly_budget: float
    budget_percentage: int


class BudgetAlertInfo(BaseModel):
    """Budget alert information"""
    show: bool
    percentage: int
    message: str


class CourseProgressInfo(BaseModel):
    """Course progress information"""
    course_id: str
    course_name: str
    percentage: int
    current_module: int
    total_modules: int


class LearningProgressInfo(BaseModel):
    """Learning progress for dashboard overview"""
    course_id: str
    course_title: str
    module_id: str
    module_title: str
    current_phase: int
    total_phases: int
    progress_percentage: int
    current_phase_id: Optional[str] = None


class DashboardStats(BaseModel):
    """Dashboard statistics"""
    lives: int
    max_lives: int
    streak: int
    coins: int
    level: int
    current_xp: int
    next_level_xp: int
    xp_percentage: int


class DashboardSummaryResponse(BaseModel):
    """Dashboard summary response"""
    stats: DashboardStats
    balance: BalanceInfo
    budget_alert: BudgetAlertInfo
    missions: List[MissionResponse]
    learning_progress: Optional[LearningProgressInfo] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
