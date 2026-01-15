# AGENTS.md

## Project Overview

Ready2Intern is an AI-powered resume evaluator for tech internships using a multi-agent system with Anthropic Claude API.

**Architecture:** React frontend ←→ FastAPI backend ←→ Claude API → Filesystem storage (no database)

## Setup Commands

### Backend
```bash
cd backend
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev  # Runs on localhost:5173
```

### Environment Variables
Create `backend/.env`:
```
ANTHROPIC_API_KEY=your_key_here
CORS_ORIGINS=["http://localhost:5173"]

# Optional LLM Configuration
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022  # Default model
LLM_MAX_RETRIES=3                            # Max retry attempts
LLM_RETRY_DELAY=1                            # Base delay in seconds
```

## Code Style

### Backend (Python)
- Python 3.11+
- FastAPI with Pydantic models
- Type hints required
- Use `async/await` for I/O operations
- Follow PEP 8

### Frontend (TypeScript)
- React 18 + TypeScript strict mode
- Functional components with hooks
- Tailwind CSS for styling
- No inline styles

## Project Structure

```
ready2intern/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry
│   │   ├── api/routes/          # API endpoints
│   │   ├── agents/              # 5 LLM agents
│   │   ├── services/            # ClaudeClient, FileService
│   │   ├── models/              # Pydantic models
│   │   └── prompts/             # LLM prompt templates
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── pages/               # Page components
│   │   ├── services/api.ts      # API client
│   │   └── store/               # State management
│   └── package.json
└── data/
    ├── resumes/                 # Uploaded resumes
    ├── company-tenets/          # Company criteria files
    └── sessions/                # Analysis results (JSON)
```

## Testing Instructions

### Backend
```bash
cd backend
pytest tests/ -v
pytest tests/test_agents.py -v  # Test specific module
```

### Frontend
```bash
cd frontend
npm test
npm run test:coverage
```

### Integration Testing
1. Start backend on localhost:8000
2. Start frontend on localhost:5173
3. Verify health check: `curl http://localhost:8000/api/health`
4. Test file upload, analysis flow, results display

## Development Workflow

### Feature Implementation (Vertical Slices)
1. Read `Ready2Intern-TODO.md` for current week's tasks
2. Read `Ready2Intern-Implementation-Plan.md` for acceptance criteria
3. Implement backend → frontend → integration
4. Test end-to-end before moving to next feature
5. Update this file with implementation notes

### Multi-Agent System (Week 4-5)
Sequential execution:
1. **Document Agent** - Extract resume data from PDF/DOCX
2. **Evaluation Agent** - Score against company tenets + role description
3. **Recommendation Agent** - Generate improvement suggestions
4. **Planner Agent** - Create timeline with milestones
5. **Orchestrator** - Coordinate agents, save results

