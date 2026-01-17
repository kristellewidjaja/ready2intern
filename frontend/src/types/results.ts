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
  overall_score: ScoreDetail & {
    key_strengths?: string[];
  };
}

// Gap Analysis Types
export interface Resource {
  type: 'course' | 'tutorial' | 'documentation' | 'project' | 'book' | 'certification';
  name: string;
  url: string;
  estimated_time: string;
  notes: string;
}

export interface Recommendation {
  action: string;
  resources: Resource[];
  success_criteria: string;
  estimated_time: string;
}

export interface ProjectIdea {
  name: string;
  description: string;
  key_features: string[];
  technologies: string[];
  estimated_time: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  portfolio_value: string;
}

export interface ExperienceRecommendation {
  action: string;
  project_ideas: ProjectIdea[];
  success_criteria: string;
  estimated_time: string;
}

export interface ResumeRecommendation {
  action: string;
  before_example?: string;
  after_example?: string;
  success_criteria: string;
  estimated_time: string;
}

export interface TechnicalGap {
  gap_id: string;
  category: 'technical_skills' | 'tools' | 'frameworks' | 'languages';
  title: string;
  description: string;
  priority: 'high' | 'medium' | 'low';
  priority_reasoning: string;
  current_level: 'none' | 'beginner' | 'intermediate';
  target_level: 'beginner' | 'intermediate' | 'advanced';
  impact_on_application: string;
  recommendations: Recommendation[];
}

export interface ExperienceGap {
  gap_id: string;
  category: 'work_experience' | 'project_experience' | 'domain_knowledge';
  title: string;
  description: string;
  priority: 'high' | 'medium' | 'low';
  priority_reasoning: string;
  impact_on_application: string;
  recommendations: ExperienceRecommendation[];
}

export interface CompanyFitGap {
  gap_id: string;
  category: 'leadership' | 'values' | 'culture' | 'communication';
  title: string;
  description: string;
  priority: 'high' | 'medium' | 'low';
  priority_reasoning: string;
  company_value: string;
  impact_on_application: string;
  recommendations: any[];
}

export interface ResumeOptimizationGap {
  gap_id: string;
  category: 'keywords' | 'formatting' | 'content' | 'storytelling';
  title: string;
  description: string;
  priority: 'high' | 'medium' | 'low';
  priority_reasoning: string;
  impact_on_application: string;
  recommendations: ResumeRecommendation[];
}

export interface QuickWin {
  title: string;
  description: string;
  impact: string;
  estimated_time: string;
  steps: string[];
}

export interface GapAnalysisSummary {
  total_gaps: number;
  high_priority_count: number;
  medium_priority_count: number;
  low_priority_count: number;
  estimated_preparation_time: string;
  overall_assessment: string;
}

export interface GapAnalysis {
  summary: GapAnalysisSummary;
  technical_gaps: TechnicalGap[];
  experience_gaps: ExperienceGap[];
  company_fit_gaps: CompanyFitGap[];
  resume_optimization_gaps: ResumeOptimizationGap[];
  quick_wins: QuickWin[];
  long_term_development: any[];
  prioritized_action_plan: any;
}

// Timeline Types
export interface Task {
  task_id: string;
  title: string;
  description: string;
  gap_ids: string[];
  estimated_hours: number;
  priority: 'high' | 'medium' | 'low';
  dependencies: string[];
  resources: string[];
  success_criteria: string | string[];
}

export interface Milestone {
  milestone_id: string;
  title: string;
  description: string;
  target_date: string | null;
  completion_criteria: string[];
  deliverables: string[];
}

export interface TimelinePhase {
  phase_id: string;
  phase_number: number;
  title: string;
  description: string;
  start_week: number;
  end_week: number;
  focus_areas: string[];
  tasks: Task[];
  milestones: Milestone[];
  estimated_hours_per_week: number;
  success_metrics: string[];
}

export interface WeeklySummary {
  week_number: number;
  start_date: string | null;
  end_date: string | null;
  phase: string;
  focus: string;
  tasks: string[];
  estimated_hours: number;
  key_deliverable: string;
}

export interface TimelineMetadata {
  total_weeks: number;
  total_hours: number;
  hours_per_week: number;
  start_date: string | null;
  target_deadline: string | null;
  intensity_level: 'light' | 'moderate' | 'intensive';
  feasibility_assessment: string;
}

export interface TimelineResult {
  metadata: TimelineMetadata;
  phases: TimelinePhase[];
  weekly_breakdown: WeeklySummary[];
  critical_path: string[];
  flexibility_notes: string[];
  motivation_tips: string[];
}

export interface ResultsResponse {
  session_id: string;
  status: 'completed' | 'partial' | 'failed';
  resume_analysis: any | null;
  match_analysis: MatchAnalysis | null;
  gap_analysis: GapAnalysis | null;
  timeline: TimelineResult | null;
  overall_score: number | null;
  message: string;
}
