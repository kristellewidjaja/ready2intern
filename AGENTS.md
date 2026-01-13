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

### Current Status (Week 1)
- ✅ Backend setup (Python 3.13 + FastAPI + uv)
- ✅ Frontend setup (React 19 + TypeScript + Vite + Tailwind v4)
- ✅ Health check endpoint
- ✅ Theme toggle (light/dark mode)

## Implementation Notes

### Week 1 - Foundation (Completed Jan 13, 2026)

**Key Decisions:**
- Using Python 3.13 (3.14 not yet supported by PyO3/pydantic-core)
- Tailwind CSS v4 requires `@tailwindcss/postcss` plugin
- Theme state managed via React Context + localStorage

**Services Created:**
- Health check endpoint: `/api/health` (GET)

**Reusable Patterns:**
- ThemeContext pattern for global state
- MainLayout wrapper for consistent page structure
- Environment variable configuration with `.env.example` files

**Common Pitfalls:**
- npm cache permissions: use `--cache /tmp/npm-cache` or fix with `sudo chown`
- Tailwind v4 syntax: use `@import "tailwindcss"` not `@tailwind` directives
- FastAPI on_event deprecated: consider lifespan handlers for future endpoints
