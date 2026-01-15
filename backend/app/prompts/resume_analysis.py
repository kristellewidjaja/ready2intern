"""
Prompt templates for resume analysis.
"""


SYSTEM_PROMPT = """You are an expert technical recruiter and resume analyst specializing in tech internships at top companies like Amazon, Meta, and Google.

Your task is to analyze resumes and extract structured information that will be used to evaluate candidates for technical internship positions.

You should:
- Extract factual information accurately
- Identify technical skills, programming languages, frameworks, and tools
- Summarize work experience and projects with focus on technical achievements
- Note educational background and relevant coursework
- Be objective and thorough in your analysis"""


RESUME_ANALYSIS_PROMPT = """Analyze the following resume and extract structured information.

RESUME TEXT:
{resume_text}

Please provide a comprehensive analysis in the following JSON format:

{{
  "personal_info": {{
    "name": "Full name if available, otherwise 'Not provided'",
    "email": "Email if available, otherwise 'Not provided'",
    "phone": "Phone if available, otherwise 'Not provided'",
    "location": "Location if available, otherwise 'Not provided'",
    "linkedin": "LinkedIn URL if available, otherwise 'Not provided'",
    "github": "GitHub URL if available, otherwise 'Not provided'",
    "portfolio": "Portfolio URL if available, otherwise 'Not provided'"
  }},
  "education": [
    {{
      "institution": "University/College name",
      "degree": "Degree type and major",
      "graduation_date": "Expected or actual graduation date",
      "gpa": "GPA if mentioned, otherwise 'Not provided'",
      "relevant_coursework": ["Course 1", "Course 2", "..."]
    }}
  ],
  "skills": {{
    "programming_languages": ["Python", "Java", "JavaScript", "..."],
    "frameworks_libraries": ["React", "Django", "TensorFlow", "..."],
    "tools_technologies": ["Git", "Docker", "AWS", "..."],
    "databases": ["PostgreSQL", "MongoDB", "..."],
    "soft_skills": ["Leadership", "Communication", "..."]
  }},
  "experience": [
    {{
      "title": "Job title or role",
      "company": "Company name",
      "duration": "Time period (e.g., 'Jun 2023 - Aug 2023')",
      "location": "Location if provided",
      "description": "Brief description of role and responsibilities",
      "achievements": ["Achievement 1", "Achievement 2", "..."],
      "technologies_used": ["Tech 1", "Tech 2", "..."]
    }}
  ],
  "projects": [
    {{
      "name": "Project name",
      "description": "Brief description of the project",
      "technologies": ["Tech 1", "Tech 2", "..."],
      "highlights": ["Key achievement or feature 1", "Key achievement or feature 2", "..."],
      "link": "Project URL if available, otherwise 'Not provided'"
    }}
  ],
  "certifications": [
    {{
      "name": "Certification name",
      "issuer": "Issuing organization",
      "date": "Date obtained if provided"
    }}
  ],
  "awards_honors": [
    {{
      "name": "Award or honor name",
      "issuer": "Issuing organization",
      "date": "Date received if provided",
      "description": "Brief description if available"
    }}
  ],
  "summary": "A 2-3 sentence summary of the candidate's background, key strengths, and experience level"
}}

IMPORTANT:
- Return ONLY valid JSON, no additional text or markdown formatting
- If a section is not present in the resume, use an empty array [] or "Not provided"
- Extract all technical skills mentioned, even if they appear in project descriptions
- For experience and projects, focus on quantifiable achievements and technical details
- Be thorough but concise in descriptions"""


def create_resume_analysis_prompt(resume_text: str) -> str:
    """
    Create a prompt for resume analysis.
    
    Args:
        resume_text: Extracted text from resume
        
    Returns:
        Formatted prompt string
    """
    return RESUME_ANALYSIS_PROMPT.format(resume_text=resume_text)
