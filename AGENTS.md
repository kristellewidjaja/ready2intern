Ready2Intern
AI-powered resume evaluator for tech internships. Students upload a resume, pick a target company (Amazon/Meta/Google), paste a role description, and get scored with gap analysis and a development timeline.

Quick reference
Stack: Python 3.13 + FastAPI + Pydantic (backend), React 19 + TypeScript + Vite + Tailwind v4 (frontend), Anthropic Claude API (LLM). No database — filesystem storage under data/.

Project structure
backend/
  app/main.py            # FastAPI entry point
  app/api/routes/        # health, upload, companies, analyze, results
  app/services/          # llm_service, resume_parser, resume_analysis_service,
                         # role_matching_service, gap_analysis_service, timeline_service,
                         # company_service, file_service
  app/models/            # Pydantic models (analysis, company, gap_analysis, results, timeline, upload)
  app/prompts/           # LLM prompt templates (resume_analysis, role_matching, gap_analysis, timeline_generation)
  tests/                 # pytest unit tests
frontend/
  src/pages/             # Dashboard, ResultsPage
  src/components/        # UI components (FileDropzone, CompanyLogoSelector, OverallScoreCard, etc.)
  src/services/api.ts    # Axios API client
  src/types/             # TypeScript interfaces
  src/contexts/          # ThemeContext (light/dark)
data/
  resumes/               # Uploaded files: {session_id}_{timestamp}.{ext}
  company-tenets/        # Plain-text company criteria files
  sessions/              # Analysis results as JSON per session
docs/                    # PRD, TDD, API spec, build guide, implementation plan

Dev commands
# Backend
cd backend && uv venv && source .venv/bin/activate && uv pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend && npm install && npm run dev   # runs on localhost:5173

# Tests
cd backend && pytest tests/ -v
cd frontend && npm test

# Lint
cd frontend && npm run lint

Environment variables (backend/.env)
ANTHROPIC_API_KEY=...
CORS_ORIGINS=["http://localhost:5173"]
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022   # optional, default model
LLM_MAX_RETRIES=3                            # optional
LLM_RETRY_DELAY=1                            # optional, seconds

API endpoints
GET  /api/health                  # health check
POST /api/upload                  # upload resume (multipart, PDF/DOCX, 5MB max) -> session_id
GET  /api/companies               # list available companies
POST /api/analyze                 # start analysis (session_id, company, role_description)
GET  /api/results/{session_id}    # get complete results

Analysis pipeline (sequential)
1. ResumeParser extracts text from PDF/DOCX
2. ResumeAnalysisService sends to Claude for structured extraction
3. RoleMatchingService scores ATS (20%), Role Match (50%), Company Fit (30%)
4. GapAnalysisService identifies gaps across 4 categories (technical, experience, fit, resume)
5. TimelineService generates phased development plan
Results saved as JSON files under data/sessions/{session_id}/

Development workflow
Features are built as vertical slices:
1. Read docs/Ready2Intern-TODO.md for current tasks
2. Read docs/Ready2Intern-Implementation-Plan.md for acceptance criteria
3. Implement backend -> frontend -> integration
4. Test end-to-end before moving to next feature

Integration testing
1. Start backend on localhost:8000, frontend on localhost:5173
2. Verify health: curl http://localhost:8000/api/health
3. Test full flow: file upload -> company selection -> analyze -> results display

Conventions
- Commit messages: <type>: <description> — types: fix, feat, refactor, docs, test
- Backend: type hints required, async/await for I/O, PEP 8
- Frontend: functional components with hooks, Tailwind CSS only (no inline styles), TypeScript strict
- Services use lazy initialization (don't require env vars at import time)
- LLM temperature: 0.3 for scoring/extraction, 0.4 for creative generation
- LLM responses may include markdown code blocks — strip them before JSON parsing
- No real person/company names in test data — use fictitious names only
- Company IDs must be lowercase and match across service/tenets/logos

Security rules
- Validate all file uploads (type, size, content) on both client and server
- Sanitize user inputs before passing to LLM calls
- Never expose API keys in frontend code
- Session IDs are UUIDs (not sequential)

Troubleshooting
- CORS errors: verify backend/.env has CORS_ORIGINS=["http://localhost:5173"]
- File upload: must use FormData with multipart/form-data, max 5MB, PDF/DOCX only
- LLM failures: retry logic (3 attempts, exponential backoff), save partial results if agent fails
- PDF extraction: can fail for image-based PDFs — handle gracefully
- Tailwind v4: use @import "tailwindcss" not @tailwind directives

Current status
Completed: resume upload, company selection, role description input, LLM analysis pipeline (resume + matching + gaps + timeline), results page with animated scores, strengths/gaps display, timeline visualization
Next up: Strands Agent migration (slice 14), PDF export (slice 15), error handling & polish (slice 16)
