/**
 * Tests for StrengthsSection component
 */
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { StrengthsSection } from '../StrengthsSection';
import type { MatchAnalysis } from '../../types';

describe('StrengthsSection', () => {
  const mockMatchAnalysis: MatchAnalysis = {
    ats_score: {
      score: 88,
      explanation: 'Strong ATS optimization',
      strengths: [
        'Comprehensive programming language coverage',
        'Cloud platform experience explicitly mentioned',
        'Database systems clearly listed',
      ],
      weaknesses: ['Missing distributed systems terminology'],
    },
    role_match_score: {
      score: 82,
      explanation: 'Good role match',
      strengths: [
        'Full-stack development background',
        'Cloud platform knowledge',
      ],
      weaknesses: ['Limited distributed systems experience'],
    },
    company_fit_score: {
      score: 79,
      explanation: 'Decent company fit',
      strengths: [
        'Results-oriented mindset demonstrated',
        'Academic excellence shown',
      ],
      weaknesses: ['Limited collaboration evidence'],
    },
    overall_score: {
      score: 82,
      explanation: 'Strong overall candidate',
      strengths: [],
      weaknesses: [],
      key_strengths: [
        'Strong technical foundation with comprehensive programming',
        'Proven ability to deliver results with measurable impact',
        'Excellent academic credentials',
      ],
    },
  };

  describe('rendering', () => {
    it('renders the strengths section with correct title', () => {
      render(<StrengthsSection matchAnalysis={mockMatchAnalysis} />);
      expect(screen.getByText('Your Strengths')).toBeInTheDocument();
    });

    it('renders key strengths section when available', () => {
      render(<StrengthsSection matchAnalysis={mockMatchAnalysis} />);
      expect(screen.getByText('Key Highlights')).toBeInTheDocument();
    });

    it('renders all key strengths with numbering', () => {
      render(<StrengthsSection matchAnalysis={mockMatchAnalysis} />);
      expect(screen.getByText('Strong technical foundation with comprehensive programming')).toBeInTheDocument();
      expect(screen.getByText('Proven ability to deliver results with measurable impact')).toBeInTheDocument();
      expect(screen.getByText('Excellent academic credentials')).toBeInTheDocument();
      expect(screen.getByText('1')).toBeInTheDocument();
      expect(screen.getByText('2')).toBeInTheDocument();
      expect(screen.getByText('3')).toBeInTheDocument();
    });

    it('renders category-specific strengths', () => {
      render(<StrengthsSection matchAnalysis={mockMatchAnalysis} />);
      expect(screen.getByText('ATS Optimization')).toBeInTheDocument();
      expect(screen.getByText('Role Alignment')).toBeInTheDocument();
      expect(screen.getByText('Company Fit')).toBeInTheDocument();
    });

    it('renders all ATS strengths', () => {
      render(<StrengthsSection matchAnalysis={mockMatchAnalysis} />);
      expect(screen.getByText('Comprehensive programming language coverage')).toBeInTheDocument();
      expect(screen.getByText('Cloud platform experience explicitly mentioned')).toBeInTheDocument();
      expect(screen.getByText('Database systems clearly listed')).toBeInTheDocument();
    });

    it('renders all role match strengths', () => {
      render(<StrengthsSection matchAnalysis={mockMatchAnalysis} />);
      expect(screen.getByText('Full-stack development background')).toBeInTheDocument();
      expect(screen.getByText('Cloud platform knowledge')).toBeInTheDocument();
    });

    it('renders all company fit strengths', () => {
      render(<StrengthsSection matchAnalysis={mockMatchAnalysis} />);
      expect(screen.getByText('Results-oriented mindset demonstrated')).toBeInTheDocument();
      expect(screen.getByText('Academic excellence shown')).toBeInTheDocument();
    });
  });

  describe('conditional rendering', () => {
    it('does not render when no strengths are available', () => {
      const emptyAnalysis: MatchAnalysis = {
        ats_score: { score: 50, explanation: 'Test', strengths: [], weaknesses: [] },
        role_match_score: { score: 50, explanation: 'Test', strengths: [], weaknesses: [] },
        company_fit_score: { score: 50, explanation: 'Test', strengths: [], weaknesses: [] },
        overall_score: { score: 50, explanation: 'Test', strengths: [], weaknesses: [] },
      };
      const { container } = render(<StrengthsSection matchAnalysis={emptyAnalysis} />);
      expect(container.firstChild).toBeNull();
    });

    it('does not render ATS section when no ATS strengths', () => {
      const noATS = { ...mockMatchAnalysis };
      noATS.ats_score.strengths = [];
      render(<StrengthsSection matchAnalysis={noATS} />);
      expect(screen.queryByText('ATS Optimization')).not.toBeInTheDocument();
    });

    it('renders when only key strengths are available', () => {
      const onlyKey: MatchAnalysis = {
        ats_score: { score: 50, explanation: 'Test', strengths: [], weaknesses: [] },
        role_match_score: { score: 50, explanation: 'Test', strengths: [], weaknesses: [] },
        company_fit_score: { score: 50, explanation: 'Test', strengths: [], weaknesses: [] },
        overall_score: {
          score: 50,
          explanation: 'Test',
          strengths: [],
          weaknesses: [],
          key_strengths: ['Key strength 1'],
        },
      };
      render(<StrengthsSection matchAnalysis={onlyKey} />);
      expect(screen.getByText('Your Strengths')).toBeInTheDocument();
      expect(screen.getByText('Key strength 1')).toBeInTheDocument();
    });
  });

  describe('styling and icons', () => {
    it('renders category icons', () => {
      const { container } = render(<StrengthsSection matchAnalysis={mockMatchAnalysis} />);
      // Check for emoji presence in text content
      expect(container.textContent).toContain('🤖'); // ATS icon
      expect(container.textContent).toContain('🎯'); // Role match icon
      expect(container.textContent).toContain('🏢'); // Company fit icon
      expect(container.textContent).toContain('✨'); // Main section icon
      expect(container.textContent).toContain('🌟'); // Key highlights icon
    });

    it('renders checkmarks for category strengths', () => {
      const { container } = render(<StrengthsSection matchAnalysis={mockMatchAnalysis} />);
      const checkmarks = container.querySelectorAll('.text-green-500');
      expect(checkmarks.length).toBeGreaterThan(0);
    });
  });

  describe('edge cases', () => {
    it('handles undefined key_strengths gracefully', () => {
      const noKeyStrengths = { ...mockMatchAnalysis };
      delete (noKeyStrengths.overall_score as any).key_strengths;
      render(<StrengthsSection matchAnalysis={noKeyStrengths} />);
      expect(screen.queryByText('Key Highlights')).not.toBeInTheDocument();
    });

    it('handles undefined strengths arrays gracefully', () => {
      const undefinedStrengths: MatchAnalysis = {
        ats_score: { score: 50, explanation: 'Test' },
        role_match_score: { score: 50, explanation: 'Test' },
        company_fit_score: { score: 50, explanation: 'Test' },
        overall_score: { score: 50, explanation: 'Test' },
      };
      const { container } = render(<StrengthsSection matchAnalysis={undefinedStrengths} />);
      expect(container.firstChild).toBeNull();
    });

    it('renders correctly with only one category having strengths', () => {
      const oneCategory: MatchAnalysis = {
        ats_score: {
          score: 88,
          explanation: 'Test',
          strengths: ['Single strength'],
          weaknesses: [],
        },
        role_match_score: { score: 50, explanation: 'Test', strengths: [], weaknesses: [] },
        company_fit_score: { score: 50, explanation: 'Test', strengths: [], weaknesses: [] },
        overall_score: { score: 50, explanation: 'Test', strengths: [], weaknesses: [] },
      };
      render(<StrengthsSection matchAnalysis={oneCategory} />);
      expect(screen.getByText('ATS Optimization')).toBeInTheDocument();
      expect(screen.getByText('Single strength')).toBeInTheDocument();
      expect(screen.queryByText('Role Alignment')).not.toBeInTheDocument();
      expect(screen.queryByText('Company Fit')).not.toBeInTheDocument();
    });
  });
});
