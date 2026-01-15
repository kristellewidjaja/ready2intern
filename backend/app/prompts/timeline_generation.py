"""
Prompt templates for timeline generation.
"""


SYSTEM_PROMPT = """You are an expert career coach and project planner specializing in helping students prepare for tech internships.

Your task is to create a realistic, actionable development timeline that helps candidates address their gaps and improve their candidacy before their target deadline.

Focus on:
1. **Realism** - Consider the candidate's current level and time constraints
2. **Prioritization** - Focus on high-impact activities that improve candidacy
3. **Balance** - Mix quick wins with longer-term skill development
4. **Motivation** - Create achievable milestones to maintain momentum
5. **Flexibility** - Build in buffer time and alternatives for setbacks

Remember: This is for internship preparation, not a multi-year career plan. Be ambitious but realistic."""


TIMELINE_GENERATION_PROMPT = """Based on the gap analysis, create a personalized development timeline to prepare for the target role.

## GAP ANALYSIS SUMMARY

**Total Gaps:** {total_gaps}
- High Priority: {high_priority_count}
- Medium Priority: {medium_priority_count}
- Low Priority: {low_priority_count}

**Estimated Preparation Time:** {estimated_preparation_time}

**Overall Assessment:** {overall_assessment}

### Technical Gaps ({technical_gaps_count})
{technical_gaps_summary}

### Experience Gaps ({experience_gaps_count})
{experience_gaps_summary}

### Company Fit Gaps ({company_fit_gaps_count})
{company_fit_gaps_summary}

### Resume Optimization Gaps ({resume_gaps_count})
{resume_gaps_summary}

---

## TIMELINE CONSTRAINTS

**Target Deadline:** {target_deadline}
**Weeks Available:** {weeks_available}
**Recommended Hours/Week:** {hours_per_week}

---

## JOB ROLE DESCRIPTION

{role_description}

---

Please create a comprehensive development timeline in the following JSON format:

{{{{
  "metadata": {{{{
    "total_weeks": {weeks_available},
    "total_hours": 0,
    "hours_per_week": {hours_per_week},
    "start_date": "{start_date}",
    "target_deadline": "{target_deadline}",
    "intensity_level": "light|moderate|intensive",
    "feasibility_assessment": "Assessment of whether timeline is realistic given constraints"
  }}}},
  "phases": [
    {{{{
      "phase_id": "phase_1",
      "phase_number": 1,
      "title": "Phase title",
      "description": "What this phase accomplishes",
      "start_week": 1,
      "end_week": 2,
      "focus_areas": ["Focus area 1", "Focus area 2"],
      "tasks": [
        {{{{
          "task_id": "task_1",
          "title": "Task title",
          "description": "What to do and why",
          "gap_ids": ["gap_id_1", "gap_id_2"],
          "estimated_hours": 10,
          "priority": "high|medium|low",
          "dependencies": [],
          "resources": ["Resource 1", "Resource 2"],
          "success_criteria": "How to know task is complete"
        }}}}
      ],
      "milestones": [
        {{{{
          "milestone_id": "milestone_1",
          "title": "Milestone title",
          "description": "What this milestone represents",
          "target_date": "YYYY-MM-DD",
          "completion_criteria": ["Criterion 1", "Criterion 2"],
          "deliverables": ["Deliverable 1", "Deliverable 2"]
        }}}}
      ],
      "estimated_hours_per_week": 10,
      "success_metrics": ["Metric 1", "Metric 2"]
    }}}}
  ],
  "weekly_breakdown": [
    {{{{
      "week_number": 1,
      "start_date": "YYYY-MM-DD",
      "end_date": "YYYY-MM-DD",
      "phase": "Phase 1: Foundation",
      "focus": "What to focus on this week",
      "tasks": ["Task title 1", "Task title 2"],
      "estimated_hours": 10,
      "key_deliverable": "Main thing to complete this week"
    }}}}
  ],
  "critical_path": ["task_1", "task_3", "task_5"],
  "flexibility_notes": [
    "What can be adjusted if timeline is too aggressive",
    "Alternative approaches if certain tasks take longer"
  ],
  "motivation_tips": [
    "Tip 1 to stay motivated",
    "Tip 2 to maintain momentum",
    "Tip 3 for when feeling overwhelmed"
  ]
}}}}

## GUIDELINES

### Phase Structure
Organize the timeline into 3-4 logical phases:
- **Phase 1 (Weeks 1-2)**: Quick wins and foundation
  - Resume optimization (immediate impact)
  - High-priority technical gaps (if quick to address)
  - Setup and environment preparation
  
- **Phase 2 (Weeks 3-6)**: Core skill development
  - Medium/high priority technical skills
  - Start building portfolio projects
  - Practice coding problems
  
- **Phase 3 (Weeks 7-10)**: Experience building
  - Complete portfolio projects
  - Contribute to open source (if applicable)
  - Build domain knowledge
  
- **Phase 4 (Weeks 11+)**: Polish and preparation
  - Company fit demonstrations
  - Interview preparation
  - Final resume polish
  - Application materials

### Task Design
- Each task should be **specific and actionable**
- Include **realistic time estimates** (don't underestimate)
- Reference **gap_ids** from the gap analysis
- Specify **dependencies** between tasks
- Provide **success criteria** for completion
- List **resources** needed (courses, tutorials, etc.)

### Weekly Breakdown
- Provide a **week-by-week plan** for the entire timeline
- Keep weekly hours **realistic** (10-15 hours for students with classes)
- Identify the **key deliverable** for each week
- Balance **different types of activities** (learning, building, practicing)

### Timeline Realism
- **If timeline is too short**: Focus on highest-priority gaps only
- **If timeline is adequate**: Cover high and medium priority gaps
- **If timeline is generous**: Include low priority gaps and stretch goals
- Always include **buffer time** for unexpected challenges
- Build in **review and iteration** time for projects

### Critical Path
- Identify tasks that **must be completed** to be competitive
- These are typically:
  - High-priority technical skills for the role
  - At least one substantial portfolio project
  - Resume ATS optimization
  - Key company fit demonstrations

### Flexibility Notes
- Suggest what can be **cut or shortened** if time is tight
- Provide **alternative approaches** for difficult tasks
- Identify **optional enhancements** vs required work

### Motivation Tips
- Provide **3-5 practical tips** for staying on track
- Address common challenges (procrastination, overwhelm, burnout)
- Suggest ways to **celebrate progress** and maintain momentum

## IMPORTANT NOTES
1. **CRITICAL**: Return ONLY valid JSON, no additional text or markdown formatting
2. **CRITICAL**: Ensure all strings are properly escaped and terminated
3. **CRITICAL**: Ensure all JSON arrays and objects are properly closed
4. All task_ids, milestone_ids, and phase_ids must be unique
5. Gap_ids must reference actual gaps from the gap analysis
6. Weekly breakdown should cover all weeks from start to deadline
7. Total hours should sum up realistically across all tasks
8. Hours per week should be realistic for a student (typically 10-15 hours)
9. Phase dates should be sequential and not overlap
10. Success criteria should be measurable and specific
11. Dependencies should only reference task_ids that exist
12. Critical path should include 5-10 most important tasks
13. If deadline is very soon (< 4 weeks), focus only on highest-impact activities
14. If deadline is far (> 12 weeks), include more comprehensive skill development
"""


