/**
 * Services Index
 * Barrel export for all services
 */

export { api, getErrorMessage } from './api';
export { authService } from './authService';
export { fimService } from './fimService';
export { transactionService } from './transactionService';
export { dashboardService } from './dashboardService';
export { learningService } from './learningService';

// Re-export types
export type { APIResponse, APIError } from './api';