### File Operations
- Resumes saved as: `data/resumes/{session_id}_{timestamp}.{ext}`
- Results saved as: `data/sessions/{session_id}/*.json`
- Company tenets: `data/company-tenets/{company}-*.txt`

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/health` | GET | Health check |
| `/api/upload` | POST | Upload resume → session_id |
| `/api/companies` | GET | List available companies |
| `/api/analyze` | POST | Start analysis (session_id, company, role_description) |
| `/api/results/{session_id}` | GET | Get complete results |
| `/api/export/{session_id}` | POST | Generate PDF report |

## Common Issues

### CORS Errors
Verify `backend/.env` has: `CORS_ORIGINS=["http://localhost:5173"]`

### File Upload Issues
- Use `FormData` with `Content-Type: multipart/form-data`
- Max file size: 5MB
- Accepted formats: PDF, DOCX only

### LLM API Failures
- Implement retry logic (3 attempts, exponential backoff)
- Save partial results if agent fails
- Log errors for debugging

## Security Considerations

- Validate all file uploads (type, size, content)
- Sanitize user inputs before LLM calls
- Never expose API keys in frontend
- Session IDs are UUIDs (not sequential)
- Clean up old sessions after 24 hours

## Reference Documents

- `Ready2Intern-TODO.md` - Sequential task checklist
- `Ready2Intern-Implementation-Plan.md` - Feature slices with acceptance criteria
- `Ready2Intern-PRD.md` - Product requirements
- `Ready2Intern-API-Spec.md` - Detailed API specifications
- `BUILD-GUIDE.md` - Comprehensive setup guide

## Status Tracking

Track implementation status in this file using:
- ⏳ Not implemented
- 🚧 In progress
- ✅ Complete
- ❌ Blocked

### Current Status (Week 4)
- ✅ Backend setup (Python 3.13 + FastAPI + uv)
- ✅ Frontend setup (React 19 + TypeScript + Vite + Tailwind v4)
- ✅ Health check endpoint
- ✅ Theme toggle (light/dark mode)
- ✅ Resume upload (drag-and-drop, validation, session management)
- ✅ Company selection (logos, tenets, API endpoint)
- ✅ Role description input (textarea, validation, character counter)
- ✅ Analyze button (loading states, progress messages, API integration)
- ✅ LLM integration (Anthropic Claude API, resume parsing, structured extraction)
- ✅ Role matching (ATS, Role Match, Company Fit scores with weighted overall score)

## Implementation Notes

### Week 4 - LLM Role Matching (Completed Jan 15, 2026)

**Key Decisions:**
- Three-dimensional scoring system: ATS (20%), Role Match (50%), Company Fit (30%)
- Weighted average calculation for overall score with clear recommendation levels
- Structured JSON prompt with detailed scoring guidelines for consistency
- Resume summary formatting to provide context-rich input to LLM
- Score validation and clamping (0-100 range) with automatic recalculation
- Separate prompt template for role matching vs resume analysis

**Services Created:**
- RoleMatchingService: Orchestrates role matching analysis (`app/services/role_matching_service.py`)
- Role matching prompts: Structured templates with scoring criteria (`app/prompts/role_matching.py`)

**Reusable Patterns:**
- Multi-dimensional scoring with weighted averages
- Structured JSON prompts with clear evaluation criteria
- Score validation and normalization (clamping to valid ranges)
- Resume data formatting for LLM context
- Recommendation level mapping based on score thresholds
- Lazy service initialization pattern (continued from previous feature)

**Common Pitfalls:**
- Scores must be validated and clamped to 0-100 range
- Overall score should be recalculated even if LLM provides one
- Resume summary must include all relevant sections for accurate matching
- Company tenets must be loaded from file system before analysis
- LLM responses may not include all required fields - provide defaults
- Temperature should be low (0.3) for consistent scoring

**Testing Approach:**
- Backend: 99 total tests passing (82 original + 17 new)
- 17 role matching service tests (analysis, scoring, validation)
- Updated analyze endpoint tests to mock both services
- Score calculation tests with various ranges and edge cases
- Recommendation level tests for all score thresholds
- JSON parsing tests with markdown and invalid responses

**Scoring System:**
- **ATS Score (20% weight)**: Keyword matching, formatting, ATS-friendliness
- **Role Match Score (50% weight)**: Technical skills, experience, projects, education alignment
- **Company Fit Score (30% weight)**: Values alignment, cultural indicators
- **Overall Score**: Weighted average with 5 recommendation levels

**Recommendation Levels:**
- strong_match (85-100): Highly recommend for interview
- good_match (70-84): Recommend for interview
- moderate_match (55-69): Consider for interview
- weak_match (40-54): Likely not a fit
- poor_match (0-39): Not recommended

**File Structure:**
```
backend/app/
├── services/
│   └── role_matching_service.py    # Role matching orchestration
├── prompts/
│   └── role_matching.py             # Scoring prompts and templates
└── api/routes/
    └── analyze.py                   # Updated with two-phase analysis
