"""
Prompt templates for role matching and scoring.
"""


SYSTEM_PROMPT = """You are an expert technical recruiter and ATS (Applicant Tracking System) specialist with deep knowledge of tech industry hiring practices.

Your task is to analyze how well a candidate's resume matches a specific job role and company culture. You will evaluate three key dimensions:

1. **ATS Score**: How well the resume would perform in automated screening systems
2. **Role Match Score**: How well the candidate's skills and experience align with the role requirements
3. **Company Fit Score**: How well the candidate aligns with the company's values and culture

Be objective, thorough, and provide specific evidence for your scores."""


ROLE_MATCHING_PROMPT = """Analyze the following candidate's resume against the job role and company values.

## CANDIDATE RESUME SUMMARY

{resume_summary}

## JOB ROLE DESCRIPTION

{role_description}

## COMPANY VALUES & CULTURE

{company_tenets}

---

Please provide a comprehensive matching analysis in the following JSON format:

{{{{
  "ats_score": {{{{
    "score": 0-100,
    "explanation": "Detailed explanation of ATS score",
    "strengths": [
      "Strength 1 with specific evidence",
      "Strength 2 with specific evidence"
    ],
    "weaknesses": [
      "Weakness 1 with specific evidence",
      "Weakness 2 with specific evidence"
    ],
    "keyword_matches": {{{{
      "matched_keywords": ["keyword1", "keyword2", "..."],
      "missing_keywords": ["keyword1", "keyword2", "..."]
    }}}},
    "formatting_score": 0-100,
    "formatting_notes": "Comments on resume structure, clarity, and ATS-friendliness"
  }}}},
  "role_match_score": {{{{
    "score": 0-100,
    "explanation": "Detailed explanation of role match",
    "technical_skills_match": {{{{
      "score": 0-100,
      "matched_skills": ["skill1", "skill2", "..."],
      "missing_skills": ["skill1", "skill2", "..."],
      "notes": "Analysis of technical skills alignment"
    }}}},
    "experience_match": {{{{
      "score": 0-100,
      "relevant_experience": ["experience1", "experience2", "..."],
      "experience_gaps": ["gap1", "gap2", "..."],
      "notes": "Analysis of experience level and relevance"
    }}}},
    "project_relevance": {{{{
      "score": 0-100,
      "relevant_projects": ["project1", "project2", "..."],
      "notes": "How projects demonstrate required skills"
    }}}},
    "education_match": {{{{
      "score": 0-100,
      "notes": "How education aligns with role requirements"
    }}}}
  }}}},
  "company_fit_score": {{{{
    "score": 0-100,
    "explanation": "Detailed explanation of company fit",
    "value_alignments": [
      {{{{
        "company_value": "Value name from company tenets",
        "evidence": "Specific evidence from resume showing alignment",
        "strength": "strong|moderate|weak"
      }}}}
    ],
    "cultural_indicators": [
      "Indicator 1 from resume showing cultural fit",
      "Indicator 2 from resume showing cultural fit"
    ],
    "potential_concerns": [
      "Concern 1 if any",
      "Concern 2 if any"
    ]
  }}}},
  "overall_score": {{{{
    "score": 0-100,
    "calculation": "Weighted average: ATS (20%) + Role Match (50%) + Company Fit (30%)",
    "recommendation": "strong_match|good_match|moderate_match|weak_match|poor_match",
    "summary": "2-3 sentence overall assessment",
    "key_strengths": [
      "Top strength 1",
      "Top strength 2",
      "Top strength 3"
    ],
    "key_concerns": [
      "Top concern 1",
      "Top concern 2"
    ],
    "next_steps": "Recommendation for hiring decision (e.g., 'Proceed to interview', 'Request additional information', 'Not a fit')"
  }}}}
}}}}

## SCORING GUIDELINES

### ATS Score (0-100)
- **90-100**: Excellent keyword optimization, perfect formatting, highly likely to pass ATS
- **75-89**: Good keyword coverage, minor formatting issues
- **60-74**: Adequate keywords, some formatting concerns
- **40-59**: Missing key keywords, formatting issues
- **0-39**: Poor keyword match, significant ATS barriers

### Role Match Score (0-100)
- **90-100**: Exceptional match, exceeds requirements
- **75-89**: Strong match, meets all key requirements
- **60-74**: Good match, meets most requirements
- **40-59**: Moderate match, missing some key requirements
- **0-39**: Weak match, significant gaps

### Company Fit Score (0-100)
- **90-100**: Exceptional cultural alignment, strong value match
- **75-89**: Strong cultural fit, clear value alignment
- **60-74**: Good fit, demonstrates some values
- **40-59**: Moderate fit, limited evidence of alignment
- **0-39**: Weak fit, concerns about cultural match

### Overall Score Calculation
- ATS Score: 20% weight
- Role Match Score: 50% weight (most important)
- Company Fit Score: 30% weight

### Recommendation Levels
- **strong_match** (85-100): Highly recommend for interview
- **good_match** (70-84): Recommend for interview
- **moderate_match** (55-69): Consider for interview, may need additional screening
- **weak_match** (40-54): Likely not a fit, but review manually
- **poor_match** (0-39): Not recommended

## IMPORTANT NOTES

1. Be specific and cite evidence from the resume
2. Consider the internship level - don't expect senior-level experience
3. Look for potential and learning ability, not just current skills
4. Consider projects and coursework as valid experience for interns
5. Evaluate cultural fit based on demonstrated behaviors and values, not assumptions
6. **CRITICAL**: Return ONLY valid JSON, no additional text or markdown formatting
7. **CRITICAL**: Ensure all strings are properly escaped and terminated with closing quotes
8. **CRITICAL**: Ensure all JSON arrays and objects are properly closed with ] and }}
9. All scores must be integers between 0 and 100
10. Provide constructive, actionable feedback
11. Keep explanations concise to ensure complete JSON response
"""


