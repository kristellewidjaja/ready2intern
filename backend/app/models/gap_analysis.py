"""
Gap analysis data models.
"""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class Resource(BaseModel):
    """Resource for addressing a gap."""
    
    type: Literal["course", "tutorial", "documentation", "project", "book", "certification"]
    name: str
    url: str = Field(default="Search online", description="URL or 'Search online'")
    estimated_time: str
    notes: str


class Recommendation(BaseModel):
    """Recommendation for addressing a gap."""
    
    action: str
    resources: List[Resource] = Field(default_factory=list)
    success_criteria: str
    estimated_time: str


class ProjectIdea(BaseModel):
    """Project idea for gaining experience."""
    
    name: str
    description: str
    key_features: List[str]
    technologies: List[str]
    estimated_time: str
    difficulty: Literal["beginner", "intermediate", "advanced"]
    portfolio_value: str


class ExperienceRecommendation(BaseModel):
    """Recommendation for experience gaps."""
    
    action: str
    project_ideas: List[ProjectIdea] = Field(default_factory=list)
    success_criteria: str
    estimated_time: str


class ResumeRecommendation(BaseModel):
    """Recommendation for resume improvements."""
    
    action: str
    before_example: Optional[str] = None
    after_example: Optional[str] = None
    success_criteria: str
    estimated_time: str


class TechnicalGap(BaseModel):
    """Technical skill or knowledge gap."""
    
    gap_id: str
    category: Literal["technical_skills", "tools", "frameworks", "languages"]
    title: str
    description: str
    priority: Literal["high", "medium", "low"]
    priority_reasoning: str
    current_level: Literal["none", "beginner", "intermediate"]
    target_level: Literal["beginner", "intermediate", "advanced"]
    impact_on_application: str
    recommendations: List[Recommendation]


class ExperienceGap(BaseModel):
    """Work or project experience gap."""
    
    gap_id: str
    category: Literal["work_experience", "project_experience", "domain_knowledge"]
    title: str
    description: str
    priority: Literal["high", "medium", "low"]
    priority_reasoning: str
    impact_on_application: str
    recommendations: List[ExperienceRecommendation]


class CompanyFitGap(BaseModel):
    """Company culture or values alignment gap."""
    
    gap_id: str
    category: Literal["leadership", "values", "culture", "communication"]
    title: str
    description: str
    priority: Literal["high", "medium", "low"]
    priority_reasoning: str
    company_value: str
    impact_on_application: str
    recommendations: List[dict]  # Flexible structure for company fit recommendations


class ResumeOptimizationGap(BaseModel):
    """Resume formatting or content gap."""
    
    gap_id: str
    category: Literal["keywords", "formatting", "content", "storytelling"]
    title: str
    description: str
    priority: Literal["high", "medium", "low"]
    priority_reasoning: str
    impact_on_application: str
    recommendations: List[ResumeRecommendation]


class QuickWin(BaseModel):
    """Quick, high-impact action."""
    
    title: str
    description: str
    impact: str
    estimated_time: str
    steps: List[str]


class Milestone(BaseModel):
    """Development milestone."""
    
    milestone: str
    estimated_time: str
    success_criteria: str


class LongTermDevelopment(BaseModel):
    """Long-term career development goal."""
    
    title: str
    description: str
    rationale: str
    estimated_time: str
    milestones: List[Milestone]


class PhaseAction(BaseModel):
    """Action item in a development phase."""
    
    action: str
    gap_ids: List[str]
    estimated_time: str


class DevelopmentPhase(BaseModel):
    """Development phase with timeframe and actions."""
    
    timeframe: str
    focus: str
    actions: List[PhaseAction]


class PrioritizedActionPlan(BaseModel):
    """Prioritized action plan with phases."""
    
    phase_1_immediate: DevelopmentPhase
    phase_2_short_term: DevelopmentPhase
    phase_3_medium_term: DevelopmentPhase


class GapAnalysisSummary(BaseModel):
    """Summary of gap analysis."""
    
    total_gaps: int
    high_priority_count: int
    medium_priority_count: int
    low_priority_count: int
    estimated_preparation_time: str
    overall_assessment: str


class GapAnalysisResult(BaseModel):
    """Complete gap analysis result."""
    
    summary: GapAnalysisSummary
    technical_gaps: List[TechnicalGap] = Field(default_factory=list)
    experience_gaps: List[ExperienceGap] = Field(default_factory=list)
    company_fit_gaps: List[CompanyFitGap] = Field(default_factory=list)
    resume_optimization_gaps: List[ResumeOptimizationGap] = Field(default_factory=list)
    quick_wins: List[QuickWin] = Field(default_factory=list)
    long_term_development: List[LongTermDevelopment] = Field(default_factory=list)
    prioritized_action_plan: Optional[PrioritizedActionPlan] = None
