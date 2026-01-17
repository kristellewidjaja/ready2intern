/**
 * Results page component - displays complete analysis results
 */
import { useEffect, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { fetchResults } from '../services/api';
import { OverallScoreCard } from '../components/OverallScoreCard';
import { CategoryScoreCard } from '../components/CategoryScoreCard';
import { StrengthsSection } from '../components/StrengthsSection';
import { GapsSection } from '../components/GapsSection';
import type { ResultsResponse } from '../types';

export const ResultsPage = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const sessionId = searchParams.get('session');

  const [results, setResults] = useState<ResultsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!sessionId) {
      setError('No session ID provided');
      setLoading(false);
      return;
    }

    const loadResults = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await fetchResults(sessionId);
        setResults(data);
      } catch (err: any) {
        console.error('Failed to load results:', err);
        setError(err.response?.data?.detail || 'Failed to load results. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    loadResults();
  }, [sessionId]);

  const handleStartNew = () => {
    navigate('/');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-purple-600 mb-4"></div>
          <p className="text-gray-600 dark:text-gray-300 text-lg">Loading your results...</p>
        </div>
      </div>
    );
  }

  if (error || !results) {
    return (
      <div className="min-h-screen flex items-center justify-center px-4">
        <div className="max-w-md w-full bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8 text-center">
          <div className="text-6xl mb-4">❌</div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
            Unable to Load Results
          </h2>
          <p className="text-gray-600 dark:text-gray-300 mb-6">
            {error || 'Results not found for this session.'}
          </p>
          <button
            onClick={handleStartNew}
            className="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white font-semibold py-3 px-6 rounded-lg hover:from-purple-700 hover:to-blue-700 transition-all duration-200"
          >
            Start New Analysis
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 py-8 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8 flex justify-between items-center">
          <div>
            <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
              Your Analysis Results
            </h1>
            <p className="text-gray-600 dark:text-gray-400">
              Session: {results.session_id.substring(0, 8)}...
            </p>
          </div>
          <button
            onClick={handleStartNew}
            className="bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 font-semibold py-2 px-6 rounded-lg border-2 border-gray-300 dark:border-gray-600 hover:border-purple-600 dark:hover:border-purple-500 transition-all duration-200"
          >
            Start New Analysis
          </button>
        </div>

        {/* Overall Score Card */}
        {results.overall_score !== null && (
          <OverallScoreCard score={results.overall_score} status={results.status} />
        )}

        {/* Score Breakdown */}
        {results.match_analysis && (
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8 mb-8">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
              Score Breakdown
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* ATS Score */}
              <CategoryScoreCard
                title="ATS Score"
                scoreDetail={results.match_analysis.ats_score}
                icon="🤖"
                color="blue"
              />

              {/* Role Match Score */}
              <CategoryScoreCard
                title="Role Match"
                scoreDetail={results.match_analysis.role_match_score}
                icon="🎯"
                color="purple"
              />

              {/* Company Fit Score */}
              <CategoryScoreCard
                title="Company Fit"
                scoreDetail={results.match_analysis.company_fit_score}
                icon="🏢"
                color="green"
              />
            </div>
          </div>
        )}

        {/* Strengths Section */}
        {results.match_analysis && <StrengthsSection matchAnalysis={results.match_analysis} />}

        {/* Gaps Section */}
        {results.gap_analysis && <GapsSection gapAnalysis={results.gap_analysis} />}

        {/* Placeholder for Timeline */}
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8 mb-8 text-center">
          <p className="text-gray-500 dark:text-gray-400">
            📅 Timeline visualization coming in next feature slice...
          </p>
        </div>
      </div>
    </div>
  );
};
