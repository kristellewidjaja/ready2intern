/**
 * PhaseCard component tests
 */
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { PhaseCard } from '../PhaseCard';
import type { TimelinePhase } from '../../types/results';

const mockPhase: TimelinePhase = {
  phase_id: 'phase_1',
  phase_number: 1,
  title: 'Foundation & Quick Wins',
  description: 'Establish strong foundation by optimizing resume.',
  start_week: 1,
  end_week: 2,
  focus_areas: [
    'Resume optimization',
    'GitHub profile setup',
    'Distributed systems fundamentals',
  ],
  tasks: [
    {
      task_id: 'task_1',
      title: 'Resume Audit',
      description: 'Conduct comprehensive audit of resume.',
      gap_ids: ['gap_1', 'gap_2'],
      estimated_hours: 6,
      priority: 'high',
      dependencies: [],
      resources: ['Resource 1', 'Resource 2', 'Resource 3', 'Resource 4'],
      success_criteria: 'Resume includes all keywords',
    },
    {
      task_id: 'task_2',
      title: 'GitHub Setup',
      description: 'Create GitHub profile.',
      gap_ids: ['gap_3'],
      estimated_hours: 4,
      priority: 'medium',
      dependencies: [],
      resources: ['GitHub guide'],
      success_criteria: 'Profile is live',
    },
  ],
  milestones: [
    {
      milestone_id: 'milestone_1',
      title: 'Resume Complete',
      description: 'Resume updated with all keywords.',
      target_date: '2026-01-22',
      completion_criteria: ['Resume audit complete', 'Keywords integrated'],
      deliverables: ['Updated resume PDF', 'ATS score screenshot'],
    },
  ],
  estimated_hours_per_week: 12,
  success_metrics: [
    'Resume ATS score increases to 95+',
    'GitHub profile receives first visit',
  ],
};

