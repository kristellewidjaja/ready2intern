/**
 * TimelineSection component tests
 */
import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { TimelineSection } from '../TimelineSection';
import type { TimelineResult } from '../../types/results';

const mockTimeline: TimelineResult = {
  metadata: {
    total_weeks: 12,
    total_hours: 144,
    hours_per_week: 12,
    start_date: '2026-01-15',
    target_deadline: '2026-04-09',
    intensity_level: 'moderate',
    feasibility_assessment: 'Highly feasible. With 12 weeks and 12 hours/week, you have plenty of time.',
  },
  phases: [
    {
      phase_id: 'phase_1',
      phase_number: 1,
      title: 'Foundation Phase',
      description: 'Build foundation skills',
      start_week: 1,
      end_week: 3,
      focus_areas: ['Resume optimization', 'GitHub setup'],
      tasks: [
        {
          task_id: 'task_1',
          title: 'Resume Audit',
          description: 'Audit resume',
          gap_ids: ['gap_1'],
          estimated_hours: 6,
          priority: 'high',
          dependencies: [],
          resources: ['Resource 1'],
          success_criteria: 'Complete',
        },
      ],
      milestones: [
        {
          milestone_id: 'm1',
          title: 'Resume Complete',
          description: 'Resume done',
          target_date: '2026-01-22',
          completion_criteria: ['Criteria 1'],
          deliverables: ['Resume PDF'],
        },
      ],
      estimated_hours_per_week: 12,
      success_metrics: ['Metric 1'],
    },
    {
      phase_id: 'phase_2',
      phase_number: 2,
      title: 'Development Phase',
      description: 'Build skills',
      start_week: 4,
      end_week: 6,
      focus_areas: ['Coding'],
      tasks: [],
      milestones: [],
      estimated_hours_per_week: 12,
      success_metrics: [],
    },
  ],
  weekly_breakdown: [
    {
      week_number: 1,
      start_date: '2026-01-15',
      end_date: '2026-01-22',
      phase: 'Foundation Phase',
      focus: 'Resume optimization',
      tasks: ['Resume Audit', 'GitHub Setup'],
      estimated_hours: 12,
      key_deliverable: 'Updated resume',
    },
    {
      week_number: 2,
      start_date: '2026-01-22',
      end_date: '2026-01-29',
      phase: 'Foundation Phase',
      focus: 'Technical setup',
      tasks: ['Environment setup'],
      estimated_hours: 10,
      key_deliverable: 'Dev environment ready',
    },
  ],
  critical_path: ['task_1'],
  flexibility_notes: ['You can extend by 2 weeks if needed', 'Skip optional tasks'],
  motivation_tips: ['Set weekly goals', 'Track your progress', 'Celebrate small wins'],
};

