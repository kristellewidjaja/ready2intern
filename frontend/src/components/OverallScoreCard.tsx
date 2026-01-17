/**
 * Overall score card component with animated circular progress
 */
import { useEffect, useState } from 'react';

interface OverallScoreCardProps {
  score: number;
  status: 'completed' | 'partial' | 'failed';
}

export const OverallScoreCard = ({ score, status }: OverallScoreCardProps) => {
  const [displayScore, setDisplayScore] = useState(0);
  const [isAnimating, setIsAnimating] = useState(true);

  // Animate score counting on mount
  useEffect(() => {
    if (score === 0) {
      setIsAnimating(false);
      return;
    }

    const duration = 2000; // 2 seconds
    const steps = 60;
    const increment = score / steps;
    const stepDuration = duration / steps;

    let currentStep = 0;
    const timer = setInterval(() => {
      currentStep++;
      if (currentStep >= steps) {
        setDisplayScore(score);
        setIsAnimating(false);
        clearInterval(timer);
      } else {
        setDisplayScore(Math.floor(increment * currentStep));
      }
    }, stepDuration);

    return () => clearInterval(timer);
  }, [score]);

  // Determine gradient and status message based on score
  const getScoreColor = (score: number): string => {
    if (score >= 85) return 'from-green-500 to-emerald-600';
    if (score >= 70) return 'from-blue-500 to-cyan-600';
    if (score >= 55) return 'from-yellow-500 to-orange-500';
    if (score >= 40) return 'from-orange-500 to-red-500';
    return 'from-red-500 to-red-700';
  };

  const getStatusMessage = (score: number): string => {
    if (score >= 85) return 'Excellent Match!';
    if (score >= 70) return 'Good Match';
    if (score >= 55) return 'Moderate Match';
    if (score >= 40) return 'Needs Improvement';
    return 'Significant Gaps';
  };

  const getStatusDescription = (score: number): string => {
    if (score >= 85) return 'Your profile is highly competitive for this role. Focus on final polish and interview prep.';
    if (score >= 70) return 'You have a solid foundation. Address key gaps to strengthen your application.';
    if (score >= 55) return 'You meet some requirements. Follow the development timeline to improve your match.';
    if (score >= 40) return 'Several areas need work. Focus on high-priority gaps first.';
    return 'Significant preparation needed. Start with foundational skills and experience.';
  };

  const gradientClass = getScoreColor(score);
  const statusMessage = getStatusMessage(score);
  const statusDescription = getStatusDescription(score);

  // Calculate circle progress (0-100 maps to 0-360 degrees)
  const circumference = 2 * Math.PI * 120; // radius = 120
  const offset = circumference - (displayScore / 100) * circumference;

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8 mb-8">
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 text-center">
        Overall Match Score
      </h2>

      <div className="flex flex-col items-center">
        {/* Circular Progress */}
        <div className="relative w-64 h-64 mb-6">
          <svg className="transform -rotate-90 w-64 h-64">
            {/* Background circle */}
            <circle
              cx="128"
              cy="128"
              r="120"
              stroke="currentColor"
              strokeWidth="16"
              fill="none"
              className="text-gray-200 dark:text-gray-700"
            />
            {/* Progress circle */}
            <circle
              cx="128"
              cy="128"
              r="120"
              stroke="url(#gradient)"
              strokeWidth="16"
              fill="none"
              strokeDasharray={circumference}
              strokeDashoffset={offset}
              strokeLinecap="round"
              className="transition-all duration-1000 ease-out"
            />
            {/* Gradient definition */}
            <defs>
              <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" className={`stop-${gradientClass.split(' ')[0].replace('from-', '')}`} />
                <stop offset="100%" className={`stop-${gradientClass.split(' ')[1].replace('to-', '')}`} />
              </linearGradient>
            </defs>
          </svg>

          {/* Score text in center */}
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <div className={`text-6xl font-bold bg-gradient-to-r ${gradientClass} bg-clip-text text-transparent`}>
              {displayScore}
            </div>
            <div className="text-gray-500 dark:text-gray-400 text-sm mt-2">out of 100</div>
          </div>
        </div>

        {/* Status message */}
        <div className="text-center max-w-md">
          <h3 className={`text-2xl font-bold mb-2 bg-gradient-to-r ${gradientClass} bg-clip-text text-transparent`}>
            {statusMessage}
          </h3>
          <p className="text-gray-600 dark:text-gray-300 text-sm leading-relaxed">
            {statusDescription}
          </p>
        </div>

        {/* Status badge */}
        {status === 'partial' && (
          <div className="mt-4 px-4 py-2 bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-200 rounded-full text-sm">
            ⚠️ Partial results - some analysis still in progress
          </div>
        )}
      </div>
    </div>
  );
};
