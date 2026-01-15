/**
 * API service for backend communication
 */
import axios from 'axios';
import type { UploadResponse, CompaniesResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Upload resume file
 */
export const uploadResume = async (
  file: File,
  onProgress?: (progress: number) => void
): Promise<UploadResponse> => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await api.post<UploadResponse>('/api/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    onUploadProgress: (progressEvent: any) => {
      if (progressEvent.total && onProgress) {
        const percentage = Math.round((progressEvent.loaded * 100) / progressEvent.total);
        onProgress(percentage);
      }
    },
  });

  return response.data;
};

/**
 * Health check
 */
export const checkHealth = async () => {
  const response = await api.get('/api/health');
  return response.data;
};

/**
 * Fetch available companies
 */
export const fetchCompanies = async (): Promise<CompaniesResponse> => {
  const response = await api.get<CompaniesResponse>('/api/companies');
  return response.data;
};

/**
 * Start resume analysis
 */
export interface AnalyzeRequest {
  session_id: string;
  company: string;
  role_description: string;
  target_deadline?: string;
}

export interface AnalyzeResponse {
  analysis_id: string;
  session_id: string;
  status: string;
  message: string;
}

export const analyzeResume = async (request: AnalyzeRequest): Promise<AnalyzeResponse> => {
  const response = await api.post<AnalyzeResponse>('/api/analyze', request);
  return response.data;
};
