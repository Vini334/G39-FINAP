"""
Learning Models
Defines structures for learning modules, lessons, and quizzes.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict
from enum import Enum


class QuestionType(str, Enum):
    """Question type"""
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"


class Question(BaseModel):
    """Quiz question"""
    id: str
    question: str
    options: List[str]
    correct_answer: int  # Index of correct option
    explanation: Optional[str] = None
    type: QuestionType = QuestionType.MULTIPLE_CHOICE


class Quiz(BaseModel):
    """Quiz model"""
    id: str
    title: str
    description: Optional[str] = None
    questions: List[Question]
    passing_score: int = 70  # Percentage
    xp_reward: int = 50
    coins_reward: int = 20
    lives_cost: int = 1  # Cost to retry if failed


class Lesson(BaseModel):
    """Lesson model"""
    id: str
    title: str
    content: str  # Markdown content
    duration_minutes: int = 5
    order: int


class ModuleStatus(str, Enum):
    """Module completion status"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class LearningModule(BaseModel):
    """Learning module model"""
    id: Optional[str] = None
    title: str
    description: str
    icon: str = "📚"
    lessons: List[Lesson]
    quiz: Quiz
    xp_reward: int = 80
    coins_reward: int = 30
    estimated_duration_minutes: int = 30
    difficulty: str = "beginner"  # beginner, intermediate, advanced
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class UserModuleProgress(BaseModel):
    """User's progress in a learning module"""
    id: Optional[str] = None
    user_id: str
    module_id: str
    status: ModuleStatus = ModuleStatus.NOT_STARTED
    lessons_completed: List[str] = Field(default_factory=list)
    quiz_attempts: int = 0
    quiz_best_score: int = 0
    quiz_completed: bool = False
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    last_accessed: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class QuizAttempt(BaseModel):
    """Quiz attempt record"""
    id: Optional[str] = None
    user_id: str
    module_id: str
    quiz_id: str
    answers: Dict[str, int]  # question_id -> selected_option_index
    score: int  # Percentage
    passed: bool
    xp_earned: int
    coins_earned: int
    lives_spent: int = 0
    time_taken_seconds: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class QuizResult(BaseModel):
    """Quiz result with feedback"""
    score: int
    passed: bool
    total_questions: int
    correct_answers: int
    incorrect_answers: int
    xp_earned: int
    coins_earned: int
    feedback: str
    question_results: List[Dict]  # Detailed results per question
