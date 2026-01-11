# Technical Design Document: Ready2Intern POC
**High-Level Architecture Guide for Implementation**

---

## 1. System Overview

**What:** AI-powered resume evaluator for tech internships  
**How:** Multi-agent system using Anthropic Claude API  
**Storage:** Filesystem only (no database)  
**Deployment:** Local development environment

---

## 2. Architecture

### 2.1 Three-Tier Architecture

```
Frontend (React) ←→ Backend API (FastAPI) ←→ Claude API
                         ↓
                   Filesystem Storage
```

### 2.2 Data Flow

```
1. Upload resume → Generate session_id → Save to filesystem
2. Extract data with LLM → Store in memory
3. User selects companies → Paste role description for each (required)
4. Trigger analysis with company + role context
5. Run 4 agents sequentially → Each calls Claude API
6. Save all results as JSON files
7. Frontend loads and displays results
```

---

## 3. Technology Stack

### Backend
- **Language:** Python 3.11+
- **Framework:** FastAPI
- **LLM:** Anthropic Claude API (claude-sonnet-4-20250514)
- **Package Manager:** uv
- **PDF/DOCX:** pdfplumber, python-docx

### Frontend
- **Framework:** React 18 + TypeScript
- **Build:** Vite
- **Styling:** Tailwind CSS
- **State:** Zustand
- **HTTP:** Axios

---

## 4. Directory Structure

```
ready2intern/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry
│   │   ├── config.py            # Settings
│   │   ├── api/routes.py        # Endpoints
│   │   ├── agents/              # 5 agent files
│   │   ├── services/            # Claude client, file ops
│   │   ├── models/              # Pydantic models
│   │   └── prompts/             # LLM prompts
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── pages/               # Page components
│   │   ├── services/api.ts      # API client
│   │   └── store/               # Zustand store
│   └── package.json
└── data/
    ├── uploads/                 # User resumes
    ├── company_tenets/          # Company criteria (markdown)
    └── results/                 # Analysis outputs (JSON/PDF)
```

---

## 5. Backend Components

### 5.1 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/upload` | POST | Upload resume, return session_id |
| `/api/analyze/{session_id}` | POST | Start analysis with companies + role descriptions (required) |
| `/api/status/{session_id}` | GET | Check analysis status |
| `/api/results/{session_id}` | GET | Get complete results |
| `/api/download/{session_id}/report` | GET | Download PDF report |

### 5.2 Multi-Agent System

**5 Agents (Sequential Execution):**

1. **Document Agent**
   - Input: Resume text
   - LLM Task: Extract structured data (name, GPA, projects, skills, etc.)
   - Output: JSON with student info

2. **Evaluation Agent**
   - Input: Resume data + company tenets + role description (required)
   - LLM Task: Score resume against company criteria and specific role requirements
   - Output: Scores, strengths, gaps per company and role

3. **Recommendation Agent**
   - Input: Resume data + evaluation results
   - LLM Task: Generate 5-10 prioritized recommendations
   - Output: Actionable improvement suggestions

4. **Planner Agent**
   - Input: Recommendations + target deadline
   - LLM Task: Create timeline with phases and milestones
   - Output: Development plan with dates

5. **Orchestrator**
   - Coordinates all agents
   - Manages state between agents
   - Saves results to filesystem

### 5.3 Key Services

**ClaudeClient:**
- Wraps Anthropic API
- Handles retries with exponential backoff
- Manages extended thinking feature
- Returns text responses

**FileService:**
- Save/load uploaded resumes
- Extract text from PDF/DOCX
- Save/load JSON results
- Load company tenets (markdown files)

**SessionService:**
- In-memory session storage (Python dict)
- Track analysis status
- No persistence across restarts

---

## 6. Data Models

### 6.1 Session Data (In-Memory)
```
Session {
  session_id: UUID
  status: "uploading" | "analyzing" | "complete" | "error"
  resume_filename: string
  selected_companies: string[]
  extracted_data: dict (optional)
}
```

### 6.2 Filesystem Storage

**uploads/{session_id}/resume.pdf**
- Original uploaded file

**company_tenets/{company}.md**
- Amazon, Meta, Google evaluation criteria
- Markdown format for readability

**results/{session_id}/job_descriptions.json** (required)
- User-provided role descriptions for each selected company
- Primary evaluation criteria (company tenets provide supplemental context)

**results/{session_id}/evaluation.json**
```json
{
  "evaluations": [
    {
      "company": "Amazon",
      "overall_score": 75,
      "category_scores": {...},
      "strengths": [...],
      "gaps": [...]
    }
  ]
}
```

