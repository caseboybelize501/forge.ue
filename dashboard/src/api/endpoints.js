/**
 * FORGE API Endpoints
 * 
 * Centralized endpoint definitions.
 */

export const endpoints = {
  // Projects
  createProject: '/api/projects',
  getProject: (projectId) => `/api/projects/${projectId}`,
  
  // Architecture
  getArchitecture: (projectId) => `/api/projects/${projectId}/architecture`,
  
  // Generation
  triggerGeneration: (projectId) => `/api/projects/${projectId}/generate`,
  getProgress: (projectId) => `/api/projects/${projectId}/generate/progress`,
  getFileTree: (projectId) => `/api/projects/${projectId}/generate/files`,
  
  // Build
  getBuildStatus: (projectId) => `/api/projects/${projectId}/build`,
  
  // Package
  triggerPackaging: (projectId) => `/api/projects/${projectId}/package`,
  downloadPackage: (projectId, platform) => `/api/projects/${projectId}/package/${platform}`,
  
  // Store
  getStoreSubmission: (projectId) => `/api/projects/${projectId}/store`,
  
  // Critic Log
  getCriticLog: (projectId) => `/api/projects/${projectId}/critic-log`,
  
  // Auth
  getToken: '/api/auth/token',
  verifyToken: '/api/auth/verify',
  
  // Health
  health: '/health',
};

export default endpoints;
