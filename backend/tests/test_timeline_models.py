"""
Tests for timeline data models.
"""

import pytest
from pydantic import ValidationError

from app.models.timeline import (
    Task,
    Milestone,
    TimelinePhase,
    WeeklySummary,
    TimelineMetadata,
    TimelineResult,
)


def test_task_model_valid():
    """Test Task model with valid data."""
    task = Task(
        task_id="task_1",
        title="Learn Python",
        description="Complete Python tutorial",
        gap_ids=["tech_1"],
        estimated_hours=10,
        priority="high",
        dependencies=[],
        resources=["Python.org tutorial"],
        success_criteria="Complete all exercises",
    )
    
    assert task.task_id == "task_1"
    assert task.title == "Learn Python"
    assert task.estimated_hours == 10
    assert task.priority == "high"
    assert len(task.gap_ids) == 1


def test_task_model_defaults():
    """Test Task model with default values."""
    task = Task(
        task_id="task_1",
        title="Learn Python",
        description="Complete Python tutorial",
        estimated_hours=10,
        priority="high",
        success_criteria="Complete all exercises",
    )
    
    # Should have empty lists as defaults
    assert task.gap_ids == []
    assert task.dependencies == []
    assert task.resources == []


def test_task_model_invalid_priority():
    """Test Task model with invalid priority."""
    with pytest.raises(ValidationError):
        Task(
            task_id="task_1",
            title="Learn Python",
            description="Complete Python tutorial",
            estimated_hours=10,
            priority="urgent",  # Invalid priority
            success_criteria="Complete all exercises",
        )


def test_milestone_model_valid():
    """Test Milestone model with valid data."""
    milestone = Milestone(
        milestone_id="milestone_1",
        title="Complete Phase 1",
        description="Finish foundation phase",
        target_date="2026-02-01",
        completion_criteria=["All tasks done", "Tests passing"],
        deliverables=["Updated resume", "Portfolio project"],
    )
    
    assert milestone.milestone_id == "milestone_1"
    assert milestone.title == "Complete Phase 1"
    assert milestone.target_date == "2026-02-01"
    assert len(milestone.completion_criteria) == 2
    assert len(milestone.deliverables) == 2


def test_milestone_model_optional_date():
    """Test Milestone model with optional target date."""
    milestone = Milestone(
        milestone_id="milestone_1",
        title="Complete Phase 1",
        description="Finish foundation phase",
        completion_criteria=["All tasks done"],
        deliverables=["Updated resume"],
    )
    
    assert milestone.target_date is None


def test_timeline_phase_model_valid():
    """Test TimelinePhase model with valid data."""
    task = Task(
        task_id="task_1",
        title="Learn Python",
        description="Complete Python tutorial",
        estimated_hours=10,
        priority="high",
        success_criteria="Complete all exercises",
    )
    
    milestone = Milestone(
        milestone_id="milestone_1",
        title="Complete Phase 1",
        description="Finish foundation phase",
        completion_criteria=["All tasks done"],
        deliverables=["Updated resume"],
    )
    
    phase = TimelinePhase(
        phase_id="phase_1",
        phase_number=1,
        title="Foundation",
        description="Build foundation skills",
        start_week=1,
        end_week=2,
        focus_areas=["Python", "Git"],
        tasks=[task],
        milestones=[milestone],
        estimated_hours_per_week=12,
        success_metrics=["Skills improved"],
    )
    
    assert phase.phase_id == "phase_1"
    assert phase.phase_number == 1
    assert phase.start_week == 1
    assert phase.end_week == 2
    assert len(phase.tasks) == 1
    assert len(phase.milestones) == 1


def test_timeline_phase_model_defaults():
    """Test TimelinePhase model with default values."""
    phase = TimelinePhase(
        phase_id="phase_1",
        phase_number=1,
        title="Foundation",
        description="Build foundation skills",
        start_week=1,
        end_week=2,
        focus_areas=["Python"],
        tasks=[],
        estimated_hours_per_week=12,
        success_metrics=["Skills improved"],
    )
    
    # Milestones should default to empty list
    assert phase.milestones == []


def test_weekly_summary_model_valid():
    """Test WeeklySummary model with valid data."""
    summary = WeeklySummary(
        week_number=1,
        start_date="2026-01-15",
        end_date="2026-01-21",
        phase="Phase 1: Foundation",
        focus="Python basics",
        tasks=["Learn Python", "Setup Git"],
        estimated_hours=12,
        key_deliverable="Python project",
    )
    
    assert summary.week_number == 1
    assert summary.start_date == "2026-01-15"
    assert summary.phase == "Phase 1: Foundation"
    assert len(summary.tasks) == 2