**results/{session_id}/recommendations.json**
```json
{
  "recommendations": [
    {
      "priority": "high",
      "category": "projects",
      "action": "Build distributed system",
      "rationale": "...",
      "timeline": "2-3 months"
    }
  ]
}
```

**results/{session_id}/timeline.json**
```json
{
  "target_deadline": "2026-09-01",
  "phases": [
    {
      "name": "Immediate (0-4 weeks)",
      "actions": [...]
    }
  ]
}
```

---

## 7. Frontend Components

### 7.1 Pages & Flow

```
Single Dashboard Page (All-in-One)
├── Left Panel: Upload & Company Selection
│   ├── Resume Upload (drag-drop)
│   ├── Company Logos (clickable)
│   └── Role Description Textarea
└── Right Panel: Results Display
    ├── Analysis Status / Loading
    └── Results (when complete)
```

### 7.2 Key Components

**Dashboard (Single Page):**

**Left Panel - Input Section:**
- Resume upload (drag-drop zone, always visible)
- Company logo grid (Amazon, Meta, Google logos)
- Click logo to select company
- Selected company shows role description textarea below logos
- "Analyze Resume" button (enabled when resume + company + role description ready)

**Right Panel - Results Section:**
- Empty state: "Upload resume and select company to begin"
- Loading state: Progress animation with status
- Results state:
  - Company score (circular progress)
  - Gap analysis (expandable)
  - Recommendations (prioritized list)
  - Timeline (visual)
  - Download report button

**Key Features:**
- No navigation between pages
- All actions on one screen
- Real-time validation feedback
- Smooth transitions between states

### 7.3 State Management (Zustand)

```typescript
AppState {
  // Upload
  sessionId: string | null
  uploadedFile: File | null
  
  // Selection (single company at a time)
  selectedCompany: string | null  // "Amazon" | "Meta" | "Google"
  jobDescription: string
  
  // Analysis
  analysisStatus: 'idle' | 'uploading' | 'analyzing' | 'complete' | 'error'
  progress: number  // 0-100
  
  // Results
  results: object | null
  error: string | null
  
  // UI State
  rightPanelView: 'empty' | 'loading' | 'results'
}
```

---

## 8. LLM Integration Strategy

### 8.1 Prompt Engineering Principles

**For Each Agent:**
1. Clear role definition (system prompt)
2. Structured input (JSON format)
3. Explicit output format (JSON schema)
4. Specific instructions
5. Use extended thinking for complex reasoning

### 8.2 Example Prompt Structure

```
System Prompt: "You are an expert resume parser..."

User Prompt:
"""
Extract structured information from this resume:

[RESUME TEXT]

Return JSON with this structure:
{
  "student_info": {...},
  "education": [...],
  ...
}

Return ONLY valid JSON.
"""
```

### 8.3 Response Parsing

- Claude returns text (may include thinking blocks)
- Extract JSON from response
- Validate with Pydantic models
- Handle parsing errors gracefully

---

## 9. Configuration

### 9.1 Environment Variables

**Backend (.env):**
```
ANTHROPIC_API_KEY=sk-ant-xxxxx
ANTHROPIC_MODEL=claude-sonnet-4-20250514
MAX_FILE_SIZE_MB=5
LOG_LEVEL=INFO
```

**Frontend (.env):**
```
VITE_API_URL=http://localhost:8000/api
```

### 9.2 Settings Management

- Use Pydantic Settings for type-safe config
- Load from .env file
- Validate on startup
- Fail fast if API key missing

---

## 10. Error Handling

### 10.1 Error Types

1. **File Upload Errors**
   - Invalid file type → 400 error
   - File too large → 400 error
   - Upload failed → 500 error

2. **LLM Errors**
   - API timeout → Retry 3x with backoff
   - Rate limit → Wait and retry
   - Invalid response → Parse error handling

3. **Session Errors**
   - Session not found → 404 error
   - Analysis not complete → 400 error

### 10.2 Error Response Format

```json
{
  "error": "Error type",
  "message": "Human-readable message",
  "details": {...}
}
```

---

## 11. Security

### 11.1 File Upload Security
- Validate file extensions (.pdf, .docx only)
- Check file size (max 5MB)
- Sanitize filenames
- Store in session-specific directories

### 11.2 API Security
- API key in environment variable (never hardcode)
- CORS: Only allow localhost origins
- Input validation with Pydantic
- No authentication needed (POC single-user)

---

## 12. Performance Targets

| Operation | Target Time |
|-----------|-------------|
| Resume upload | < 2 seconds |
| Text extraction | < 5 seconds |
| Each agent | < 15 seconds |
| Total analysis | < 60 seconds |
| Results load | < 1 second |

---

