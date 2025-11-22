"""
Learning API Routes
Endpoints for learning modules, lessons, and quizzes.
"""

from fastapi import APIRouter, HTTPException, status
from typing import List
from services.learning_service import LearningService
from schemas.learning import (
    StartModuleRequest, CompleteLessonRequest, SubmitQuizRequest,
    LearningModuleResponse, ModulesListResponse, QuizResultResponse,
    ModuleProgressResponse, UserProgressSummary,
    LessonResponse, QuizResponse, QuestionResponse, QuizQuestionResult
)
from schemas.common import APIResponse

router = APIRouter()
learning_service = LearningService()


@router.get("/modules", response_model=APIResponse)
async def get_all_modules(user_id: str = None):
    """Get all learning modules with optional user progress"""

    try:
        modules = learning_service.get_all_modules(user_id)

        modules_response = []
        for module in modules:
            # Get user progress if user_id provided
            progress = None
            if user_id:
                user_progress = learning_service.get_user_module_progress(user_id, module.id)
                if user_progress:
                    lessons_progress_pct = int(
                        (len(user_progress.lessons_completed) / len(module.lessons)) * 100
                    )

                    progress = ModuleProgressResponse(
                        module_id=module.id,
                        status=user_progress.status,
                        lessons_completed=user_progress.lessons_completed,
                        total_lessons=len(module.lessons),
                        lessons_progress_percentage=lessons_progress_pct,
                        quiz_attempts=user_progress.quiz_attempts,
                        quiz_best_score=user_progress.quiz_best_score,
                        quiz_completed=user_progress.quiz_completed,
                        started_at=user_progress.started_at,
                        completed_at=user_progress.completed_at
                    )

            # Build lessons response
            lessons_resp = []
            for lesson in module.lessons:
                completed = False
                if progress:
                    completed = lesson.id in progress.lessons_completed

                lessons_resp.append(LessonResponse(
                    id=lesson.id,
                    title=lesson.title,
                    content=lesson.content,
                    duration_minutes=lesson.duration_minutes,
                    order=lesson.order,
                    completed=completed
                ))

            # Build quiz response (without correct answers)
            quiz_questions = [
                QuestionResponse(
                    id=q.id,
                    question=q.question,
                    options=q.options,
                    type=q.type
                ) for q in module.quiz.questions
            ]

            quiz_resp = QuizResponse(
                id=module.quiz.id,
                title=module.quiz.title,
                description=module.quiz.description,
                questions=quiz_questions,
                passing_score=module.quiz.passing_score,
                xp_reward=module.quiz.xp_reward,
                coins_reward=module.quiz.coins_reward,
                lives_cost=module.quiz.lives_cost,
                attempts=progress.quiz_attempts if progress else 0,
                best_score=progress.quiz_best_score if progress else 0,
                completed=progress.quiz_completed if progress else False
            )

            module_resp = LearningModuleResponse(
                id=module.id,
                title=module.title,
                description=module.description,
                icon=module.icon,
                lessons=lessons_resp,
                quiz=quiz_resp,
                xp_reward=module.xp_reward,
                coins_reward=module.coins_reward,
                estimated_duration_minutes=module.estimated_duration_minutes,
                difficulty=module.difficulty,
                progress=progress
            )

            modules_response.append(module_resp)

        response = ModulesListResponse(
            modules=modules_response,
            total=len(modules_response)
        )

        return APIResponse(
            success=True,
            data=response.dict(),
            message=f"Found {len(modules_response)} modules"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/modules/{module_id}", response_model=APIResponse)
async def get_module(module_id: str, user_id: str = None):
    """Get specific learning module"""

    try:
        module = learning_service.get_module_by_id(module_id)

        if not module:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Module {module_id} not found"
            )

        # Get user progress if user_id provided
        progress = None
        if user_id:
            user_progress = learning_service.get_user_module_progress(user_id, module.id)
            if user_progress:
                lessons_progress_pct = int(
                    (len(user_progress.lessons_completed) / len(module.lessons)) * 100
                )

                progress = ModuleProgressResponse(
                    module_id=module.id,
                    status=user_progress.status,
                    lessons_completed=user_progress.lessons_completed,
                    total_lessons=len(module.lessons),
                    lessons_progress_percentage=lessons_progress_pct,
                    quiz_attempts=user_progress.quiz_attempts,
                    quiz_best_score=user_progress.quiz_best_score,
                    quiz_completed=user_progress.quiz_completed,
                    started_at=user_progress.started_at,
                    completed_at=user_progress.completed_at
                )

        # Build lessons response
        lessons_resp = []
        for lesson in module.lessons:
            completed = False
            if progress:
                completed = lesson.id in progress.lessons_completed

            lessons_resp.append(LessonResponse(
                id=lesson.id,
                title=lesson.title,
                content=lesson.content,
                duration_minutes=lesson.duration_minutes,
                order=lesson.order,
                completed=completed
            ))

        # Build quiz response
        quiz_questions = [
            QuestionResponse(
                id=q.id,
                question=q.question,
                options=q.options,
                type=q.type
            ) for q in module.quiz.questions
        ]

        quiz_resp = QuizResponse(
            id=module.quiz.id,
            title=module.quiz.title,
            description=module.quiz.description,
            questions=quiz_questions,
            passing_score=module.quiz.passing_score,
            xp_reward=module.quiz.xp_reward,
            coins_reward=module.quiz.coins_reward,
            lives_cost=module.quiz.lives_cost,
            attempts=progress.quiz_attempts if progress else 0,
            best_score=progress.quiz_best_score if progress else 0,
            completed=progress.quiz_completed if progress else False
        )

        module_resp = LearningModuleResponse(
            id=module.id,
            title=module.title,
            description=module.description,
            icon=module.icon,
            lessons=lessons_resp,
            quiz=quiz_resp,
            xp_reward=module.xp_reward,
            coins_reward=module.coins_reward,
            estimated_duration_minutes=module.estimated_duration_minutes,
            difficulty=module.difficulty,
            progress=progress
        )

        return APIResponse(
            success=True,
            data=module_resp.dict(),
            message="Module retrieved successfully"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/modules/start", response_model=APIResponse)
async def start_module(request: StartModuleRequest):
    """Start a learning module"""

    try:
        progress = learning_service.start_module(request.user_id, request.module_id)

        # Get module to calculate progress
        module = learning_service.get_module_by_id(request.module_id)
        if not module:
            raise ValueError(f"Module {request.module_id} not found")

        lessons_progress_pct = int(
            (len(progress.lessons_completed) / len(module.lessons)) * 100
        )

        progress_resp = ModuleProgressResponse(
            module_id=progress.module_id,
            status=progress.status,
            lessons_completed=progress.lessons_completed,
            total_lessons=len(module.lessons),
            lessons_progress_percentage=lessons_progress_pct,
            quiz_attempts=progress.quiz_attempts,
            quiz_best_score=progress.quiz_best_score,
            quiz_completed=progress.quiz_completed,
            started_at=progress.started_at,
            completed_at=progress.completed_at
        )

        return APIResponse(
            success=True,
            data=progress_resp.dict(),
            message=f"Started module: {module.title}"
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/lessons/complete", response_model=APIResponse)
async def complete_lesson(request: CompleteLessonRequest):
    """Mark a lesson as completed"""

    try:
        progress = learning_service.complete_lesson(
            request.user_id,
            request.module_id,
            request.lesson_id
        )

        # Get module to calculate progress
        module = learning_service.get_module_by_id(request.module_id)
        if not module:
            raise ValueError(f"Module {request.module_id} not found")

        lessons_progress_pct = int(
            (len(progress.lessons_completed) / len(module.lessons)) * 100
        )

        progress_resp = ModuleProgressResponse(
            module_id=progress.module_id,
            status=progress.status,
            lessons_completed=progress.lessons_completed,
            total_lessons=len(module.lessons),
            lessons_progress_percentage=lessons_progress_pct,
            quiz_attempts=progress.quiz_attempts,
            quiz_best_score=progress.quiz_best_score,
            quiz_completed=progress.quiz_completed,
            started_at=progress.started_at,
            completed_at=progress.completed_at
        )

        return APIResponse(
            success=True,
            data=progress_resp.dict(),
            message="Lesson completed!"
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/quiz/submit", response_model=APIResponse)
async def submit_quiz(request: SubmitQuizRequest):
    """Submit quiz answers and get results"""

    try:
        result, progress = learning_service.submit_quiz(
            user_id=request.user_id,
            module_id=request.module_id,
            quiz_id=request.quiz_id,
            answers=request.answers,
            time_taken_seconds=request.time_taken_seconds
        )

        # Convert question_results to proper schema
        question_results = [
            QuizQuestionResult(**qr) for qr in result.question_results
        ]

        result_resp = QuizResultResponse(
            quiz_id=request.quiz_id,
            score=result.score,
            passed=result.passed,
            total_questions=result.total_questions,
            correct_answers=result.correct_answers,
            incorrect_answers=result.incorrect_answers,
            xp_earned=result.xp_earned,
            coins_earned=result.coins_earned,
            lives_spent=0,  # TODO: Track lives spent
            feedback=result.feedback,
            question_results=question_results
        )

        return APIResponse(
            success=True,
            data=result_resp.dict(),
            message=result.feedback
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/progress/{user_id}", response_model=APIResponse)
async def get_user_progress(user_id: str):
    """Get user's learning progress summary"""

    try:
        summary = learning_service.get_user_learning_summary(user_id)

        summary_resp = UserProgressSummary(**summary)

        return APIResponse(
            success=True,
            data=summary_resp.dict(),
            message="Learning progress retrieved successfully"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/progress/{user_id}/{module_id}", response_model=APIResponse)
async def get_module_progress(user_id: str, module_id: str):
    """Get user's progress for specific module"""

    try:
        progress = learning_service.get_user_module_progress(user_id, module_id)

        if not progress:
            return APIResponse(
                success=True,
                data=None,
                message="No progress found for this module"
            )

        # Get module to calculate progress
        module = learning_service.get_module_by_id(module_id)
        if not module:
            raise ValueError(f"Module {module_id} not found")

        lessons_progress_pct = int(
            (len(progress.lessons_completed) / len(module.lessons)) * 100
        )

        progress_resp = ModuleProgressResponse(
            module_id=progress.module_id,
            status=progress.status,
            lessons_completed=progress.lessons_completed,
            total_lessons=len(module.lessons),
            lessons_progress_percentage=lessons_progress_pct,
            quiz_attempts=progress.quiz_attempts,
            quiz_best_score=progress.quiz_best_score,
            quiz_completed=progress.quiz_completed,
            started_at=progress.started_at,
            completed_at=progress.completed_at
        )

        return APIResponse(
            success=True,
            data=progress_resp.dict(),
            message="Progress retrieved successfully"
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
