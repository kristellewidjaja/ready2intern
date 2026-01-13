/**
 * Types for resume upload functionality
 */

export interface UploadResponse {
  session_id: string;
  status: 'uploaded';
  message: string;
  filename: string;
  file_size: number;
}

export interface ErrorResponse {
  error: string;
  message: string;
  details: Record<string, any>;
}

export interface UploadProgress {
  loaded: number;
  total: number;
  percentage: number;
}
