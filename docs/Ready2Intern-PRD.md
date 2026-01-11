# Product Requirements Document: Ready2Intern

**Version:** 1.0  
**Date:** January 10, 2026  
**Status:** Draft - POC Phase

---

## 1. Executive Summary

Ready2Intern is an AI-powered internship readiness platform designed to help college students pursuing tech internships at top-tier companies (Amazon, Meta, Google). The platform leverages a custom multi-agent architecture powered by Anthropic's Claude API to provide comprehensive resume evaluation, gap analysis, and personalized career guidance.

The system analyzes student resumes against specific internship role requirements and company-specific evaluation criteria (e.g., Amazon Leadership Principles), providing actionable feedback tailored to each target company. Unlike generic resume reviewers, Ready2Intern understands the unique requirements and cultural values of top tech companies, helping students align their profiles with what recruiters are looking for.

This PRD covers the initial Proof of Concept (POC) phase, focusing on local deployment with UI and backend API running locally using direct Anthropic API integration (no AWS/Bedrock). Company-specific core tenets are stored locally as documents, and Python dependencies are managed with uv for fast, reliable package management. Cloud deployment, infrastructure as code, and production scaling considerations are explicitly out of scope for this phase.

---

## 2. Problem Statement

### What problem are we solving?

College students applying for competitive tech internships face several critical challenges:

1. **Lack of targeted feedback**: Generic resume advice doesn't address company-specific requirements
2. **Unknown evaluation criteria**: Students don't understand how companies like Amazon evaluate candidates against leadership principles
3. **Gap identification**: Difficulty identifying specific weaknesses in their profiles relative to role requirements
4. **Timeline planning**: Unclear on what improvements to prioritize given application deadlines
5. **Information overload**: Too many generic resources, not enough actionable, personalized guidance

### Why is it important?

- Top tech internships are highly competitive (acceptance rates < 5%)
- Early career opportunities significantly impact long-term career trajectories
- Students invest significant time applying without understanding why they're rejected
- Company-specific preparation can dramatically increase success rates
- Current solutions are either too generic or prohibitively expensive ($500+ for career coaching)

### Current alternatives and their limitations

| Alternative | Limitations |
|------------|-------------|
| University career centers | Generic advice, not company-specific, limited availability |
| Resume review services | Expensive ($100-500), not AI-powered, slow turnaround |
| Peer feedback | Inconsistent quality, lacks professional insight |
| ChatGPT/Claude direct use | No structured evaluation, no company-specific knowledge, requires prompt engineering |
| LinkedIn Premium | Generic suggestions, not internship-focused |

---

## 3. Goals & Objectives

### Clear, measurable goals

**Primary Goals:**
1. Deliver actionable resume feedback in < 2 minutes per evaluation
2. Achieve 85%+ student satisfaction with feedback quality (measured via survey)
3. Identify 5-10 specific improvement areas per resume with prioritization
4. Generate company-specific evaluation reports for Amazon, Meta, and Google
5. Successfully process 100% of standard resume formats (PDF, DOCX)

**Secondary Goals:**
1. Create personalized development timelines aligned with application deadlines
2. Demonstrate multi-agent architecture viability for career guidance use cases
3. Validate AgentCore primitives for production-ready agent systems
4. Build reusable framework for adding new companies/roles

### Success criteria

- **Technical:** System processes resumes end-to-end without manual intervention
- **Quality:** Feedback is specific, actionable, and company-aligned (validated by career counselors)
- **Performance:** < 30 second response time for resume analysis
- **Usability:** Students can complete evaluation flow without external help
- **Accuracy:** 90%+ accuracy in extracting resume information (GPA, coursework, projects)

### What we're NOT trying to achieve (out of scope)

❌ **Database implementation** - Postponed to MVP (filesystem only for POC)  
❌ **Cloud deployment** and production infrastructure  
❌ **Infrastructure as code** (Terraform, CloudFormation)  
❌ **User authentication** and multi-user support  
❌ **Data persistence** across sessions (in-memory only)  
❌ **Payment processing** or monetization  
❌ **Mobile applications** (iOS/Android)  
❌ **Integration with ATS** (Applicant Tracking Systems)  
❌ **Role application tracking** or management  
❌ **Interview preparation** or coding practice  
❌ **Resume writing/editing tools**  
❌ **Networking or mentorship** features  

**POC Focus:** Single-user, filesystem-based storage, LLM evaluation and document generation only.  

---

## 4. Target Users

### Primary user personas

**Persona 1: Sarah - The Ambitious Freshman**
- **Profile:** CS Freshman at state university, 3.7 GPA
- **Goals:** Land first internship at a top tech company
- **Pain points:** Limited experience, doesn't know what companies look for
- **Needs:** Clear guidance on what to build/learn, timeline for skill development

**Persona 2: Marcus - The Experienced Junior**
- **Profile:** CS Junior at target school, 3.5 GPA, 1 previous internship
- **Goals:** Upgrade to FAANG internship
- **Pain points:** Rejected from Amazon/Google, doesn't know why
- **Needs:** Gap analysis against top company standards, specific improvement areas

**Persona 3: Priya - The Career Switcher**
- **Profile:** Senior in related major (EE, Math), self-taught programming
- **Goals:** Break into software engineering internships
- **Pain points:** Non-traditional background, unsure how to position herself
- **Needs:** Guidance on highlighting transferable skills, company-specific positioning

### User characteristics and needs

**Demographics:**
- Age: 18-22 years old
- Education: Currently enrolled in 4-year university
- Major: Computer Science, Software Engineering, or related technical fields
- Experience level: 0-2 previous internships

**Technical proficiency:**
- Comfortable with web applications
- Familiar with PDF/document uploads
- Basic understanding of tech industry

**Key needs:**
1. Fast, actionable feedback (students are time-constrained)
2. Clear prioritization (what to fix first)
3. Company-specific insights (not generic advice)
4. Timeline-based planning (aligned with recruiting cycles)
5. Confidence building (understanding their competitive position)