def create_timeline_prompt(
    gap_analysis: dict,
    role_description: str,
    target_deadline: str,
    start_date: str,
    weeks_available: int,
    hours_per_week: int = 12,
) -> str:
    """
    Create a prompt for timeline generation.
    
    Args:
        gap_analysis: Gap analysis results
        role_description: Job role description
        target_deadline: Target deadline (ISO date string)
        start_date: Start date (ISO date string)
        weeks_available: Number of weeks available
        hours_per_week: Recommended hours per week
        
    Returns:
        Formatted prompt string
    """
    # Extract summary data
    summary = gap_analysis.get("summary", {})
    total_gaps = summary.get("total_gaps", 0)
    high_priority_count = summary.get("high_priority_count", 0)
    medium_priority_count = summary.get("medium_priority_count", 0)
    low_priority_count = summary.get("low_priority_count", 0)
    estimated_preparation_time = summary.get("estimated_preparation_time", "Unknown")
    overall_assessment = summary.get("overall_assessment", "No assessment available")
    
    # Extract technical gaps summary
    technical_gaps = gap_analysis.get("technical_gaps", [])
    technical_gaps_count = len(technical_gaps)
    technical_gaps_summary = "\n".join([
        f"- [{gap.get('priority', 'medium').upper()}] {gap.get('title', 'Untitled')}: {gap.get('description', 'No description')}"
        for gap in technical_gaps[:5]  # Limit to top 5
    ]) or "None identified"
    
    # Extract experience gaps summary
    experience_gaps = gap_analysis.get("experience_gaps", [])
    experience_gaps_count = len(experience_gaps)
    experience_gaps_summary = "\n".join([
        f"- [{gap.get('priority', 'medium').upper()}] {gap.get('title', 'Untitled')}: {gap.get('description', 'No description')}"
        for gap in experience_gaps[:5]
    ]) or "None identified"
    
    # Extract company fit gaps summary
    company_fit_gaps = gap_analysis.get("company_fit_gaps", [])
    company_fit_gaps_count = len(company_fit_gaps)
    company_fit_gaps_summary = "\n".join([
        f"- [{gap.get('priority', 'medium').upper()}] {gap.get('title', 'Untitled')}: {gap.get('description', 'No description')}"
        for gap in company_fit_gaps[:5]
    ]) or "None identified"
    
    # Extract resume optimization gaps summary
    resume_gaps = gap_analysis.get("resume_optimization_gaps", [])
    resume_gaps_count = len(resume_gaps)
    resume_gaps_summary = "\n".join([
        f"- [{gap.get('priority', 'medium').upper()}] {gap.get('title', 'Untitled')}: {gap.get('description', 'No description')}"
        for gap in resume_gaps[:5]
    ]) or "None identified"
    
    return TIMELINE_GENERATION_PROMPT.format(
        total_gaps=total_gaps,
        high_priority_count=high_priority_count,
        medium_priority_count=medium_priority_count,
        low_priority_count=low_priority_count,
        estimated_preparation_time=estimated_preparation_time,
        overall_assessment=overall_assessment,
        technical_gaps_count=technical_gaps_count,
        technical_gaps_summary=technical_gaps_summary,
        experience_gaps_count=experience_gaps_count,
        experience_gaps_summary=experience_gaps_summary,
        company_fit_gaps_count=company_fit_gaps_count,
        company_fit_gaps_summary=company_fit_gaps_summary,
        resume_gaps_count=resume_gaps_count,
        resume_gaps_summary=resume_gaps_summary,
        target_deadline=target_deadline,
        weeks_available=weeks_available,
        hours_per_week=hours_per_week,
        role_description=role_description,
        start_date=start_date,
    )
