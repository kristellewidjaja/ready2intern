/**
 * PhaseCard component - displays a single timeline phase with expandable tasks
 */
import { useState } from 'react';
import type { TimelinePhase } from '../types/results';

interface PhaseCardProps {
  phase: TimelinePhase;
  isExpanded?: boolean;
}

export const PhaseCard = ({ phase, isExpanded = false }: PhaseCardProps) => {
  const [expanded, setExpanded] = useState(isExpanded);

  const toggleExpanded = () => {
    setExpanded(!expanded);
  };

  // Priority color mapping
  const getPriorityColor = (priority: 'high' | 'medium' | 'low') => {
    switch (priority) {
      case 'high':
        return 'text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-900/20';
      case 'medium':
        return 'text-orange-600 dark:text-orange-400 bg-orange-50 dark:bg-orange-900/20';
      case 'low':
        return 'text-yellow-600 dark:text-yellow-400 bg-yellow-50 dark:bg-yellow-900/20';
    }
  };

  return (
    <div className="border-2 border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden hover:border-purple-300 dark:hover:border-purple-600 transition-colors duration-200">
      {/* Phase Header */}
      <button
        onClick={toggleExpanded}
        className="w-full px-6 py-4 bg-gradient-to-r from-purple-50 to-blue-50 dark:from-purple-900/30 dark:to-blue-900/30 flex items-center justify-between hover:from-purple-100 hover:to-blue-100 dark:hover:from-purple-900/50 dark:hover:to-blue-900/50 transition-colors duration-200"
      >
        <div className="flex items-center gap-4">
          <div className="flex items-center justify-center w-12 h-12 rounded-full bg-purple-600 text-white font-bold text-lg">
            {phase.phase_number}
          </div>
          <div className="text-left">
            <h3 className="text-xl font-bold text-gray-900 dark:text-white">
              {phase.title}
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
              Weeks {phase.start_week}-{phase.end_week} • {phase.tasks.length} tasks • {phase.estimated_hours_per_week} hrs/week
            </p>
          </div>
        </div>
        <div className="text-2xl text-gray-500 dark:text-gray-400 transform transition-transform duration-200" style={{ transform: expanded ? 'rotate(180deg)' : 'rotate(0deg)' }}>
          ▼
        </div>
      </button>

      {/* Phase Content */}
      {expanded && (
        <div className="px-6 py-4 bg-white dark:bg-gray-800">
          {/* Description */}
          <p className="text-gray-700 dark:text-gray-300 mb-4">
            {phase.description}
          </p>

          {/* Focus Areas */}
          {phase.focus_areas && phase.focus_areas.length > 0 && (
            <div className="mb-6">
              <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-2 flex items-center gap-2">
                🎯 Focus Areas
              </h4>
              <ul className="space-y-2">
                {phase.focus_areas.map((area, index) => (
                  <li key={index} className="flex items-start gap-2 text-gray-700 dark:text-gray-300">
                    <span className="text-purple-600 dark:text-purple-400 mt-1">•</span>
                    <span>{area}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Tasks */}
          {phase.tasks && phase.tasks.length > 0 && (
            <div className="mb-6">
              <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-3 flex items-center gap-2">
                ✅ Tasks
              </h4>
              <div className="space-y-4">
                {phase.tasks.map((task) => (
                  <div
                    key={task.task_id}
                    className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:border-purple-300 dark:hover:border-purple-600 transition-colors duration-200"
                  >
                    <div className="flex items-start justify-between mb-2">
                      <h5 className="text-base font-semibold text-gray-900 dark:text-white flex-1">
                        {task.title}
                      </h5>
                      <span className={`text-xs font-semibold px-2 py-1 rounded-full ${getPriorityColor(task.priority)}`}>
                        {task.priority.toUpperCase()}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                      {task.description}
                    </p>
                    <div className="grid grid-cols-2 gap-2 text-sm">
                      <div className="text-gray-700 dark:text-gray-300">
                        <span className="font-semibold">⏱️ Time:</span> {task.estimated_hours} hours
                      </div>
                      {task.gap_ids && task.gap_ids.length > 0 && (
                        <div className="text-gray-700 dark:text-gray-300">
                          <span className="font-semibold">🔗 Addresses:</span> {task.gap_ids.length} gap(s)
                        </div>
                      )}
                    </div>
                    {task.resources && task.resources.length > 0 && (
                      <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
                        <p className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">📚 Resources:</p>
                        <ul className="space-y-1">
                          {task.resources.slice(0, 3).map((resource, index) => (
                            <li key={index} className="text-sm text-gray-600 dark:text-gray-400 flex items-start gap-2">
                              <span className="text-purple-600 dark:text-purple-400">•</span>
                              <span>{resource}</span>
                            </li>
                          ))}
                          {task.resources.length > 3 && (
                            <li className="text-sm text-gray-500 dark:text-gray-500 italic">
                              +{task.resources.length - 3} more resources
                            </li>
                          )}
                        </ul>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Milestones */}
          {phase.milestones && phase.milestones.length > 0 && (
            <div className="mb-6">
              <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-3 flex items-center gap-2">
                🏆 Milestones
              </h4>
              <div className="space-y-3">
                {phase.milestones.map((milestone) => (
                  <div
                    key={milestone.milestone_id}
                    className="bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 border-2 border-green-200 dark:border-green-700 rounded-lg p-4"
                  >
                    <div className="flex items-start justify-between mb-2">
                      <h5 className="text-base font-semibold text-gray-900 dark:text-white">
                        {milestone.title}
                      </h5>
                      {milestone.target_date && (
                        <span className="text-sm text-gray-600 dark:text-gray-400">
                          📅 {new Date(milestone.target_date).toLocaleDateString()}
                        </span>
                      )}
                    </div>
                    <p className="text-sm text-gray-700 dark:text-gray-300 mb-2">
                      {milestone.description}
                    </p>
                    {milestone.completion_criteria && milestone.completion_criteria.length > 0 && (
                      <div className="mt-2">
                        <p className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1">Completion Criteria:</p>
                        <ul className="space-y-1">
                          {milestone.completion_criteria.map((criteria, index) => (
                            <li key={index} className="text-sm text-gray-600 dark:text-gray-400 flex items-start gap-2">
                              <span className="text-green-600 dark:text-green-400">✓</span>
                              <span>{criteria}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Success Metrics */}
          {phase.success_metrics && phase.success_metrics.length > 0 && (
            <div>
              <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-2 flex items-center gap-2">
                📊 Success Metrics
              </h4>
              <ul className="space-y-2">
                {phase.success_metrics.map((metric, index) => (
                  <li key={index} className="flex items-start gap-2 text-gray-700 dark:text-gray-300 text-sm">
                    <span className="text-purple-600 dark:text-purple-400 mt-1">•</span>
                    <span>{metric}</span>
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
