"""
Learning Service
Business logic for learning modules, lessons, and quizzes.
"""

from datetime import datetime
from typing import Optional, List, Dict, Tuple
from core.database import get_firestore_client
from models.learning import (
    LearningModule, Lesson, Quiz, Question,
    UserModuleProgress, ModuleStatus, QuizAttempt, QuizResult
)
from models.gamification import XPAction
from services.gamification_service import GamificationService
import uuid


class LearningService:
    """Service for managing learning features"""

    def __init__(self):
        self.db = get_firestore_client()
        self.gamification_service = GamificationService()

    def get_all_modules(self, user_id: str = None) -> List[LearningModule]:
        """Get all learning modules with optional user progress"""

        modules_ref = self.db.collection('learning_modules')
        modules_docs = modules_ref.stream()

        modules = []
        for doc in modules_docs:
            module_data = doc.to_dict()
            module_data['id'] = doc.id
            module = LearningModule(**module_data)
            modules.append(module)

        # If user_id provided, attach progress
        if user_id:
            for module in modules:
                progress = self.get_user_module_progress(user_id, module.id)
                # Attach progress as dict (will be handled in response schema)

        return modules

    def get_module_by_id(self, module_id: str) -> Optional[LearningModule]:
        """Get specific learning module"""

        module_doc = self.db.collection('learning_modules').document(module_id).get()

        if not module_doc.exists:
            return None

        module_data = module_doc.to_dict()
        module_data['id'] = module_doc.id
        return LearningModule(**module_data)

    def start_module(self, user_id: str, module_id: str) -> UserModuleProgress:
        """Start a learning module"""

        # Check if module exists
        module = self.get_module_by_id(module_id)
        if not module:
            raise ValueError(f"Module {module_id} not found")

        # Check if already started
        existing_progress = self.get_user_module_progress(user_id, module_id)
        if existing_progress and existing_progress.status != ModuleStatus.NOT_STARTED:
            return existing_progress

        # Create new progress
        progress = UserModuleProgress(
            id=str(uuid.uuid4()),
            user_id=user_id,
            module_id=module_id,
            status=ModuleStatus.IN_PROGRESS,
            started_at=datetime.now(),
            last_accessed=datetime.now()
        )

        self.db.collection('user_module_progress').document(progress.id).set(
            progress.dict()
        )

        return progress

    def complete_lesson(self, user_id: str, module_id: str, lesson_id: str) -> UserModuleProgress:
        """Mark a lesson as completed"""

        progress = self.get_user_module_progress(user_id, module_id)

        if not progress:
            # Auto-start module if not started
            progress = self.start_module(user_id, module_id)

        # Add lesson to completed list if not already there
        if lesson_id not in progress.lessons_completed:
            progress.lessons_completed.append(lesson_id)

        # Update progress
        progress_ref = self.db.collection('user_module_progress').document(progress.id)
        progress_ref.update({
            'lessons_completed': progress.lessons_completed,
            'last_accessed': datetime.now(),
            'status': ModuleStatus.IN_PROGRESS
        })

        return progress

    def submit_quiz(
        self,
        user_id: str,
        module_id: str,
        quiz_id: str,
        answers: Dict[str, int],
        time_taken_seconds: Optional[int] = None
    ) -> Tuple[QuizResult, UserModuleProgress]:
        """
        Submit quiz answers and calculate results.

        Returns:
            Tuple of (QuizResult, UpdatedUserModuleProgress)
        """

        # Get module and quiz
        module = self.get_module_by_id(module_id)
        if not module:
            raise ValueError(f"Module {module_id} not found")

        quiz = module.quiz

        # Check if user has enough lives
        user_ref = self.db.collection('users').document(user_id)
        user_doc = user_ref.get()

        if not user_doc.exists:
            raise ValueError(f"User {user_id} not found")

        user_data = user_doc.to_dict()
        gamification = user_data.get('gamification', {})
        current_lives = gamification.get('lives', 5)

        # Get progress
        progress = self.get_user_module_progress(user_id, module_id)
        if not progress:
            progress = self.start_module(user_id, module_id)

        # If quiz already completed and perfect score, don't allow retake
        if progress.quiz_completed and progress.quiz_best_score == 100:
            raise ValueError("Quiz already completed with perfect score")

        # Check lives for retry
        lives_spent = 0
        if progress.quiz_attempts > 0 and not progress.quiz_completed:
            if current_lives < quiz.lives_cost:
                raise ValueError(f"Not enough lives. Need {quiz.lives_cost}, have {current_lives}")
            lives_spent = quiz.lives_cost

        # Calculate score
        correct_count = 0
        question_results = []

        for question in quiz.questions:
            user_answer = answers.get(question.id, -1)
            is_correct = user_answer == question.correct_answer

            if is_correct:
                correct_count += 1

            question_results.append({
                'question_id': question.id,
                'question': question.question,
                'selected_answer': user_answer,
                'correct_answer': question.correct_answer,
                'is_correct': is_correct,
                'explanation': question.explanation
            })

        total_questions = len(quiz.questions)
        score = int((correct_count / total_questions) * 100)
        passed = score >= quiz.passing_score

        # Calculate rewards
        xp_earned = 0
        coins_earned = 0
        level_up = False
        new_level = None

        if passed:
            # XP reward based on score
            if score == 100:
                xp_earned_from_action, level_up, new_level = self.gamification_service.add_xp(
                    user_id, XPAction.COMPLETE_QUIZ_PERFECT, {'module_id': module_id, 'quiz_id': quiz_id}
                )
            else:
                xp_earned_from_action, level_up, new_level = self.gamification_service.add_xp(
                    user_id, XPAction.COMPLETE_QUIZ, {'module_id': module_id, 'quiz_id': quiz_id}
                )

            xp_earned = xp_earned_from_action

            # Award coins
            coins_earned = quiz.coins_reward
            self.gamification_service.award_coins(user_id, coins_earned, f"Completed quiz: {quiz.title}")

        # Spend lives if retry
        if lives_spent > 0:
            self.gamification_service.spend_lives(user_id, lives_spent)

        # Update progress
        new_attempts = progress.quiz_attempts + 1
        new_best_score = max(progress.quiz_best_score, score)
        quiz_completed = passed

        # Check if all module is completed
        module_completed = False
        if quiz_completed and len(progress.lessons_completed) == len(module.lessons):
            module_completed = True

            # Award module completion XP
            module_xp, module_level_up, module_new_level = self.gamification_service.add_xp(
                user_id, XPAction.COMPLETE_MODULE, {'module_id': module_id}
            )
            xp_earned += module_xp

            if module_level_up:
                level_up = True
                new_level = module_new_level

            # Award module completion coins
            self.gamification_service.award_coins(user_id, module.coins_reward, f"Completed module: {module.title}")
            coins_earned += module.coins_reward

        progress_ref = self.db.collection('user_module_progress').document(progress.id)
        update_data = {
            'quiz_attempts': new_attempts,
            'quiz_best_score': new_best_score,
            'quiz_completed': quiz_completed,
            'last_accessed': datetime.now()
        }

        if module_completed:
            update_data['status'] = ModuleStatus.COMPLETED
            update_data['completed_at'] = datetime.now()

        progress_ref.update(update_data)

        # Record quiz attempt
        attempt = QuizAttempt(
            id=str(uuid.uuid4()),
            user_id=user_id,
            module_id=module_id,
            quiz_id=quiz_id,
            answers=answers,
            score=score,
            passed=passed,
            xp_earned=xp_earned,
            coins_earned=coins_earned,
            lives_spent=lives_spent,
            time_taken_seconds=time_taken_seconds,
            created_at=datetime.now()
        )

        self.db.collection('quiz_attempts').document(attempt.id).set(attempt.dict())

        # Create result
        feedback = self._generate_quiz_feedback(score, passed)

        result = QuizResult(
            score=score,
            passed=passed,
            total_questions=total_questions,
            correct_answers=correct_count,
            incorrect_answers=total_questions - correct_count,
            xp_earned=xp_earned,
            coins_earned=coins_earned,
            feedback=feedback,
            question_results=question_results
        )

        # Update progress object
        progress.quiz_attempts = new_attempts
        progress.quiz_best_score = new_best_score
        progress.quiz_completed = quiz_completed
        if module_completed:
            progress.status = ModuleStatus.COMPLETED
            progress.completed_at = datetime.now()

        return result, progress

    def get_user_module_progress(self, user_id: str, module_id: str) -> Optional[UserModuleProgress]:
        """Get user's progress for a specific module"""

        progress_ref = self.db.collection('user_module_progress')\
            .where('user_id', '==', user_id)\
            .where('module_id', '==', module_id)\
            .limit(1)

        progress_docs = list(progress_ref.stream())

        if not progress_docs:
            return None

        progress_data = progress_docs[0].to_dict()
        progress_data['id'] = progress_docs[0].id
        return UserModuleProgress(**progress_data)

    def get_user_all_progress(self, user_id: str) -> List[UserModuleProgress]:
        """Get all user's module progress"""

        progress_ref = self.db.collection('user_module_progress')\
            .where('user_id', '==', user_id)

        progress_docs = progress_ref.stream()

        progress_list = []
        for doc in progress_docs:
            progress_data = doc.to_dict()
            progress_data['id'] = doc.id
            progress_list.append(UserModuleProgress(**progress_data))

        return progress_list

    def _generate_quiz_feedback(self, score: int, passed: bool) -> str:
        """Generate feedback message based on score"""

        if score == 100:
            return "🎉 Perfeito! Você dominou este conteúdo completamente!"
        elif score >= 90:
            return "🌟 Excelente! Você está quase lá, continue assim!"
        elif score >= 70:
            return "👏 Bom trabalho! Você passou no quiz!"
        elif score >= 50:
            return "📖 Quase lá! Revise o conteúdo e tente novamente."
        else:
            return "💪 Continue estudando! Você vai conseguir na próxima tentativa!"

    def get_user_learning_summary(self, user_id: str) -> Dict:
        """Get user's overall learning statistics"""

        all_progress = self.get_user_all_progress(user_id)
        all_modules = self.get_all_modules()

        total_modules = len(all_modules)
        completed_modules = len([p for p in all_progress if p.status == ModuleStatus.COMPLETED])
        in_progress_modules = len([p for p in all_progress if p.status == ModuleStatus.IN_PROGRESS])

        total_quizzes_taken = sum([p.quiz_attempts for p in all_progress])
        total_quiz_scores = [p.quiz_best_score for p in all_progress if p.quiz_best_score > 0]
        average_quiz_score = sum(total_quiz_scores) / len(total_quiz_scores) if total_quiz_scores else 0

        # Calculate total XP earned from learning (from quiz_attempts)
        attempts_ref = self.db.collection('quiz_attempts').where('user_id', '==', user_id)
        attempts_docs = attempts_ref.stream()
        total_xp_earned = sum([doc.to_dict().get('xp_earned', 0) for doc in attempts_docs])

        return {
            'total_modules': total_modules,
            'completed_modules': completed_modules,
            'in_progress_modules': in_progress_modules,
            'total_quizzes_taken': total_quizzes_taken,
            'average_quiz_score': round(average_quiz_score, 1),
            'total_xp_earned': total_xp_earned,
            'total_time_spent_minutes': 0  # TODO: Track time spent
        }