describe('TimelineSection', () => {
  describe('Rendering', () => {
    it('should render section header', () => {
      render(<TimelineSection timeline={mockTimeline} />);

      expect(screen.getByText('📅 Your Development Timeline')).toBeInTheDocument();
      expect(screen.getByText('Personalized roadmap to strengthen your candidacy')).toBeInTheDocument();
    });

    it('should render metadata summary cards', () => {
      render(<TimelineSection timeline={mockTimeline} />);

      expect(screen.getByText('12')).toBeInTheDocument(); // Total weeks
      expect(screen.getByText('Total Weeks')).toBeInTheDocument();
      expect(screen.getByText('Hours/Week')).toBeInTheDocument();
      expect(screen.getByText('144')).toBeInTheDocument(); // Total hours
      expect(screen.getByText('Total Hours')).toBeInTheDocument();
    });

    it('should render intensity level badge', () => {
      render(<TimelineSection timeline={mockTimeline} />);

      expect(screen.getByText('MODERATE')).toBeInTheDocument();
      expect(screen.getByText('Intensity Level')).toBeInTheDocument();
    });

    it('should render feasibility assessment', () => {
      render(<TimelineSection timeline={mockTimeline} />);

      expect(screen.getByText('💡 Feasibility Assessment')).toBeInTheDocument();
      expect(screen.getByText(/Highly feasible/)).toBeInTheDocument();
    });
  });

  describe('Metadata Display', () => {
    it('should display correct intensity badge color for light', () => {
      const lightTimeline = {
        ...mockTimeline,
        metadata: { ...mockTimeline.metadata, intensity_level: 'light' as const },
      };
      render(<TimelineSection timeline={lightTimeline} />);

      const badge = screen.getByText('LIGHT');
      expect(badge).toHaveClass('bg-green-100');
      expect(badge).toHaveClass('text-green-700');
    });

    it('should display correct intensity badge color for moderate', () => {
      render(<TimelineSection timeline={mockTimeline} />);

      const badge = screen.getByText('MODERATE');
      expect(badge).toHaveClass('bg-yellow-100');
      expect(badge).toHaveClass('text-yellow-700');
    });

    it('should display correct intensity badge color for intensive', () => {
      const intensiveTimeline = {
        ...mockTimeline,
        metadata: { ...mockTimeline.metadata, intensity_level: 'intensive' as const },
      };
      render(<TimelineSection timeline={intensiveTimeline} />);

      const badge = screen.getByText('INTENSIVE');
      expect(badge).toHaveClass('bg-red-100');
      expect(badge).toHaveClass('text-red-700');
    });

    it('should not render feasibility section if missing', () => {
      const noFeasibility = {
        ...mockTimeline,
        metadata: { ...mockTimeline.metadata, feasibility_assessment: '' },
      };
      render(<TimelineSection timeline={noFeasibility} />);

      expect(screen.queryByText('💡 Feasibility Assessment')).not.toBeInTheDocument();
    });
  });

  describe('View Mode Toggle', () => {
    it('should default to phases view', () => {
      render(<TimelineSection timeline={mockTimeline} />);

      const phasesButton = screen.getByText('📋 By Phase');
      expect(phasesButton).toHaveClass('bg-purple-600');
      expect(phasesButton).toHaveClass('text-white');
    });

    it('should switch to weekly view when clicked', () => {
      render(<TimelineSection timeline={mockTimeline} />);

      const weeklyButton = screen.getByText('📆 Week by Week');
      fireEvent.click(weeklyButton);

      expect(weeklyButton).toHaveClass('bg-purple-600');
      expect(weeklyButton).toHaveClass('text-white');
    });

    it('should show phases in phases view', () => {
      render(<TimelineSection timeline={mockTimeline} />);

      expect(screen.getByText('Foundation Phase')).toBeInTheDocument();
      expect(screen.getByText('Development Phase')).toBeInTheDocument();
    });

    it('should show weekly breakdown in weekly view', () => {
      render(<TimelineSection timeline={mockTimeline} />);

      const weeklyButton = screen.getByText('📆 Week by Week');
      fireEvent.click(weeklyButton);

      expect(screen.getByText('Week 1')).toBeInTheDocument();
      expect(screen.getByText('Week 2')).toBeInTheDocument();
    });

    it('should only show expand all button in phases view', () => {
      render(<TimelineSection timeline={mockTimeline} />);

      expect(screen.getByText('▼ Expand All')).toBeInTheDocument();

      const weeklyButton = screen.getByText('📆 Week by Week');
      fireEvent.click(weeklyButton);

      expect(screen.queryByText('▼ Expand All')).not.toBeInTheDocument();
    });
  });

  describe('Expand All Functionality', () => {
    it('should toggle expand all text', () => {
      render(<TimelineSection timeline={mockTimeline} />);

      const expandButton = screen.getByText('▼ Expand All');
      fireEvent.click(expandButton);

      expect(screen.getByText('▲ Collapse All')).toBeInTheDocument();
    });
  });

  describe('Weekly Breakdown Display', () => {
    beforeEach(() => {
      render(<TimelineSection timeline={mockTimeline} />);
      const weeklyButton = screen.getByText('📆 Week by Week');
      fireEvent.click(weeklyButton);
    });

    it('should display week numbers', () => {
      expect(screen.getByText('Week 1')).toBeInTheDocument();
      expect(screen.getByText('Week 2')).toBeInTheDocument();
    });

    it('should display week date ranges', () => {
      expect(screen.getByText(/1\/15\/2026/)).toBeInTheDocument();
      expect(screen.getByText(/1\/22\/2026/)).toBeInTheDocument();
    });

    it('should display estimated hours', () => {
      expect(screen.getByText('12 hrs')).toBeInTheDocument();
      expect(screen.getByText('10 hrs')).toBeInTheDocument();
    });

    it('should display phase and focus', () => {
      expect(screen.getByText(/Phase: Foundation Phase/)).toBeInTheDocument();
      expect(screen.getByText('Resume optimization')).toBeInTheDocument();
    });

    it('should display tasks list', () => {
      expect(screen.getByText('Resume Audit')).toBeInTheDocument();
      expect(screen.getByText('GitHub Setup')).toBeInTheDocument();
    });

    it('should display key deliverable', () => {
      expect(screen.getByText(/Updated resume/)).toBeInTheDocument();
      expect(screen.getByText(/Dev environment ready/)).toBeInTheDocument();
    });

    it('should not display date range if dates are null', () => {
      const noDateTimeline = {
        ...mockTimeline,
        weekly_breakdown: [
          {
            ...mockTimeline.weekly_breakdown[0],
            start_date: null,
            end_date: null,
          },
        ],
      };
      const { container } = render(<TimelineSection timeline={noDateTimeline} />);
      const weeklyButton = screen.getByText('📆 Week by Week');
      fireEvent.click(weeklyButton);

      // Should not find any date elements
      const dates = container.querySelectorAll('p.text-sm.text-gray-600');
      const hasDatePattern = Array.from(dates).some(el => /\d{1,2}\/\d{1,2}\/\d{4}/.test(el.textContent || ''));
      expect(hasDatePattern).toBe(false);
    });
  });

  describe('Critical Path Display', () => {
    it('should display critical path section', () => {
      render(<TimelineSection timeline={mockTimeline} />);

      expect(screen.getByText('🚨 Critical Path (Must Complete)')).toBeInTheDocument();
      expect(screen.getByText(/These tasks are essential/)).toBeInTheDocument();
    });

    it('should display critical task titles', () => {
      render(<TimelineSection timeline={mockTimeline} />);

      expect(screen.getByText('Resume Audit')).toBeInTheDocument();
    });

    it('should not display critical path if empty', () => {
      const noCritical = { ...mockTimeline, critical_path: [] };
      render(<TimelineSection timeline={noCritical} />);

      expect(screen.queryByText('🚨 Critical Path (Must Complete)')).not.toBeInTheDocument();
    });

    it('should display task ID if task not found', () => {
      const unknownTask = { ...mockTimeline, critical_path: ['unknown_task_id'] };
      render(<TimelineSection timeline={unknownTask} />);

      expect(screen.getByText('unknown_task_id')).toBeInTheDocument();
    });
  });

  describe('Flexibility Notes Display', () => {
    it('should display flexibility notes section', () => {
      render(<TimelineSection timeline={mockTimeline} />);

      expect(screen.getByText('🔄 Flexibility Options')).toBeInTheDocument();
      expect(screen.getByText(/If the timeline feels too aggressive/)).toBeInTheDocument();
    });

    it('should display all flexibility notes', () => {
      render(<TimelineSection timeline={mockTimeline} />);

      expect(screen.getByText('You can extend by 2 weeks if needed')).toBeInTheDocument();
      expect(screen.getByText('Skip optional tasks')).toBeInTheDocument();
    });

    it('should not display flexibility section if empty', () => {
      const noFlex = { ...mockTimeline, flexibility_notes: [] };
      render(<TimelineSection timeline={noFlex} />);

      expect(screen.queryByText('🔄 Flexibility Options')).not.toBeInTheDocument();
    });
  });

  describe('Motivation Tips Display', () => {
    it('should display motivation tips section', () => {
      render(<TimelineSection timeline={mockTimeline} />);

      expect(screen.getByText('💪 Staying Motivated')).toBeInTheDocument();
    });

    it('should display all motivation tips', () => {
      render(<TimelineSection timeline={mockTimeline} />);

      expect(screen.getByText('Set weekly goals')).toBeInTheDocument();
      expect(screen.getByText('Track your progress')).toBeInTheDocument();
      expect(screen.getByText('Celebrate small wins')).toBeInTheDocument();
    });

    it('should not display motivation section if empty', () => {
      const noMotivation = { ...mockTimeline, motivation_tips: [] };
      render(<TimelineSection timeline={noMotivation} />);

      expect(screen.queryByText('💪 Staying Motivated')).not.toBeInTheDocument();
    });
  });

  describe('Edge Cases', () => {
    it('should handle timeline with no phases', () => {
      const noPhases = { ...mockTimeline, phases: [] };
      render(<TimelineSection timeline={noPhases} />);

      expect(screen.getByText('📅 Your Development Timeline')).toBeInTheDocument();
      // Should not crash
    });

    it('should handle timeline with no weekly breakdown', () => {
      const noWeekly = { ...mockTimeline, weekly_breakdown: [] };
      render(<TimelineSection timeline={noWeekly} />);

      const weeklyButton = screen.getByText('📆 Week by Week');
      fireEvent.click(weeklyButton);

      // Should not crash, just show empty state
    });

    it('should handle minimal timeline data', () => {
      const minimalTimeline: TimelineResult = {
        metadata: {
          total_weeks: 8,
          total_hours: 96,
          hours_per_week: 12,
          start_date: null,
          target_deadline: null,
          intensity_level: 'light',
          feasibility_assessment: '',
        },
        phases: [],
        weekly_breakdown: [],
        critical_path: [],
        flexibility_notes: [],
        motivation_tips: [],
      };

      render(<TimelineSection timeline={minimalTimeline} />);

      expect(screen.getByText('8')).toBeInTheDocument();
      expect(screen.getByText('96')).toBeInTheDocument();
      expect(screen.getByText('LIGHT')).toBeInTheDocument();
    });

    it('should handle very long feasibility assessment', () => {
      const longAssessment = {
        ...mockTimeline,
        metadata: {
          ...mockTimeline.metadata,
          feasibility_assessment: 'A'.repeat(500),
        },
      };

      render(<TimelineSection timeline={longAssessment} />);

      expect(screen.getByText(/A{500}/)).toBeInTheDocument();
    });
  });

  describe('Styling and Layout', () => {
    it('should apply correct styling to section container', () => {
      const { container } = render(<TimelineSection timeline={mockTimeline} />);

      const section = container.firstChild;
      expect(section).toHaveClass('bg-white');
      expect(section).toHaveClass('rounded-xl');
      expect(section).toHaveClass('shadow-lg');
    });

    it('should use grid layout for metadata cards', () => {
      const { container } = render(<TimelineSection timeline={mockTimeline} />);

      const grid = container.querySelector('.grid');
      expect(grid).toHaveClass('md:grid-cols-4');
    });

    it('should apply hover effects to weekly cards', () => {
      render(<TimelineSection timeline={mockTimeline} />);

      const weeklyButton = screen.getByText('📆 Week by Week');
      fireEvent.click(weeklyButton);

      const weekCard = screen.getByText('Week 1').closest('.border-2');
      expect(weekCard).toHaveClass('hover:border-purple-300');
    });
  });

  describe('Accessibility', () => {
    it('should have accessible button roles', () => {
      render(<TimelineSection timeline={mockTimeline} />);

      const phasesButton = screen.getByRole('button', { name: /By Phase/ });
      const weeklyButton = screen.getByRole('button', { name: /Week by Week/ });

      expect(phasesButton).toBeInTheDocument();
      expect(weeklyButton).toBeInTheDocument();
    });

    it('should be keyboard navigable', () => {
      render(<TimelineSection timeline={mockTimeline} />);

      const phasesButton = screen.getByText('📋 By Phase');
      phasesButton.focus();
      expect(phasesButton).toHaveFocus();
    });
  });
});
