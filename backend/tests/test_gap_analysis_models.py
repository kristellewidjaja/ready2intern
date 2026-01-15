"""
Tests for gap analysis data models.
"""

import pytest
from pydantic import ValidationError

from app.models.gap_analysis import (
    Resource,
    Recommendation,
    ProjectIdea,
    TechnicalGap,
    ExperienceGap,
    CompanyFitGap,
    ResumeOptimizationGap,
    QuickWin,
    Milestone,
    LongTermDevelopment,
    PhaseAction,
    DevelopmentPhase,
    PrioritizedActionPlan,
    GapAnalysisSummary,
    GapAnalysisResult,
)


class TestResource:
    """Test Resource model."""

    def test_valid_resource(self):
        """Test creating a valid resource."""
        resource = Resource(
            type="course",
            name="Kubernetes Basics",
            url="https://kubernetes.io/docs/tutorials/",
            estimated_time="10 hours",
            notes="Official documentation",
        )
        assert resource.type == "course"
        assert resource.name == "Kubernetes Basics"
        assert resource.url == "https://kubernetes.io/docs/tutorials/"

    def test_resource_default_url(self):
        """Test resource with default URL."""
        resource = Resource(
            type="tutorial",
            name="GraphQL Tutorial",
            estimated_time="5 hours",
            notes="Beginner-friendly",
        )
        assert resource.url == "Search online"

    def test_invalid_resource_type(self):
        """Test resource with invalid type."""
        with pytest.raises(ValidationError):
            Resource(
                type="invalid_type",
                name="Test",
                estimated_time="1 hour",
                notes="Test",
            )


class TestTechnicalGap:
    """Test TechnicalGap model."""

    def test_valid_technical_gap(self):
        """Test creating a valid technical gap."""
        gap = TechnicalGap(
            gap_id="tech_1",
            category="tools",
            title="Kubernetes Experience",
            description="Missing container orchestration",
            priority="high",
            priority_reasoning="Critical for cloud-native development",
            current_level="none",
            target_level="intermediate",
            impact_on_application="Significant gap",
            recommendations=[
                Recommendation(
                    action="Complete tutorial",
                    resources=[],
                    success_criteria="Deploy app",
                    estimated_time="2 weeks",
                )
            ],
        )
        assert gap.gap_id == "tech_1"
        assert gap.priority == "high"
        assert gap.current_level == "none"

    def test_invalid_priority(self):
        """Test technical gap with invalid priority."""
        with pytest.raises(ValidationError):
            TechnicalGap(
                gap_id="tech_1",
                category="tools",
                title="Test",
                description="Test",
                priority="invalid",
                priority_reasoning="Test",
                current_level="none",
                target_level="intermediate",
                impact_on_application="Test",
                recommendations=[],
            )


class TestExperienceGap:
    """Test ExperienceGap model."""

    def test_valid_experience_gap(self):
        """Test creating a valid experience gap."""
        gap = ExperienceGap(
            gap_id="exp_1",
            category="project_experience",
            title="Distributed Systems Projects",
            description="Lack of distributed systems experience",
            priority="medium",
            priority_reasoning="Important for role",
            impact_on_application="Moderate impact",
            recommendations=[],
        )
        assert gap.gap_id == "exp_1"
        assert gap.category == "project_experience"


class TestProjectIdea:
    """Test ProjectIdea model."""

    def test_valid_project_idea(self):
        """Test creating a valid project idea."""
        project = ProjectIdea(
            name="Distributed Cache",
            description="Build a distributed caching system",
            key_features=["Consistent hashing", "Replication", "Fault tolerance"],
            technologies=["Go", "Redis", "Docker"],
            estimated_time="4 weeks",
            difficulty="advanced",
            portfolio_value="Demonstrates distributed systems knowledge",
        )
        assert project.name == "Distributed Cache"
        assert project.difficulty == "advanced"
        assert len(project.key_features) == 3


class TestQuickWin:
    """Test QuickWin model."""

    def test_valid_quick_win(self):
        """Test creating a valid quick win."""
        win = QuickWin(
            title="Add missing keywords",
            description="Update resume with role keywords",
            impact="Improves ATS score significantly",
            estimated_time="2 hours",
            steps=["Identify keywords", "Update resume", "Review"],
        )
        assert win.title == "Add missing keywords"
        assert len(win.steps) == 3


class TestGapAnalysisSummary:
    """Test GapAnalysisSummary model."""

    def test_valid_summary(self):
        """Test creating a valid summary."""
        summary = GapAnalysisSummary(
            total_gaps=10,
            high_priority_count=3,
            medium_priority_count=5,
            low_priority_count=2,
            estimated_preparation_time="6-8 weeks",
            overall_assessment="Strong candidate with some gaps",
        )
        assert summary.total_gaps == 10
        assert summary.high_priority_count == 3


class TestPrioritizedActionPlan:
    """Test PrioritizedActionPlan model."""

    def test_valid_action_plan(self):
        """Test creating a valid action plan."""
        plan = PrioritizedActionPlan(
            phase_1_immediate=DevelopmentPhase(
                timeframe="0-2 weeks",
                focus="Quick wins",
                actions=[
                    PhaseAction(
                        action="Update resume",
                        gap_ids=["resume_1"],
                        estimated_time="2 hours",
                    )
                ],
            ),
            phase_2_short_term=DevelopmentPhase(
                timeframe="2-6 weeks",
                focus="Core skills",
                actions=[],
            ),
            phase_3_medium_term=DevelopmentPhase(
                timeframe="6+ weeks",
                focus="Advanced topics",
                actions=[],
            ),
        )
        assert plan.phase_1_immediate.timeframe == "0-2 weeks"
        assert len(plan.phase_1_immediate.actions) == 1


class TestGapAnalysisResult:
    """Test GapAnalysisResult model."""

    def test_valid_result(self):
        """Test creating a valid gap analysis result."""
        result = GapAnalysisResult(
            summary=GapAnalysisSummary(
                total_gaps=5,
                high_priority_count=2,
                medium_priority_count=2,
                low_priority_count=1,
                estimated_preparation_time="4 weeks",
                overall_assessment="Good candidate",
            ),
            technical_gaps=[],
            experience_gaps=[],
            company_fit_gaps=[],
            resume_optimization_gaps=[],
            quick_wins=[],
            long_term_development=[],
        )
        assert result.summary.total_gaps == 5
        assert len(result.technical_gaps) == 0

    def test_result_with_gaps(self):
        """Test result with actual gaps."""
        result = GapAnalysisResult(
            summary=GapAnalysisSummary(
                total_gaps=2,
                high_priority_count=1,
                medium_priority_count=1,
                low_priority_count=0,
                estimated_preparation_time="3 weeks",
                overall_assessment="Needs improvement",
            ),
            technical_gaps=[
                TechnicalGap(
                    gap_id="tech_1",
                    category="tools",
                    title="Docker",
                    description="Missing containerization skills",
                    priority="high",
                    priority_reasoning="Essential for role",
                    current_level="none",
                    target_level="intermediate",
                    impact_on_application="High impact",
                    recommendations=[],
                )
            ],
            experience_gaps=[
                ExperienceGap(
                    gap_id="exp_1",
                    category="project_experience",
                    title="Open source",
                    description="No open source contributions",
                    priority="medium",
                    priority_reasoning="Demonstrates collaboration",
                    impact_on_application="Moderate impact",
                    recommendations=[],
                )
            ],
        )
        assert len(result.technical_gaps) == 1
        assert len(result.experience_gaps) == 1
        assert result.technical_gaps[0].priority == "high"
