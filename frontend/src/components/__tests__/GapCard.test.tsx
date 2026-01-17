/**
 * Tests for GapCard component
 */
import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { GapCard } from '../GapCard';
import type { TechnicalGap, ExperienceGap, CompanyFitGap, ResumeOptimizationGap } from '../../types';

describe('GapCard', () => {
  const mockTechnicalGap: TechnicalGap = {
    gap_id: 'tech_1',
    category: 'technical_skills',
    title: 'Distributed Systems Knowledge',
    description: 'Need to learn distributed systems fundamentals',
    priority: 'high',
    priority_reasoning: 'Core requirement for the role',
    current_level: 'none',
    target_level: 'intermediate',
    impact_on_application: 'Significant impact on interview performance',
    recommendations: [
      {
        action: 'Take a distributed systems course',
        resources: [
          {
            type: 'course',
            name: 'MIT Distributed Systems',
            url: 'https://example.com/course',
            estimated_time: '20 hours',
            notes: 'Comprehensive coverage',
          },
        ],
        success_criteria: 'Can explain CAP theorem',
        estimated_time: '4 weeks',
      },
    ],
  };

  const mockExperienceGap: ExperienceGap = {
    gap_id: 'exp_1',
    category: 'project_experience',
    title: 'Microservices Project',
    description: 'Need hands-on microservices experience',
    priority: 'medium',
    priority_reasoning: 'Demonstrates practical skills',
    impact_on_application: 'Shows initiative and learning ability',
    recommendations: [
      {
        action: 'Build a microservices project',
        project_ideas: [
          {
            name: 'E-commerce Platform',
            description: 'Multi-service online store',
            key_features: ['User service', 'Product catalog', 'Order processing'],
            technologies: ['Docker', 'Kubernetes', 'Node.js'],
            estimated_time: '40 hours',
            difficulty: 'intermediate',
            portfolio_value: 'High - demonstrates modern architecture',
          },
        ],
        success_criteria: 'Deploy working system',
        estimated_time: '6 weeks',
      },
    ],
  };

  const mockCompanyFitGap: CompanyFitGap = {
    gap_id: 'fit_1',
    category: 'values',
    title: 'Customer Obsession',
    description: 'Need to demonstrate customer-first mindset',
    priority: 'medium',
    priority_reasoning: 'Key company value',
    company_value: 'Customer Obsession',
    impact_on_application: 'Important for culture fit',
    recommendations: [
      {
        action: 'Add customer impact stories to resume',
      },
    ],
  };

  const mockResumeGap: ResumeOptimizationGap = {
    gap_id: 'resume_1',
    category: 'keywords',
    title: 'ATS Keyword Optimization',
    description: 'Missing key technical keywords',
    priority: 'high',
    priority_reasoning: 'Critical for passing ATS screening',
    impact_on_application: 'May not pass initial screening',
    recommendations: [
      {
        action: 'Add missing keywords naturally',
        before_example: 'Built a web app',
        after_example: 'Built a scalable web application using microservices architecture',
        success_criteria: 'All key terms present',
        estimated_time: '2 hours',
      },
    ],
  };

  describe('rendering', () => {
    it('renders gap card with title and description', () => {
      render(<GapCard gap={mockTechnicalGap} type="technical" />);
      expect(screen.getByText('Distributed Systems Knowledge')).toBeInTheDocument();
      expect(screen.getByText('Need to learn distributed systems fundamentals')).toBeInTheDocument();
    });

    it('renders priority badge with correct styling', () => {
      render(<GapCard gap={mockTechnicalGap} type="technical" />);
      expect(screen.getByText('High Priority')).toBeInTheDocument();
    });

    it('renders type label', () => {
      render(<GapCard gap={mockTechnicalGap} type="technical" />);
      expect(screen.getByText('Technical')).toBeInTheDocument();
    });

    it('renders category', () => {
      render(<GapCard gap={mockTechnicalGap} type="technical" />);
      expect(screen.getByText('technical skills')).toBeInTheDocument();
    });

    it('renders expand/collapse icon', () => {
      const { container } = render(<GapCard gap={mockTechnicalGap} type="technical" />);
      const svg = container.querySelector('svg');
      expect(svg).toBeInTheDocument();
    });
  });

  describe('expand/collapse functionality', () => {
    it('starts in collapsed state', () => {
      render(<GapCard gap={mockTechnicalGap} type="technical" />);
      expect(screen.queryByText('Why This Matters:')).not.toBeInTheDocument();
    });

    it('expands when clicked', async () => {
      const user = userEvent.setup();
      render(<GapCard gap={mockTechnicalGap} type="technical" />);
      
      const button = screen.getByRole('button');
      await user.click(button);
      
      expect(screen.getByText('Why This Matters:')).toBeInTheDocument();
      expect(screen.getByText('Core requirement for the role')).toBeInTheDocument();
    });

    it('collapses when clicked again', async () => {
      const user = userEvent.setup();
      render(<GapCard gap={mockTechnicalGap} type="technical" />);
      
      const button = screen.getByRole('button');
      await user.click(button);
      await user.click(button);
      
      expect(screen.queryByText('Why This Matters:')).not.toBeInTheDocument();
    });

    it('rotates icon when expanded', async () => {
      const user = userEvent.setup();
      const { container } = render(<GapCard gap={mockTechnicalGap} type="technical" />);
      
      const button = screen.getByRole('button');
      await user.click(button);
      
      const iconContainer = container.querySelector('.rotate-180');
      expect(iconContainer).toBeInTheDocument();
    });
  });

  describe('priority levels', () => {
    it('renders high priority with red styling', () => {
      render(<GapCard gap={mockTechnicalGap} type="technical" />);
      const badge = screen.getByText('High Priority');
      expect(badge).toHaveClass('text-red-800');
    });

    it('renders medium priority with orange styling', () => {
      render(<GapCard gap={mockExperienceGap} type="experience" />);
      const badge = screen.getByText('Medium Priority');
      expect(badge).toHaveClass('text-orange-800');
    });

    it('renders low priority with yellow styling', () => {
      const lowPriorityGap = { ...mockTechnicalGap, priority: 'low' as const };
      render(<GapCard gap={lowPriorityGap} type="technical" />);
      const badge = screen.getByText('Low Priority');
      expect(badge).toHaveClass('text-yellow-800');
    });
  });

  describe('gap types', () => {
    it('renders technical gap icon', () => {
      const { container } = render(<GapCard gap={mockTechnicalGap} type="technical" />);
      expect(container.textContent).toContain('💻');
    });

    it('renders experience gap icon', () => {
      const { container } = render(<GapCard gap={mockExperienceGap} type="experience" />);
      expect(container.textContent).toContain('🚀');
    });

    it('renders company fit gap icon', () => {
      const { container } = render(<GapCard gap={mockCompanyFitGap} type="company_fit" />);
      expect(container.textContent).toContain('🤝');
    });

    it('renders resume gap icon', () => {
      const { container } = render(<GapCard gap={mockResumeGap} type="resume" />);
      expect(container.textContent).toContain('📝');
    });
  });

  describe('expanded content - technical gaps', () => {
    it('shows skill level progression', async () => {
      const user = userEvent.setup();
      render(<GapCard gap={mockTechnicalGap} type="technical" />);
      
      await user.click(screen.getByRole('button'));
      
      expect(screen.getByText('Skill Level:')).toBeInTheDocument();
      expect(screen.getByText('none')).toBeInTheDocument();
      expect(screen.getByText('intermediate')).toBeInTheDocument();
    });

    it('shows recommendations with resources', async () => {
      const user = userEvent.setup();
      render(<GapCard gap={mockTechnicalGap} type="technical" />);
      
      await user.click(screen.getByRole('button'));
      
      expect(screen.getByText('🎯 Recommendations:')).toBeInTheDocument();
      expect(screen.getByText('Take a distributed systems course')).toBeInTheDocument();
      expect(screen.getByText('📚 Resources:')).toBeInTheDocument();
      expect(screen.getByText('MIT Distributed Systems')).toBeInTheDocument();
    });

    it('renders resource details', async () => {
      const user = userEvent.setup();
      render(<GapCard gap={mockTechnicalGap} type="technical" />);
      
      await user.click(screen.getByRole('button'));
      
      expect(screen.getByText('course')).toBeInTheDocument();
      expect(screen.getByText('⏱️ 20 hours')).toBeInTheDocument();
      expect(screen.getByText('Comprehensive coverage')).toBeInTheDocument();
    });

    it('renders clickable resource URL', async () => {
      const user = userEvent.setup();
      render(<GapCard gap={mockTechnicalGap} type="technical" />);
      
      await user.click(screen.getByRole('button'));
      
      const link = screen.getByRole('link', { name: /example.com/ });
      expect(link).toHaveAttribute('href', 'https://example.com/course');
      expect(link).toHaveAttribute('target', '_blank');
    });
  });

  describe('expanded content - experience gaps', () => {
    it('shows project ideas', async () => {
      const user = userEvent.setup();
      render(<GapCard gap={mockExperienceGap} type="experience" />);
      
      await user.click(screen.getByRole('button'));
      
      expect(screen.getByText('💡 Project Ideas:')).toBeInTheDocument();
      expect(screen.getByText('E-commerce Platform')).toBeInTheDocument();
      expect(screen.getByText('Multi-service online store')).toBeInTheDocument();
    });

    it('shows project difficulty badge', async () => {
      const user = userEvent.setup();
      render(<GapCard gap={mockExperienceGap} type="experience" />);
      
      await user.click(screen.getByRole('button'));
      
      expect(screen.getByText('intermediate')).toBeInTheDocument();
    });

    it('shows key features list', async () => {
      const user = userEvent.setup();
      render(<GapCard gap={mockExperienceGap} type="experience" />);
      
      await user.click(screen.getByRole('button'));
      
      expect(screen.getByText('User service')).toBeInTheDocument();
      expect(screen.getByText('Product catalog')).toBeInTheDocument();
      expect(screen.getByText('Order processing')).toBeInTheDocument();
    });

    it('shows technologies', async () => {
      const user = userEvent.setup();
      render(<GapCard gap={mockExperienceGap} type="experience" />);
      
      await user.click(screen.getByRole('button'));
      
      expect(screen.getByText('Docker')).toBeInTheDocument();
      expect(screen.getByText('Kubernetes')).toBeInTheDocument();
      expect(screen.getByText('Node.js')).toBeInTheDocument();
    });

    it('shows portfolio value', async () => {
      const user = userEvent.setup();
      render(<GapCard gap={mockExperienceGap} type="experience" />);
      
      await user.click(screen.getByRole('button'));
      
      expect(screen.getByText(/High - demonstrates modern architecture/)).toBeInTheDocument();
    });
  });

  describe('expanded content - company fit gaps', () => {
    it('shows company value', async () => {
      const user = userEvent.setup();
      render(<GapCard gap={mockCompanyFitGap} type="company_fit" />);
      
      await user.click(screen.getByRole('button'));
      
      expect(screen.getByText('Company Value:')).toBeInTheDocument();
      expect(screen.getByText('Customer Obsession')).toBeInTheDocument();
    });
  });

  describe('expanded content - resume gaps', () => {
    it('shows before/after examples', async () => {
      const user = userEvent.setup();
      render(<GapCard gap={mockResumeGap} type="resume" />);
      
      await user.click(screen.getByRole('button'));
      
      expect(screen.getByText('📝 Example:')).toBeInTheDocument();
      expect(screen.getByText('❌ Before:')).toBeInTheDocument();
      expect(screen.getByText('Built a web app')).toBeInTheDocument();
      expect(screen.getByText('✓ After:')).toBeInTheDocument();
      expect(screen.getByText('Built a scalable web application using microservices architecture')).toBeInTheDocument();
    });
  });

  describe('common expanded content', () => {
    it('shows priority reasoning', async () => {
      const user = userEvent.setup();
      render(<GapCard gap={mockTechnicalGap} type="technical" />);
      
      await user.click(screen.getByRole('button'));
      
      expect(screen.getByText('Why This Matters:')).toBeInTheDocument();
      expect(screen.getByText('Core requirement for the role')).toBeInTheDocument();
    });

    it('shows impact on application', async () => {
      const user = userEvent.setup();
      render(<GapCard gap={mockTechnicalGap} type="technical" />);
      
      await user.click(screen.getByRole('button'));
      
      expect(screen.getByText('Impact on Application:')).toBeInTheDocument();
      expect(screen.getByText('Significant impact on interview performance')).toBeInTheDocument();
    });

    it('shows success criteria', async () => {
      const user = userEvent.setup();
      render(<GapCard gap={mockTechnicalGap} type="technical" />);
      
      await user.click(screen.getByRole('button'));
      
      expect(screen.getByText(/Can explain CAP theorem/)).toBeInTheDocument();
    });

    it('shows estimated time', async () => {
      const user = userEvent.setup();
      render(<GapCard gap={mockTechnicalGap} type="technical" />);
      
      await user.click(screen.getByRole('button'));
      
      expect(screen.getByText(/4 weeks/)).toBeInTheDocument();
    });
  });

  describe('edge cases', () => {
    it('handles gap with no recommendations', async () => {
      const noRecs = { ...mockTechnicalGap, recommendations: [] };
      const user = userEvent.setup();
      render(<GapCard gap={noRecs} type="technical" />);
      
      await user.click(screen.getByRole('button'));
      
      expect(screen.getByText('🎯 Recommendations:')).toBeInTheDocument();
    });

    it('handles resource with "Search online" URL', async () => {
      const searchOnline = { ...mockTechnicalGap };
      searchOnline.recommendations[0].resources[0].url = 'Search online';
      const user = userEvent.setup();
      render(<GapCard gap={searchOnline} type="technical" />);
      
      await user.click(screen.getByRole('button'));
      
      expect(screen.queryByRole('link')).not.toBeInTheDocument();
    });

    it('handles recommendation without resources', async () => {
      const noResources = { ...mockTechnicalGap };
      noResources.recommendations[0].resources = [];
      const user = userEvent.setup();
      render(<GapCard gap={noResources} type="technical" />);
      
      await user.click(screen.getByRole('button'));
      
      expect(screen.queryByText('📚 Resources:')).not.toBeInTheDocument();
    });

    it('handles project idea without key features', async () => {
      const noFeatures = { ...mockExperienceGap };
      noFeatures.recommendations[0].project_ideas[0].key_features = [];
      const user = userEvent.setup();
      render(<GapCard gap={noFeatures} type="experience" />);
      
      await user.click(screen.getByRole('button'));
      
      expect(screen.queryByText('Key Features:')).not.toBeInTheDocument();
    });

    it('handles resume recommendation without before example', async () => {
      const noExample = { ...mockResumeGap };
      delete noExample.recommendations[0].before_example;
      const user = userEvent.setup();
      render(<GapCard gap={noExample} type="resume" />);
      
      await user.click(screen.getByRole('button'));
      
      expect(screen.queryByText('📝 Example:')).not.toBeInTheDocument();
    });
  });
});
