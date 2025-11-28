/**
 * Learning Service
 * Handles all learning-related API calls (modules, lessons, quizzes)
 */

import { api, getErrorMessage, APIResponse } from './api';

// ==================
// Legacy Types (keeping for backward compatibility)
// ==================

export interface Lesson {
  id: string;
  title: string;
  content: string;
  duration_minutes: number;
  order: number;
  completed?: boolean;
}

export interface Quiz {
  id: string;
  title: string;
  description: string;
  questions: QuizQuestion[];
  passing_score: number;
  xp_reward: number;
  coins_reward: number;
  lives_cost: number;
  attempts?: number;
  best_score?: number;
  completed?: boolean;
}

export interface QuizQuestion {
  id: string;
  question: string;
  options: string[];
  type: 'multiple_choice' | 'true_false';
  correct_answer?: string;
}

export interface LearningModule {
  id: string;
  title: string;
  description: string;
  icon: string;
  lessons: Lesson[];
  quiz: Quiz;
  xp_reward: number;
  coins_reward: number;
  difficulty: string;
  progress?: ModuleProgress;
}

export interface ModuleProgress {
  module_id: string;
  status: 'not_started' | 'in_progress' | 'completed';
  lessons_completed: string[];
  total_lessons: number;
  lessons_progress_percentage: number;
  quiz_attempts: number;
  quiz_best_score: number;
  quiz_completed: boolean;
  started_at?: string;
  completed_at?: string;
}

export interface QuizSubmission {
  answers: { [questionId: string]: string };
}

export interface QuizResult {
  quiz_id: string;
  score: number;
  total_questions: number;
  passed: boolean;
  xp_earned: number;
  coins_earned: number;
  lives_lost: number;
  question_results: Array<{
    question_id: string;
    correct: boolean;
    user_answer: string;
    correct_answer: string;
  }>;
}

// ==================
// New Types for Courses and Phases
// ==================

export interface Course {
  id: string;
  title: string;
  description: string;
  icon: string;
  color: string;
  gradient: string;
  order: number;
  total_modules: number;
  estimated_hours: number;
  difficulty: string;
  progress_percentage: number;
  modules_completed: number;
}

export interface PhaseLesson {
  id: string;
  title: string;
  content: string;
  duration_minutes: number;
  order: number;
  completed?: boolean;
}

export interface PhaseQuizQuestion {
  id: string;
  question: string;
  options: string[];
  correct_answer: number;  // Index of the correct option (0-based)
  explanation?: string;
}

export interface PhaseQuiz {
  id: string;
  title: string;
  description?: string;
  questions: PhaseQuizQuestion[];
  passing_score: number;
  xp_reward: number;
  coins_reward: number;
  lives_cost: number;
}

export interface Phase {
  id: string;
  title: string;
  description: string;
  order: number;
  status: 'locked' | 'current' | 'completed';
  lessons: PhaseLesson[];
  quiz: PhaseQuiz;
  lessons_completed: string[];
  quiz_score: number | null;
  quiz_stars: number;
  xp_reward: number;
  coins_reward: number;
}

export interface ModuleWithPhases {
  id: string;
  title: string;
  description: string;
  icon: string;
  order: number;
  difficulty: string;
  estimated_duration_minutes: number;
  xp_reward: number;
  coins_reward: number;
  total_phases: number;
  phases: Phase[];
  progress_percentage: number;
  phases_completed: number;
  status: 'not_started' | 'in_progress' | 'completed';
}

export interface PhaseQuizQuestionResult {
  question_id: string;
  question: string;
  selected_answer: number;
  correct_answer: number;
  is_correct: boolean;
  explanation?: string;
}

export interface PhaseQuizResult {
  phase_id: string;
  quiz_id: string;
  score: number;
  stars: number;
  passed: boolean;
  correct_answers: number;
  total_questions: number;
  xp_earned: number;
  coins_earned: number;
  feedback: string;
  question_results: PhaseQuizQuestionResult[];
  next_phase_unlocked: boolean;
  next_phase_id?: string;
  module_completed: boolean;
}

export interface UserStats {
  xp: number;
  level: number;
  coins: number;
  lives: number;
  streak: number;
}

