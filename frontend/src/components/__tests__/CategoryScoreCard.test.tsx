/**
 * Tests for CategoryScoreCard component
 */
import { describe, it, expect } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { userEvent } from '@testing-library/user-event';
import { CategoryScoreCard } from '../CategoryScoreCard';
import type { ScoreDetail } from '../../types';

describe('CategoryScoreCard', () => {
  const mockScoreDetail: ScoreDetail = {
    score: 85,
    explanation: 'Strong resume formatting with good keyword optimization.',
    strengths: [
      'Well-structured sections',
      'Good use of action verbs',
      'Quantified achievements',
    ],
    weaknesses: [
      'Could add more technical keywords',
      'Consider reducing length',
    ],
  };

  describe('Rendering', () => {
    it('renders the title correctly', () => {
      render(
        <CategoryScoreCard
          title="ATS Score"
          scoreDetail={mockScoreDetail}
          icon="🤖"
          color="blue"
        />
      );

      expect(screen.getByText('ATS Score')).toBeInTheDocument();
    });

    it('renders the icon correctly', () => {
      render(
        <CategoryScoreCard
          title="ATS Score"
          scoreDetail={mockScoreDetail}
          icon="🤖"
          color="blue"
        />
      );

      expect(screen.getByText('🤖')).toBeInTheDocument();
    });

    it('renders the score correctly', () => {
      render(
        <CategoryScoreCard
          title="ATS Score"
          scoreDetail={mockScoreDetail}
          icon="🤖"
          color="blue"
        />
      );

      expect(screen.getByText('85')).toBeInTheDocument();
      expect(screen.getByText('/100')).toBeInTheDocument();
    });

    it('renders the explanation', () => {
      render(
        <CategoryScoreCard
          title="ATS Score"
          scoreDetail={mockScoreDetail}
          icon="🤖"
          color="blue"
        />
      );

      expect(
        screen.getByText('Strong resume formatting with good keyword optimization.')
      ).toBeInTheDocument();
    });

    it('renders with different colors', () => {
      const { container: blueContainer } = render(
        <CategoryScoreCard
          title="ATS Score"
          scoreDetail={mockScoreDetail}
          icon="🤖"
          color="blue"
        />
      );
      expect(blueContainer.querySelector('.text-blue-600')).toBeInTheDocument();

      const { container: purpleContainer } = render(
        <CategoryScoreCard
          title="Role Match"
          scoreDetail={mockScoreDetail}
          icon="🎯"
          color="purple"
        />
      );
      expect(purpleContainer.querySelector('.text-purple-600')).toBeInTheDocument();

      const { container: greenContainer } = render(
        <CategoryScoreCard
          title="Company Fit"
          scoreDetail={mockScoreDetail}
          icon="🏢"
          color="green"
        />
      );
      expect(greenContainer.querySelector('.text-green-600')).toBeInTheDocument();
    });
  });

  describe('Progress Bar', () => {
    it('renders progress bar with correct width', () => {
      const { container } = render(
        <CategoryScoreCard
          title="ATS Score"
          scoreDetail={mockScoreDetail}
          icon="🤖"
          color="blue"
        />
      );

      const progressBar = container.querySelector('.bg-blue-600');
      expect(progressBar).toBeInTheDocument();
      expect(progressBar).toHaveStyle({ width: '85%' });
    });

    it('handles zero score correctly', () => {
      const zeroScoreDetail: ScoreDetail = {
        ...mockScoreDetail,
        score: 0,
      };

      const { container } = render(
        <CategoryScoreCard
          title="ATS Score"
          scoreDetail={zeroScoreDetail}
          icon="🤖"
          color="blue"
        />
      );

      const progressBar = container.querySelector('.bg-blue-600');
      expect(progressBar).toHaveStyle({ width: '0%' });
    });

    it('handles full score correctly', () => {
      const fullScoreDetail: ScoreDetail = {
        ...mockScoreDetail,
        score: 100,
      };

      const { container } = render(
        <CategoryScoreCard
          title="ATS Score"
          scoreDetail={fullScoreDetail}
          icon="🤖"
          color="blue"
        />
      );

      const progressBar = container.querySelector('.bg-blue-600');
      expect(progressBar).toHaveStyle({ width: '100%' });
    });
  });

  describe('Tooltip Behavior', () => {
    it('does not show tooltip initially', () => {
      render(
        <CategoryScoreCard
          title="ATS Score"
          scoreDetail={mockScoreDetail}
          icon="🤖"
          color="blue"
        />
      );

      // Tooltip content should not be visible initially
      const strengthsHeading = screen.queryByText('✓ Strengths');
      expect(strengthsHeading).not.toBeInTheDocument();
    });

    it('shows tooltip on hover', async () => {
      const user = userEvent.setup();
      
      const { container } = render(
        <CategoryScoreCard
          title="ATS Score"
          scoreDetail={mockScoreDetail}
          icon="🤖"
          color="blue"
        />
      );

      const card = container.querySelector('.cursor-pointer');
      expect(card).toBeInTheDocument();
      
      if (card) {
        await user.hover(card);

        await waitFor(() => {
          expect(screen.getByText('✓ Strengths')).toBeInTheDocument();
        });
      }
    });

    it('hides tooltip when mouse leaves', async () => {
      const user = userEvent.setup();
      
      const { container } = render(
        <CategoryScoreCard
          title="ATS Score"
          scoreDetail={mockScoreDetail}
          icon="🤖"
          color="blue"
        />
      );

      const card = container.querySelector('.cursor-pointer');
      expect(card).toBeInTheDocument();
      
      if (card) {
        // Hover to show tooltip
        await user.hover(card);
        await waitFor(() => {
          expect(screen.getByText('✓ Strengths')).toBeInTheDocument();
        });

        // Unhover to hide tooltip
        await user.unhover(card);
        await waitFor(() => {
          expect(screen.queryByText('✓ Strengths')).not.toBeInTheDocument();
        });
      }
    });

    it('displays strengths in tooltip', async () => {
      const user = userEvent.setup();
      
      const { container } = render(
        <CategoryScoreCard
          title="ATS Score"
          scoreDetail={mockScoreDetail}
          icon="🤖"
          color="blue"
        />
      );

      const card = container.querySelector('.cursor-pointer');
      if (card) {
        await user.hover(card);

        await waitFor(() => {
          expect(screen.getByText('Well-structured sections')).toBeInTheDocument();
          expect(screen.getByText('Good use of action verbs')).toBeInTheDocument();
          expect(screen.getByText('Quantified achievements')).toBeInTheDocument();
        });
      }
    });

    it('displays weaknesses in tooltip', async () => {
      const user = userEvent.setup();
      
      const { container } = render(
        <CategoryScoreCard
          title="ATS Score"
          scoreDetail={mockScoreDetail}
          icon="🤖"
          color="blue"
        />
      );

      const card = container.querySelector('.cursor-pointer');
      if (card) {
        await user.hover(card);

        await waitFor(() => {
          expect(screen.getByText('⚠ Areas for Improvement')).toBeInTheDocument();
          expect(screen.getByText('Could add more technical keywords')).toBeInTheDocument();
          expect(screen.getByText('Consider reducing length')).toBeInTheDocument();
        });
      }
    });

    it('handles missing strengths gracefully', async () => {
      const user = userEvent.setup();
      
      const scoreWithoutStrengths: ScoreDetail = {
        score: 50,
        explanation: 'Moderate performance',
        weaknesses: ['Needs improvement'],
      };

      const { container } = render(
        <CategoryScoreCard
          title="ATS Score"
          scoreDetail={scoreWithoutStrengths}
          icon="🤖"
          color="blue"
        />
      );

      const card = container.querySelector('.cursor-pointer');
      if (card) {
        await user.hover(card);

        await waitFor(() => {
          expect(screen.queryByText('✓ Strengths')).not.toBeInTheDocument();
          expect(screen.getByText('⚠ Areas for Improvement')).toBeInTheDocument();
        });
      }
    });

    it('handles missing weaknesses gracefully', async () => {
      const user = userEvent.setup();
      
      const scoreWithoutWeaknesses: ScoreDetail = {
        score: 95,
        explanation: 'Excellent performance',
        strengths: ['Perfect execution'],
      };

      const { container } = render(
        <CategoryScoreCard
          title="ATS Score"
          scoreDetail={scoreWithoutWeaknesses}
          icon="🤖"
          color="blue"
        />
      );

      const card = container.querySelector('.cursor-pointer');
      if (card) {
        await user.hover(card);

        await waitFor(() => {
          expect(screen.getByText('✓ Strengths')).toBeInTheDocument();
          expect(screen.queryByText('⚠ Areas for Improvement')).not.toBeInTheDocument();
        });
      }
    });

    it('handles empty strengths array', async () => {
      const user = userEvent.setup();
      
      const scoreWithEmptyStrengths: ScoreDetail = {
        score: 50,
        explanation: 'Moderate performance',
        strengths: [],
        weaknesses: ['Needs improvement'],
      };

      const { container } = render(
        <CategoryScoreCard
          title="ATS Score"
          scoreDetail={scoreWithEmptyStrengths}
          icon="🤖"
          color="blue"
        />
      );

      const card = container.querySelector('.cursor-pointer');
      if (card) {
        await user.hover(card);

        await waitFor(() => {
          expect(screen.queryByText('✓ Strengths')).not.toBeInTheDocument();
        });
      }
    });
  });

  describe('Accessibility', () => {
    it('has proper hover interaction', async () => {
      const user = userEvent.setup();
      
      const { container } = render(
        <CategoryScoreCard
          title="ATS Score"
          scoreDetail={mockScoreDetail}
          icon="🤖"
          color="blue"
        />
      );

      const card = container.querySelector('.cursor-pointer');
      expect(card).toHaveClass('hover:shadow-lg');
      expect(card).toHaveClass('hover:scale-105');
      
      if (card) {
        await user.hover(card);
        // Tooltip should appear
        await waitFor(() => {
          expect(screen.getByText('✓ Strengths')).toBeInTheDocument();
        });
      }
    });
  });

  describe('Visual Styling', () => {
    it('applies correct color classes for blue theme', () => {
      const { container } = render(
        <CategoryScoreCard
          title="ATS Score"
          scoreDetail={mockScoreDetail}
          icon="🤖"
          color="blue"
        />
      );

      expect(container.querySelector('.text-blue-600')).toBeInTheDocument();
      expect(container.querySelector('.border-blue-200')).toBeInTheDocument();
      expect(container.querySelector('.bg-blue-50')).toBeInTheDocument();
    });

    it('applies correct color classes for purple theme', () => {
      const { container } = render(
        <CategoryScoreCard
          title="Role Match"
          scoreDetail={mockScoreDetail}
          icon="🎯"
          color="purple"
        />
      );

      expect(container.querySelector('.text-purple-600')).toBeInTheDocument();
      expect(container.querySelector('.border-purple-200')).toBeInTheDocument();
      expect(container.querySelector('.bg-purple-50')).toBeInTheDocument();
    });

    it('applies correct color classes for green theme', () => {
      const { container } = render(
        <CategoryScoreCard
          title="Company Fit"
          scoreDetail={mockScoreDetail}
          icon="🏢"
          color="green"
        />
      );

      expect(container.querySelector('.text-green-600')).toBeInTheDocument();
      expect(container.querySelector('.border-green-200')).toBeInTheDocument();
      expect(container.querySelector('.bg-green-50')).toBeInTheDocument();
    });

    it('has rounded corners and proper padding', () => {
      const { container } = render(
        <CategoryScoreCard
          title="ATS Score"
          scoreDetail={mockScoreDetail}
          icon="🤖"
          color="blue"
        />
      );

      const card = container.querySelector('.rounded-lg');
      expect(card).toHaveClass('p-6');
    });
  });
});
