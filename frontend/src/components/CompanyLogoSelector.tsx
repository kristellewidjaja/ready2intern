import React, { useEffect, useState } from 'react';
import type { Company } from '../types';
import { fetchCompanies } from '../services/api';

interface CompanyLogoSelectorProps {
  selectedCompany: string | null;
  onCompanySelect: (companyId: string) => void;
}

export const CompanyLogoSelector: React.FC<CompanyLogoSelectorProps> = ({
  selectedCompany,
  onCompanySelect,
}) => {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadCompanies = async () => {
      try {
        setLoading(true);
        const data = await fetchCompanies();
        setCompanies(data.companies);
        setError(null);
      } catch (err) {
        setError('Failed to load companies. Please try again.');
        console.error('Error loading companies:', err);
      } finally {
        setLoading(false);
      }
    };

    loadCompanies();
  }, []);

  if (loading) {
    return (
      <div className="w-full">
        <h2 className="text-2xl font-bold mb-4 text-gray-900 dark:text-white">
          Select Target Company
        </h2>
        <div className="flex gap-4 justify-center">
          {[1, 2, 3].map((i) => (
            <div
              key={i}
              className="w-48 h-48 bg-gray-200 dark:bg-gray-700 rounded-xl animate-pulse"
            />
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="w-full">
        <h2 className="text-2xl font-bold mb-4 text-gray-900 dark:text-white">
          Select Target Company
        </h2>
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 text-red-700 dark:text-red-400">
          {error}
        </div>
      </div>
    );
  }

  return (
    <div className="w-full">
      <h2 className="text-2xl font-bold mb-2 text-gray-900 dark:text-white">
        Select Target Company
      </h2>
      <p className="text-gray-600 dark:text-gray-400 mb-6">
        Choose the company you're targeting for your internship application
      </p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {companies.map((company) => {
          const isSelected = selectedCompany === company.id;

          return (
            <button
              key={company.id}
              onClick={() => onCompanySelect(company.id)}
              className={`
                relative group
                p-6 rounded-xl border-2 transition-all duration-200
                hover:scale-105 hover:shadow-lg
                focus:outline-none focus:ring-4 focus:ring-opacity-50
                ${
                  isSelected
                    ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20 shadow-md'
                    : 'border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 hover:border-gray-300 dark:hover:border-gray-600'
                }
              `}
              style={
                isSelected
                  ? {
                      borderColor: company.color,
                      boxShadow: `0 4px 12px ${company.color}40`,
                    }
                  : undefined
              }
              aria-pressed={isSelected}
              aria-label={`Select ${company.display_name}`}
            >
              {/* Checkmark overlay */}
              {isSelected && (
                <div
                  className="absolute top-3 right-3 w-8 h-8 rounded-full flex items-center justify-center text-white"
                  style={{ backgroundColor: company.color }}
                >
                  <svg
                    className="w-5 h-5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={3}
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                </div>
              )}

              {/* Company logo */}
              <div className="flex justify-center mb-4">
                <img
                  src={company.logo_url}
                  alt={`${company.display_name} logo`}
                  className="w-24 h-24 object-contain"
                />
              </div>

              {/* Company name */}
              <h3
                className="text-xl font-bold mb-2 text-center"
                style={isSelected ? { color: company.color } : undefined}
              >
                {company.display_name}
              </h3>

              {/* Description */}
              <p className="text-sm text-gray-600 dark:text-gray-400 text-center">
                {company.description}
              </p>

              {/* Hover indicator */}
              {!isSelected && (
                <div className="absolute inset-0 rounded-xl border-2 border-transparent group-hover:border-gray-300 dark:group-hover:border-gray-600 transition-colors pointer-events-none" />
              )}
            </button>
          );
        })}
      </div>

      {/* Selection indicator */}
      {selectedCompany && (
        <div className="mt-4 text-center text-sm text-gray-600 dark:text-gray-400">
          Selected:{' '}
          <span className="font-semibold text-gray-900 dark:text-white">
            {companies.find((c) => c.id === selectedCompany)?.display_name}
          </span>
        </div>
      )}
    </div>
  );
};
