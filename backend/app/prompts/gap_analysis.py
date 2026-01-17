"""
Prompt templates for gap analysis and recommendations.
"""


SYSTEM_PROMPT = """You are an expert career coach and technical mentor specializing in helping students and early-career professionals prepare for tech internships.

Your task is to identify skill and experience gaps between a candidate's current profile and their target role, then provide actionable, specific recommendations to address these gaps.

Focus on:
1. **Realistic improvements** - What can be achieved in weeks/months, not years
2. **Prioritization** - What will have the biggest impact on their candidacy
3. **Specificity** - Concrete resources, projects, and action items
4. **Encouragement** - Frame gaps as growth opportunities, not deficiencies

CRITICAL: Keep your response concise. Identify 3-5 HIGH PRIORITY gaps per category maximum. Quality over quantity.

Be honest but supportive. Remember this is for internship-level roles, not senior positions."""


GAP_ANALYSIS_PROMPT = """Based on the role matching analysis, identify skill and experience gaps and provide actionable recommendations.

## ROLE MATCHING ANALYSIS

### ATS Score: {ats_score}/100
**Matched Keywords:** {matched_keywords}
**Missing Keywords:** {missing_keywords}

### Role Match Score: {role_match_score}/100
**Matched Skills:** {matched_skills}
**Missing Skills:** {missing_skills}
**Experience Gaps:** {experience_gaps}

### Company Fit Score: {company_fit_score}/100
**Value Alignments:** {value_alignments}
**Potential Concerns:** {potential_concerns}

### Overall Score: {overall_score}/100
**Recommendation:** {recommendation}
**Key Concerns:** {key_concerns}

---

## JOB ROLE DESCRIPTION

{role_description}

---

## COMPANY VALUES

{company_tenets}

---

Please provide a comprehensive gap analysis in the following JSON format:

{{{{
  "summary": {{{{
    "total_gaps": 0,
    "high_priority_count": 0,
    "medium_priority_count": 0,
    "low_priority_count": 0,
    "estimated_preparation_time": "X weeks/months",
    "overall_assessment": "2-3 sentence summary of candidate's readiness and main areas for improvement"
  }}}},
  "technical_gaps": [
    {{{{
      "gap_id": "tech_1",
      "category": "technical_skills|tools|frameworks|languages",
      "title": "Short descriptive title",
      "description": "What is missing and why it matters for this role",
      "priority": "high|medium|low",
      "priority_reasoning": "Why this priority level",
      "current_level": "none|beginner|intermediate",
      "target_level": "beginner|intermediate|advanced",
      "impact_on_application": "How this gap affects candidacy (1-2 sentences)",
      "recommendations": [
        {{{{
          "action": "Specific action to take",
          "resources": [
            {{{{
              "type": "course|tutorial|documentation|project|book|certification",
              "name": "Resource name",
              "url": "URL if applicable (or 'Search online')",
              "estimated_time": "X hours/days/weeks",
              "notes": "Why this resource is recommended"
            }}}}
          ],
          "success_criteria": "How to know you've addressed this gap",
          "estimated_time": "X hours/days/weeks"
        }}}}
      ]
    }}}}
  ],
  "experience_gaps": [
    {{{{
      "gap_id": "exp_1",
      "category": "work_experience|project_experience|domain_knowledge",
      "title": "Short descriptive title",
      "description": "What experience is missing and why it matters",
      "priority": "high|medium|low",
      "priority_reasoning": "Why this priority level",
      "impact_on_application": "How this gap affects candidacy",
      "recommendations": [
        {{{{
          "action": "Specific action to take",
          "project_ideas": [
            {{{{
              "name": "Project name",
              "description": "What to build and why",
              "key_features": ["Feature 1", "Feature 2", "Feature 3"],
              "technologies": ["Tech 1", "Tech 2"],
              "estimated_time": "X hours/days/weeks",
              "difficulty": "beginner|intermediate|advanced",
              "portfolio_value": "Why this project strengthens the resume"
            }}}}
          ],
          "success_criteria": "How to know you've addressed this gap",
          "estimated_time": "X hours/days/weeks"
        }}}}
      ]
    }}}}
  ],
  "company_fit_gaps": [
    {{{{
      "gap_id": "fit_1",
      "category": "leadership|values|culture|communication",
      "title": "Short descriptive title",
      "description": "What aspect of company fit needs strengthening",
      "priority": "high|medium|low",
      "priority_reasoning": "Why this priority level",
      "company_value": "Which company value this relates to",
      "impact_on_application": "How this gap affects candidacy",
      "recommendations": [
        {{{{
          "action": "Specific action to take",
          "examples": [
            "Concrete example 1 of how to demonstrate this value",
            "Concrete example 2 of how to demonstrate this value"
          ],
          "resume_improvements": [
            "How to better showcase this on resume",
            "What to add or emphasize"
          ],
          "success_criteria": "How to know you've addressed this gap",
          "estimated_time": "X hours/days/weeks"
        }}}}
      ]
    }}}}
  ],
  "resume_optimization_gaps": [
    {{{{
      "gap_id": "resume_1",
      "category": "keywords|formatting|content|storytelling",
      "title": "Short descriptive title",
      "description": "What needs improvement on the resume",
      "priority": "high|medium|low",
      "priority_reasoning": "Why this priority level",
      "impact_on_application": "How this affects ATS and recruiter screening",
      "recommendations": [
        {{{{
          "action": "Specific change to make",
          "before_example": "Example of current state (if applicable)",
          "after_example": "Example of improved state",
          "success_criteria": "How to verify improvement",
          "estimated_time": "X hours"
        }}}}
      ]
    }}}}
  ],
  "quick_wins": [
    {{{{
      "title": "Quick win title",
      "description": "What to do",
      "impact": "Why this is high-impact",
      "estimated_time": "X hours/days",
      "steps": [
        "Step 1",
        "Step 2",
        "Step 3"
      ]
    }}}}
  ],
  "long_term_development": [
    {{{{
      "title": "Long-term goal title",
      "description": "What to work towards",
      "rationale": "Why this matters for career growth",
      "estimated_time": "X months",
      "milestones": [
        {{{{
          "milestone": "Milestone description",
          "estimated_time": "X weeks/months",
          "success_criteria": "How to measure completion"
        }}}}
      ]
    }}}}
  ],
  "prioritized_action_plan": {{{{
    "phase_1_immediate": {{{{
      "timeframe": "0-2 weeks",
      "focus": "What to focus on in this phase",
      "actions": [
        {{{{
          "action": "Specific action",
          "gap_ids": ["gap_id_1", "gap_id_2"],
          "estimated_time": "X hours/days"
        }}}}
      ]
    }}}},
    "phase_2_short_term": {{{{
      "timeframe": "2-6 weeks",
      "focus": "What to focus on in this phase",
      "actions": [
        {{{{
          "action": "Specific action",
          "gap_ids": ["gap_id_1", "gap_id_2"],
          "estimated_time": "X hours/days"
        }}}}
      ]
    }}}},
    "phase_3_medium_term": {{{{
      "timeframe": "6+ weeks",
      "focus": "What to focus on in this phase",
      "actions": [
        {{{{
          "action": "Specific action",
          "gap_ids": ["gap_id_1", "gap_id_2"],
          "estimated_time": "X hours/days"
        }}}}
      ]
    }}}}
  }}}}
}}}}

## CRITICAL REQUIREMENTS

1. **LIMIT GAPS**: Identify maximum 3-5 gaps PER CATEGORY (technical, experience, company fit, resume)
2. **LIMIT RECOMMENDATIONS**: Maximum 2 recommendations per gap
3. **LIMIT RESOURCES**: Maximum 3 resources per recommendation
4. **LIMIT PROJECT IDEAS**: Maximum 2 project ideas per experience gap
5. **LIMIT QUICK WINS**: Maximum 3 quick wins total
6. **LIMIT LONG-TERM GOALS**: Maximum 2 long-term goals total
7. **BE CONCISE**: Keep descriptions to 1-2 sentences, not paragraphs

FOCUS ON QUALITY OVER QUANTITY. Better to have 3 excellent, actionable gaps than 10 vague ones.

## GUIDELINES

### Priority Levels
- **HIGH**: Critical gaps that significantly impact candidacy. Missing these makes the application weak.
- **MEDIUM**: Important gaps that would strengthen the application. Having these improves chances.
- **LOW**: Nice-to-have improvements. These are differentiators but not dealbreakers.

### Gap Categories
- **Technical Skills**: Programming languages, frameworks, tools, technologies
- **Experience**: Work experience, project experience, domain knowledge
- **Company Fit**: Leadership principles, values, cultural alignment
- **Resume**: ATS optimization, formatting, content, storytelling

### Recommendation Quality
- Be **specific**: Name actual courses, projects, resources
- Be **realistic**: Focus on what can be done in weeks/months
- Be **actionable**: Provide clear steps, not vague advice
- Be **encouraging**: Frame as growth opportunities

### Important Notes
1. **CRITICAL**: Return ONLY valid JSON, no additional text or markdown formatting
2. **CRITICAL**: Ensure all strings are properly escaped and terminated
3. **CRITICAL**: Ensure all JSON arrays and objects are properly closed
4. All gap_ids must be unique
5. All estimated times should be realistic for an internship candidate
6. Provide 3-5 gaps per category (technical, experience, company fit, resume)
7. Include 2-3 quick wins that can be done immediately
8. Include 1-2 long-term development goals
9. Prioritized action plan should reference gap_ids from the gaps
10. Focus on internship-level expectations, not senior engineer standards
"""