### User segments

| Segment | Characteristics | Priority |
|---------|----------------|----------|
| Target school students | Top CS programs, high GPA | High - early adopters |
| Non-target school students | State universities, need more guidance | High - largest market |
| International students | Additional visa/sponsorship concerns | Medium - future phase |
| Bootcamp graduates | Career switchers, non-traditional | Low - POC phase |

---

## 5. User Stories

### Key user scenarios

**Core Flow:**
```
As a college student,
I want to upload my resume and select target companies,
So that I can receive specific feedback on my readiness for those internships.
```

**Detailed User Stories:**

1. **Resume Upload & Analysis**
   - As a student, I want to upload my resume in PDF format, so that the system can analyze my qualifications
   - As a student, I want to see my resume information extracted correctly (GPA, projects, skills), so that I can verify the system understood my profile

2. **Company Selection**
   - As a student, I want to select which companies I'm targeting (Amazon/Meta/Google), so that I receive company-specific feedback
   - As a student, I want to understand what each company values, so that I can make informed choices

3. **Resume Evaluation**
   - As a student, I want to see how my resume aligns with Amazon Leadership Principles, so that I can understand my fit
   - As a student, I want to receive a gap analysis showing what I'm missing, so that I know what to improve
   - As a student, I want feedback prioritized by impact, so that I focus on high-value improvements

4. **Action Planning**
   - As a student, I want a timeline-based development plan, so that I know when to complete improvements before application deadlines
   - As a student, I want specific project suggestions, so that I can build relevant experience

5. **Report Generation**
   - As a student, I want to download my evaluation report, so that I can reference it later
   - As a student, I want to see my progress over time, so that I can track improvements

### User journey/workflow

```
1. Landing Page
   ↓
2. Upload Resume (PDF/DOCX)
   ↓
3. Resume Parsing & Verification
   ↓
4. Select Target Companies (Amazon/Meta/Google)
   ↓
5. Select Target Roles (SDE Intern, AWS, etc.)
   ↓
6. AI Analysis (30-60 seconds)
   ↓
7. Results Dashboard
   - Overall readiness score
   - Company-specific evaluations
   - Gap analysis
   - Prioritized recommendations
   ↓
8. Development Plan
   - Timeline view
   - Milestone tracking
   - Resource suggestions
   ↓
9. Download Report (PDF)
```

### Edge cases to consider

1. **Resume parsing failures**
   - Non-standard resume formats
   - Heavily designed resumes with graphics
   - Multi-page resumes with inconsistent formatting
   - Missing key information (no GPA, no dates)

2. **Ambiguous information**
   - Unclear project descriptions
   - Generic skill listings
   - Conflicting information (e.g., graduation date vs. year)

3. **Extreme profiles**
   - No experience (complete beginners)
   - Overqualified (PhD students, multiple internships)
   - Non-traditional backgrounds (bootcamps, self-taught)

4. **System limitations**
   - Very large files (>10MB)
   - Concurrent requests (POC single-user)
   - Network timeouts during analysis

---

## 6. Functional Requirements

### Core features (must-have)

**FR-1: Resume Upload & Processing**
- FR-1.1: Accept PDF and DOCX resume uploads (max 5MB)
- FR-1.2: Generate unique session ID (UUID)
- FR-1.3: Save uploaded file to `./uploads/{session_id}/resume.{ext}`
- FR-1.4: Extract key information using LLM: name, GPA, graduation date, coursework, projects, skills, experience
- FR-1.5: Display extracted information for user verification
- FR-1.6: Allow manual correction of extracted data (stored in-memory)

**FR-2: Company & Role Selection**
- FR-2.1: Display list of supported companies (Amazon, Meta, Google)
- FR-2.2: Display company-specific roles (e.g., Amazon: SDE Intern, AWS)
- FR-2.3: Allow selection of multiple companies for comparison
- FR-2.4: Show company evaluation criteria overview

**FR-3: Multi-Agent Resume Analysis**
- FR-3.1: Orchestrator Agent coordinates analysis workflow
- FR-3.2: Document Agent processes resume and extracts structured data
- FR-3.3: Internship Analyzer Agent evaluates against company criteria
- FR-3.4: Student Planner Agent generates development timeline
- FR-3.5: Company-specific sub-agents apply specialized evaluation logic
- FR-3.6: All agents use Anthropic Claude API with structured prompts

**FR-4: Company-Specific Evaluation**
- FR-4.1: Amazon: Evaluate against 16 Leadership Principles
- FR-4.2: Meta: Evaluate against company values and technical bar
- FR-4.3: Google: Evaluate against Googleyness and technical skills
- FR-4.4: Generate company-specific readiness scores (0-100)
- FR-4.5: Identify alignment strengths and gaps per company

**FR-5: Gap Analysis & Recommendations (LLM-Generated)**
- FR-5.1: LLM identifies missing qualifications vs. role requirements
- FR-5.2: LLM prioritizes gaps by impact (high/medium/low)
- FR-5.3: LLM generates 5-10 specific, actionable recommendations
- FR-5.4: LLM suggests relevant projects, coursework, or experiences
- FR-5.5: LLM explains reasoning behind each recommendation
- FR-5.6: Save recommendations to `./results/{session_id}/recommendations.json`

**FR-6: Development Timeline (LLM-Generated)**
- FR-6.1: LLM generates timeline based on application deadlines
- FR-6.2: LLM breaks down improvements into phases (immediate, short-term, long-term)
- FR-6.3: LLM suggests milestone dates for each improvement
- FR-6.4: LLM accounts for academic calendar (semesters, breaks)
- FR-6.5: Save timeline to `./results/{session_id}/timeline.json`

**FR-7: Results Dashboard**
- FR-7.1: Load evaluation data from `./results/{session_id}/evaluation.json`
- FR-7.2: Display overall readiness score
- FR-7.3: Show company-specific evaluation results
- FR-7.4: Visualize gap analysis (charts/graphs)
- FR-7.5: Present prioritized recommendations list
- FR-7.6: Display development timeline
- FR-7.7: All data loaded from filesystem (no database queries)