## 13. Development Workflow

### 13.1 Setup

```bash
# Backend
cd backend
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
cp .env.example .env  # Add API key

# Frontend
cd frontend
npm install

# Create company tenets
mkdir -p data/company_tenets
# Add amazon.md, meta.md, google.md
```

### 13.2 Running

```bash
# Terminal 1: Backend
uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend
npm run dev
```

### 13.3 Testing Flow

1. Upload sample resume
2. Select companies
3. Wait for analysis
4. View results
5. Download report

---

## 14. Implementation Order

### Phase 1: Foundation (Week 1-2)
1. Setup project structure
2. Configure FastAPI + React
3. Implement file upload endpoint
4. Create Claude API client
5. Build Document Agent (resume extraction)

### Phase 2: Core Analysis (Week 3-4)
6. Implement Evaluation Agent
7. Implement Recommendation Agent
8. Implement Planner Agent
9. Build Orchestrator
10. Create company tenets files

### Phase 3: Frontend (Week 5-6)
11. Build upload page
12. Build company selection
13. Build analysis loading page
14. Build results dashboard
15. Integrate all pages

### Phase 4: Polish (Week 7-8)
16. Add error handling
17. Improve UI/UX
18. Add loading states
19. Generate PDF reports
20. Test end-to-end

---

## 15. Key Design Decisions

### Why Filesystem?
- Simplest for POC
- Easy debugging (just check files)
- No database setup/migrations
- Clear migration path to database later

### Why Sequential Agents?
- Simpler than parallel execution
- Easier to debug
- Each agent needs previous agent's output
- Performance acceptable for POC

### Why In-Memory Sessions?
- No persistence needed for POC
- Faster than database
- Results saved to filesystem anyway
- Fresh start on each server restart

### Why Extended Thinking?
- Better reasoning for complex evaluations
- More accurate recommendations
- Worth the extra tokens for quality

---

## 16. Migration to MVP

**When ready for production:**

1. **Add Database (PostgreSQL)**
   - User accounts and authentication
   - Session persistence
   - Historical evaluations
   - Analytics tracking

2. **Add Cloud Storage (S3)**
   - Resume files
   - Generated reports
   - Backup and archival

3. **Add Caching (Redis)**
   - API responses
   - Session data
   - Company tenets

4. **Deploy to Cloud**
   - Backend: Railway/Render
   - Frontend: Vercel/Netlify
   - Database: Managed PostgreSQL

5. **Add Monitoring**
   - Error tracking (Sentry)
   - Performance monitoring
   - Usage analytics

---

## 17. Common Pitfalls to Avoid

1. **Don't** try to parse JSON with regex - use proper JSON parsing
2. **Don't** forget to handle Claude API rate limits
3. **Don't** store API keys in code or git
4. **Don't** assume file uploads will always succeed
5. **Don't** forget to validate user inputs
6. **Don't** make agents too complex - keep prompts focused
7. **Don't** skip error handling for "happy path only"
8. **Don't** forget to create necessary directories on startup

---

## 18. Success Criteria

**POC is complete when:**
- ✅ Can upload resume (PDF/DOCX)
- ✅ Can select 1-3 companies
- ✅ Analysis completes in < 60 seconds
- ✅ Results display correctly
- ✅ Can download PDF report
- ✅ Works for 10+ test resumes
- ✅ Error messages are clear
- ✅ Code is documented

---

## 19. Quick Reference

### Agent Input/Output

| Agent | Input | Output |
|-------|-------|--------|
| Document | Resume text | Structured JSON |
| Evaluation | Resume data + tenets | Scores + gaps |
| Recommendation | Resume + evaluation | Prioritized actions |
| Planner | Recommendations | Timeline with dates |

### File Locations

| Data | Path |
|------|------|
| Uploads | `data/uploads/{session_id}/resume.pdf` |
| Tenets | `data/company_tenets/{company}.md` |
| Results | `data/results/{session_id}/*.json` |

### API Flow

```
POST /upload → session_id
POST /analyze/{session_id} → starts background task
GET /status/{session_id} → poll until "complete"
GET /results/{session_id} → display results
```

---

## 20. Resources

**Documentation:**
- Anthropic API: https://docs.anthropic.com/
- FastAPI: https://fastapi.tiangolo.com/
- React: https://react.dev/
- uv: https://github.com/astral-sh/uv

**Company Info:**
- Amazon Leadership Principles: https://www.amazon.jobs/principles
- Meta Values: https://www.metacareers.com/
- Google Careers: https://careers.google.com/

---

**This TDD provides everything needed to implement the POC without prescribing specific code implementations. Use it as a reference during development with LLM assistance.**
