/**
 * Learning Service
 * Handles all learning-related API calls (modules, lessons, quizzes)
 */

import { api, getErrorMessage, APIResponse } from './api';

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
  }
};
