/**
 * Tests for ResultsPage component
 */
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { userEvent } from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import { ResultsPage } from '../ResultsPage';
import * as api from '../../services/api';
import type { ResultsResponse } from '../../types';

// Mock the api module
vi.mock('../../services/api', () => ({
  fetchResults: vi.fn(),
}));

// Mock react-router-dom navigate
const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

const mockResultsResponse: ResultsResponse = {
  session_id: 'test-session-123',
  status: 'completed',
  overall_score: 85,
  resume_analysis: {
    personal_info: { name: 'John Doe' },
  },
  match_analysis: {
    ats_score: {
      score: 88,
      explanation: 'Strong ATS compatibility with good formatting.',
      strengths: ['Clear structure', 'Good keywords'],
      weaknesses: ['Could improve length'],
    },
    role_match_score: {
      score: 85,
      explanation: 'Good alignment with role requirements.',
      strengths: ['Relevant experience', 'Strong skills'],
      weaknesses: ['Missing some advanced topics'],
    },
    company_fit_score: {
      score: 82,
      explanation: 'Good cultural fit indicators.',
      strengths: ['Leadership examples', 'Team collaboration'],
      weaknesses: ['Could show more innovation'],
    },
    overall_score: {
      score: 85,
      explanation: 'Strong overall match.',
    },
  },
  gap_analysis: null,
  timeline: null,
  message: 'Analysis complete',
};

