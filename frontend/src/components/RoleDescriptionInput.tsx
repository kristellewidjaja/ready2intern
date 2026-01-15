import React, { useState, useEffect } from 'react';

interface RoleDescriptionInputProps {
  value: string;
  onChange: (value: string) => void;
  error?: string | null;
}

const MIN_CHARS = 50;
const MAX_CHARS = 10000;

export const RoleDescriptionInput: React.FC<RoleDescriptionInputProps> = ({
  value,
  onChange,
  error: externalError,
}) => {
  const [internalError, setInternalError] = useState<string | null>(null);
  const charCount = value.length;
  const isValid = charCount >= MIN_CHARS && charCount <= MAX_CHARS;
  const isTooShort = charCount > 0 && charCount < MIN_CHARS;
  const isTooLong = charCount > MAX_CHARS;

  // Update internal error based on validation
  useEffect(() => {
    if (isTooShort) {
      setInternalError(`Minimum ${MIN_CHARS} characters required (${MIN_CHARS - charCount} more needed)`);
    } else if (isTooLong) {
      setInternalError(`Maximum ${MAX_CHARS} characters exceeded (${charCount - MAX_CHARS} over limit)`);
    } else {
      setInternalError(null);
    }
  }, [charCount, isTooShort, isTooLong]);

  const displayError = externalError || internalError;

  const getCharCountColor = () => {
    if (isTooLong) return 'text-red-600 dark:text-red-400';
    if (isTooShort && charCount > 0) return 'text-orange-600 dark:text-orange-400';
    if (isValid) return 'text-green-600 dark:text-green-400';
    return 'text-gray-500 dark:text-gray-400';
  };

  const getTextareaClasses = () => {
    const baseClasses = `
      w-full px-4 py-3 rounded-lg border-2 
      bg-white dark:bg-gray-800 
      text-gray-900 dark:text-white
      placeholder-gray-400 dark:placeholder-gray-500
      focus:outline-none focus:ring-2 focus:ring-opacity-50
      transition-colors duration-200
      resize-none
    `;

    if (displayError) {
      return `${baseClasses} border-red-300 dark:border-red-700 focus:border-red-500 focus:ring-red-500`;
    }
    if (isValid) {
      return `${baseClasses} border-green-300 dark:border-green-700 focus:border-green-500 focus:ring-green-500`;
    }
    return `${baseClasses} border-gray-300 dark:border-gray-600 focus:border-blue-500 focus:ring-blue-500`;
  };

  const placeholderText = `Paste the job description here...

Example:
We are looking for a Software Development Engineer Intern to join our team. You will work on building scalable systems, collaborating with senior engineers, and contributing to production code.

Responsibilities:
- Design and implement features for our web platform
- Write clean, maintainable code
- Participate in code reviews
- Debug and resolve technical issues

Requirements:
- Currently pursuing a degree in Computer Science or related field
- Strong programming skills in Python, Java, or JavaScript
- Understanding of data structures and algorithms
- Excellent problem-solving abilities`;

  return (
    <div className="w-full space-y-2">
      <div className="flex justify-between items-center">
        <label
          htmlFor="role-description"
          className="text-sm font-medium text-gray-700 dark:text-gray-300"
        >
          Role Description
        </label>
        <span className={`text-sm font-medium ${getCharCountColor()}`}>
          {charCount.toLocaleString()} / {MAX_CHARS.toLocaleString()} characters
          {isValid && ' ✓'}
        </span>
      </div>

      <textarea
        id="role-description"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholderText}
        className={getTextareaClasses()}
        rows={12}
        aria-invalid={!!displayError}
        aria-describedby={displayError ? 'role-description-error' : undefined}
      />

      {displayError && (
        <div
          id="role-description-error"
          className="flex items-start space-x-2 text-sm text-red-600 dark:text-red-400"
          role="alert"
        >
          <svg
            className="w-5 h-5 flex-shrink-0 mt-0.5"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path
              fillRule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
              clipRule="evenodd"
            />
          </svg>
          <span>{displayError}</span>
        </div>
      )}

      {!displayError && charCount > 0 && charCount < MIN_CHARS && (
        <div className="text-sm text-gray-600 dark:text-gray-400">
          <span className="font-medium">{MIN_CHARS - charCount}</span> more characters needed
        </div>
      )}

      {isValid && (
        <div className="flex items-center space-x-2 text-sm text-green-600 dark:text-green-400">
          <svg
            className="w-5 h-5"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path
              fillRule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
              clipRule="evenodd"
            />
          </svg>
          <span>Role description looks good!</span>
        </div>
      )}
    </div>
  );
};