def test_weekly_summary_model_optional_dates():
    """Test WeeklySummary model with optional dates."""
    summary = WeeklySummary(
        week_number=1,
        phase="Phase 1: Foundation",
        focus="Python basics",
        tasks=["Learn Python"],
        estimated_hours=12,
        key_deliverable="Python project",
    )
    
    assert summary.start_date is None
    assert summary.end_date is None


def test_timeline_metadata_model_valid():
    """Test TimelineMetadata model with valid data."""
    metadata = TimelineMetadata(
        total_weeks=8,
        total_hours=96,
        hours_per_week=12,
        start_date="2026-01-15",
        target_deadline="2026-03-12",
        intensity_level="moderate",
        feasibility_assessment="Timeline is realistic",
    )
    
    assert metadata.total_weeks == 8
    assert metadata.total_hours == 96
    assert metadata.hours_per_week == 12
    assert metadata.intensity_level == "moderate"


def test_timeline_metadata_model_invalid_intensity():
    """Test TimelineMetadata model with invalid intensity level."""
    with pytest.raises(ValidationError):
        TimelineMetadata(
            total_weeks=8,
            total_hours=96,
            hours_per_week=12,
            intensity_level="extreme",  # Invalid intensity
            feasibility_assessment="Timeline is realistic",
        )


def test_timeline_metadata_model_optional_dates():
    """Test TimelineMetadata model with optional dates."""
    metadata = TimelineMetadata(
        total_weeks=8,
        total_hours=96,
        hours_per_week=12,
        intensity_level="moderate",
        feasibility_assessment="Timeline is realistic",
    )
    
    assert metadata.start_date is None
    assert metadata.target_deadline is None


def test_timeline_result_model_valid():
    """Test TimelineResult model with valid data."""
    metadata = TimelineMetadata(
        total_weeks=8,
        total_hours=96,
        hours_per_week=12,
        intensity_level="moderate",
        feasibility_assessment="Timeline is realistic",
    )
    
    task = Task(
        task_id="task_1",
        title="Learn Python",
        description="Complete Python tutorial",
        estimated_hours=10,
        priority="high",
        success_criteria="Complete all exercises",
    )
    
    phase = TimelinePhase(
        phase_id="phase_1",
        phase_number=1,
        title="Foundation",
        description="Build foundation skills",
        start_week=1,
        end_week=2,
        focus_areas=["Python"],
        tasks=[task],
        estimated_hours_per_week=12,
        success_metrics=["Skills improved"],
    )
    
    summary = WeeklySummary(
        week_number=1,
        phase="Phase 1: Foundation",
        focus="Python basics",
        tasks=["Learn Python"],
        estimated_hours=12,
        key_deliverable="Python project",
    )
    
    result = TimelineResult(
        metadata=metadata,
        phases=[phase],
        weekly_breakdown=[summary],
        critical_path=["task_1"],
        flexibility_notes=["Can adjust scope"],
        motivation_tips=["Celebrate wins"],
    )
    
    assert result.metadata.total_weeks == 8
    assert len(result.phases) == 1
    assert len(result.weekly_breakdown) == 1
    assert len(result.critical_path) == 1


def test_timeline_result_model_defaults():
    """Test TimelineResult model with default values."""
    metadata = TimelineMetadata(
        total_weeks=8,
        total_hours=96,
        hours_per_week=12,
        intensity_level="moderate",
        feasibility_assessment="Timeline is realistic",
    )
    
    result = TimelineResult(
        metadata=metadata,
        phases=[],
        weekly_breakdown=[],
    )
    
    # Should have empty lists as defaults
    assert result.critical_path == []
    assert result.flexibility_notes == []
    assert result.motivation_tips == []


def test_timeline_result_model_json_serialization():
    """Test TimelineResult model JSON serialization."""
    metadata = TimelineMetadata(
        total_weeks=8,
        total_hours=96,
        hours_per_week=12,
        intensity_level="moderate",
        feasibility_assessment="Timeline is realistic",
    )
    
    result = TimelineResult(
        metadata=metadata,
        phases=[],
        weekly_breakdown=[],
    )
    
    # Should be able to convert to dict
    result_dict = result.model_dump()
    assert "metadata" in result_dict
    assert "phases" in result_dict
    assert "weekly_breakdown" in result_dict
    
    # Should be able to convert to JSON
    result_json = result.model_dump_json()
    assert isinstance(result_json, str)
    assert "metadata" in result_json
