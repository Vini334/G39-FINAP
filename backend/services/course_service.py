"""
Course Service
Business logic for courses, modules with phases, and phase-based progression.
"""

from datetime import datetime
from typing import Optional, List, Dict, Tuple
from core.database import get_firestore_client
from services.gamification_service import GamificationService
from models.gamification import XPAction
import uuid


class CourseService:
    """Service for managing courses and phase-based learning"""

    def __init__(self):
        self.db = get_firestore_client()
        self.gamification_service = GamificationService()

    # =========================================================================
    # COURSES
    # =========================================================================

    def get_all_courses(self, user_id: str = None) -> List[Dict]:
        """Get all courses with optional user progress"""
        courses_ref = self.db.collection('courses').order_by('order')
        courses_docs = courses_ref.stream()

        courses = []
        for doc in courses_docs:
            course_data = doc.to_dict()
            course_data['id'] = doc.id

            # Calculate progress if user_id provided
            if user_id:
                progress = self._calculate_course_progress(user_id, course_data['id'])
                course_data['progress_percentage'] = progress['percentage']
                course_data['modules_completed'] = progress['modules_completed']
            else:
                course_data['progress_percentage'] = 0
                course_data['modules_completed'] = 0

            courses.append(course_data)

        return courses

    def get_course_by_id(self, course_id: str, user_id: str = None) -> Optional[Dict]:
        """Get course by ID with modules"""
        course_doc = self.db.collection('courses').document(course_id).get()

        if not course_doc.exists:
            return None

        course_data = course_doc.to_dict()
        course_data['id'] = course_doc.id

        # Get modules for this course
        modules = self.get_course_modules(course_id, user_id)
        course_data['modules'] = modules

        # Calculate progress
        if user_id:
            progress = self._calculate_course_progress(user_id, course_id)
            course_data['progress_percentage'] = progress['percentage']
            course_data['modules_completed'] = progress['modules_completed']

        return course_data

    def get_course_modules(self, course_id: str, user_id: str = None) -> List[Dict]:
        """Get all modules for a course"""
        # Query without order_by to avoid needing composite index
        modules_ref = self.db.collection('learning_modules')\
            .where('course_id', '==', course_id)

        modules_docs = modules_ref.stream()

        modules = []
        for doc in modules_docs:
            module_data = doc.to_dict()
            module_data['id'] = doc.id

            # Get user progress for module
            if user_id:
                progress = self.get_user_module_progress(user_id, module_data['id'])
                if progress:
                    module_data['user_progress'] = progress
                    module_data['status'] = progress.get('status', 'not_started')
                else:
                    module_data['status'] = 'not_started'
            else:
                module_data['status'] = 'not_started'

            modules.append(module_data)

        # Sort by order field manually (to avoid needing composite index)
        modules.sort(key=lambda x: x.get('order', 0))

        return modules

    def _calculate_course_progress(self, user_id: str, course_id: str) -> Dict:
        """Calculate user's progress in a course based on completed phases"""
        modules = self.get_course_modules(course_id, user_id)

        total_phases = 0
        completed_phases = 0

        for module in modules:
            # Get module with phases to count total phases
            module_doc = self.db.collection('learning_modules').document(module['id']).get()
            if module_doc.exists:
                module_data = module_doc.to_dict()
                phases = module_data.get('phases', [])
                total_phases += len(phases)

                # Get user progress for this module
                progress = self.get_user_module_progress(user_id, module['id'])
                if progress:
                    phases_progress = progress.get('phases', {})
                    for phase in phases:
                        phase_status = phases_progress.get(phase['id'], {}).get('status')
                        if phase_status == 'completed':
                            completed_phases += 1

        percentage = int((completed_phases / total_phases) * 100) if total_phases > 0 else 0

        return {
            'percentage': percentage,
            'modules_completed': completed_phases,  # Now represents phases completed
            'total_modules': total_phases  # Now represents total phases
        }

    # =========================================================================
    # MODULES WITH PHASES
    # =========================================================================

    def get_module_with_phases(self, module_id: str, user_id: str = None) -> Optional[Dict]:
        """Get module with all phases and user progress"""
        module_doc = self.db.collection('learning_modules').document(module_id).get()

        if not module_doc.exists:
            return None

        module_data = module_doc.to_dict()
        module_data['id'] = module_doc.id

        # Get user progress
        user_progress = None
        if user_id:
            user_progress = self.get_user_module_progress(user_id, module_id)

        # Process phases with progress
        phases = module_data.get('phases', [])
        processed_phases = []

        for i, phase in enumerate(phases):
            phase_progress = None
            if user_progress:
                phase_progress = user_progress.get('phases', {}).get(phase['id'], {})

            # Determine phase status
            if i == 0:
                # First phase is always unlocked
                if phase_progress and phase_progress.get('status') == 'completed':
                    phase_status = 'completed'
                elif phase_progress and phase_progress.get('status') == 'in_progress':
                    phase_status = 'current'
                elif user_progress:
                    phase_status = 'current'
                else:
                    phase_status = 'current'  # First phase always accessible
            else:
                # Check if previous phase is completed
                prev_phase = phases[i - 1]
                prev_progress = user_progress.get('phases', {}).get(prev_phase['id'], {}) if user_progress else {}

                if phase_progress and phase_progress.get('status') == 'completed':
                    phase_status = 'completed'
                elif prev_progress.get('status') == 'completed':
                    if phase_progress and phase_progress.get('status') == 'in_progress':
                        phase_status = 'current'
                    else:
                        phase_status = 'current'
                else:
                    phase_status = 'locked'

            # Build phase response
            processed_phase = {
                **phase,
                'status': phase_status,
                'lessons_completed': phase_progress.get('lessons_completed', []) if phase_progress else [],
                'quiz_score': phase_progress.get('quiz_score') if phase_progress else None,
                'quiz_stars': phase_progress.get('quiz_stars', 0) if phase_progress else 0,
                'xp_reward': phase.get('rewards', {}).get('xp', 30),
                'coins_reward': phase.get('rewards', {}).get('coins', 15)
            }

            # Keep correct answers in quiz questions for frontend validation
            # Note: In a production app, you might want to validate answers server-side only
            # For now, we keep correct_answer to enable instant feedback in the quiz

            processed_phases.append(processed_phase)

        module_data['phases'] = processed_phases

        # Calculate module progress
        completed_phases = sum(1 for p in processed_phases if p['status'] == 'completed')
        total_phases = len(processed_phases)

        module_data['phases_completed'] = completed_phases
        module_data['total_phases'] = total_phases
        module_data['progress_percentage'] = int((completed_phases / total_phases) * 100) if total_phases > 0 else 0

        if completed_phases == total_phases and total_phases > 0:
            module_data['status'] = 'completed'
        elif completed_phases > 0 or any(p['status'] == 'current' for p in processed_phases):
            module_data['status'] = 'in_progress'
        else:
            module_data['status'] = 'not_started'

        return module_data

    # =========================================================================
    # USER PROGRESS
    # =========================================================================

    def get_user_module_progress(self, user_id: str, module_id: str) -> Optional[Dict]:
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
        return progress_data

    def start_module(self, user_id: str, module_id: str) -> Dict:
        """Start a module for user"""
        # Check if already started
        existing = self.get_user_module_progress(user_id, module_id)
        if existing:
            return existing

        # Get module to get phase info
        module = self.get_module_with_phases(module_id)
        if not module:
            raise ValueError(f"Module {module_id} not found")

        # Initialize progress
        phases_progress = {}
        for i, phase in enumerate(module.get('phases', [])):
            phases_progress[phase['id']] = {
                'status': 'current' if i == 0 else 'locked',
                'lessons_completed': [],
                'quiz_score': None,
                'quiz_stars': 0,
                'started_at': datetime.now().isoformat() if i == 0 else None,
                'completed_at': None
            }

        progress = {
            'id': str(uuid.uuid4()),
            'user_id': user_id,
            'module_id': module_id,
            'status': 'in_progress',
            'phases': phases_progress,
            'started_at': datetime.now(),
            'completed_at': None,
            'last_accessed': datetime.now()
        }

        self.db.collection('user_module_progress').document(progress['id']).set(progress)

        return progress

    def complete_phase_lesson(
        self,
        user_id: str,
        module_id: str,
        phase_id: str,
        lesson_id: str
    ) -> Dict:
        """Mark a lesson within a phase as completed"""
        progress = self.get_user_module_progress(user_id, module_id)

        if not progress:
            progress = self.start_module(user_id, module_id)

        # Update phase progress
        phases = progress.get('phases', {})
        phase_progress = phases.get(phase_id, {
            'status': 'in_progress',
            'lessons_completed': [],
            'quiz_score': None,
            'quiz_stars': 0
        })

        if lesson_id not in phase_progress['lessons_completed']:
            phase_progress['lessons_completed'].append(lesson_id)

        phase_progress['status'] = 'in_progress'
        phases[phase_id] = phase_progress

        # Update in database
        progress_ref = self.db.collection('user_module_progress').document(progress['id'])
        progress_ref.update({
            'phases': phases,
            'last_accessed': datetime.now()
        })

        progress['phases'] = phases
        return progress

    def submit_phase_quiz(
        self,
        user_id: str,
        module_id: str,
        phase_id: str,
        answers: Dict[str, int],
        time_taken_seconds: Optional[int] = None
    ) -> Dict:
        """Submit quiz for a phase and calculate results"""
        # Get module and phase
        module_doc = self.db.collection('learning_modules').document(module_id).get()
        if not module_doc.exists:
            raise ValueError(f"Module {module_id} not found")

        module_data = module_doc.to_dict()
        phases = module_data.get('phases', [])

        # Find the phase
        phase = None
        phase_index = -1
        for i, p in enumerate(phases):
            if p['id'] == phase_id:
                phase = p
                phase_index = i
                break

        if not phase:
            raise ValueError(f"Phase {phase_id} not found")

        quiz = phase.get('quiz', {})
        questions = quiz.get('questions', [])

        # Calculate score
        correct_count = 0
        question_results = []

        for question in questions:
            user_answer = answers.get(question['id'], -1)
            is_correct = user_answer == question['correct_answer']

            if is_correct:
                correct_count += 1

            question_results.append({
                'question_id': question['id'],
                'question': question['question'],
                'selected_answer': user_answer,
                'correct_answer': question['correct_answer'],
                'is_correct': is_correct,
                'explanation': question.get('explanation', '')
            })

        total_questions = len(questions)
        score = int((correct_count / total_questions) * 100) if total_questions > 0 else 0

        # Calculate stars (1 star = 1 correct, 2 stars = 2 correct, 3 stars = 3 correct)
        stars = correct_count

        # Passed if at least 1 correct (1 star)
        passed = stars >= 1

        # Calculate rewards based on stars
        base_xp = phase.get('rewards', {}).get('xp', 30)
        base_coins = phase.get('rewards', {}).get('coins', 15)

        if stars == 3:
            xp_earned = base_xp
            coins_earned = base_coins
        elif stars == 2:
            xp_earned = int(base_xp * 0.66)
            coins_earned = int(base_coins * 0.66)
        elif stars == 1:
            xp_earned = int(base_xp * 0.33)
            coins_earned = int(base_coins * 0.33)
        else:
            xp_earned = 0
            coins_earned = 0

        # Get user progress
        progress = self.get_user_module_progress(user_id, module_id)
        if not progress:
            progress = self.start_module(user_id, module_id)

        # Update phase progress
        phases_progress = progress.get('phases', {})
        phase_progress = phases_progress.get(phase_id, {})

        # Only update if passed
        next_phase_unlocked = False
        next_phase_id = None
        module_completed = False

        if passed:
            # Update phase as completed
            phase_progress['status'] = 'completed'
            phase_progress['quiz_score'] = score
            phase_progress['quiz_stars'] = stars
            phase_progress['completed_at'] = datetime.now().isoformat()
            phases_progress[phase_id] = phase_progress

            # Unlock next phase if exists
            if phase_index < len(phases) - 1:
                next_phase = phases[phase_index + 1]
                next_phase_id = next_phase['id']
                next_phase_unlocked = True

                if next_phase_id not in phases_progress:
                    phases_progress[next_phase_id] = {
                        'status': 'current',
                        'lessons_completed': [],
                        'quiz_score': None,
                        'quiz_stars': 0,
                        'started_at': datetime.now().isoformat()
                    }
                else:
                    phases_progress[next_phase_id]['status'] = 'current'

            # Check if module is complete (all phases completed)
            all_completed = all(
                phases_progress.get(p['id'], {}).get('status') == 'completed'
                for p in phases
            )

            if all_completed:
                module_completed = True

            # Award XP and coins
            if xp_earned > 0:
                self.gamification_service.add_xp(
                    user_id,
                    XPAction.COMPLETE_QUIZ if stars < 3 else XPAction.COMPLETE_QUIZ_PERFECT,
                    {'module_id': module_id, 'phase_id': phase_id}
                )

            if coins_earned > 0:
                self.gamification_service.award_coins(
                    user_id,
                    coins_earned,
                    f"Quiz fase: {phase['title']}"
                )

            # Award module completion bonus
            if module_completed:
                self.gamification_service.add_xp(
                    user_id,
                    XPAction.COMPLETE_MODULE,
                    {'module_id': module_id}
                )
                self.gamification_service.award_coins(
                    user_id,
                    module_data.get('coins_reward', 50),
                    f"Módulo completo: {module_data['title']}"
                )

        # Update progress in database
        progress_ref = self.db.collection('user_module_progress').document(progress['id'])

        update_data = {
            'phases': phases_progress,
            'last_accessed': datetime.now()
        }

        if module_completed:
            update_data['status'] = 'completed'
            update_data['completed_at'] = datetime.now()

        progress_ref.update(update_data)

        # Generate feedback
        if stars == 3:
            feedback = "🌟 Perfeito! Você mandou muito bem!"
        elif stars == 2:
            feedback = "👏 Muito bom! Continue assim!"
        elif stars == 1:
            feedback = "✅ Você passou! Pode seguir em frente!"
        else:
            feedback = "😅 Não foi dessa vez. Revise o conteúdo e tente novamente!"

        # Record quiz attempt
        attempt_data = {
            'id': str(uuid.uuid4()),
            'user_id': user_id,
            'module_id': module_id,
            'phase_id': phase_id,
            'quiz_id': quiz.get('id', f'quiz_{phase_id}'),
            'answers': answers,
            'score': score,
            'stars': stars,
            'passed': passed,
            'xp_earned': xp_earned,
            'coins_earned': coins_earned,
            'time_taken_seconds': time_taken_seconds,
            'created_at': datetime.now()
        }

        self.db.collection('quiz_attempts').document(attempt_data['id']).set(attempt_data)

        return {
            'phase_id': phase_id,
            'quiz_id': quiz.get('id', f'quiz_{phase_id}'),
            'score': score,
            'stars': stars,
            'passed': passed,
            'correct_answers': correct_count,
            'total_questions': total_questions,
            'xp_earned': xp_earned,
            'coins_earned': coins_earned,
            'feedback': feedback,
            'question_results': question_results,
            'next_phase_unlocked': next_phase_unlocked,
            'next_phase_id': next_phase_id,
            'module_completed': module_completed
        }

    def get_user_gamification_stats(self, user_id: str) -> Dict:
        """Get user's gamification stats"""
        user_ref = self.db.collection('users').document(user_id)
        user_doc = user_ref.get()

        if not user_doc.exists:
            return {
                'xp': 0,
                'level': 1,
                'coins': 0,
                'lives': 5,
                'streak': 0
            }

        user_data = user_doc.to_dict()
        gamification = user_data.get('gamification', {})

        return {
            'xp': gamification.get('xp', 0),
            'level': gamification.get('level', 1),
            'coins': gamification.get('coins', 0),
            'lives': gamification.get('lives', 5),
            'streak': gamification.get('current_streak', 0)
        }
