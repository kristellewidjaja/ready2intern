import { useState, useRef, DragEvent, ChangeEvent } from 'react';
import { uploadResume } from '../services/api';
import type { UploadResponse, ErrorResponse } from '../types/upload';

interface FileDropzoneProps {
  onUploadSuccess: (response: UploadResponse) => void;
  onUploadError?: (error: ErrorResponse) => void;
}

const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB
const ALLOWED_TYPES = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
const ALLOWED_EXTENSIONS = ['.pdf', '.docx'];

export const FileDropzone = ({ onUploadSuccess, onUploadError }: FileDropzoneProps) => {
  const [isDragging, setIsDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [uploadedFile, setUploadedFile] = useState<UploadResponse | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const validateFile = (file: File): string | null => {
    // Check file size
    if (file.size === 0) {
      return 'File is empty';
    }
    if (file.size > MAX_FILE_SIZE) {
      const sizeMB = (file.size / (1024 * 1024)).toFixed(2);
      return `File size (${sizeMB}MB) exceeds maximum allowed size (5MB)`;
    }

    // Check file type
    if (!ALLOWED_TYPES.includes(file.type)) {
      const extension = file.name.split('.').pop()?.toLowerCase();
      if (!extension || !ALLOWED_EXTENSIONS.includes(`.${extension}`)) {
        return `Invalid file type. Allowed types: ${ALLOWED_EXTENSIONS.join(', ')}`;
      }
    }

    return null;
  };

  const handleFile = async (file: File) => {
    setError(null);
    setUploadedFile(null);

    // Validate file
    const validationError = validateFile(file);
    if (validationError) {
      setError(validationError);
      return;
    }

    // Upload file
    setUploading(true);
    setUploadProgress(0);

    try {
      const response = await uploadResume(file, (progress) => {
        setUploadProgress(progress);
      });
      
      setUploadedFile(response);
      onUploadSuccess(response);
      setError(null);
    } catch (err: any) {
      const errorResponse = err.response?.data as ErrorResponse;
      const errorMessage = errorResponse?.message || 'Failed to upload file. Please try again.';
      setError(errorMessage);
      if (onUploadError && errorResponse) {
        onUploadError(errorResponse);
      }
    } finally {
      setUploading(false);
      setUploadProgress(0);
    }
  };

  const handleDragEnter = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFile(files[0]);
    }
  };

  const handleFileInput = (e: ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      handleFile(files[0]);
    }
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return `${bytes} bytes`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(2)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
  };

  return (
    <div className="w-full">
      <div
        className={`
          relative border-2 border-dashed rounded-lg p-8 text-center cursor-pointer
          transition-all duration-200
          ${isDragging 
            ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20' 
            : 'border-gray-300 dark:border-gray-600 hover:border-primary-400 dark:hover:border-primary-500'
          }
          ${uploading ? 'pointer-events-none opacity-75' : ''}
          ${uploadedFile ? 'border-green-500 bg-green-50 dark:bg-green-900/20' : ''}
        `}
        onDragEnter={handleDragEnter}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={handleClick}
      >
        <input
          ref={fileInputRef}
          type="file"
          className="hidden"
          accept={ALLOWED_EXTENSIONS.join(',')}
          onChange={handleFileInput}
          disabled={uploading}
        />

        {!uploading && !uploadedFile && (
          <div className="space-y-4">
            <div className="flex justify-center">
              <svg
                className="w-16 h-16 text-gray-400 dark:text-gray-500"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                />
              </svg>
            </div>
            <div>
              <p className="text-lg font-medium text-gray-700 dark:text-gray-300">
                Drop your resume here or click to browse
              </p>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
                PDF or DOCX • Max 5MB
              </p>
            </div>
          </div>
        )}

        {uploading && (
          <div className="space-y-4">
            <div className="flex justify-center">
              <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary-500"></div>
            </div>
            <div>
              <p className="text-lg font-medium text-gray-700 dark:text-gray-300">
                Uploading...
              </p>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
                {uploadProgress}%
              </p>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mt-4">
                <div
                  className="bg-primary-500 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${uploadProgress}%` }}
                ></div>
              </div>
            </div>
          </div>
        )}

        {uploadedFile && (
          <div className="space-y-4">
            <div className="flex justify-center">
              <svg
                className="w-16 h-16 text-green-500"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                  clipRule="evenodd"
                />
              </svg>
            </div>
            <div>
              <p className="text-lg font-medium text-green-700 dark:text-green-300">
                Upload successful!
              </p>
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
                {uploadedFile.filename} • {formatFileSize(uploadedFile.file_size)}
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-500 mt-1">
                Session ID: {uploadedFile.session_id}
              </p>
            </div>
          </div>
        )}
      </div>

      {error && (
        <div className="mt-4 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
          <div className="flex items-start space-x-2">
            <svg
              className="w-5 h-5 text-red-600 dark:text-red-400 mt-0.5"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                clipRule="evenodd"
              />
            </svg>
            <p className="text-sm text-red-800 dark:text-red-200">{error}</p>
          </div>
        </div>
      )}
    </div>
  );
};
