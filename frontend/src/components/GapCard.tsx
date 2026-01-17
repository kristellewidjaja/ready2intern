/**
 * GapCard component - displays a single gap with expandable details
 */
import { useState } from 'react';
import type { TechnicalGap, ExperienceGap, CompanyFitGap, ResumeOptimizationGap } from '../types';

type Gap = TechnicalGap | ExperienceGap | CompanyFitGap | ResumeOptimizationGap;

interface GapCardProps {
  gap: Gap;
  type: 'technical' | 'experience' | 'company_fit' | 'resume';
}

const priorityConfig = {
  high: {
    label: 'High Priority',
    bgColor: 'bg-red-100 dark:bg-red-900/30',
    textColor: 'text-red-800 dark:text-red-300',
    borderColor: 'border-red-500',
    dotColor: 'bg-red-500',
  },
  medium: {
    label: 'Medium Priority',
    bgColor: 'bg-orange-100 dark:bg-orange-900/30',
    textColor: 'text-orange-800 dark:text-orange-300',
    borderColor: 'border-orange-500',
    dotColor: 'bg-orange-500',
  },
  low: {
    label: 'Low Priority',
    bgColor: 'bg-yellow-100 dark:bg-yellow-900/30',
    textColor: 'text-yellow-800 dark:text-yellow-300',
    borderColor: 'border-yellow-500',
    dotColor: 'bg-yellow-500',
  },
};

const typeConfig = {
  technical: { icon: '💻', label: 'Technical' },
  experience: { icon: '🚀', label: 'Experience' },
  company_fit: { icon: '🤝', label: 'Company Fit' },
  resume: { icon: '📝', label: 'Resume' },
};

