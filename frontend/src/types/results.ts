/**
 * Results types for complete analysis data
 */

export interface ScoreDetail {
  score: number;
  explanation: string;
  strengths?: string[];
  weaknesses?: string[];
}

export interface MatchAnalysis {
  ats_score: ScoreDetail;
  role_match_score: ScoreDetail;
  company_fit_score: ScoreDetail;
  overall_score: ScoreDetail;
}

export interface ResultsResponse {
  session_id: string;
  status: 'completed' | 'partial' | 'failed';
  resume_analysis: any | null;
  match_analysis: MatchAnalysis | null;
  gap_analysis: any | null;
  timeline: any | null;
  overall_score: number | null;
  message: string;
}
