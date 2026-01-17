/**
 * GapsSection component - displays all gaps with filtering and categorization
 */
import { useState } from 'react';
import { GapCard } from './GapCard';
import type { GapAnalysis } from '../types';

interface GapsSectionProps {
  gapAnalysis: GapAnalysis;
}

type FilterType = 'all' | 'technical' | 'experience' | 'company_fit' | 'resume';
type PriorityFilter = 'all' | 'high' | 'medium' | 'low';

export const GapsSection = ({ gapAnalysis }: GapsSectionProps) => {
  const [typeFilter, setTypeFilter] = useState<FilterType>('all');
  const [priorityFilter, setPriorityFilter] = useState<PriorityFilter>('all');

  // Collect all gaps with their types
  const allGaps: Array<{ gap: any; type: 'technical' | 'experience' | 'company_fit' | 'resume' }> = [
    ...gapAnalysis.technical_gaps.map((gap) => ({ gap, type: 'technical' as const })),
    ...gapAnalysis.experience_gaps.map((gap) => ({ gap, type: 'experience' as const })),
    ...gapAnalysis.company_fit_gaps.map((gap) => ({ gap, type: 'company_fit' as const })),
    ...gapAnalysis.resume_optimization_gaps.map((gap) => ({ gap, type: 'resume' as const })),
  ];

  // Apply filters
  const filteredGaps = allGaps.filter((item) => {
    if (typeFilter !== 'all' && item.type !== typeFilter) return false;
    if (priorityFilter !== 'all' && item.gap.priority !== priorityFilter) return false;
    return true;
  });

  // Sort by priority (high -> medium -> low)
  const priorityOrder = { high: 0, medium: 1, low: 2 };
  filteredGaps.sort((a, b) => priorityOrder[a.gap.priority] - priorityOrder[b.gap.priority]);

  if (allGaps.length === 0) {
    return null;
  }

  const typeFilterOptions = [
    { value: 'all' as const, label: 'All Types', icon: '📋' },
    { value: 'technical' as const, label: 'Technical', icon: '💻' },
    { value: 'experience' as const, label: 'Experience', icon: '🚀' },
    { value: 'company_fit' as const, label: 'Company Fit', icon: '🤝' },
    { value: 'resume' as const, label: 'Resume', icon: '📝' },
  ];

  const priorityFilterOptions = [
    { value: 'all' as const, label: 'All Priorities', color: 'gray' },
    { value: 'high' as const, label: 'High', color: 'red' },
    { value: 'medium' as const, label: 'Medium', color: 'orange' },
    { value: 'low' as const, label: 'Low', color: 'yellow' },
  ];

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8 mb-8">
      {/* Header */}
      <div className="flex items-center mb-6">
        <div className="text-3xl mr-3">🎯</div>
        <div className="flex-1">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Areas for Improvement</h2>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
            {gapAnalysis.summary.total_gaps} gaps identified • Estimated preparation:{' '}
            {gapAnalysis.summary.estimated_preparation_time}
          </p>
        </div>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="p-4 bg-red-50 dark:bg-red-900/20 rounded-lg border-2 border-red-200 dark:border-red-800">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">High Priority</p>
              <p className="text-2xl font-bold text-red-800 dark:text-red-300">
                {gapAnalysis.summary.high_priority_count}
              </p>
            </div>
            <div className="text-3xl">🔴</div>
          </div>
        </div>

        <div className="p-4 bg-orange-50 dark:bg-orange-900/20 rounded-lg border-2 border-orange-200 dark:border-orange-800">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Medium Priority</p>
              <p className="text-2xl font-bold text-orange-800 dark:text-orange-300">
                {gapAnalysis.summary.medium_priority_count}
              </p>
            </div>
            <div className="text-3xl">🟠</div>
          </div>
        </div>

        <div className="p-4 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg border-2 border-yellow-200 dark:border-yellow-800">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Low Priority</p>
              <p className="text-2xl font-bold text-yellow-800 dark:text-yellow-300">
                {gapAnalysis.summary.low_priority_count}
              </p>
            </div>
            <div className="text-3xl">🟡</div>
          </div>
        </div>
      </div>

      {/* Overall Assessment */}
      <div className="mb-6 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border-l-4 border-blue-500">
        <h3 className="text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2 flex items-center">
          <span className="mr-2">💡</span>
          Overall Assessment
        </h3>
        <p className="text-sm text-gray-700 dark:text-gray-300">{gapAnalysis.summary.overall_assessment}</p>
      </div>

      {/* Quick Wins */}
      {gapAnalysis.quick_wins && gapAnalysis.quick_wins.length > 0 && (
        <div className="mb-6">
          <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-3 flex items-center">
            <span className="text-xl mr-2">⚡</span>
            Quick Wins (Start Here!)
          </h3>
          <div className="space-y-3">
            {gapAnalysis.quick_wins.map((win, index) => (
              <div
                key={index}
                className="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border-2 border-green-200 dark:border-green-800"
              >
                <div className="flex items-start justify-between mb-2">
                  <h4 className="font-bold text-gray-900 dark:text-white flex-1">{win.title}</h4>
                  <span className="text-xs px-2 py-1 bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300 rounded ml-2">
                    ⏱️ {win.estimated_time}
                  </span>
                </div>
                <p className="text-sm text-gray-700 dark:text-gray-300 mb-2">{win.description}</p>
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                  <span className="font-semibold">Impact:</span> {win.impact}
                </p>
                {win.steps && win.steps.length > 0 && (
                  <div>
                    <p className="text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">Steps:</p>
                    <ol className="text-sm text-gray-600 dark:text-gray-400 list-decimal list-inside space-y-1">
                      {win.steps.map((step, stepIndex) => (
                        <li key={stepIndex}>{step}</li>
                      ))}
                    </ol>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="mb-6">
        <div className="flex flex-col md:flex-row gap-4">
          {/* Type Filter */}
          <div className="flex-1">
            <label className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2 block">
              Filter by Type:
            </label>
            <div className="flex flex-wrap gap-2">
              {typeFilterOptions.map((option) => (
                <button
                  key={option.value}
                  onClick={() => setTypeFilter(option.value)}
                  className={`px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                    typeFilter === option.value
                      ? 'bg-purple-600 text-white shadow-lg scale-105'
                      : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                  }`}
                >
                  <span className="mr-1">{option.icon}</span>
                  {option.label}
                </button>
              ))}
            </div>
          </div>

          {/* Priority Filter */}
          <div className="flex-1">
            <label className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2 block">
              Filter by Priority:
            </label>
            <div className="flex flex-wrap gap-2">
              {priorityFilterOptions.map((option) => (
                <button
                  key={option.value}
                  onClick={() => setPriorityFilter(option.value)}
                  className={`px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                    priorityFilter === option.value
                      ? `bg-${option.color}-600 text-white shadow-lg scale-105`
                      : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                  }`}
                >
                  {option.label}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Gap Cards */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200">
            Detailed Gaps ({filteredGaps.length})
          </h3>
          {(typeFilter !== 'all' || priorityFilter !== 'all') && (
            <button
              onClick={() => {
                setTypeFilter('all');
                setPriorityFilter('all');
              }}
              className="text-sm text-purple-600 dark:text-purple-400 hover:underline"
            >
              Clear Filters
            </button>
          )}
        </div>

        {filteredGaps.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">🎉</div>
            <p className="text-gray-600 dark:text-gray-400">
              No gaps match your filters. Try adjusting your selection.
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {filteredGaps.map((item, index) => (
              <GapCard key={item.gap.gap_id || index} gap={item.gap} type={item.type} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