describe('ResultsPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  const renderWithRouter = (sessionId: string = 'test-session-123') => {
    return render(
      <BrowserRouter>
        <ResultsPage />
      </BrowserRouter>,
      {
        wrapper: ({ children }) => (
          <div>{children}</div>
        ),
      }
    );
  };

  describe('Loading State', () => {
    it('shows loading state while fetching results', () => {
      vi.mocked(api.fetchResults).mockImplementation(
        () => new Promise(() => {}) // Never resolves
      );

      renderWithRouter();

      expect(screen.getByText('Loading your results...')).toBeInTheDocument();
      expect(screen.getByRole('status', { hidden: true })).toBeInTheDocument();
    });
  });

  describe('Error Handling', () => {
    it('displays error when session ID is missing', async () => {
      // Render without session ID in URL
      render(
        <BrowserRouter>
          <ResultsPage />
        </BrowserRouter>
      );

      await waitFor(() => {
        expect(screen.getByText('Unable to Load Results')).toBeInTheDocument();
        expect(screen.getByText(/No session ID provided/)).toBeInTheDocument();
      });
    });

    it('displays error when results fetch fails', async () => {
      vi.mocked(api.fetchResults).mockRejectedValue({
        response: { data: { detail: 'Session not found' } },
      });

      renderWithRouter();

      await waitFor(() => {
        expect(screen.getByText('Unable to Load Results')).toBeInTheDocument();
        expect(screen.getByText(/Session not found/)).toBeInTheDocument();
      });
    });

    it('displays generic error when error has no detail', async () => {
      vi.mocked(api.fetchResults).mockRejectedValue(new Error('Network error'));

      renderWithRouter();

      await waitFor(() => {
        expect(screen.getByText('Unable to Load Results')).toBeInTheDocument();
        expect(
          screen.getByText(/Failed to load results. Please try again./)
        ).toBeInTheDocument();
      });
    });

    it('shows Start New Analysis button on error', async () => {
      vi.mocked(api.fetchResults).mockRejectedValue(new Error('Error'));

      renderWithRouter();

      await waitFor(() => {
        const button = screen.getByText('Start New Analysis');
        expect(button).toBeInTheDocument();
      });
    });
  });

  describe('Successful Results Display', () => {
    beforeEach(() => {
      vi.mocked(api.fetchResults).mockResolvedValue(mockResultsResponse);
    });

    it('renders overall score card when results loaded', async () => {
      renderWithRouter();

      await waitFor(() => {
        expect(screen.getByText('Overall Match Score')).toBeInTheDocument();
        expect(screen.getByText('85')).toBeInTheDocument();
      });
    });

    it('renders score breakdown when match analysis available', async () => {
      renderWithRouter();

      await waitFor(() => {
        expect(screen.getByText('Score Breakdown')).toBeInTheDocument();
      });
    });

    it('shows ATS, Role Match, and Company Fit scores', async () => {
      renderWithRouter();

      await waitFor(() => {
        expect(screen.getByText('ATS Score')).toBeInTheDocument();
        expect(screen.getByText('Role Match')).toBeInTheDocument();
        expect(screen.getByText('Company Fit')).toBeInTheDocument();
        
        // Check score values
        expect(screen.getByText('88')).toBeInTheDocument(); // ATS
        expect(screen.getByText('85')).toBeInTheDocument(); // Role Match
        expect(screen.getByText('82')).toBeInTheDocument(); // Company Fit
      });
    });

    it('displays session ID in header', async () => {
      renderWithRouter();

      await waitFor(() => {
        expect(screen.getByText(/Session: test-sess.../)).toBeInTheDocument();
      });
    });

    it('renders page title', async () => {
      renderWithRouter();

      await waitFor(() => {
        expect(screen.getByText('Your Analysis Results')).toBeInTheDocument();
      });
    });
  });

  describe('Navigation', () => {
    beforeEach(() => {
      vi.mocked(api.fetchResults).mockResolvedValue(mockResultsResponse);
    });

    it('navigates to dashboard when Start New Analysis clicked', async () => {
      const user = userEvent.setup();
      renderWithRouter();

      await waitFor(() => {
        expect(screen.getByText('Your Analysis Results')).toBeInTheDocument();
      });

      const button = screen.getByText('Start New Analysis');
      await user.click(button);

      expect(mockNavigate).toHaveBeenCalledWith('/');
    });
  });

  describe('Partial Results', () => {
    it('handles partial results gracefully', async () => {
      const partialResults: ResultsResponse = {
        ...mockResultsResponse,
        status: 'partial',
        gap_analysis: null,
        timeline: null,
      };

      vi.mocked(api.fetchResults).mockResolvedValue(partialResults);
      renderWithRouter();

      await waitFor(() => {
        expect(screen.getByText('Overall Match Score')).toBeInTheDocument();
        expect(
          screen.getByText(/Partial results - some analysis still in progress/)
        ).toBeInTheDocument();
      });
    });

    it('does not render score breakdown when match analysis is missing', async () => {
      const noMatchResults: ResultsResponse = {
        ...mockResultsResponse,
        match_analysis: null,
        overall_score: null,
      };

      vi.mocked(api.fetchResults).mockResolvedValue(noMatchResults);
      renderWithRouter();

      await waitFor(() => {
        expect(screen.getByText('Your Analysis Results')).toBeInTheDocument();
      });

      expect(screen.queryByText('Score Breakdown')).not.toBeInTheDocument();
    });
  });

  describe('Score Breakdown Details', () => {
    beforeEach(() => {
      vi.mocked(api.fetchResults).mockResolvedValue(mockResultsResponse);
    });

    it('displays category score explanations', async () => {
      renderWithRouter();

      await waitFor(() => {
        expect(
          screen.getByText('Strong ATS compatibility with good formatting.')
        ).toBeInTheDocument();
        expect(
          screen.getByText('Good alignment with role requirements.')
        ).toBeInTheDocument();
        expect(
          screen.getByText('Good cultural fit indicators.')
        ).toBeInTheDocument();
      });
    });

    it('displays category icons', async () => {
      renderWithRouter();

      await waitFor(() => {
        expect(screen.getByText('🤖')).toBeInTheDocument(); // ATS
        expect(screen.getByText('🎯')).toBeInTheDocument(); // Role Match
        expect(screen.getByText('🏢')).toBeInTheDocument(); // Company Fit
      });
    });
  });

  describe('Future Sections Placeholder', () => {
    beforeEach(() => {
      vi.mocked(api.fetchResults).mockResolvedValue(mockResultsResponse);
    });

    it('shows placeholder for future sections', async () => {
      renderWithRouter();

      await waitFor(() => {
        expect(
          screen.getByText(
            /Detailed strengths, gaps, and timeline sections coming in next feature slices.../
          )
        ).toBeInTheDocument();
      });
    });
  });
});