export const GapCard = ({ gap, type }: GapCardProps) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const priority = priorityConfig[gap.priority];
  const typeInfo = typeConfig[type];

  const toggleExpanded = () => setIsExpanded(!isExpanded);

  // Type-specific rendering for recommendations
  const renderRecommendations = () => {
    if ('recommendations' in gap && gap.recommendations.length > 0) {
      // Technical or Company Fit or Resume gaps
      if (type === 'technical' || type === 'company_fit' || type === 'resume') {
        const recommendations = gap.recommendations as any[];
        return (
          <div className="space-y-4">
            {recommendations.map((rec, index) => (
              <div key={index} className="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-4">
                <div className="flex items-start mb-3">
                  <div className="flex-shrink-0 w-6 h-6 flex items-center justify-center bg-purple-500 text-white rounded-full text-xs font-bold mr-3 mt-0.5">
                    {index + 1}
                  </div>
                  <p className="font-semibold text-gray-900 dark:text-white flex-1">{rec.action}</p>
                </div>

                {/* Resources */}
                {rec.resources && rec.resources.length > 0 && (
                  <div className="ml-9 mb-3">
                    <h5 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                      📚 Resources:
                    </h5>
                    <div className="space-y-2">
                      {rec.resources.map((resource: any, resIndex: number) => (
                        <div
                          key={resIndex}
                          className="p-3 bg-white dark:bg-gray-800 rounded border border-gray-200 dark:border-gray-600"
                        >
                          <div className="flex items-start justify-between mb-1">
                            <p className="font-medium text-gray-900 dark:text-white text-sm">
                              {resource.name}
                            </p>
                            <span className="text-xs px-2 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-300 rounded ml-2 flex-shrink-0">
                              {resource.type}
                            </span>
                          </div>
                          {resource.url && resource.url !== 'Search online' && (
                            <a
                              href={resource.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-xs text-blue-600 dark:text-blue-400 hover:underline"
                            >
                              {resource.url}
                            </a>
                          )}
                          <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                            ⏱️ {resource.estimated_time}
                          </p>
                          {resource.notes && (
                            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1 italic">
                              {resource.notes}
                            </p>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Project Ideas (for experience gaps) */}
                {rec.project_ideas && rec.project_ideas.length > 0 && (
                  <div className="ml-9 mb-3">
                    <h5 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                      💡 Project Ideas:
                    </h5>
                    <div className="space-y-3">
                      {rec.project_ideas.map((project: any, projIndex: number) => (
                        <div
                          key={projIndex}
                          className="p-3 bg-white dark:bg-gray-800 rounded border border-gray-200 dark:border-gray-600"
                        >
                          <div className="flex items-start justify-between mb-2">
                            <p className="font-medium text-gray-900 dark:text-white text-sm">
                              {project.name}
                            </p>
                            <span className="text-xs px-2 py-1 bg-purple-100 dark:bg-purple-900/30 text-purple-800 dark:text-purple-300 rounded ml-2 flex-shrink-0">
                              {project.difficulty}
                            </span>
                          </div>
                          <p className="text-xs text-gray-600 dark:text-gray-400 mb-2">
                            {project.description}
                          </p>
                          {project.key_features && project.key_features.length > 0 && (
                            <div className="mb-2">
                              <p className="text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">
                                Key Features:
                              </p>
                              <ul className="text-xs text-gray-600 dark:text-gray-400 list-disc list-inside">
                                {project.key_features.map((feature: string, idx: number) => (
                                  <li key={idx}>{feature}</li>
                                ))}
                              </ul>
                            </div>
                          )}
                          {project.technologies && project.technologies.length > 0 && (
                            <div className="flex flex-wrap gap-1 mb-2">
                              {project.technologies.map((tech: string, idx: number) => (
                                <span
                                  key={idx}
                                  className="text-xs px-2 py-0.5 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded"
                                >
                                  {tech}
                                </span>
                              ))}
                            </div>
                          )}
                          <p className="text-xs text-gray-500 dark:text-gray-400">
                            ⏱️ {project.estimated_time} • 📊 Portfolio Value: {project.portfolio_value}
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Before/After examples (for resume gaps) */}
                {rec.before_example && (
                  <div className="ml-9 mb-3">
                    <h5 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                      📝 Example:
                    </h5>
                    <div className="space-y-2">
                      <div className="p-2 bg-red-50 dark:bg-red-900/20 rounded border-l-4 border-red-400">
                        <p className="text-xs font-semibold text-red-800 dark:text-red-300 mb-1">
                          ❌ Before:
                        </p>
                        <p className="text-xs text-gray-700 dark:text-gray-300">{rec.before_example}</p>
                      </div>
                      {rec.after_example && (
                        <div className="p-2 bg-green-50 dark:bg-green-900/20 rounded border-l-4 border-green-400">
                          <p className="text-xs font-semibold text-green-800 dark:text-green-300 mb-1">
                            ✓ After:
                          </p>
                          <p className="text-xs text-gray-700 dark:text-gray-300">{rec.after_example}</p>
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {/* Success Criteria */}
                <div className="ml-9 mb-2">
                  <p className="text-xs text-gray-600 dark:text-gray-400">
                    <span className="font-semibold">✓ Success:</span> {rec.success_criteria}
                  </p>
                </div>

                {/* Estimated Time */}
                <div className="ml-9">
                  <p className="text-xs text-gray-500 dark:text-gray-400">
                    <span className="font-semibold">⏱️ Time:</span> {rec.estimated_time}
                  </p>
                </div>
              </div>
            ))}
          </div>
        );
      }
    }

    return null;
  };

  return (
    <div
      className={`border-2 rounded-lg overflow-hidden transition-all duration-200 ${
        isExpanded ? 'ring-2 ring-purple-500' : ''
      } ${priority.borderColor}`}
    >
      {/* Header - Always Visible */}
      <button
        onClick={toggleExpanded}
        className={`w-full p-4 text-left transition-colors hover:bg-gray-50 dark:hover:bg-gray-700/50 ${
          priority.bgColor
        }`}
      >
        <div className="flex items-start justify-between mb-2">
          <div className="flex items-start flex-1">
            <span className="text-2xl mr-3">{typeInfo.icon}</span>
            <div className="flex-1">
              <h4 className="font-bold text-gray-900 dark:text-white mb-1">{gap.title}</h4>
              <div className="flex items-center gap-2 mb-2">
                <span
                  className={`text-xs px-2 py-1 rounded font-semibold ${priority.bgColor} ${priority.textColor}`}
                >
                  {priority.label}
                </span>
                <span className="text-xs px-2 py-1 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded">
                  {typeInfo.label}
                </span>
                {'category' in gap && (
                  <span className="text-xs text-gray-500 dark:text-gray-400">
                    {gap.category.replace(/_/g, ' ')}
                  </span>
                )}
              </div>
              <p className="text-sm text-gray-700 dark:text-gray-300">{gap.description}</p>
            </div>
          </div>
          <div className="ml-4 flex-shrink-0">
            <div
              className={`transform transition-transform duration-200 ${
                isExpanded ? 'rotate-180' : ''
              }`}
            >
              <svg
                className="w-6 h-6 text-gray-600 dark:text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </div>
          </div>
        </div>
      </button>

      {/* Expanded Content */}
      {isExpanded && (
        <div className="p-4 bg-white dark:bg-gray-800 border-t-2 border-gray-200 dark:border-gray-700">
          {/* Priority Reasoning */}
          <div className="mb-4">
            <h5 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
              Why This Matters:
            </h5>
            <p className="text-sm text-gray-600 dark:text-gray-400">{gap.priority_reasoning}</p>
          </div>

          {/* Impact */}
          <div className="mb-4">
            <h5 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
              Impact on Application:
            </h5>
            <p className="text-sm text-gray-600 dark:text-gray-400">{gap.impact_on_application}</p>
          </div>

          {/* Technical-specific: Current/Target Level */}
          {'current_level' in gap && 'target_level' in gap && (
            <div className="mb-4">
              <h5 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                Skill Level:
              </h5>
              <div className="flex items-center gap-4">
                <div className="flex items-center">
                  <span className="text-xs text-gray-500 dark:text-gray-400 mr-2">Current:</span>
                  <span className="text-sm px-2 py-1 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded capitalize">
                    {gap.current_level}
                  </span>
                </div>
                <div className="text-gray-400">→</div>
                <div className="flex items-center">
                  <span className="text-xs text-gray-500 dark:text-gray-400 mr-2">Target:</span>
                  <span className="text-sm px-2 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-300 rounded capitalize font-semibold">
                    {gap.target_level}
                  </span>
                </div>
              </div>
            </div>
          )}

          {/* Company Fit-specific: Company Value */}
          {'company_value' in gap && (
            <div className="mb-4">
              <h5 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                Company Value:
              </h5>
              <p className="text-sm text-gray-600 dark:text-gray-400 italic">{gap.company_value}</p>
            </div>
          )}

          {/* Recommendations */}
          <div>
            <h5 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">
              🎯 Recommendations:
            </h5>
            {renderRecommendations()}
          </div>
        </div>
      )}
    </div>
  );
};
