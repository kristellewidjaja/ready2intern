/**
 * TimelineSection component - displays complete development timeline
 */
import { useState } from 'react';
import { PhaseCard } from './PhaseCard';
import type { TimelineResult } from '../types/results';

interface TimelineSectionProps {
  timeline: TimelineResult;
}

export const TimelineSection = ({ timeline }: TimelineSectionProps) => {
  const [viewMode, setViewMode] = useState<'phases' | 'weekly'>('phases');
  const [expandAll, setExpandAll] = useState(false);

  const { metadata, phases, weekly_breakdown, critical_path, flexibility_notes, motivation_tips } = timeline;

  // Intensity level styling
  const getIntensityBadge = (intensity: 'light' | 'moderate' | 'intensive') => {
    switch (intensity) {
      case 'light':
        return 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300';
      case 'moderate':
        return 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-300';
      case 'intensive':
        return 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300';
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8 mb-8">
      {/* Header */}
      <div className="mb-6">
        <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-2 flex items-center gap-3">
          📅 Your Development Timeline
        </h2>
        <p className="text-gray-600 dark:text-gray-400">
          Personalized roadmap to strengthen your candidacy
        </p>
      </div>

      {/* Metadata Summary */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-gradient-to-r from-purple-50 to-blue-50 dark:from-purple-900/20 dark:to-blue-900/20 rounded-lg p-4 border-2 border-purple-200 dark:border-purple-700">
          <div className="text-3xl font-bold text-purple-600 dark:text-purple-400">
            {metadata.total_weeks}
          </div>
          <div className="text-sm text-gray-700 dark:text-gray-300 mt-1">
            Total Weeks
          </div>
        </div>
        <div className="bg-gradient-to-r from-blue-50 to-cyan-50 dark:from-blue-900/20 dark:to-cyan-900/20 rounded-lg p-4 border-2 border-blue-200 dark:border-blue-700">
          <div className="text-3xl font-bold text-blue-600 dark:text-blue-400">
            {metadata.hours_per_week}
          </div>
          <div className="text-sm text-gray-700 dark:text-gray-300 mt-1">
            Hours/Week
          </div>
        </div>
        <div className="bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 rounded-lg p-4 border-2 border-green-200 dark:border-green-700">
          <div className="text-3xl font-bold text-green-600 dark:text-green-400">
            {metadata.total_hours}
          </div>
          <div className="text-sm text-gray-700 dark:text-gray-300 mt-1">
            Total Hours
          </div>
        </div>
        <div className="bg-gradient-to-r from-orange-50 to-amber-50 dark:from-orange-900/20 dark:to-amber-900/20 rounded-lg p-4 border-2 border-orange-200 dark:border-orange-700">
          <div className={`text-sm font-semibold px-3 py-1 rounded-full inline-block ${getIntensityBadge(metadata.intensity_level)}`}>
            {metadata.intensity_level.toUpperCase()}
          </div>
          <div className="text-sm text-gray-700 dark:text-gray-300 mt-2">
            Intensity Level
          </div>
        </div>
      </div>

      {/* Feasibility Assessment */}
      {metadata.feasibility_assessment && (
        <div className="bg-blue-50 dark:bg-blue-900/20 border-2 border-blue-200 dark:border-blue-700 rounded-lg p-4 mb-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2 flex items-center gap-2">
            💡 Feasibility Assessment
          </h3>
          <p className="text-gray-700 dark:text-gray-300 text-sm leading-relaxed">
            {metadata.feasibility_assessment}
          </p>
        </div>
      )}

      {/* View Mode Toggle */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex gap-2">
          <button
            onClick={() => setViewMode('phases')}
            className={`px-4 py-2 rounded-lg font-semibold transition-colors duration-200 ${
              viewMode === 'phases'
                ? 'bg-purple-600 text-white'
                : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'
            }`}
          >
            📋 By Phase
          </button>
          <button
            onClick={() => setViewMode('weekly')}
            className={`px-4 py-2 rounded-lg font-semibold transition-colors duration-200 ${
              viewMode === 'weekly'
                ? 'bg-purple-600 text-white'
                : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'
            }`}
          >
            📆 Week by Week
          </button>
        </div>
        {viewMode === 'phases' && (
          <button
            onClick={() => setExpandAll(!expandAll)}
            className="text-sm text-purple-600 dark:text-purple-400 hover:text-purple-700 dark:hover:text-purple-300 font-semibold"
          >
            {expandAll ? '▲ Collapse All' : '▼ Expand All'}
          </button>
        )}
      </div>

      {/* Phases View */}
      {viewMode === 'phases' && (
        <div className="space-y-4 mb-8">
          {phases.map((phase) => (
            <PhaseCard key={phase.phase_id} phase={phase} isExpanded={expandAll} />
          ))}
        </div>
      )}

      {/* Weekly Breakdown View */}
      {viewMode === 'weekly' && (
        <div className="space-y-3 mb-8">
          {weekly_breakdown.map((week) => (
            <div
              key={week.week_number}
              className="border-2 border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:border-purple-300 dark:hover:border-purple-600 transition-colors duration-200"
            >
              <div className="flex items-start justify-between mb-3">
                <div>
                  <h4 className="text-lg font-bold text-gray-900 dark:text-white">
                    Week {week.week_number}
                  </h4>
                  {week.start_date && week.end_date && (
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {new Date(week.start_date).toLocaleDateString()} - {new Date(week.end_date).toLocaleDateString()}
                    </p>
                  )}
                </div>
                <span className="text-sm font-semibold text-purple-600 dark:text-purple-400 bg-purple-50 dark:bg-purple-900/30 px-3 py-1 rounded-full">
                  {week.estimated_hours} hrs
                </span>
              </div>
              <div className="mb-3">
                <span className="text-sm font-semibold text-gray-700 dark:text-gray-300">
                  Phase: {week.phase}
                </span>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                  {week.focus}
                </p>
              </div>
              {week.tasks && week.tasks.length > 0 && (
                <div className="mb-3">
                  <p className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">Tasks:</p>
                  <ul className="space-y-1">
                    {week.tasks.map((task, index) => (
                      <li key={index} className="text-sm text-gray-600 dark:text-gray-400 flex items-start gap-2">
                        <span className="text-purple-600 dark:text-purple-400 mt-1">•</span>
                        <span>{task}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              <div className="pt-3 border-t border-gray-200 dark:border-gray-700">
                <p className="text-sm text-gray-700 dark:text-gray-300">
                  <span className="font-semibold">🎯 Key Deliverable:</span> {week.key_deliverable}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Critical Path */}
      {critical_path && critical_path.length > 0 && (
        <div className="bg-red-50 dark:bg-red-900/20 border-2 border-red-200 dark:border-red-700 rounded-lg p-4 mb-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3 flex items-center gap-2">
            🚨 Critical Path (Must Complete)
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
            These tasks are essential to meet your deadline. Prioritize these if time becomes tight.
          </p>
          <ul className="space-y-2">
            {critical_path.map((taskId, index) => {
              // Find the task details from phases
              let taskTitle = taskId;
              phases.forEach((phase) => {
                const task = phase.tasks.find((t) => t.task_id === taskId);
                if (task) {
                  taskTitle = task.title;
                }
              });
              return (
                <li key={index} className="flex items-start gap-2 text-gray-700 dark:text-gray-300">
                  <span className="text-red-600 dark:text-red-400 font-bold">▸</span>
                  <span>{taskTitle}</span>
                </li>
              );
            })}
          </ul>
        </div>
      )}

      {/* Flexibility Notes */}
      {flexibility_notes && flexibility_notes.length > 0 && (
        <div className="bg-yellow-50 dark:bg-yellow-900/20 border-2 border-yellow-200 dark:border-yellow-700 rounded-lg p-4 mb-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3 flex items-center gap-2">
            🔄 Flexibility Options
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
            If the timeline feels too aggressive, consider these adjustments:
          </p>
          <ul className="space-y-2">
            {flexibility_notes.map((note, index) => (
              <li key={index} className="flex items-start gap-2 text-gray-700 dark:text-gray-300">
                <span className="text-yellow-600 dark:text-yellow-400 mt-1">•</span>
                <span>{note}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Motivation Tips */}
      {motivation_tips && motivation_tips.length > 0 && (
        <div className="bg-green-50 dark:bg-green-900/20 border-2 border-green-200 dark:border-green-700 rounded-lg p-4">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3 flex items-center gap-2">
            💪 Staying Motivated
          </h3>
          <ul className="space-y-2">
            {motivation_tips.map((tip, index) => (
              <li key={index} className="flex items-start gap-2 text-gray-700 dark:text-gray-300">
                <span className="text-green-600 dark:text-green-400 mt-1">✓</span>
                <span>{tip}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
