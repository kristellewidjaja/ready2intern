import React, { useState } from 'react';

interface AnalyzeButtonProps {
  sessionId: string | null;
  company: string | null;
  roleDescription: string;
  onAnalyze: () => Promise<void>;
  disabled?: boolean;
}

export const AnalyzeButton: React.FC<AnalyzeButtonProps> = ({
  sessionId,
  company,
  roleDescription,
  onAnalyze,
  disabled = false,
}) => {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [progress, setProgress] = useState<string>('');

  // Check if all required fields are filled
  const isFormValid =
    sessionId !== null &&
    company !== null &&
    roleDescription.trim().length >= 50 &&
    roleDescription.trim().length <= 10000;

  const isDisabled = disabled || !isFormValid || isAnalyzing;

  const handleClick = async () => {
    if (isDisabled) return;

    setIsAnalyzing(true);
    setProgress('Preparing analysis...');

    try {
      // Simulate progress updates
      setTimeout(() => setProgress('Analyzing resume...'), 500);
      setTimeout(() => setProgress('Evaluating company fit...'), 1500);
      setTimeout(() => setProgress('Generating recommendations...'), 2500);

      await onAnalyze();

      setProgress('Analysis complete!');
    } catch (error) {
      setProgress('');
      console.error('Analysis failed:', error);
    } finally {
      setTimeout(() => {
        setIsAnalyzing(false);
        setProgress('');
      }, 500);
    }
  };

  const getButtonClasses = () => {
    const baseClasses = `
      w-full px-6 py-4 rounded-lg font-semibold text-lg
      transition-all duration-200
      focus:outline-none focus:ring-4 focus:ring-opacity-50
    `;

    if (isDisabled) {
      return `${baseClasses} 
        bg-gray-300 dark:bg-gray-700 
        text-gray-500 dark:text-gray-500 
        cursor-not-allowed`;
    }

    return `${baseClasses}
      bg-gradient-to-r from-blue-600 to-purple-600
      hover:from-blue-700 hover:to-purple-700
      text-white shadow-lg hover:shadow-xl
      transform hover:scale-105
      cursor-pointer`;
  };

  const getMissingFields = () => {
    const missing: string[] = [];
    if (!sessionId) missing.push('Resume');
    if (!company) missing.push('Company');
    if (roleDescription.trim().length < 50) missing.push('Role Description');
    return missing;
  };

  const missingFields = getMissingFields();

  return (
    <div className="w-full space-y-3">
      <button
        onClick={handleClick}
        disabled={isDisabled}
        className={getButtonClasses()}
        aria-label="Analyze resume"
        aria-busy={isAnalyzing}
      >
        {isAnalyzing ? (
          <div className="flex items-center justify-center space-x-3">
            <svg
              className="animate-spin h-6 w-6 text-white"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
            <span>Analyzing...</span>
          </div>
        ) : (
          <div className="flex items-center justify-center space-x-2">
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"
              />
            </svg>
            <span>Analyze Resume</span>
          </div>
        )}
      </button>

      {/* Progress message */}
      {isAnalyzing && progress && (
        <div className="flex items-center justify-center space-x-2 text-sm text-gray-600 dark:text-gray-400 animate-pulse">
          <svg
            className="w-4 h-4 text-blue-500"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path
              fillRule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
              clipRule="evenodd"
            />
          </svg>
          <span>{progress}</span>
        </div>
      )}

      {/* Missing fields message */}
      {!isAnalyzing && missingFields.length > 0 && (
        <div className="text-sm text-gray-600 dark:text-gray-400 text-center">
          <span className="font-medium">Required:</span> {missingFields.join(', ')}
        </div>
      )}

      {/* Ready message */}
      {!isAnalyzing && isFormValid && (
        <div className="flex items-center justify-center space-x-2 text-sm text-green-600 dark:text-green-400">
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
          <span>Ready to analyze!</span>
        </div>
      )}
    </div>
  );
};