export const learningService = {
  /**
   * Get all learning modules with optional user progress
   */
  async getModules(userId?: string): Promise<LearningModule[]> {
    try {
      const params = userId ? { user_id: userId } : {};
      const response = await api.get<APIResponse>('/learning/modules', { params });
      return response.data.data.modules || [];
    } catch (error) {
      throw new Error(getErrorMessage(error));
    }
  },

  /**
   * Get a specific module by ID
   */
  async getModule(moduleId: string, userId?: string): Promise<LearningModule> {
    try {
      const params = userId ? { user_id: userId } : {};
      const response = await api.get<APIResponse>(`/learning/modules/${moduleId}`, { params });
      return response.data.data.module;
    } catch (error) {
      throw new Error(getErrorMessage(error));
    }
  },

  /**
   * Start a learning module
   */
  async startModule(userId: string, moduleId: string): Promise<void> {
    try {
      await api.post<APIResponse>('/learning/start-module', {
        user_id: userId,
        module_id: moduleId
      });
    } catch (error) {
      throw new Error(getErrorMessage(error));
    }
  },

  /**
   * Complete a lesson
   */
  async completeLesson(userId: string, moduleId: string, lessonId: string): Promise<void> {
    try {
      await api.post<APIResponse>('/learning/complete-lesson', {
        user_id: userId,
        module_id: moduleId,
        lesson_id: lessonId
      });
    } catch (error) {
      throw new Error(getErrorMessage(error));
    }
  },

  /**
   * Submit a quiz
   */
  async submitQuiz(
    userId: string,
    moduleId: string,
    quizId: string,
    answers: { [questionId: string]: string }
  ): Promise<QuizResult> {
    try {
      const response = await api.post<APIResponse>('/learning/submit-quiz', {
        user_id: userId,
        module_id: moduleId,
        quiz_id: quizId,
        answers
      });
      return response.data.data.result;
    } catch (error) {
      throw new Error(getErrorMessage(error));
    }
  },

  /**
   * Get user's progress summary across all modules
   */
  async getUserProgress(userId: string): Promise<any> {
    try {
      const response = await api.get<APIResponse>(`/learning/progress/${userId}`);
      return response.data.data.progress;
    } catch (error) {
      throw new Error(getErrorMessage(error));
    }
  },

  // ==================
  // New Methods for Courses and Phases
  // ==================

  /**
   * Get all courses
   */
  async getCourses(userId?: string): Promise<Course[]> {
    try {
      const url = userId ? `/learning/courses?user_id=${userId}` : '/learning/courses';
      const response = await api.get<APIResponse>(url);
      return response.data.data.courses || [];
    } catch (error) {
      throw new Error(getErrorMessage(error));
    }
  },

  /**
   * Get course by ID with modules
   */
  async getCourse(courseId: string, userId?: string): Promise<any> {
    try {
      const url = userId
        ? `/learning/courses/${courseId}?user_id=${userId}`
        : `/learning/courses/${courseId}`;
      const response = await api.get<APIResponse>(url);
      return response.data.data;
    } catch (error) {
      throw new Error(getErrorMessage(error));
    }
  },

  /**
   * Get module with phases and user progress
   */
  async getModuleWithPhases(moduleId: string, userId?: string): Promise<ModuleWithPhases> {
    try {
      const url = userId
        ? `/learning/modules/${moduleId}/phases?user_id=${userId}`
        : `/learning/modules/${moduleId}/phases`;
      const response = await api.get<APIResponse>(url);
      return response.data.data;
    } catch (error) {
      throw new Error(getErrorMessage(error));
    }
  },

  /**
   * Start a module (v2 - with phases support)
   */
  async startModuleV2(moduleId: string, userId: string): Promise<any> {
    try {
      const response = await api.post<APIResponse>(
        `/learning/modules/${moduleId}/start?user_id=${userId}`
      );
      return response.data.data;
    } catch (error) {
      throw new Error(getErrorMessage(error));
    }
  },

  /**
   * Complete a lesson within a phase
   */
  async completePhaseLesson(
    userId: string,
    moduleId: string,
    phaseId: string,
    lessonId: string
  ): Promise<any> {
    try {
      const response = await api.post<APIResponse>('/learning/phases/lesson/complete', {
        user_id: userId,
        module_id: moduleId,
        phase_id: phaseId,
        lesson_id: lessonId,
      });
      return response.data.data;
    } catch (error) {
      throw new Error(getErrorMessage(error));
    }
  },

  /**
   * Submit quiz answers for a phase
   */
  async submitPhaseQuiz(
    userId: string,
    moduleId: string,
    phaseId: string,
    answers: Record<string, number>,
    timeTakenSeconds?: number
  ): Promise<PhaseQuizResult> {
    try {
      const response = await api.post<APIResponse>('/learning/phases/quiz/submit', {
        user_id: userId,
        module_id: moduleId,
        phase_id: phaseId,
        answers,
        time_taken_seconds: timeTakenSeconds,
      });
      return response.data.data;
    } catch (error) {
      throw new Error(getErrorMessage(error));
    }
  },

  /**
   * Get user stats (XP, coins, level, etc.)
   */
  async getUserStats(userId: string): Promise<UserStats> {
    try {
      const response = await api.get<APIResponse>(`/learning/user/${userId}/stats`);
      return response.data.data;
    } catch (error) {
      throw new Error(getErrorMessage(error));
    }
  }
};