```

**Data Flow:**
1. Resume analysis completes → results saved
2. RoleMatchingService loads resume analysis
3. Service loads company tenets from file system
4. Resume data formatted into readable summary
5. Combined with role description and company tenets
6. LLM analyzes match across three dimensions
7. Scores validated and overall score calculated
8. Results saved to `data/sessions/{session_id}/match_analysis.json`

**Performance:**
- Role matching time: 10-20 seconds (after resume analysis)
- Total analysis time: 20-50 seconds (resume + role matching)
- Token usage: ~3,500-4,000 tokens per complete analysis
- Cost: ~$0.03-0.04 per complete analysis (resume + matching)

### Week 4 - LLM Resume Analysis (Completed Jan 15, 2026)

**Key Decisions:**
- Lazy initialization of LLM service to avoid requiring API key at import time
- Comprehensive retry logic with exponential backoff for API failures
- Structured JSON prompt for consistent LLM responses
- Separate services for LLM client, resume parsing, and analysis orchestration
- Support for both PDF and DOCX resume formats
- Extensive error handling and logging throughout the pipeline

**Services Created:**
- LLMService: Anthropic Claude API client with retry logic (`app/services/llm_service.py`)
- ResumeParser: PDF/DOCX text extraction (`app/services/resume_parser.py`)
- ResumeAnalysisService: Orchestrates parsing + LLM analysis (`app/services/resume_analysis_service.py`)
- Prompt templates: Structured prompts for resume analysis (`app/prompts/resume_analysis.py`)

**Reusable Patterns:**
- Lazy service initialization: Avoid requiring env vars at module import time
- Retry with exponential backoff: Handle rate limits and transient failures gracefully
- Structured JSON prompts: Get consistent, parseable responses from LLM
- Service layer separation: LLM client, parser, and orchestrator as separate concerns
- Comprehensive error handling: Catch and log errors at each step
- File system persistence: Save analysis results as JSON for later retrieval
- Mock-friendly architecture: Services can be easily mocked for testing

**Common Pitfalls:**
- Don't initialize LLM service at module level (requires API key)
- LLM responses may include markdown code blocks - strip them before parsing
- PDF extraction can fail for image-based PDFs - handle gracefully
- API errors need proper exception types with required parameters
- Always validate LLM response structure and provide defaults for missing fields
- Use lower temperature (0.3) for structured extraction vs creative tasks

**Testing Approach:**
- Backend: 75 total tests passing (24 new tests for LLM features)
- Unit tests for LLM service (retry logic, error handling, API mocking)
- Unit tests for resume parser (PDF, DOCX, error cases)
- Unit tests for analysis service (orchestration, JSON parsing, file I/O)
- Integration tests for analyze endpoint (mocked LLM service)
- Manual E2E test script available (`test_e2e_manual.py`)

**LLM Integration Details:**
- Model: Claude 3.5 Sonnet (claude-3-5-sonnet-20241022) - configurable via `ANTHROPIC_MODEL`
- Max retries: 3 attempts with exponential backoff (1s, 2s, 4s) - configurable via `LLM_MAX_RETRIES`
- Retry delay: 1 second base delay - configurable via `LLM_RETRY_DELAY`
- Default max tokens: 4096
- Temperature: 0.3 for structured extraction (lower = more consistent)
- Handles: RateLimitError, APITimeoutError, APIError, generic exceptions
- Output: Structured JSON with personal info, education, skills, experience, projects, certifications, awards, summary

**Available Claude Models:**
- `claude-3-5-sonnet-20241022` (recommended, default) - Best balance of speed and quality
- `claude-3-5-haiku-20241022` - Faster and cheaper, good for simple resumes
- `claude-3-opus-20240229` - Highest quality, slower and more expensive

**File Structure:**
```
backend/app/
├── services/
│   ├── llm_service.py              # Claude API client
│   ├── resume_parser.py            # PDF/DOCX extraction
│   └── resume_analysis_service.py  # Orchestration
├── prompts/
│   └── resume_analysis.py          # LLM prompt templates
└── api/routes/
    └── analyze.py                  # Updated with LLM integration
