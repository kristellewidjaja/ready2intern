/**
 * StrengthsSection component - displays key strengths from match analysis
 */
import type { MatchAnalysis } from '../types';

interface StrengthsSectionProps {
  matchAnalysis: MatchAnalysis;
}

export const StrengthsSection = ({ matchAnalysis }: StrengthsSectionProps) => {
  // Collect all strengths from different score categories
  const allStrengths: { category: string; icon: string; items: string[] }[] = [];

  if (matchAnalysis.ats_score.strengths && matchAnalysis.ats_score.strengths.length > 0) {
    allStrengths.push({
      category: 'ATS Optimization',
      icon: '🤖',
      items: matchAnalysis.ats_score.strengths,
    });
  }

  if (matchAnalysis.role_match_score.strengths && matchAnalysis.role_match_score.strengths.length > 0) {
    allStrengths.push({
      category: 'Role Alignment',
      icon: '🎯',
      items: matchAnalysis.role_match_score.strengths,
    });
  }

  if (matchAnalysis.company_fit_score.strengths && matchAnalysis.company_fit_score.strengths.length > 0) {
    allStrengths.push({
      category: 'Company Fit',
      icon: '🏢',
      items: matchAnalysis.company_fit_score.strengths,
    });
  }

  // Key strengths from overall score
  const keyStrengths = matchAnalysis.overall_score.key_strengths || [];

  if (allStrengths.length === 0 && keyStrengths.length === 0) {
    return null;
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8 mb-8">
      <div className="flex items-center mb-6">
        <div className="text-3xl mr-3">✨</div>
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Your Strengths</h2>
      </div>

      {/* Key Strengths */}
      {keyStrengths.length > 0 && (
        <div className="mb-6">
          <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-3 flex items-center">
            <span className="text-xl mr-2">🌟</span>
            Key Highlights
          </h3>
          <div className="space-y-3">
            {keyStrengths.map((strength, index) => (
              <div
                key={index}
                className="flex items-start p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border-l-4 border-green-500"
              >
                <div className="flex-shrink-0 w-6 h-6 flex items-center justify-center bg-green-500 text-white rounded-full text-sm font-bold mr-3 mt-0.5">
                  {index + 1}
                </div>
                <p className="text-gray-700 dark:text-gray-300 flex-1">{strength}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Category-specific Strengths */}
      {allStrengths.length > 0 && (
        <div className="space-y-6">
          {allStrengths.map((category, catIndex) => (
            <div key={catIndex}>
              <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-3 flex items-center">
                <span className="text-xl mr-2">{category.icon}</span>
                {category.category}
              </h3>
              <div className="space-y-2">
                {category.items.map((item, itemIndex) => (
                  <div
                    key={itemIndex}
                    className="flex items-start p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg hover:bg-blue-100 dark:hover:bg-blue-900/30 transition-colors"
                  >
                    <div className="flex-shrink-0 text-green-500 mr-3 mt-0.5">✓</div>
                    <p className="text-gray-700 dark:text-gray-300 text-sm">{item}</p>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
