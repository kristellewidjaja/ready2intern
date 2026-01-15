"""
Timeline generation data models.
"""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from datetime import date


class Task(BaseModel):
    """Individual task in a timeline phase."""
    
    task_id: str
    title: str
    description: str
    gap_ids: List[str] = Field(default_factory=list, description="Gap IDs this task addresses")
    estimated_hours: int
    priority: Literal["high", "medium", "low"]
    dependencies: List[str] = Field(default_factory=list, description="Task IDs that must be completed first")
    resources: List[str] = Field(default_factory=list, description="Resources needed for this task")
    success_criteria: str


class Milestone(BaseModel):
    """Milestone checkpoint in the timeline."""
    
    milestone_id: str
    title: str
    description: str
    target_date: Optional[str] = None  # ISO date string (YYYY-MM-DD)
    completion_criteria: List[str]
    deliverables: List[str]


class TimelinePhase(BaseModel):
    """Phase in the development timeline."""
    
    phase_id: str
    phase_number: int
    title: str
    description: str
    start_week: int
    end_week: int
    focus_areas: List[str]
    tasks: List[Task]
    milestones: List[Milestone] = Field(default_factory=list)
    estimated_hours_per_week: int
    success_metrics: List[str]


class WeeklySummary(BaseModel):
    """Summary of what to accomplish each week."""
    
    week_number: int
    start_date: Optional[str] = None  # ISO date string
    end_date: Optional[str] = None  # ISO date string
    phase: str
    focus: str
    tasks: List[str]  # Task titles
    estimated_hours: int
    key_deliverable: str


class TimelineMetadata(BaseModel):
    """Metadata about the timeline."""
    
    total_weeks: int
    total_hours: int
    hours_per_week: int
    start_date: Optional[str] = None  # ISO date string
    target_deadline: Optional[str] = None  # ISO date string
    intensity_level: Literal["light", "moderate", "intensive"]
    feasibility_assessment: str


class TimelineResult(BaseModel):
    """Complete timeline generation result."""
    
    metadata: TimelineMetadata
    phases: List[TimelinePhase]
    weekly_breakdown: List[WeeklySummary]
    critical_path: List[str] = Field(
        default_factory=list,
        description="Task IDs that are critical to complete on time"
    )
    flexibility_notes: List[str] = Field(
        default_factory=list,
        description="Notes about what can be adjusted if timeline is too aggressive"
    )
    motivation_tips: List[str] = Field(
        default_factory=list,
        description="Tips to stay motivated and on track"
    )