**FR-8: Report Export**
- FR-8.1: Generate comprehensive markdown/PDF report using LLM
- FR-8.2: Include all evaluation results and recommendations
- FR-8.3: Format for readability and printing
- FR-8.4: Save to filesystem (`./results/{session_id}/report.pdf`)
- FR-8.5: Allow download via browser

### Secondary features (should-have)

**FR-9: Session Management (Simplified for POC)**
- FR-9.1: Generate unique session ID per upload
- FR-9.2: Store session data in-memory during analysis
- FR-9.3: Save final results to filesystem as JSON
- FR-9.4: No cross-session persistence (fresh start each time)

**FR-10: Company Tenets Storage**
- FR-10.1: Store company core tenets as local documents
- FR-10.2: Load tenets dynamically during evaluation
- FR-10.3: Support updates to tenet documents

**FR-11: Feedback Mechanism**
- FR-11.1: Allow users to rate feedback quality
- FR-11.2: Collect user comments on recommendations
- FR-11.3: Store feedback locally for analysis

### Future considerations (nice-to-have)

**FR-12: Progress Tracking**
- Track improvements over multiple resume versions
- Show before/after comparisons
- Celebrate milestone achievements

**FR-13: Resource Library**
- Curated project ideas by company
- Example resume bullet points
- Company-specific interview prep resources

**FR-14: Peer Comparison**
- Anonymous benchmarking against similar profiles
- Percentile rankings
- Competitive positioning insights

### Feature prioritization

**Phase 1 (POC - Week 1-4):**
- FR-1: Resume Upload & Processing
- FR-2: Company & Role Selection
- FR-3: Multi-Agent Resume Analysis
- FR-4: Company-Specific Evaluation

**Phase 2 (POC - Week 5-8):**
- FR-5: Gap Analysis & Recommendations
- FR-6: Development Timeline
- FR-7: Results Dashboard

**Phase 3 (POC - Week 9-12):**
- FR-8: Report Export (LLM-generated)
- FR-9: Session Management (filesystem-based)
- FR-10: Company Tenets Storage (markdown files)
- FR-11: Feedback Mechanism (optional)

**Deferred to MVP:**
- Database implementation
- User authentication
- Multi-user support
- Session persistence across restarts

---

## 7. Non-Functional Requirements

### Performance expectations

**NFR-1: Response Time**
- Resume upload and parsing: < 5 seconds
- Complete analysis workflow: < 60 seconds
- Dashboard rendering: < 2 seconds
- Report generation: < 10 seconds

**NFR-2: Throughput**
- POC phase: Support single concurrent user
- Handle resume files up to 5MB
- Process resumes with up to 10 pages

**NFR-3: Availability**
- Local development environment: 99% uptime during testing
- Graceful degradation if AI service unavailable
- Clear error messages for failures

### Security requirements

**NFR-4: Data Privacy**
- All resume data stored locally only
- No transmission of PII to external services (except Amazon Bedrock API)
- Clear data retention policy (delete after session)
- No logging of sensitive information

**NFR-5: API Security**
- Secure API key management for Amazon Bedrock
- Environment variable-based configuration
- No hardcoded credentials

**NFR-6: Input Validation**
- Validate file types and sizes
- Sanitize user inputs
- Prevent code injection attacks

### Scalability needs

**NFR-7: POC Scalability**
- Single-user deployment sufficient for POC
- Architecture designed for future multi-user scaling
- Modular agent design for easy replication
- Stateless API design where possible

**NFR-8: Extensibility**
- Easy addition of new companies (plug-in architecture)
- Simple updates to evaluation criteria
- Configurable agent behaviors

### Accessibility standards

**NFR-9: Web Accessibility**
- WCAG 2.1 Level AA compliance target
- Keyboard navigation support
- Screen reader compatibility
- Sufficient color contrast (4.5:1 minimum)
- Responsive design for different screen sizes

**NFR-10: Usability**
- Intuitive UI requiring no training
- Clear progress indicators during analysis
- Helpful error messages
- Mobile-responsive design (view-only for POC)

### Compliance requirements

**NFR-11: Educational Use**
- Comply with FERPA (if handling student records)
- Transparent AI usage disclosure
- Ethical AI practices (no bias in recommendations)

**NFR-12: Licensing**
- Proper licensing for all dependencies
- Compliance with Amazon Bedrock terms of service
- Anthropic Claude API usage guidelines

---

## 8. Technical Considerations

### Suggested architecture approach

**Overall Architecture: Custom Multi-Agent System with Anthropic API**

```
┌─────────────────────────────────────────────────────────┐
│                     Frontend (React)                     │
│  - Resume Upload UI                                      │
│  - Company Selection                                     │
│  - Results Dashboard                                     │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/REST
┌────────────────────▼────────────────────────────────────┐
│              Backend API (FastAPI)                       │
│  - REST endpoints                                        │
│  - Session management (in-memory)                       │
│  - File upload handling                                  │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│         Custom Multi-Agent Orchestration                 │
│                                                          │
│  ┌──────────────────────────────────────────────┐      │
│  │      Orchestrator Agent                      │      │
│  │  - Workflow coordination                     │      │
│  │  - Agent sequencing                          │      │
│  │  - State management                          │      │
│  └──────────┬───────────────────────────────────┘      │
│             │                                            │
│  ┌──────────▼───────────┐  ┌────────────────────┐     │
│  │   Document Agent     │  │ Internship Analyzer│     │
│  │  - Resume parsing    │  │ - Company evaluation│     │
│  │  - Data extraction   │  │ - Gap analysis      │     │
│  └──────────────────────┘  └─────────┬──────────┘     │
│                                       │                 │
│                            ┌──────────▼──────────┐     │
│                            │ Company Sub-Agents  │     │
│                            │ - Amazon Agent      │     │
│                            │ - Meta Agent        │     │
│                            │ - Google Agent      │     │
│                            └──────────┬──────────┘     │
│                                       │                 │
│  ┌────────────────────────────────────▼──────────┐    │
│  │         Student Planner Agent                  │    │
│  │  - Timeline generation                         │    │
│  │  - Recommendation prioritization               │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  Each agent uses structured prompts + Claude API        │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│          Anthropic Claude API (Direct)                  │
│  - Model: claude-sonnet-4-20250514                      │
│  - Messages API with structured prompts                 │
│  - Extended thinking for complex reasoning              │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│              Local Storage                               │
│  - Resume files (./uploads/)                            │
│  - Company tenets (./company_tenets/)                   │
│  - Session data (in-memory dict)                        │
│  - Results cache (./results/)                           │
└─────────────────────────────────────────────────────────┘
```

