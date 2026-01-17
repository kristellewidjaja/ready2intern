import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { FileDropzone } from '../components/FileDropzone';
import { CompanyLogoSelector } from '../components/CompanyLogoSelector';
import { RoleDescriptionInput } from '../components/RoleDescriptionInput';
import { AnalyzeButton } from '../components/AnalyzeButton';
import { analyzeResume } from '../services/api';
import type { UploadResponse } from '../types/upload';

interface HealthStatus {
  status: string;
  timestamp: string;
  service: string;
}

export const Dashboard = () => {
  const navigate = useNavigate();
  const [healthStatus, setHealthStatus] = useState<HealthStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [selectedCompany, setSelectedCompany] = useState<string | null>(null);
  const [roleDescription, setRoleDescription] = useState<string>('');

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const response = await axios.get<HealthStatus>(
          `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/health`
        );
        setHealthStatus(response.data);
        setError(null);
      } catch (err) {
        setError('Failed to connect to backend API');
        console.error('Health check failed:', err);
      } finally {
        setLoading(false);
      }
    };

    checkHealth();
  }, []);

  const handleUploadSuccess = (response: UploadResponse) => {
    setSessionId(response.session_id);
    console.log('Upload successful:', response);
  };

  const handleCompanySelect = (companyId: string) => {
    setSelectedCompany(companyId);
    console.log('Company selected:', companyId);
  };

  const handleRoleDescriptionChange = (value: string) => {
    setRoleDescription(value);
  };

  const handleAnalyze = async () => {
    if (!sessionId || !selectedCompany) {
      console.error('Missing required fields');
      return;
    }

    try {
      const response = await analyzeResume({
        session_id: sessionId,
        company: selectedCompany,
        role_description: roleDescription,
      });

      console.log('Analysis completed:', response);
      
      // Navigate to results page with session ID
      navigate(`/results?session=${sessionId}`);
    } catch (err) {
      console.error('Analysis failed:', err);
      alert('Failed to start analysis. Please try again.');
    }
  };

  return (
    <div className="space-y-8">
      <div className="text-center">
        <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
          Welcome to Ready2Intern
        </h2>
        <p className="text-xl text-gray-600 dark:text-gray-300">
          AI-powered resume evaluation for tech internships
        </p>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          System Status
        </h3>
        
        {loading && (
          <div className="flex items-center space-x-2 text-gray-600 dark:text-gray-400">
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-primary-500"></div>
            <span>Checking backend connection...</span>
          </div>
        )}

        {error && (
          <div className="flex items-center space-x-2 text-red-600 dark:text-red-400">
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
            <span>{error}</span>
          </div>
        )}

        {healthStatus && (
          <div className="space-y-2">
            <div className="flex items-center space-x-2 text-green-600 dark:text-green-400">
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <span className="font-medium">Backend is {healthStatus.status}</span>
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400">
              <p>Service: {healthStatus.service}</p>
              <p>Last checked: {new Date(healthStatus.timestamp).toLocaleString()}</p>
            </div>
          </div>
        )}
      </div>

      {/* Resume Upload Section */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
          Step 1: Upload Resume
        </h3>
        <FileDropzone onUploadSuccess={handleUploadSuccess} />
      </div>

      {/* Company Selection Section */}
      {sessionId && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
          <CompanyLogoSelector
            selectedCompany={selectedCompany}
            onCompanySelect={handleCompanySelect}
          />
        </div>
      )}

      {/* Role Description Section */}
      {sessionId && selectedCompany && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            Step 3: Paste Role Description
          </h3>
          <RoleDescriptionInput
            value={roleDescription}
            onChange={handleRoleDescriptionChange}
          />
        </div>
      )}

      {/* Analyze Button Section */}
      {sessionId && selectedCompany && roleDescription.length > 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            Step 4: Start Analysis
          </h3>
          <AnalyzeButton
            sessionId={sessionId}
            company={selectedCompany}
            roleDescription={roleDescription}
            onAnalyze={handleAnalyze}
          />
        </div>
      )}

      {/* Progress Steps */}
      <div className="grid md:grid-cols-3 gap-6">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
          <div className="text-primary-500 mb-3">
            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            1. Upload Resume
          </h3>
          <p className="text-gray-600 dark:text-gray-400 text-sm">
            {sessionId ? '✓ Resume uploaded' : 'Upload your resume in PDF or DOCX format'}
          </p>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
          <div className="text-primary-500 mb-3">
            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
          </div>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            2. Select Company
          </h3>
          <p className="text-gray-600 dark:text-gray-400 text-sm">
            {selectedCompany ? '✓ Company selected' : 'Choose your target company'}
          </p>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
          <div className="text-primary-500 mb-3">
            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            3. Role Description
          </h3>
          <p className="text-gray-600 dark:text-gray-400 text-sm">
            {roleDescription.length >= 50 ? '✓ Role description added' : 'Paste the job description'}
          </p>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
          <div className="text-primary-500 mb-3">
            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
            </svg>
          </div>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            4. Get Analysis
          </h3>
          <p className="text-gray-600 dark:text-gray-400 text-sm">
            Receive AI-powered insights (Coming soon)
          </p>
        </div>
      </div>
    </div>
  );
};