```

**Data Flow:**
1. User uploads resume → saved to `data/resumes/{session_id}_{timestamp}.{ext}`
2. User clicks analyze → POST /api/analyze
3. ResumeParser extracts text from PDF/DOCX
4. LLMService sends text to Claude with structured prompt
5. Response parsed into JSON with validation and defaults
6. Results saved to `data/sessions/{session_id}/resume_analysis.json`
7. Success response returned to frontend

### Week 3 - Analyze Button & Loading State (Completed Jan 14, 2026)

**Key Decisions:**
- Smart button state: shows what's missing vs generic "disabled"
- Progress messages during loading to keep users engaged
- Stub endpoint allows frontend development without blocking
- Session directory creation prepares for future LLM results
- Alert for now, will add results page navigation in future

**Components Created:**
- AnalyzeButton: Smart button with loading states and validation
- POST /api/analyze: Stub endpoint with full validation

**Reusable Patterns:**
- Conditional button enabling based on form validation
- Loading state with progress message updates
- Stub endpoints that validate inputs and prepare infrastructure
- Session directory structure for future data storage
- UUID-based ID generation for tracking

**Common Pitfalls:**
- Button should show what's missing, not just be disabled
- Progress messages keep users engaged during loading
- Need to validate resume file exists before analysis
- Session directory should be created even for stub endpoint
- Loading state should prevent multiple submissions

**Testing Approach:**
- Backend: 8 tests for analyze endpoint (validation, errors, success)
- Frontend: Placeholder tests for future implementation
- Manual testing: Verify button states, loading, API integration
- All 43 backend tests passing

### Week 3 - Role Description Input (Completed Jan 14, 2026)

**Key Decisions:**
- Real-time validation with visual feedback (color-coded borders)
- Character counter with contextual messages ("X more needed")
- Progressive disclosure: appears after company selection
- Backend validation models ready for future analyze endpoint
- Pydantic validators for robust input validation

**Components Created:**
- RoleDescriptionInput: Controlled textarea component with validation
- AnalysisRequest: Pydantic model with field validators

**Reusable Patterns:**
- Controlled component with external state management
- Real-time validation with dynamic styling
- Character counter with min/max limits
- Contextual error messages (too short vs too long)
- Success indicators for valid input
- Pydantic field validators for backend validation

**Common Pitfalls:**
- Need to trim whitespace before validation
- Character counter should update on every keystroke
- Error messages should be specific and actionable
- Border colors must have sufficient contrast in dark mode
- Placeholder text should include realistic example

**Testing Approach:**
- Backend: 11 tests for validation models (min/max length, company validation)
- Frontend: Placeholder tests for future implementation
- Manual testing: Verify real-time validation, character counter, visual feedback
- All 35 backend tests passing

### Week 2 - Company Selection (Completed Jan 13, 2026)

**Key Decisions:**
- Company tenets stored as plain text files (easy to edit, LLM-friendly)
- SVG logos for scalability and small file size
- Company data configured in service layer (not database)
- Progressive disclosure: company selector appears after resume upload
- Dynamic styling with company brand colors

**Services Created:**
- Company selection endpoint: `/api/companies` (GET)
- CompanyService: Company data management and tenets loading (`app/services/company_service.py`)
- Company models: Pydantic schemas for API responses (`app/models/company.py`)

**Reusable Patterns:**
- Service layer pattern: CompanyService encapsulates business logic
- Configuration as data: Company list in service, easy to extend
- Progressive disclosure: Show features as user progresses through flow
- Dynamic theming: Apply company colors programmatically
- Controlled components: CompanyLogoSelector accepts props for state management
- SVG graphics: Lightweight, scalable logos with brand colors

**Common Pitfalls:**
- Company tenets files must exist in `data/company-tenets/` directory
- Logo paths must match frontend public directory structure
- Company IDs must be lowercase and match across service/tenets/logos
- Conditional rendering: Check session state before showing company selector
- Color contrast: Ensure company colors meet accessibility standards

**Testing Approach:**
- Backend: 14 tests for companies endpoint and service
- Frontend: Placeholder tests with TESTING.md guide for future setup
- Manual testing: Verify UI interaction, API integration, responsive design
- End-to-end: Test full flow from resume upload → company selection

### Week 1 - Foundation (Completed Jan 13, 2026)

**Key Decisions:**
- Using Python 3.13 (3.14 not yet supported by PyO3/pydantic-core)
- Tailwind CSS v4 requires `@tailwindcss/postcss` plugin
- Theme state managed via React Context + localStorage

**Services Created:**
- Health check endpoint: `/api/health` (GET)
- FileService: File validation, storage, and session ID generation (`app/services/file_service.py`)
- Resume upload endpoint: `/api/upload` (POST)

**Reusable Patterns:**
- ThemeContext pattern for global state
- MainLayout wrapper for consistent page structure
- Environment variable configuration with `.env.example` files
- Service layer pattern: Business logic separated from route handlers
- FormData uploads with progress tracking via Axios
- Drag-and-drop file upload with click fallback
- Client + server-side validation for file uploads

**Common Pitfalls:**
- npm cache permissions: use `--cache /tmp/npm-cache` or fix with `sudo chown`
- Tailwind v4 syntax: use `@import "tailwindcss"` not `@tailwind` directives
- FastAPI on_event deprecated: consider lifespan handlers for future endpoints
- File upload requires `python-multipart` package for FastAPI
- MIME type validation: use file extension as fallback if python-magic unavailable
- File naming: Include timestamp to avoid collisions when same session uploads twice