### Technology stack recommendations

**Backend Stack:**
- **Framework:** FastAPI (Python 3.11+)
  - Fast, modern, async support
  - Automatic API documentation
  - Type hints and validation
  
- **Package Management:** uv
  - Fast Python package installer and resolver
  - Drop-in replacement for pip/pip-tools
  - Lockfile support for reproducible builds
  - 10-100x faster than pip
  
- **Agent Framework:** Custom orchestration layer
  - Simple Python classes for each agent
  - Sequential agent execution with state passing
  - JSON-based agent communication
  - In-memory session management
  
- **LLM:** Anthropic Claude API (Direct)
  - Model: claude-sonnet-4-20250514
  - Messages API with extended thinking
  - Large context window (200K tokens)
  - Excellent for structured outputs
  
- **Document Processing:** 
  - pdfplumber for PDF parsing (more reliable)
  - python-docx for DOCX files
  - Custom text extraction and structuring

**Frontend Stack:**
- **Framework:** React 18+ with TypeScript
  - Component reusability
  - Type safety
  - Large ecosystem
  
- **Styling:** Tailwind CSS
  - Rapid UI development
  - Consistent design system
  - Responsive utilities
  
- **State Management:** React Context or Zustand
  - Simple for POC scope
  - Easy to upgrade to Redux if needed
  
- **HTTP Client:** Axios or Fetch API
  - API communication
  - File upload support

**Development Tools:**
- **Package Management:** uv (Python), npm/pnpm (Node.js)
- **Code Quality:** Ruff (linting + formatting), ESLint, Prettier
- **Testing:** pytest (backend), Vitest (frontend)
- **API Documentation:** FastAPI automatic Swagger/OpenAPI
- **Type Checking:** mypy (Python), TypeScript (frontend)

### Integration points

**External Integrations:**
1. **Anthropic Claude API**
   - Purpose: LLM inference for all agents
   - Authentication: API key (environment variable)
   - Endpoint: https://api.anthropic.com/v1/messages
   - Rate limits: Monitor token usage and requests/minute
   - Error handling: Retry logic with exponential backoff
   - Model: claude-sonnet-4-20250514

**Internal Integrations:**
1. **Frontend ↔ Backend API**
   - Protocol: REST over HTTP
   - Format: JSON
   - Authentication: None (POC single-user)
   - Endpoints: `/upload`, `/analyze`, `/results`, `/report`

2. **Backend ↔ Agent System**
   - Protocol: Python function calls
   - Format: Structured data models (Pydantic)
   - Communication: Synchronous for POC
   - State passing: Python dictionaries

3. **Agent ↔ LLM**
   - Protocol: Anthropic Messages API (REST)
   - Format: JSON with messages array
   - Authentication: Bearer token (API key)
   - Context: Prompt templates with company tenets
   - Features: Extended thinking, tool use (future)

### Data model considerations

**Core Data Models:**

```python
# Resume Data
class Resume:
    id: str
    filename: str
    upload_date: datetime
    student_info: StudentInfo
    education: List[Education]
    experience: List[Experience]
    projects: List[Project]
    skills: List[str]
    raw_text: str

class StudentInfo:
    name: str
    email: Optional[str]
    phone: Optional[str]
    linkedin: Optional[str]
    github: Optional[str]

class Education:
    institution: str
    degree: str
    major: str
    gpa: Optional[float]
    graduation_date: str
    relevant_coursework: List[str]

class Experience:
    company: str
    title: str
    start_date: str
    end_date: Optional[str]
    description: List[str]
    technologies: List[str]

class Project:
    name: str
    description: str
    technologies: List[str]
    url: Optional[str]
    highlights: List[str]

# Evaluation Data
class Evaluation:
    resume_id: str
    company: str
    role: str
    timestamp: datetime
    overall_score: float
    category_scores: Dict[str, float]
    strengths: List[str]
    gaps: List[Gap]
    recommendations: List[Recommendation]

class Gap:
    category: str
    description: str
    impact: str  # high, medium, low
    current_state: str
    desired_state: str

class Recommendation:
    priority: int
    category: str
    action: str
    rationale: str
    timeline: str
    resources: List[str]

# Development Plan
class DevelopmentPlan:
    resume_id: str
    target_deadline: date
    phases: List[Phase]
    milestones: List[Milestone]

class Phase:
    name: str
    duration_weeks: int
    goals: List[str]
    actions: List[str]

class Milestone:
    date: date
    title: str
    deliverables: List[str]
```

**Data Storage (POC - Filesystem Only):**
- **Resume files:** Local filesystem (`./uploads/{session_id}/resume.pdf`)
- **Company tenets:** Local markdown documents (`./company_tenets/{company_name}.md`)
- **Session data:** In-memory Python dictionary (no persistence needed for POC)
- **Evaluation results:** Local JSON files (`./results/{session_id}/evaluation.json`)
- **Generated reports:** Local PDF files (`./results/{session_id}/report.pdf`)

**No Database for POC** - All data stored as files. Database implementation postponed to MVP phase.

### Infrastructure needs

