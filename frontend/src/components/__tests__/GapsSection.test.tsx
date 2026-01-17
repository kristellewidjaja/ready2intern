/**
 * Tests for GapsSection component
 */
import { describe, it, expect } from 'vitest';
import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { GapsSection } from '../GapsSection';
import type { GapAnalysis } from '../../types';

describe('GapsSection', () => {
  const mockGapAnalysis: GapAnalysis = {
    summary: {
      total_gaps: 6,
      high_priority_count: 3,
      medium_priority_count: 2,
      low_priority_count: 1,
      estimated_preparation_time: '6-8 weeks',
      overall_assessment: 'Strong candidate with some areas for improvement',
    },
    technical_gaps: [
      {
        gap_id: 'tech_1',
        category: 'technical_skills',
        title: 'Distributed Systems',
        description: 'Need distributed systems knowledge',
        priority: 'high',
        priority_reasoning: 'Core requirement',
        current_level: 'none',
        target_level: 'intermediate',
        impact_on_application: 'High impact',
        recommendations: [],
      },
      {
        gap_id: 'tech_2',
        category: 'tools',
        title: 'CI/CD Pipelines',
        description: 'Need CI/CD experience',
        priority: 'medium',
        priority_reasoning: 'Important skill',
        current_level: 'beginner',
        target_level: 'intermediate',
        impact_on_application: 'Medium impact',
        recommendations: [],
      },
    ],
    experience_gaps: [
      {
        gap_id: 'exp_1',
        category: 'project_experience',
        title: 'Microservices Project',
        description: 'Build microservices application',
        priority: 'high',
        priority_reasoning: 'Demonstrates practical skills',
        impact_on_application: 'Shows initiative',
        recommendations: [],
      },
    ],
    company_fit_gaps: [
      {
        gap_id: 'fit_1',
        category: 'values',
        title: 'Customer Obsession',
        description: 'Show customer focus',
        priority: 'medium',
        priority_reasoning: 'Company value',
        company_value: 'Customer Obsession',
        impact_on_application: 'Culture fit',
        recommendations: [],
      },
    ],
    resume_optimization_gaps: [
      {
        gap_id: 'resume_1',
        category: 'keywords',
        title: 'ATS Keywords',
        description: 'Add missing keywords',
        priority: 'high',
        priority_reasoning: 'Pass ATS screening',
        impact_on_application: 'Critical for screening',
        recommendations: [],
      },
      {
        gap_id: 'resume_2',
        category: 'formatting',
        title: 'Resume Structure',
        description: 'Improve formatting',
        priority: 'low',
        priority_reasoning: 'Polish',
        impact_on_application: 'Minor impact',
        recommendations: [],
      },
    ],
    quick_wins: [
      {
        title: 'Add Keywords',
        description: 'Add missing technical keywords',
        impact: 'High - improves ATS score',
        estimated_time: '2 hours',
        steps: ['Identify missing keywords', 'Add naturally to resume', 'Review for readability'],
      },
    ],
    long_term_development: [],
    prioritized_action_plan: null,
  };

  describe('rendering', () => {
    it('renders the gaps section with correct title', () => {
      render(<GapsSection gapAnalysis={mockGapAnalysis} />);
      expect(screen.getByText('Areas for Improvement')).toBeInTheDocument();
    });

    it('renders summary stats', () => {
      render(<GapsSection gapAnalysis={mockGapAnalysis} />);
      expect(screen.getByText('6 gaps identified • Estimated preparation: 6-8 weeks')).toBeInTheDocument();
    });

    it('renders priority count cards', () => {
      render(<GapsSection gapAnalysis={mockGapAnalysis} />);
      expect(screen.getByText('High Priority')).toBeInTheDocument();
      expect(screen.getByText('Medium Priority')).toBeInTheDocument();
      expect(screen.getByText('Low Priority')).toBeInTheDocument();
      expect(screen.getByText('3')).toBeInTheDocument(); // high count
      expect(screen.getByText('2')).toBeInTheDocument(); // medium count
      expect(screen.getByText('1')).toBeInTheDocument(); // low count
    });

    it('renders overall assessment', () => {
      render(<GapsSection gapAnalysis={mockGapAnalysis} />);
      expect(screen.getByText('Overall Assessment')).toBeInTheDocument();
      expect(screen.getByText('Strong candidate with some areas for improvement')).toBeInTheDocument();
    });

    it('renders all gap cards', () => {
      render(<GapsSection gapAnalysis={mockGapAnalysis} />);
      expect(screen.getByText('Distributed Systems')).toBeInTheDocument();
      expect(screen.getByText('CI/CD Pipelines')).toBeInTheDocument();
      expect(screen.getByText('Microservices Project')).toBeInTheDocument();
      expect(screen.getByText('Customer Obsession')).toBeInTheDocument();
      expect(screen.getByText('ATS Keywords')).toBeInTheDocument();
      expect(screen.getByText('Resume Structure')).toBeInTheDocument();
    });

    it('shows correct gap count', () => {
      render(<GapsSection gapAnalysis={mockGapAnalysis} />);
      expect(screen.getByText('Detailed Gaps (6)')).toBeInTheDocument();
    });
  });

  describe('quick wins section', () => {
    it('renders quick wins when available', () => {
      render(<GapsSection gapAnalysis={mockGapAnalysis} />);
      expect(screen.getByText('Quick Wins (Start Here!)')).toBeInTheDocument();
      expect(screen.getByText('Add Keywords')).toBeInTheDocument();
    });

    it('renders quick win details', () => {
      render(<GapsSection gapAnalysis={mockGapAnalysis} />);
      expect(screen.getByText('Add missing technical keywords')).toBeInTheDocument();
      expect(screen.getByText(/High - improves ATS score/)).toBeInTheDocument();
      expect(screen.getByText('⏱️ 2 hours')).toBeInTheDocument();
    });

    it('renders quick win steps', () => {
      render(<GapsSection gapAnalysis={mockGapAnalysis} />);
      expect(screen.getByText('Identify missing keywords')).toBeInTheDocument();
      expect(screen.getByText('Add naturally to resume')).toBeInTheDocument();
      expect(screen.getByText('Review for readability')).toBeInTheDocument();
    });

    it('does not render quick wins section when empty', () => {
      const noQuickWins = { ...mockGapAnalysis, quick_wins: [] };
      render(<GapsSection gapAnalysis={noQuickWins} />);
      expect(screen.queryByText('Quick Wins (Start Here!)')).not.toBeInTheDocument();
    });
  });

  describe('type filtering', () => {
    it('shows all gaps by default', () => {
      render(<GapsSection gapAnalysis={mockGapAnalysis} />);
      expect(screen.getByText('Detailed Gaps (6)')).toBeInTheDocument();
    });

    it('filters to technical gaps only', async () => {
      const user = userEvent.setup();
      render(<GapsSection gapAnalysis={mockGapAnalysis} />);
      
      const technicalButton = screen.getByRole('button', { name: /💻 Technical/ });
      await user.click(technicalButton);
      
      expect(screen.getByText('Detailed Gaps (2)')).toBeInTheDocument();
      expect(screen.getByText('Distributed Systems')).toBeInTheDocument();
      expect(screen.getByText('CI/CD Pipelines')).toBeInTheDocument();
      expect(screen.queryByText('Microservices Project')).not.toBeInTheDocument();
    });

    it('filters to experience gaps only', async () => {
      const user = userEvent.setup();
      render(<GapsSection gapAnalysis={mockGapAnalysis} />);
      
      const experienceButton = screen.getByRole('button', { name: /🚀 Experience/ });
      await user.click(experienceButton);
      
      expect(screen.getByText('Detailed Gaps (1)')).toBeInTheDocument();
      expect(screen.getByText('Microservices Project')).toBeInTheDocument();
      expect(screen.queryByText('Distributed Systems')).not.toBeInTheDocument();
    });

    it('filters to company fit gaps only', async () => {
      const user = userEvent.setup();
      render(<GapsSection gapAnalysis={mockGapAnalysis} />);
      
      const companyFitButton = screen.getByRole('button', { name: /🤝 Company Fit/ });
      await user.click(companyFitButton);
      
      expect(screen.getByText('Detailed Gaps (1)')).toBeInTheDocument();
      expect(screen.getByText('Customer Obsession')).toBeInTheDocument();
    });

    it('filters to resume gaps only', async () => {
      const user = userEvent.setup();
      render(<GapsSection gapAnalysis={mockGapAnalysis} />);
      
      const resumeButton = screen.getByRole('button', { name: /📝 Resume/ });
      await user.click(resumeButton);
      
      expect(screen.getByText('Detailed Gaps (2)')).toBeInTheDocument();
      expect(screen.getByText('ATS Keywords')).toBeInTheDocument();
      expect(screen.getByText('Resume Structure')).toBeInTheDocument();
    });

    it('highlights selected type filter', async () => {
      const user = userEvent.setup();
      render(<GapsSection gapAnalysis={mockGapAnalysis} />);
      
      const technicalButton = screen.getByRole('button', { name: /💻 Technical/ });
      await user.click(technicalButton);
      
      expect(technicalButton).toHaveClass('bg-purple-600', 'text-white');
    });
  });

  describe('priority filtering', () => {
    it('filters to high priority only', async () => {
      const user = userEvent.setup();
      render(<GapsSection gapAnalysis={mockGapAnalysis} />);
      
      const highButton = screen.getByRole('button', { name: 'High' });
      await user.click(highButton);
      
      expect(screen.getByText('Detailed Gaps (3)')).toBeInTheDocument();
      expect(screen.getByText('Distributed Systems')).toBeInTheDocument();
      expect(screen.getByText('Microservices Project')).toBeInTheDocument();
      expect(screen.getByText('ATS Keywords')).toBeInTheDocument();
      expect(screen.queryByText('CI/CD Pipelines')).not.toBeInTheDocument();
    });

    it('filters to medium priority only', async () => {
      const user = userEvent.setup();
      render(<GapsSection gapAnalysis={mockGapAnalysis} />);
      
      const mediumButton = screen.getByRole('button', { name: 'Medium' });
      await user.click(mediumButton);
      
      expect(screen.getByText('Detailed Gaps (2)')).toBeInTheDocument();
      expect(screen.getByText('CI/CD Pipelines')).toBeInTheDocument();
      expect(screen.getByText('Customer Obsession')).toBeInTheDocument();
    });

    it('filters to low priority only', async () => {
      const user = userEvent.setup();
      render(<GapsSection gapAnalysis={mockGapAnalysis} />);
      
      const lowButton = screen.getByRole('button', { name: 'Low' });
      await user.click(lowButton);
      
      expect(screen.getByText('Detailed Gaps (1)')).toBeInTheDocument();
      expect(screen.getByText('Resume Structure')).toBeInTheDocument();
    });
  });

  describe('combined filtering', () => {
    it('applies both type and priority filters', async () => {
      const user = userEvent.setup();
      render(<GapsSection gapAnalysis={mockGapAnalysis} />);
      
      const technicalButton = screen.getByRole('button', { name: /💻 Technical/ });
      const highButton = screen.getByRole('button', { name: 'High' });
      
      await user.click(technicalButton);
      await user.click(highButton);
      
      expect(screen.getByText('Detailed Gaps (1)')).toBeInTheDocument();
      expect(screen.getByText('Distributed Systems')).toBeInTheDocument();
      expect(screen.queryByText('CI/CD Pipelines')).not.toBeInTheDocument();
    });

    it('shows clear filters button when filters are active', async () => {
      const user = userEvent.setup();
      render(<GapsSection gapAnalysis={mockGapAnalysis} />);
      
      expect(screen.queryByText('Clear Filters')).not.toBeInTheDocument();
      
      const technicalButton = screen.getByRole('button', { name: /💻 Technical/ });
      await user.click(technicalButton);
      
      expect(screen.getByText('Clear Filters')).toBeInTheDocument();
    });

    it('clears all filters when clear button is clicked', async () => {
      const user = userEvent.setup();
      render(<GapsSection gapAnalysis={mockGapAnalysis} />);
      
      const technicalButton = screen.getByRole('button', { name: /💻 Technical/ });
      const highButton = screen.getByRole('button', { name: 'High' });
      
      await user.click(technicalButton);
      await user.click(highButton);
      
      expect(screen.getByText('Detailed Gaps (1)')).toBeInTheDocument();
      
      const clearButton = screen.getByText('Clear Filters');
      await user.click(clearButton);
      
      expect(screen.getByText('Detailed Gaps (6)')).toBeInTheDocument();
    });

    it('shows empty state when no gaps match filters', async () => {
      const user = userEvent.setup();
      const noHighExperience = { ...mockGapAnalysis };
      noHighExperience.experience_gaps[0].priority = 'low';
      
      render(<GapsSection gapAnalysis={noHighExperience} />);
      
      const experienceButton = screen.getByRole('button', { name: /🚀 Experience/ });
      const highButton = screen.getByRole('button', { name: 'High' });
      
      await user.click(experienceButton);
      await user.click(highButton);
      
      expect(screen.getByText('🎉')).toBeInTheDocument();
      expect(screen.getByText('No gaps match your filters. Try adjusting your selection.')).toBeInTheDocument();
    });
  });

  describe('sorting', () => {
    it('sorts gaps by priority (high, medium, low)', () => {
      const { container } = render(<GapsSection gapAnalysis={mockGapAnalysis} />);
      const gapCards = container.querySelectorAll('button');
      
      // First gaps should be high priority
      const firstCardText = gapCards[5].textContent; // Skip filter buttons
      expect(firstCardText).toContain('High Priority');
    });
  });

  describe('edge cases', () => {
    it('does not render when no gaps exist', () => {
      const noGaps: GapAnalysis = {
        summary: {
          total_gaps: 0,
          high_priority_count: 0,
          medium_priority_count: 0,
          low_priority_count: 0,
          estimated_preparation_time: '0 weeks',
          overall_assessment: 'No gaps identified',
        },
        technical_gaps: [],
        experience_gaps: [],
        company_fit_gaps: [],
        resume_optimization_gaps: [],
        quick_wins: [],
        long_term_development: [],
        prioritized_action_plan: null,
      };
      
      const { container } = render(<GapsSection gapAnalysis={noGaps} />);
      expect(container.firstChild).toBeNull();
    });

    it('handles gaps with missing gap_id', () => {
      const missingId = { ...mockGapAnalysis };
      delete (missingId.technical_gaps[0] as any).gap_id;
      
      render(<GapsSection gapAnalysis={missingId} />);
      expect(screen.getByText('Distributed Systems')).toBeInTheDocument();
    });

    it('renders correctly with only one type of gap', () => {
      const onlyTechnical: GapAnalysis = {
        summary: {
          total_gaps: 1,
          high_priority_count: 1,
          medium_priority_count: 0,
          low_priority_count: 0,
          estimated_preparation_time: '2 weeks',
          overall_assessment: 'One gap to address',
        },
        technical_gaps: [mockGapAnalysis.technical_gaps[0]],
        experience_gaps: [],
        company_fit_gaps: [],
        resume_optimization_gaps: [],
        quick_wins: [],
        long_term_development: [],
        prioritized_action_plan: null,
      };
      
      render(<GapsSection gapAnalysis={onlyTechnical} />);
      expect(screen.getByText('Detailed Gaps (1)')).toBeInTheDocument();
      expect(screen.getByText('Distributed Systems')).toBeInTheDocument();
    });
  });

  describe('icons and styling', () => {
    it('renders priority icons', () => {
      const { container } = render(<GapsSection gapAnalysis={mockGapAnalysis} />);
      expect(container.textContent).toContain('🔴'); // High priority
      expect(container.textContent).toContain('🟠'); // Medium priority
      expect(container.textContent).toContain('🟡'); // Low priority
    });

    it('renders section icon', () => {
      const { container } = render(<GapsSection gapAnalysis={mockGapAnalysis} />);
      expect(container.textContent).toContain('🎯');
    });

    it('renders quick wins icon', () => {
      const { container } = render(<GapsSection gapAnalysis={mockGapAnalysis} />);
      expect(container.textContent).toContain('⚡');
    });
  });
});