def create_role_matching_prompt(
    resume_summary: dict,
    role_description: str,
    company_tenets: str,
) -> str:
    """
    Create a prompt for role matching analysis.
    
    Args:
        resume_summary: Parsed resume data from resume analysis
        role_description: Job role description
        company_tenets: Company values and culture description
        
    Returns:
        Formatted prompt string
    """
    # Format resume summary into readable text
    resume_text = _format_resume_summary(resume_summary)
    
    return ROLE_MATCHING_PROMPT.format(
        resume_summary=resume_text,
        role_description=role_description,
        company_tenets=company_tenets,
    )


def _format_resume_summary(resume_data: dict) -> str:
    """
    Format resume data into a readable summary for the prompt.
    
    Args:
        resume_data: Parsed resume data dictionary
        
    Returns:
        Formatted resume summary string
    """
    sections = []
    
    # Personal Info
    if "personal_info" in resume_data:
        info = resume_data["personal_info"]
        sections.append(f"**Candidate:** {info.get('name', 'N/A')}")
        if info.get('email') != 'Not provided':
            sections.append(f"**Email:** {info.get('email')}")
    
    # Summary
    if "summary" in resume_data:
        sections.append(f"\n**Summary:**\n{resume_data['summary']}")
    
    # Education
    if "education" in resume_data and resume_data["education"]:
        sections.append("\n**Education:**")
        for edu in resume_data["education"]:
            sections.append(f"- {edu.get('degree', 'N/A')} from {edu.get('institution', 'N/A')}")
            if edu.get('gpa') != 'Not provided':
                sections.append(f"  GPA: {edu.get('gpa')}")
            if edu.get('relevant_coursework'):
                sections.append(f"  Coursework: {', '.join(edu['relevant_coursework'][:5])}")
    
    # Skills
    if "skills" in resume_data:
        skills = resume_data["skills"]
        sections.append("\n**Skills:**")
        if skills.get("programming_languages"):
            sections.append(f"- Programming: {', '.join(skills['programming_languages'])}")
        if skills.get("frameworks_libraries"):
            sections.append(f"- Frameworks: {', '.join(skills['frameworks_libraries'])}")
        if skills.get("tools_technologies"):
            sections.append(f"- Tools: {', '.join(skills['tools_technologies'])}")
        if skills.get("databases"):
            sections.append(f"- Databases: {', '.join(skills['databases'])}")
    
    # Experience
    if "experience" in resume_data and resume_data["experience"]:
        sections.append("\n**Experience:**")
        for exp in resume_data["experience"]:
            sections.append(f"- {exp.get('title', 'N/A')} at {exp.get('company', 'N/A')} ({exp.get('duration', 'N/A')})")
            if exp.get('achievements'):
                for achievement in exp['achievements'][:3]:
                    sections.append(f"  • {achievement}")
    
    # Projects
    if "projects" in resume_data and resume_data["projects"]:
        sections.append("\n**Projects:**")
        for proj in resume_data["projects"]:
            sections.append(f"- {proj.get('name', 'N/A')}")
            sections.append(f"  {proj.get('description', 'N/A')}")
            if proj.get('technologies'):
                sections.append(f"  Technologies: {', '.join(proj['technologies'])}")
    
    # Certifications
    if "certifications" in resume_data and resume_data["certifications"]:
        sections.append("\n**Certifications:**")
        for cert in resume_data["certifications"]:
            sections.append(f"- {cert.get('name', 'N/A')} from {cert.get('issuer', 'N/A')}")
    
    # Awards
    if "awards_honors" in resume_data and resume_data["awards_honors"]:
        sections.append("\n**Awards & Honors:**")
        for award in resume_data["awards_honors"]:
            sections.append(f"- {award.get('name', 'N/A')}")
    
    return "\n".join(sections)