def create_gap_analysis_prompt(
    match_analysis: dict,
    role_description: str,
    company_tenets: str,
) -> str:
    """
    Create a prompt for gap analysis.
    
    Args:
        match_analysis: Role matching analysis results
        role_description: Job role description
        company_tenets: Company values and culture description
        
    Returns:
        Formatted prompt string
    """
    # Extract data from match analysis
    ats_score_data = match_analysis.get("ats_score", {})
    role_match_data = match_analysis.get("role_match_score", {})
    company_fit_data = match_analysis.get("company_fit_score", {})
    overall_data = match_analysis.get("overall_score", {})
    
    # Extract specific fields
    ats_score = ats_score_data.get("score", 0)
    role_match_score = role_match_data.get("score", 0)
    company_fit_score = company_fit_data.get("score", 0)
    overall_score = overall_data.get("score", 0)
    
    # Extract keyword matches
    keyword_data = ats_score_data.get("keyword_matches", {})
    matched_keywords = ", ".join(keyword_data.get("matched_keywords", [])[:15])
    missing_keywords = ", ".join(keyword_data.get("missing_keywords", [])[:15])
    
    # Extract technical skills
    tech_skills = role_match_data.get("technical_skills_match", {})
    matched_skills = ", ".join(tech_skills.get("matched_skills", [])[:10])
    missing_skills = ", ".join(tech_skills.get("missing_skills", [])[:10])
    
    # Extract experience gaps
    experience_data = role_match_data.get("experience_match", {})
    experience_gaps = ", ".join(experience_data.get("experience_gaps", [])[:5])
    
    # Extract value alignments
    value_alignments = []
    for alignment in company_fit_data.get("value_alignments", [])[:3]:
        value_alignments.append(
            f"{alignment.get('company_value', 'N/A')} ({alignment.get('strength', 'N/A')})"
        )
    value_alignments_str = ", ".join(value_alignments) if value_alignments else "None identified"
    
    # Extract concerns
    potential_concerns = ", ".join(company_fit_data.get("potential_concerns", [])[:3])
    key_concerns = ", ".join(overall_data.get("key_concerns", [])[:3])
    
    # Get recommendation
    recommendation = overall_data.get("recommendation", "unknown")
    
    return GAP_ANALYSIS_PROMPT.format(
        ats_score=ats_score,
        matched_keywords=matched_keywords or "None",
        missing_keywords=missing_keywords or "None",
        role_match_score=role_match_score,
        matched_skills=matched_skills or "None",
        missing_skills=missing_skills or "None",
        experience_gaps=experience_gaps or "None",
        company_fit_score=company_fit_score,
        value_alignments=value_alignments_str,
        potential_concerns=potential_concerns or "None",
        overall_score=overall_score,
        recommendation=recommendation,
        key_concerns=key_concerns or "None",
        role_description=role_description,
        company_tenets=company_tenets,
    )
