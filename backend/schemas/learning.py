"""
Learning Schemas
Request and response schemas for learning endpoints.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict
from models.learning import ModuleStatus, QuestionType


# Request Schemas

class StartModuleRequest(BaseModel):
    """Request to start a learning module"""
    user_id: str
    module_id: str


class CompleteLessonRequest(BaseModel):
    """Request to mark lesson as completed"""
    user_id: str
    module_id: str
    lesson_id: str


class SubmitQuizRequest(BaseModel):
    """Request to submit quiz answers"""
    user_id: str
    module_id: str
    quiz_id: str
    answers: Dict[str, int]  # question_id -> selected_option_index
    time_taken_seconds: Optional[int] = None


# Response Schemas

class LessonResponse(BaseModel):
    """Lesson response"""
    id: str
    title: str
    content: str
    duration_minutes: int
    order: int
    completed: bool = False


class QuestionResponse(BaseModel):
    """Question response (without correct answer)"""
    id: str
    question: str
    options: List[str]
    type: QuestionType = QuestionType.MULTIPLE_CHOICE


class QuizResponse(BaseModel):
    """Quiz response"""
    id: str
    title: str
    description: Optional[str] = None
    questions: List[QuestionResponse]
    passing_score: int
    xp_reward: int
    coins_reward: int
    lives_cost: int
    attempts: int = 0
    best_score: int = 0
    completed: bool = False


class ModuleProgressResponse(BaseModel):
    """Module progress response"""
    module_id: str
    status: ModuleStatus
    lessons_completed: List[str]
    total_lessons: int
    lessons_progress_percentage: int
    quiz_attempts: int
    quiz_best_score: int
    quiz_completed: bool
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class LearningModuleResponse(BaseModel):
    """Learning module response"""
    id: str
    title: str
    description: str
    icon: str
    lessons: List[LessonResponse]
    quiz: QuizResponse
    xp_reward: int
    coins_reward: int
    estimated_duration_minutes: int
    difficulty: str
    progress: Optional[ModuleProgressResponse] = None


class QuizQuestionResult(BaseModel):
    """Individual question result"""
    question_id: str
    question: str
    selected_answer: int
    correct_answer: int
    is_correct: bool
    explanation: Optional[str] = None


class QuizResultResponse(BaseModel):
    """Quiz result response"""
    quiz_id: str
    score: int
    passed: bool
    total_questions: int
    correct_answers: int
    incorrect_answers: int
    xp_earned: int
    coins_earned: int
    lives_spent: int
    feedback: str
    question_results: List[QuizQuestionResult]
    level_up: bool = False
    new_level: Optional[int] = None


class ModulesListResponse(BaseModel):
    """List of learning modules"""
    modules: List[LearningModuleResponse]
    total: int


class UserProgressSummary(BaseModel):
    """User's overall learning progress"""
    total_modules: int
    completed_modules: int
    in_progress_modules: int
    total_quizzes_taken: int
    average_quiz_score: float
    total_xp_earned: int
    total_time_spent_minutes: int