describe('PhaseCard', () => {
  describe('Rendering', () => {
    it('should render phase header with basic information', () => {
      render(<PhaseCard phase={mockPhase} />);

      expect(screen.getByText('Foundation & Quick Wins')).toBeInTheDocument();
      expect(screen.getByText('1')).toBeInTheDocument(); // Phase number
      expect(screen.getByText(/Weeks 1-2/)).toBeInTheDocument();
      expect(screen.getByText(/2 tasks/)).toBeInTheDocument();
      expect(screen.getByText(/12 hrs\/week/)).toBeInTheDocument();
    });

    it('should render collapsed by default', () => {
      render(<PhaseCard phase={mockPhase} />);

      // Description should not be visible initially
      expect(screen.queryByText(/Establish strong foundation/)).not.toBeInTheDocument();
    });

    it('should render expanded when isExpanded prop is true', () => {
      render(<PhaseCard phase={mockPhase} isExpanded={true} />);

      // Description should be visible
      expect(screen.getByText(/Establish strong foundation/)).toBeInTheDocument();
    });
  });

  describe('Expand/Collapse Functionality', () => {
    it('should expand when header is clicked', () => {
      render(<PhaseCard phase={mockPhase} />);

      const header = screen.getByRole('button');
      fireEvent.click(header);

      expect(screen.getByText(/Establish strong foundation/)).toBeInTheDocument();
    });

    it('should collapse when clicked again', () => {
      render(<PhaseCard phase={mockPhase} isExpanded={true} />);

      const header = screen.getByRole('button');
      fireEvent.click(header);

      expect(screen.queryByText(/Establish strong foundation/)).not.toBeInTheDocument();
    });

    it('should rotate arrow icon when expanding', () => {
      render(<PhaseCard phase={mockPhase} />);

      const header = screen.getByRole('button');
      const arrow = header.querySelector('.transform');

      expect(arrow).toHaveStyle({ transform: 'rotate(0deg)' });

      fireEvent.click(header);

      expect(arrow).toHaveStyle({ transform: 'rotate(180deg)' });
    });
  });

  describe('Phase Content', () => {
    it('should render description when expanded', () => {
      render(<PhaseCard phase={mockPhase} isExpanded={true} />);

      expect(screen.getByText(/Establish strong foundation/)).toBeInTheDocument();
    });

    it('should render focus areas when expanded', () => {
      render(<PhaseCard phase={mockPhase} isExpanded={true} />);

      expect(screen.getByText('🎯 Focus Areas')).toBeInTheDocument();
      expect(screen.getByText('Resume optimization')).toBeInTheDocument();
      expect(screen.getByText('GitHub profile setup')).toBeInTheDocument();
      expect(screen.getByText('Distributed systems fundamentals')).toBeInTheDocument();
    });

    it('should not render focus areas section if empty', () => {
      const phaseNoFocus = { ...mockPhase, focus_areas: [] };
      render(<PhaseCard phase={phaseNoFocus} isExpanded={true} />);

      expect(screen.queryByText('🎯 Focus Areas')).not.toBeInTheDocument();
    });
  });

  describe('Tasks Rendering', () => {
    it('should render all tasks when expanded', () => {
      render(<PhaseCard phase={mockPhase} isExpanded={true} />);

      expect(screen.getByText('✅ Tasks')).toBeInTheDocument();
      expect(screen.getByText('Resume Audit')).toBeInTheDocument();
      expect(screen.getByText('GitHub Setup')).toBeInTheDocument();
    });

    it('should render task details', () => {
      render(<PhaseCard phase={mockPhase} isExpanded={true} />);

      expect(screen.getByText('Conduct comprehensive audit of resume.')).toBeInTheDocument();
      expect(screen.getByText(/6 hours/)).toBeInTheDocument();
      expect(screen.getByText(/2 gap\(s\)/)).toBeInTheDocument();
    });

    it('should render priority badges with correct styling', () => {
      render(<PhaseCard phase={mockPhase} isExpanded={true} />);

      const highPriority = screen.getByText('HIGH');
      expect(highPriority).toHaveClass('text-red-600');

      const mediumPriority = screen.getByText('MEDIUM');
      expect(mediumPriority).toHaveClass('text-orange-600');
    });

    it('should render task resources', () => {
      render(<PhaseCard phase={mockPhase} isExpanded={true} />);

      expect(screen.getByText('📚 Resources:')).toBeInTheDocument();
      expect(screen.getByText('Resource 1')).toBeInTheDocument();
      expect(screen.getByText('Resource 2')).toBeInTheDocument();
      expect(screen.getByText('Resource 3')).toBeInTheDocument();
      expect(screen.getByText('+1 more resources')).toBeInTheDocument();
    });

    it('should not show more resources message if 3 or fewer', () => {
      const phaseFewerResources = {
        ...mockPhase,
        tasks: [
          {
            ...mockPhase.tasks[0],
            resources: ['Resource 1', 'Resource 2'],
          },
        ],
      };
      render(<PhaseCard phase={phaseFewerResources} isExpanded={true} />);

      expect(screen.queryByText(/more resources/)).not.toBeInTheDocument();
    });

    it('should not render tasks section if no tasks', () => {
      const phaseNoTasks = { ...mockPhase, tasks: [] };
      render(<PhaseCard phase={phaseNoTasks} isExpanded={true} />);

      expect(screen.queryByText('✅ Tasks')).not.toBeInTheDocument();
    });

    it('should not show gap count if no gaps', () => {
      const phaseNoGaps = {
        ...mockPhase,
        tasks: [
          {
            ...mockPhase.tasks[0],
            gap_ids: [],
          },
        ],
      };
      render(<PhaseCard phase={phaseNoGaps} isExpanded={true} />);

      expect(screen.queryByText(/gap\(s\)/)).not.toBeInTheDocument();
    });
  });

  describe('Milestones Rendering', () => {
    it('should render milestones when expanded', () => {
      render(<PhaseCard phase={mockPhase} isExpanded={true} />);

      expect(screen.getByText('🏆 Milestones')).toBeInTheDocument();
      expect(screen.getByText('Resume Complete')).toBeInTheDocument();
      expect(screen.getByText('Resume updated with all keywords.')).toBeInTheDocument();
    });

    it('should render milestone target date', () => {
      render(<PhaseCard phase={mockPhase} isExpanded={true} />);

      expect(screen.getByText(/1\/22\/2026/)).toBeInTheDocument();
    });

    it('should render completion criteria', () => {
      render(<PhaseCard phase={mockPhase} isExpanded={true} />);

      expect(screen.getByText('Completion Criteria:')).toBeInTheDocument();
      expect(screen.getByText('Resume audit complete')).toBeInTheDocument();
      expect(screen.getByText('Keywords integrated')).toBeInTheDocument();
    });

    it('should not render milestones section if empty', () => {
      const phaseNoMilestones = { ...mockPhase, milestones: [] };
      render(<PhaseCard phase={phaseNoMilestones} isExpanded={true} />);

      expect(screen.queryByText('🏆 Milestones')).not.toBeInTheDocument();
    });

    it('should not render target date if null', () => {
      const phaseNoDate = {
        ...mockPhase,
        milestones: [
          {
            ...mockPhase.milestones[0],
            target_date: null,
          },
        ],
      };
      render(<PhaseCard phase={phaseNoDate} isExpanded={true} />);

      expect(screen.queryByText(/📅/)).not.toBeInTheDocument();
    });
  });

  describe('Success Metrics Rendering', () => {
    it('should render success metrics when expanded', () => {
      render(<PhaseCard phase={mockPhase} isExpanded={true} />);

      expect(screen.getByText('📊 Success Metrics')).toBeInTheDocument();
      expect(screen.getByText('Resume ATS score increases to 95+')).toBeInTheDocument();
      expect(screen.getByText('GitHub profile receives first visit')).toBeInTheDocument();
    });

    it('should not render success metrics section if empty', () => {
      const phaseNoMetrics = { ...mockPhase, success_metrics: [] };
      render(<PhaseCard phase={phaseNoMetrics} isExpanded={true} />);

      expect(screen.queryByText('📊 Success Metrics')).not.toBeInTheDocument();
    });
  });

  describe('Priority Colors', () => {
    it('should apply correct color for high priority', () => {
      render(<PhaseCard phase={mockPhase} isExpanded={true} />);

      const highPriority = screen.getByText('HIGH');
      expect(highPriority).toHaveClass('text-red-600');
      expect(highPriority).toHaveClass('bg-red-50');
    });

    it('should apply correct color for medium priority', () => {
      render(<PhaseCard phase={mockPhase} isExpanded={true} />);

      const mediumPriority = screen.getByText('MEDIUM');
      expect(mediumPriority).toHaveClass('text-orange-600');
      expect(mediumPriority).toHaveClass('bg-orange-50');
    });

    it('should apply correct color for low priority', () => {
      const phaseLowPriority = {
        ...mockPhase,
        tasks: [
          {
            ...mockPhase.tasks[0],
            priority: 'low' as const,
          },
        ],
      };
      render(<PhaseCard phase={phaseLowPriority} isExpanded={true} />);

      const lowPriority = screen.getByText('LOW');
      expect(lowPriority).toHaveClass('text-yellow-600');
      expect(lowPriority).toHaveClass('bg-yellow-50');
    });
  });

  describe('Edge Cases', () => {
    it('should handle phase with no content sections', () => {
      const minimalPhase: TimelinePhase = {
        phase_id: 'phase_min',
        phase_number: 1,
        title: 'Minimal Phase',
        description: 'Basic description',
        start_week: 1,
        end_week: 2,
        focus_areas: [],
        tasks: [],
        milestones: [],
        estimated_hours_per_week: 10,
        success_metrics: [],
      };

      render(<PhaseCard phase={minimalPhase} isExpanded={true} />);

      expect(screen.getByText('Minimal Phase')).toBeInTheDocument();
      expect(screen.getByText('Basic description')).toBeInTheDocument();
      // No content sections should render
      expect(screen.queryByText('🎯 Focus Areas')).not.toBeInTheDocument();
      expect(screen.queryByText('✅ Tasks')).not.toBeInTheDocument();
      expect(screen.queryByText('🏆 Milestones')).not.toBeInTheDocument();
      expect(screen.queryByText('📊 Success Metrics')).not.toBeInTheDocument();
    });

    it('should handle very long phase numbers', () => {
      const phaseHighNumber = { ...mockPhase, phase_number: 99 };
      render(<PhaseCard phase={phaseHighNumber} />);

      expect(screen.getByText('99')).toBeInTheDocument();
    });

    it('should handle phases with many tasks', () => {
      const phaseManyTasks = {
        ...mockPhase,
        tasks: Array.from({ length: 10 }, (_, i) => ({
          task_id: `task_${i}`,
          title: `Task ${i}`,
          description: `Description ${i}`,
          gap_ids: [],
          estimated_hours: 5,
          priority: 'medium' as const,
          dependencies: [],
          resources: [],
          success_criteria: 'Complete',
        })),
      };

      render(<PhaseCard phase={phaseManyTasks} isExpanded={true} />);

      expect(screen.getByText(/10 tasks/)).toBeInTheDocument();
    });
  });

  describe('Accessibility', () => {
    it('should have button role for expand/collapse', () => {
      render(<PhaseCard phase={mockPhase} />);

      const button = screen.getByRole('button');
      expect(button).toBeInTheDocument();
    });

    it('should be keyboard navigable', () => {
      render(<PhaseCard phase={mockPhase} />);

      const header = screen.getByRole('button');
      header.focus();
      expect(header).toHaveFocus();
    });
  });
});