**POC Infrastructure (Local Development):**

**Development Environment:**
- OS: macOS, Linux, or Windows with WSL
- Python: 3.11 or higher
- Node.js: 20.x or higher
- uv: Latest version (install via: `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- RAM: 8GB minimum, 16GB recommended
- Storage: 5GB free space

**Required Services:**
- Anthropic API key (get from: https://console.anthropic.com/)
- Internet connection for API calls

**Local Setup:**
```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Backend
cd backend
uv venv                           # Create virtual environment
source .venv/bin/activate         # Activate (Linux/Mac)
# or: .venv\Scripts\activate      # Activate (Windows)
uv pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

**Environment Configuration:**
```bash
# .env file
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
ANTHROPIC_MODEL=claude-sonnet-4-20250514
MAX_FILE_SIZE_MB=5
UPLOAD_DIR=./uploads
COMPANY_TENETS_DIR=./company_tenets
RESULTS_DIR=./results
LOG_LEVEL=INFO
```

**Future Infrastructure (MVP/Production - Out of Scope for POC):**
- **Database:** PostgreSQL for structured data (user profiles, evaluations, history)
- **Cloud Storage:** S3 or similar for resume files
- **Caching:** Redis for API responses and session data
- **Hosting:** Cloud platform (Vercel for frontend, Railway/Render for backend)
- **Authentication:** Auth0, Clerk, or similar
- **CDN:** CloudFront or similar for frontend assets

**POC Simplification:** No database, no cloud storage, no authentication - just filesystem and in-memory storage.

---

## 9. User Interface/Experience

### Key UI/UX principles

1. **Simplicity First**
   - Minimize steps to get results
   - Clear, linear workflow
   - No unnecessary features or distractions

2. **Transparency**
   - Show AI processing status
   - Explain evaluation reasoning
   - Make criteria visible upfront

3. **Actionability**
   - Every insight should have a clear next step
   - Prioritize recommendations
   - Provide specific examples

4. **Encouragement**
   - Positive, constructive tone
   - Celebrate strengths
   - Frame gaps as opportunities

5. **Speed**
   - Fast page loads
   - Immediate feedback
   - No unnecessary waiting

### Design requirements

**Visual Design:**
- Clean, modern interface
- Professional but approachable aesthetic
- Consistent color scheme (primary: blue, secondary: green for positive, orange for gaps)
- Clear typography hierarchy
- Ample white space

**Component Requirements:**

1. **Upload Component**
   - Drag-and-drop file upload
   - File type/size validation feedback
   - Upload progress indicator
   - Preview of uploaded file name

2. **Company Selection**
   - Card-based layout for companies
   - Visual company logos
   - Brief description of evaluation criteria
   - Multi-select capability

3. **Loading State**
   - Animated progress indicator
   - Status messages ("Analyzing resume...", "Evaluating against Amazon criteria...")
   - Estimated time remaining
   - Engaging visuals (not just spinners)

4. **Results Dashboard**
   - Score visualization (circular progress, gauges)
   - Color-coded sections (green=strong, yellow=moderate, red=needs work)
   - Expandable sections for details
   - Clear visual hierarchy

5. **Recommendations List**
   - Priority badges (High/Medium/Low)
   - Expandable cards for details
   - Action buttons ("Learn More", "Add to Plan")
   - Progress tracking checkboxes

6. **Timeline View**
   - Visual timeline with phases
   - Milestone markers
   - Current date indicator
   - Drag-to-adjust capability (future)

### Platform considerations

**Primary Platform: Web (Desktop)**
- Target browsers: Chrome, Firefox, Safari, Edge (latest 2 versions)
- Screen resolutions: 1280x720 minimum, optimized for 1920x1080
- No browser plugins required

**Secondary Platform: Web (Mobile)**
- Responsive design for tablets and phones
- View-only experience (no file upload on mobile for POC)
- Touch-friendly interactions
- Simplified layout for smaller screens

**Not Supported (POC):**
- Native mobile apps (iOS/Android)
- Desktop applications
- Browser extensions

### Accessibility requirements

**WCAG 2.1 Level AA Compliance:**
- Keyboard navigation for all interactive elements
- Focus indicators on all focusable elements
- Alt text for all images and icons
- Semantic HTML structure
- ARIA labels where needed
- Color contrast ratio 4.5:1 minimum for text
- No reliance on color alone for information
- Resizable text up to 200% without loss of functionality
- Skip navigation links
- Form labels and error messages

**Additional Considerations:**
- Screen reader testing (NVDA, JAWS, VoiceOver)
- Captions for any video content (future)
- Clear, simple language (avoid jargon)
- Consistent navigation patterns

---

## 10. Success Metrics

### KPIs to track

**User Engagement Metrics:**
1. **Completion Rate**: % of users who complete full evaluation workflow
   - Target: >80%
   - Measurement: (Users who view results) / (Users who upload resume)

2. **Time to Results**: Average time from upload to viewing results
   - Target: <60 seconds
   - Measurement: Timestamp(results viewed) - Timestamp(upload completed)

3. **Session Duration**: Average time spent on platform
   - Target: 10-15 minutes
   - Measurement: Total session time per user

4. **Report Downloads**: % of users who download PDF report
   - Target: >60%
   - Measurement: (Users who download) / (Users who view results)

**Quality Metrics:**
5. **User Satisfaction**: Self-reported satisfaction with feedback
   - Target: >4.0/5.0 average rating
   - Measurement: Post-evaluation survey

6. **Recommendation Usefulness**: % of recommendations rated as "useful"
   - Target: >75%
   - Measurement: User feedback on individual recommendations

7. **Accuracy**: % of resume information extracted correctly
   - Target: >90%
   - Measurement: User corrections / Total extracted fields

**Technical Metrics:**
8. **System Reliability**: % of successful evaluations (no errors)
   - Target: >95%
   - Measurement: Successful completions / Total attempts

9. **API Response Time**: Average API response time
   - Target: <2 seconds per endpoint
   - Measurement: Server-side logging

10. **Error Rate**: % of requests resulting in errors
    - Target: <5%
    - Measurement: Error logs / Total requests

### How we'll measure success

**Quantitative Measures:**
- Application logs and analytics
- User feedback surveys (5-point Likert scale)
- System performance monitoring
- A/B testing of recommendation formats (future)

**Qualitative Measures:**
- User interviews (5-10 students)
- Observation of user sessions
- Feedback from career counselors
- Comparison of recommendations vs. expert advice

**Success Criteria for POC:**
✅ **Technical Success:**
- System processes 20+ test resumes without failure
- All four agents communicate successfully
- Company-specific evaluations generate distinct outputs
- Reports export correctly

✅ **User Success:**
- 5 students complete full evaluation
- Average satisfaction >4.0/5.0
- Students can articulate 3+ specific improvements to make
- Feedback is perceived as more useful than generic resume reviews

✅ **Business Success:**
- Demonstrates viability of multi-agent approach
- Validates market need (positive user feedback)
- Identifies path to production deployment
- Generates interest from university career centers

### Analytics requirements

**Required Analytics:**
1. **Event Tracking:**
   - Resume uploaded
   - Company selected
   - Analysis started/completed
   - Results viewed
   - Report downloaded
   - Feedback submitted

2. **User Flow Analysis:**
   - Drop-off points in workflow
   - Time spent on each page
   - Navigation patterns

3. **Error Tracking:**
   - Error types and frequency
   - Failed uploads
   - API failures
   - Agent communication errors

**Analytics Implementation (POC):**
- Simple logging to local files
- JSON-formatted logs for easy parsing
- No external analytics services (Google Analytics, etc.)
- Privacy-focused (no PII in logs)

**Future Analytics (Production):**
- Google Analytics or Mixpanel
- Error monitoring (Sentry)
- Performance monitoring (New Relic, DataDog)
- User session recordings (Hotjar)

### Monitoring and reporting needs

**POC Monitoring:**
- Manual log review
- Weekly metrics summary
- User feedback compilation
- Bug tracking (GitHub Issues)

**Key Reports:**
1. **Weekly Status Report:**
   - Number of evaluations completed
   - Average satisfaction score
   - Top errors/issues
   - User feedback highlights

2. **Technical Performance Report:**
   - API response times
   - Agent success rates
   - Error frequency
   - System resource usage

3. **User Feedback Summary:**
   - Satisfaction ratings
   - Common themes in feedback
   - Feature requests
   - Pain points

---

## 11. Timeline & Milestones

### Suggested project phases

**Phase 1: Foundation (Weeks 1-4)**
- Set up development environment (uv, Python 3.11+, Node.js)
- Implement basic frontend structure (React + Vite)
- Build FastAPI backend skeleton
- Integrate Anthropic Claude API
- Implement resume upload and filesystem storage
- Create basic agent architecture (custom orchestration)

**Phase 2: Core Functionality (Weeks 5-8)**
- Develop multi-agent system (Orchestrator, Document, Analyzer, Planner)
- Implement company-specific evaluation logic
- Create company sub-agents (Amazon, Meta, Google)
- Build gap analysis functionality
- Develop recommendation engine
- Implement results dashboard

**Phase 3: Polish & Testing (Weeks 9-12)**
- Build development timeline generator
- Implement PDF report export
- Create session management
- Develop feedback mechanism
- Comprehensive testing (unit, integration, E2E)
- User testing with 5-10 students
- Bug fixes and refinements

### Key milestones

| Milestone | Target Date | Deliverables | Success Criteria |
|-----------|-------------|--------------|------------------|
| **M1: Dev Environment Ready** | Week 1 | - Repo setup<br>- uv installed<br>- Dependencies installed<br>- Anthropic API key configured | - Backend runs locally<br>- Frontend runs locally<br>- Can call Anthropic API |
| **M2: Resume Upload Working** | Week 2 | - File upload UI<br>- Resume parsing<br>- Data extraction | - Can upload PDF/DOCX<br>- Extracts GPA, projects, skills<br>- >80% extraction accuracy |
| **M3: Agent System Functional** | Week 4 | - All 4 agents implemented<br>- Agent communication working<br>- Basic orchestration | - Agents can pass data<br>- Orchestrator coordinates flow<br>- No blocking errors |
| **M4: Company Evaluation Live** | Week 6 | - Company selection UI<br>- Amazon/Meta/Google agents<br>- Evaluation logic | - Generates company-specific scores<br>- Different outputs per company<br>- Reasoning is clear |
| **M5: Recommendations Engine** | Week 8 | - Gap analysis<br>- Recommendation generation<br>- Prioritization logic | - Identifies 5-10 gaps<br>- Recommendations are specific<br>- Priorities make sense |
| **M6: Dashboard Complete** | Week 10 | - Results visualization<br>- Timeline view<br>- Report export | - All data displays correctly<br>- UI is intuitive<br>- PDF exports successfully |
| **M7: User Testing** | Week 11 | - 5-10 student evaluations<br>- Feedback collection<br>- Iteration | - >4.0/5.0 satisfaction<br>- <5% error rate<br>- Positive qualitative feedback |
| **M8: POC Complete** | Week 12 | - Final bug fixes<br>- Documentation<br>- Demo preparation | - System runs end-to-end<br>- Documentation complete<br>- Demo ready |

### Dependencies

**External Dependencies:**
- Anthropic API key (Week 1)
- Company tenets documentation (Week 3)
- Test resumes from students (Week 2)
- User testers availability (Week 11)

**Internal Dependencies:**
- Resume parsing must work before agent system (M2 → M3)
- Agent system must work before company evaluation (M3 → M4)
- Company evaluation must work before recommendations (M4 → M5)
- All core features must work before dashboard (M5 → M6)
- Dashboard must work before user testing (M6 → M7)

**Critical Path:**
```
M1 → M2 → M3 → M4 → M5 → M6 → M7 → M8
```

### Launch criteria

**POC Launch Criteria (Internal Demo):**
✅ All 8 milestones completed  
✅ System processes 20+ test resumes successfully  
✅ <5% error rate in user testing  
✅ >4.0/5.0 average satisfaction score  
✅ All three companies (Amazon/Meta/Google) working  
✅ Documentation complete (README, API docs, user guide)  
✅ Demo script prepared  
✅ Known bugs documented (not necessarily fixed)  

**Not Required for POC:**
❌ Production deployment  
❌ Multi-user support  
❌ Authentication system  
❌ Payment processing  
❌ Mobile apps  
❌ 99.9% uptime SLA  

---

## 12. Risks & Mitigation

### Technical risks

**Risk T-1: Anthropic API Reliability**
- **Probability:** Low
- **Impact:** High
- **Description:** API downtime or rate limiting could block all evaluations
- **Mitigation:**
  - Implement retry logic with exponential backoff (3 retries)
  - Monitor API status via status.anthropic.com
  - Respect rate limits (default: 50 requests/min)
  - Cache responses where appropriate
  - Have fallback error messages for users
  - Display clear error messages with retry options

**Risk T-2: Resume Parsing Accuracy**
- **Probability:** High
- **Impact:** Medium
- **Description:** Complex resume formats may not parse correctly
- **Mitigation:**
  - Test with diverse resume formats early
  - Implement manual correction UI
  - Use multiple parsing libraries as fallback
  - Provide clear formatting guidelines to users
  - Focus on common formats first (simple PDFs)

**Risk T-3: Agent Coordination Complexity**
- **Probability:** Low
- **Impact:** Medium
- **Description:** Custom multi-agent system may have coordination bugs
- **Mitigation:**
  - Use simple sequential agent execution (no parallelism in POC)
  - Add extensive logging for debugging
  - Build agents incrementally and test individually
  - Keep agent interfaces simple (input dict → output dict)
  - Have timeout mechanisms for each agent (60s max)
  - Test each agent in isolation before integration

**Risk T-4: Context Window Limitations**
- **Probability:** Low
- **Impact:** Medium
- **Description:** Long resumes + company tenets may exceed context limits
- **Mitigation:**
  - Monitor token usage per request
  - Implement context compression techniques
  - Summarize less critical information
  - Use Claude Sonnet's 200K context window efficiently
  - Split evaluations if needed

**Risk T-5: Performance Degradation**
- **Probability:** Medium
- **Impact:** Medium
- **Description:** Analysis may take longer than 60-second target
- **Mitigation:**
  - Optimize agent prompts for conciseness
  - Use parallel agent execution where possible
  - Cache company tenets in memory
  - Profile and optimize slow operations
  - Set realistic user expectations (show progress)

### Business risks

**Risk B-1: User Adoption**
- **Probability:** Medium
- **Impact:** High
- **Description:** Students may not trust AI-generated advice
- **Mitigation:**
  - Provide transparent explanations for recommendations
  - Show reasoning and examples
  - Get endorsements from career counselors
  - Offer comparison with human advisor feedback
  - Build credibility through accurate, helpful advice

**Risk B-2: Recommendation Quality**
- **Probability:** Medium
- **Impact:** High
- **Description:** AI may generate generic or incorrect advice
- **Mitigation:**
  - Validate recommendations with career experts
  - Use specific, detailed prompts for agents
  - Implement quality checks in recommendation engine
  - Collect user feedback on usefulness
  - Iterate based on feedback

**Risk B-3: Company Criteria Changes**
- **Probability:** Low
- **Impact:** Medium
- **Description:** Companies may change evaluation criteria (e.g., new leadership principles)
- **Mitigation:**
  - Design for easy updates to company tenets
  - Monitor company career pages for changes
  - Version company tenet documents
  - Make criteria updates part of regular maintenance

**Risk B-4: Competitive Landscape**
- **Probability:** Medium
- **Impact:** Medium
- **Description:** Similar products may launch during development
- **Mitigation:**
  - Focus on unique multi-agent approach
  - Emphasize company-specific evaluations
  - Build for extensibility (easy to add features)
  - Move quickly through POC phase

### Resource risks

**Risk R-1: API Costs**
- **Probability:** Low
- **Impact:** Low
- **Description:** Anthropic API costs may exceed budget
- **Mitigation:**
  - Monitor usage and costs weekly
  - Anthropic pricing: ~$3 per million input tokens, ~$15 per million output tokens
  - Estimated POC cost: $50-100 for 100 test evaluations
  - Optimize prompts to reduce tokens
  - Use Claude Sonnet (cost-effective) vs. Opus
  - Limit test evaluations during development
  - Cache company tenets to avoid re-sending

**Risk R-2: Development Timeline**
- **Probability:** Medium
- **Impact:** Medium
- **Description:** 12-week timeline may be optimistic
- **Mitigation:**
  - Prioritize ruthlessly (MVP features only)
  - Build in 1-week buffer
  - Use agile sprints with weekly reviews
  - Cut nice-to-have features if needed
  - Parallelize frontend/backend development

**Risk R-3: Skill Gaps**
- **Probability:** Low
- **Impact:** Low
- **Description:** Team may lack experience with multi-agent systems
- **Mitigation:**
  - Start with simple sequential agent flow
  - Use well-documented Anthropic API (excellent docs)
  - Leverage Claude's extended thinking for complex reasoning
  - Build simple proof-of-concept agents first
  - Abundant community resources and examples available

**Risk R-4: Test User Availability**
- **Probability:** Medium
- **Impact:** Low
- **Description:** May be difficult to recruit student testers
- **Mitigation:**
  - Recruit testers early (Week 8)
  - Offer incentives (free resume review, gift cards)
  - Partner with university career centers
  - Use personal networks
  - Have backup plan with synthetic testing

### Mitigation strategies summary

**Proactive Measures:**
1. Weekly risk review meetings
2. Continuous monitoring of API usage and costs
3. Early and frequent testing with real resumes
4. Regular check-ins with career counselors for validation
5. Maintain detailed documentation for troubleshooting

**Reactive Measures:**
1. Escalation path for technical blockers
2. Budget reserve for unexpected costs
3. Flexible timeline with defined cut points
4. Fallback to simpler features if needed
5. Clear communication with stakeholders on risks

**Risk Monitoring:**
- Track risks in project management tool
- Update probability/impact weekly
- Document new risks as they emerge
- Review mitigation effectiveness
- Adjust strategies based on learnings

---

## 13. Open Questions

### Items requiring further discussion

**Product Questions:**
1. Should we support resume templates/examples for students to improve their resumes before evaluation?
2. How do we handle students targeting companies not yet supported (e.g., Apple, Microsoft)?
3. Should we show comparative scores (e.g., "You're stronger for Amazon than Google")?
4. Do we need version control for resumes (track improvements over time)?
5. Should recommendations include specific courses, projects, or just general guidance?

**Technical Questions:**
6. What's the optimal prompt structure for each agent to minimize token usage?
7. Should we implement agent-to-agent communication or orchestrator-mediated only?
8. How do we handle very long resumes (>5 pages) that may exceed optimal processing?
9. Should we cache evaluation results, and if so, for how long?
10. What's the best way to structure company tenets documents for agent consumption?

**User Experience Questions:**
11. Should users see the AI "thinking" process or just final results?
12. How much detail should we show in gap analysis (high-level vs. granular)?
13. Should we gamify the experience (scores, badges, progress bars)?
14. Do users want to compare their profile against "typical" accepted interns?
15. Should we provide a "quick scan" mode vs. "deep analysis" mode?

### Decisions to be made

**Priority 1 (Decide by Week 2):**
- [ ] Exact resume parsing library to use (pdfplumber recommended)
- [ ] Agent communication pattern (sequential with state passing)
- [ ] Company tenets document format (Markdown recommended for readability)
- [x] Session storage approach (in-memory dict for POC, filesystem for results)
- [ ] Prompt engineering strategy for each agent

**Priority 2 (Decide by Week 4):**
- [ ] Recommendation prioritization algorithm (rule-based vs. LLM-scored)
- [ ] Timeline generation logic (fixed templates vs. dynamic)
- [ ] Error handling strategy (graceful degradation vs. fail-fast)
- [ ] Logging detail level (verbose for debugging vs. minimal)

**Priority 3 (Decide by Week 8):**
- [ ] Report format and design (template to use)
- [ ] User feedback mechanism (survey tool, custom form)
- [ ] Demo environment setup (local vs. cloud)
- [ ] Post-POC roadmap priorities

### Areas needing research

**Research Tasks:**

**RT-1: Company Evaluation Criteria**
- **Owner:** Product
- **Deadline:** Week 2
- **Tasks:**
  - Research Amazon Leadership Principles application to intern hiring
  - Investigate Meta's evaluation criteria for interns
  - Understand Google's Googleyness assessment
  - Interview recruiters if possible
  - Document findings in company tenets files

**RT-2: Resume Parsing Best Practices**
- **Owner:** Engineering
- **Deadline:** Week 1
- **Tasks:**
  - Benchmark parsing libraries (accuracy, speed)
  - Test with 20+ diverse resume formats
  - Identify common parsing failure modes
  - Document recommended resume formats
  - Create test suite of resumes

**RT-3: Multi-Agent Prompt Engineering**
- **Owner:** Engineering
- **Deadline:** Week 3
- **Tasks:**
  - Study Anthropic prompt engineering best practices
  - Experiment with agent prompt structures
  - Test sequential agent workflows
  - Optimize for token efficiency (use extended thinking wisely)
  - Document prompt templates for each agent
  - Test structured output formats (JSON)

**RT-4: Student Needs Validation**
- **Owner:** Product
- **Deadline:** Week 4
- **Tasks:**
  - Interview 5-10 students about resume pain points
  - Survey students on desired features
  - Understand current tools they use
  - Validate problem statement
  - Refine user personas

**RT-5: Competitive Analysis**
- **Owner:** Product
- **Deadline:** Week 3
- **Tasks:**
  - Analyze existing resume review tools
  - Identify gaps in current market
  - Understand pricing models
  - Assess differentiation opportunities
  - Document competitive landscape

---

## Appendices

### A. Glossary

- **uv:** Fast Python package installer and resolver (Rust-based)
- **Multi-Agent System:** Architecture where multiple AI agents collaborate to solve complex tasks
- **Extended Thinking:** Claude feature that allows model to "think" before responding
- **Leadership Principles:** Amazon's 16 core values used in hiring decisions
- **FAANG:** Facebook (Meta), Amazon, Apple, Netflix, Google - top tech companies
- **SDE:** Software Development Engineer (Amazon's term for software engineer)
- **STEP:** Student Training in Engineering Program (Google internship)
- **POC:** Proof of Concept - initial prototype to validate feasibility
- **Gap Analysis:** Identification of differences between current and desired state

### B. References

- Anthropic Claude API Documentation: https://docs.anthropic.com/
- Anthropic Console: https://console.anthropic.com/
- uv Documentation: https://github.com/astral-sh/uv
- FastAPI Documentation: https://fastapi.tiangolo.com/
- Amazon Leadership Principles: https://www.amazon.roles/principles
- WCAG 2.1 Guidelines: https://www.w3.org/WAI/WCAG21/quickref/
- pdfplumber Documentation: https://github.com/jsvine/pdfplumber

### C. Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-10 | Product Team | Initial PRD for POC phase |

---

**Document Status:** Draft - Awaiting Review  
**Next Review Date:** 2026-01-17  
**Approvers:** Product Lead, Engineering Lead, Stakeholders

---

*This PRD is a living document and will be updated as the project evolves. All stakeholders should review and provide feedback within 3 business days.*
