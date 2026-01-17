/**
 * Category score card component for ATS, Role Match, and Company Fit scores
 * Features: Individual progress bars, hover tooltips, icons, responsive layout
 */
import { useState } from 'react';
import type { ScoreDetail } from '../types';

interface CategoryScoreCardProps {
  title: string;
  scoreDetail: ScoreDetail;
  icon: string;
  color: 'blue' | 'purple' | 'green';
}

export const CategoryScoreCard = ({
  title,
  scoreDetail,
  icon,
  color,
}: CategoryScoreCardProps) => {
  const [showTooltip, setShowTooltip] = useState(false);

  // Color mappings for different score categories
  const colorClasses = {
    blue: {
      text: 'text-blue-600 dark:text-blue-400',
      bg: 'bg-blue-50 dark:bg-blue-900/20',
      border: 'border-blue-200 dark:border-blue-800',
      progress: 'bg-blue-600',
      progressBg: 'bg-blue-100 dark:bg-blue-900/30',
    },
    purple: {
      text: 'text-purple-600 dark:text-purple-400',
      bg: 'bg-purple-50 dark:bg-purple-900/20',
      border: 'border-purple-200 dark:border-purple-800',
      progress: 'bg-purple-600',
      progressBg: 'bg-purple-100 dark:bg-purple-900/30',
    },
    green: {
      text: 'text-green-600 dark:text-green-400',
      bg: 'bg-green-50 dark:bg-green-900/20',
      border: 'border-green-200 dark:border-green-800',
      progress: 'bg-green-600',
      progressBg: 'bg-green-100 dark:bg-green-900/30',
    },
  };

  const colors = colorClasses[color];

  return (
    <div
      className={`relative rounded-lg border-2 ${colors.border} ${colors.bg} p-6 transition-all duration-200 hover:shadow-lg hover:scale-105 cursor-pointer`}
      onMouseEnter={() => setShowTooltip(true)}
      onMouseLeave={() => setShowTooltip(false)}
    >
      {/* Icon and Title */}
      <div className="flex items-center mb-4">
        <span className="text-3xl mr-3">{icon}</span>
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
          {title}
        </h3>
      </div>

      {/* Score Display */}
      <div className={`text-5xl font-bold ${colors.text} mb-4`}>
        {scoreDetail.score}
        <span className="text-2xl text-gray-500 dark:text-gray-400">/100</span>
      </div>

      {/* Progress Bar */}
      <div className="mb-4">
        <div className={`w-full h-3 ${colors.progressBg} rounded-full overflow-hidden`}>
          <div
            className={`h-full ${colors.progress} rounded-full transition-all duration-1000 ease-out`}
            style={{ width: `${scoreDetail.score}%` }}
          />
        </div>
      </div>

      {/* Brief explanation (always visible) */}
      <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-2">
        {scoreDetail.explanation}
      </p>

      {/* Tooltip with detailed information */}
      {showTooltip && (
        <div className="absolute z-10 left-0 right-0 top-full mt-2 p-4 bg-white dark:bg-gray-800 rounded-lg shadow-xl border-2 border-gray-200 dark:border-gray-700 animate-fadeIn">
          {/* Explanation */}
          <p className="text-sm text-gray-700 dark:text-gray-300 mb-3">
            {scoreDetail.explanation}
          </p>

          {/* Strengths */}
          {scoreDetail.strengths && scoreDetail.strengths.length > 0 && (
            <div className="mb-3">
              <h4 className="text-xs font-semibold text-green-600 dark:text-green-400 mb-1 uppercase">
                ✓ Strengths
              </h4>
              <ul className="text-xs text-gray-600 dark:text-gray-400 space-y-1">
                {scoreDetail.strengths.map((strength, idx) => (
                  <li key={idx} className="flex items-start">
                    <span className="text-green-500 mr-1">•</span>
                    <span>{strength}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Weaknesses */}
          {scoreDetail.weaknesses && scoreDetail.weaknesses.length > 0 && (
            <div>
              <h4 className="text-xs font-semibold text-orange-600 dark:text-orange-400 mb-1 uppercase">
                ⚠ Areas for Improvement
              </h4>
              <ul className="text-xs text-gray-600 dark:text-gray-400 space-y-1">
                {scoreDetail.weaknesses.map((weakness, idx) => (
                  <li key={idx} className="flex items-start">
                    <span className="text-orange-500 mr-1">•</span>
                    <span>{weakness}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
