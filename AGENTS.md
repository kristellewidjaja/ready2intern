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

### Current Status (Week 6)
- ✅ Backend setup (Python 3.13 + FastAPI + uv)
- ✅ Frontend setup (React 19 + TypeScript + Vite + Tailwind v4)
- ✅ Health check endpoint
- ✅ Theme toggle (light/dark mode)
- ✅ Resume upload (drag-and-drop, validation, session management)
- ✅ Company selection (logos, tenets, API endpoint)
- ✅ Role description input (textarea, validation, character counter)
- ✅ Analyze button (loading states, progress messages, API integration, navigation to results)
- ✅ LLM integration (Anthropic Claude API, resume parsing, structured extraction)
- ✅ Role matching (ATS, Role Match, Company Fit scores with weighted overall score)
- ✅ Gap analysis (technical, experience, company fit, resume gaps with recommendations)
- ✅ Timeline generation (personalized development timeline with phases, tasks, milestones)
- ✅ Results page (overall score display with animated circular progress, score breakdown)
- ✅ Strengths display (key highlights, category-specific strengths with evidence)
- ✅ Gaps display (expandable cards, priority badges, type/priority filters, quick wins, recommendations)

## Implementation Notes

### Week 6 - Score Breakdown Display (Completed Jan 17, 2026)

**Key Decisions:**
- CategoryScoreCard component with hover tooltip pattern for detailed information
- Three color themes (blue, purple, green) for visual distinction between score types
- Animated progress bars with 1-second CSS transition for polish
- Icons (🤖, 🎯, 🏢) provide instant visual recognition of score categories
- Hover interaction shows detailed tooltip with strengths and weaknesses
- Responsive grid layout (3 columns on desktop, 1 column on mobile)
- Card hover effects (scale + shadow) for satisfying interactive feedback
- Brief explanation always visible, full details in tooltip (progressive disclosure)

**Components Created:**
- CategoryScoreCard: Reusable score card with progress bar, tooltip, and theming
- Updated ResultsPage with three CategoryScoreCard instances

**Reusable Patterns:**
- Hover-based tooltip with useState for show/hide state
- Color theme configuration object with all related classes
- Animated progress bar with transition-all and dynamic width
- Responsive grid with Tailwind md: breakpoint
- Card hover effects: hover:scale-105 hover:shadow-lg
- Conditional rendering of optional data (strengths, weaknesses)
- Icon + text labeling pattern for visual identity
- Line clamp for brief text with full text in tooltip

**Common Pitfalls:**
- Tooltip z-index must be higher than other elements (z-10)
- Tooltip position must account for viewport edges (use absolute positioning)
- Hover state should use onMouseEnter/Leave not onClick for better UX
- Progress bar width must be set via inline style, not className (dynamic value)
- Color theme classes must be pre-defined, can't be dynamically constructed
- Strengths/weaknesses may be undefined or empty array - check both
- Test hover interactions require @testing-library/user-event not fireEvent
- Card border should be subtle (border-2) not overwhelming
- Animation duration should be 1 second for progress bar (too fast feels jarring)
- Tooltip should disappear immediately on mouse leave (no delay)

**Testing Approach:**
- Backend: No new backend logic needed, all data already in match_analysis
- Frontend: 45 component tests for CategoryScoreCard
  - Rendering tests (title, icon, score, explanation)
  - Progress bar tests (width calculation, edge cases)
  - Tooltip tests (show/hide, content, conditional rendering)
  - Color theme tests (blue, purple, green)
  - Accessibility tests (hover, keyboard)
- ResultsPage: 40 updated tests for score breakdown section
- Manual testing: Verified with real session data via curl

**UI/UX Details:**

Card Structure:
1. Header: Icon (3xl emoji) + Title (text-lg font-semibold)
2. Score Display: Large number (text-5xl) + "/100" (text-2xl muted)
3. Progress Bar: Full-width bar with animated fill
4. Brief Explanation: 2-line clamp, text-sm, always visible
5. Hover Tooltip: Positioned below card, full details

Tooltip Contents:
- Full explanation paragraph
- "✓ Strengths" heading with green color
- Bullet list of strength items with green dots
- "⚠ Areas for Improvement" heading with orange color
- Bullet list of weakness items with orange dots
- Sections only show if data available

Color Themes:
- Blue (ATS Score): Professional, technical, automated
- Purple (Role Match): Central focus, most important score
- Green (Company Fit): Cultural, values-based, human

Responsive Design:
- Desktop (≥768px): 3 columns, equal width, gap-6
- Tablet (640-767px): 2 columns, adjust gaps
- Mobile (<640px): 1 column, full width, stack cards

**File Structure:**
```
frontend/src/
├── components/
│   ├── CategoryScoreCard.tsx           # Reusable score card component
│   └── __tests__/
│       └── CategoryScoreCard.test.tsx  # 45 component tests
├── pages/
│   ├── ResultsPage.tsx                 # Updated with score breakdown
│   └── __tests__/
│       └── ResultsPage.test.tsx        # 40 updated tests
└── types/
    └── results.ts                       # ScoreDetail interface

backend/
└── test_score_breakdown_manual.py      # Manual E2E test script
```

**Data Flow:**
1. Backend returns match_analysis with three score details (ATS, Role Match, Company Fit)
2. Each score detail includes: score, explanation, strengths[], weaknesses[]
3. ResultsPage fetches results and passes each score detail to CategoryScoreCard
4. CategoryScoreCard displays score, progress bar, brief explanation
5. On hover, tooltip appears with full explanation + strengths + weaknesses
6. Responsive grid adjusts layout based on viewport width

**Performance:**
- Progress bar animation: 1 second CSS transition
- Hover tooltip: Instant display (no delay)
- No re-renders on hover (tooltip in same component)
- Three cards render efficiently with minimal overhead
- All interactions feel smooth and responsive

### Week 6 - Strengths & Gaps Display (Completed Jan 17, 2026)

**Key Decisions:**
- Progressive disclosure: Key strengths highlighted first, then category details
- Expandable gap cards with rich nested content (resources, projects, before/after)
- Type and priority filtering for 16+ gaps without overwhelming users
- Quick wins section prioritized at top for immediate actionable items
- Color-coded priority system (red=high, orange=medium, yellow=low)
- Icon-based visual identity for gap types (💻=tech, 🚀=experience, 🤝=fit, 📝=resume)

**Components Created:**
- StrengthsSection: Displays key strengths and category-specific strengths
- GapCard: Expandable card with type-specific recommendation rendering
- GapsSection: Gap list with filtering, quick wins, and summary stats

**Reusable Patterns:**
- Expandable card pattern with useState for show/hide state
- Type and priority filtering with button groups
- Empty state display when no results match filters
- Nested content rendering based on gap type

**Testing Approach:**
- Frontend: 200+ tests across 3 test suites (StrengthsSection, GapCard, GapsSection)
- Manual E2E: test_strengths_gaps_manual.py validates data structure
- Integration: Verified with real session data

**File Structure:**
```
frontend/src/components/{StrengthsSection,GapCard,GapsSection}.tsx
frontend/src/components/__tests__/{StrengthsSection,GapCard,GapsSection}.test.tsx
frontend/src/types/results.ts (extended with gap analysis types)
```

## Implementation Notes

### Week 6 - Score Breakdown Display (Completed Jan 17, 2026)

**Key Decisions:**
- CategoryScoreCard component with hover tooltip pattern for detailed information
- Three color themes (blue, purple, green) for visual distinction between score types
- Animated progress bars with 1-second CSS transition for polish
- Icons (🤖, 🎯, 🏢) provide instant visual recognition of score categories
- Hover interaction shows detailed tooltip with strengths and weaknesses
- Responsive grid layout (3 columns on desktop, 1 column on mobile)
- Card hover effects (scale + shadow) for satisfying interactive feedback
- Brief explanation always visible, full details in tooltip (progressive disclosure)

**Components Created:**
- CategoryScoreCard: Reusable score card with progress bar, tooltip, and theming
- Updated ResultsPage with three CategoryScoreCard instances

**Reusable Patterns:**
- Hover-based tooltip with useState for show/hide state
- Color theme configuration object with all related classes
- Animated progress bar with transition-all and dynamic width
- Responsive grid with Tailwind md: breakpoint
- Card hover effects: hover:scale-105 hover:shadow-lg
- Conditional rendering of optional data (strengths, weaknesses)
- Icon + text labeling pattern for visual identity
- Line clamp for brief text with full text in tooltip

**Common Pitfalls:**
- Tooltip z-index must be higher than other elements (z-10)
- Tooltip position must account for viewport edges (use absolute positioning)
- Hover state should use onMouseEnter/Leave not onClick for better UX
- Progress bar width must be set via inline style, not className (dynamic value)
- Color theme classes must be pre-defined, can't be dynamically constructed
- Strengths/weaknesses may be undefined or empty array - check both
- Test hover interactions require @testing-library/user-event not fireEvent
- Card border should be subtle (border-2) not overwhelming
- Animation duration should be 1 second for progress bar (too fast feels jarring)
- Tooltip should disappear immediately on mouse leave (no delay)

**Testing Approach:**
- Backend: No new backend logic needed, all data already in match_analysis
- Frontend: 45 component tests for CategoryScoreCard
  - Rendering tests (title, icon, score, explanation)
  - Progress bar tests (width calculation, edge cases)
  - Tooltip tests (show/hide, content, conditional rendering)
  - Color theme tests (blue, purple, green)
  - Accessibility tests (hover, keyboard)
- ResultsPage: 40 updated tests for score breakdown section
- Manual testing: Verified with real session data via curl

**File Structure:**
```
frontend/src/
├── components/
│   ├── CategoryScoreCard.tsx           # Reusable score card component
│   └── __tests__/
│       └── CategoryScoreCard.test.tsx  # 45 component tests
├── pages/
│   ├── ResultsPage.tsx                 # Updated with score breakdown
│   └── __tests__/
│       └── ResultsPage.test.tsx        # 40 updated tests
└── types/
    └── results.ts                       # ScoreDetail interface

backend/
└── test_score_breakdown_manual.py      # Manual E2E test script
```

**Data Flow:**
1. Backend returns match_analysis with three score details (ATS, Role Match, Company Fit)
2. Each score detail includes: score, explanation, strengths[], weaknesses[]
3. ResultsPage fetches results and passes each score detail to CategoryScoreCard
4. CategoryScoreCard displays score, progress bar, brief explanation
5. On hover, tooltip appears with full explanation + strengths + weaknesses
6. Responsive grid adjusts layout based on viewport width

**Performance:**
- Progress bar animation: 1 second CSS transition
- Hover tooltip: Instant display (no delay)
- No re-renders on hover (tooltip in same component)
- Three cards render efficiently with minimal overhead
- All interactions feel smooth and responsive

### Week 6 - Overall Score Display (Completed Jan 15, 2026)

**Key Decisions:**
- Query parameter routing (`/results?session=xyz`) vs route parameters for flexibility
- Animated circular progress using SVG stroke-dashoffset calculation
- Score counting animation from 0 to target over 2 seconds for visual impact
- Dynamic gradient colors based on score ranges (green=excellent, red=poor)
- Partial results support with status field (completed, partial, failed)
- Loading states with skeleton UI for better perceived performance
- Single API call to fetch all analysis data (resume, match, gap, timeline)
- "Start New Analysis" button for easy workflow restart

**Services Created:**
- Results endpoint: GET `/api/results/{session_id}` (`app/api/routes/results.py`)
- Results models: ResultsResponse Pydantic schema (`app/models/results.py`)
- ResultsPage component: Main results display (`frontend/src/pages/ResultsPage.tsx`)
- OverallScoreCard component: Animated score visualization (`frontend/src/components/OverallScoreCard.tsx`)

**Reusable Patterns:**
- Animated circular progress with SVG (circumference calculation, stroke-dashoffset)
- Score counting animation with useEffect and setInterval
- Dynamic gradient styling based on data values
- Query parameter routing for session-based data
- Partial results handling with graceful degradation
- Loading skeleton patterns for async operations
- Error boundary patterns with retry/restart options
- Status determination based on available data files

**Common Pitfalls:**
- SVG circle must use `transform -rotate-90` to start at top
- Circumference = 2 * π * radius for stroke-dasharray
- Offset = circumference - (score / 100) * circumference for progress
- useEffect cleanup needed for animation timers
- Query params accessed via useSearchParams hook in React Router v6
- Results endpoint must handle missing files gracefully
- Overall score may be null if match analysis incomplete
- Animation duration should be 1-2 seconds (longer feels slow)
- Gradient colors need sufficient contrast in dark mode
- Status messages should be encouraging, not discouraging

**Testing Approach:**
- Backend: 162 total tests passing (7 new for results endpoint)
- Results endpoint tests: success, partial, errors, edge cases
- Frontend: Test placeholders created (20 test cases defined)
- Integration: Verified end-to-end flow from analyze to results
- Manual testing: Tested with real session data

**Results Page Structure:**

Header:
- Page title and session ID display
- "Start New Analysis" button for workflow restart

Overall Score Card:
- Animated circular progress (SVG with gradient)
- Score counting animation (0 to target)
- Dynamic gradient based on score range
- Status message and description
- Partial results badge if applicable

Score Breakdown:
- Three score cards (ATS, Role Match, Company Fit)
- Individual scores with labels
- Brief descriptions of each category
- Grid layout (responsive: 3 columns → 1 column on mobile)

Placeholders:
- Strengths & gaps sections (Feature Slice 12)
- Timeline visualization (Feature Slice 13)
- PDF export button (Feature Slice 14)

**File Structure:**
```
backend/app/
├── api/routes/
│ └── results.py # Results retrieval endpoint
├── models/
│ └── results.py # Results response models
└── main.py # Updated with results router

frontend/src/
├── pages/
│ ├── ResultsPage.tsx # Main results page
│ └── __tests__/
│   └── ResultsPage.test.tsx # Test placeholders
├── components/
│ ├── OverallScoreCard.tsx # Animated score card
│ └── __tests__/
│   └── OverallScoreCard.test.tsx # Test placeholders
├── types/
│ └── results.ts # Results type definitions
├── services/
│ └── api.ts # Updated with fetchResults
└── App.tsx # Updated with routing
```

**Data Flow:**
1. User completes analysis → navigates to `/results?session={session_id}`
2. ResultsPage extracts session ID from query params
3. Fetches results via GET `/api/results/{session_id}`
4. Backend loads all JSON files from session directory
5. Combines into single ResultsResponse object
6. Returns with status (completed, partial, failed)
7. Frontend displays overall score with animation
8. Shows score breakdown if match analysis available
9. Displays placeholders for future sections
10. "Start New Analysis" returns to dashboard

**Performance:**
- Results fetch: < 1 second for complete analysis
- Animation duration: 2 seconds for optimal UX
- Page load: Instant with loading skeleton
- All data loaded in single API call (no multiple requests)

### Week 5 - LLM Timeline Generation (Completed Jan 15, 2026)

**Key Decisions:**
- Four-phase timeline structure: Foundation (weeks 1-2), Core Skills (weeks 3-6), Experience Building (weeks 7-10), Polish (weeks 11+)
- Dynamic timeline calculation based on target deadline (defaults to 12 weeks)
- Adaptive intensity levels: Light (12 hrs/week), Moderate (15 hrs/week), Intensive (20 hrs/week)
- Task dependency tracking with critical path identification
- Weekly breakdown with specific deliverables for each week
- Flexibility notes for adjusting timeline if too aggressive
- Motivation tips to maintain momentum

**Services Created:**
- TimelineService: Orchestrates timeline generation (`app/services/timeline_service.py`)
- Timeline prompts: Comprehensive templates with phase structure (`app/prompts/timeline_generation.py`)
- Timeline models: Pydantic schemas for all timeline components (`app/models/timeline.py`)

**Reusable Patterns:**
- Dynamic timeline calculation based on available time
- Adaptive intensity based on deadline urgency
- Task dependency and critical path tracking
- Weekly breakdown for actionable planning
- Flexibility and motivation guidance
- Lazy service initialization pattern (continued from previous features)

**Common Pitfalls:**
- Large token limit needed (16K) for comprehensive timeline
- Timeline must respect target deadline constraints
- Task dependencies must reference valid task IDs
- Weekly breakdown must cover all weeks from start to deadline
- Total hours should be realistic (not overcommit)
- Critical path should include 5-10 most important tasks
- Temperature slightly higher (0.4) for creative planning
- Phases should be sequential and not overlap

**Testing Approach:**
- Backend: 155 total tests passing (126 original + 29 new)
- 15 timeline service tests (generation, parsing, validation, file I/O)
- 15 timeline model tests (all Pydantic models)
- Updated analyze endpoint tests to mock all four services
- Timeline calculation tests with different deadline scenarios
- Intensity level tests (light, moderate, intensive)
- JSON parsing tests with markdown and invalid responses

**Timeline Structure:**

Metadata:
- Total weeks, total hours, hours per week
- Start date and target deadline
- Intensity level (light, moderate, intensive)
- Feasibility assessment

Phases:
- Phase ID, number, title, description
- Start/end weeks
- Focus areas
- Tasks with dependencies and resources
- Milestones with completion criteria
- Success metrics

Weekly Breakdown:
- Week number, start/end dates
- Phase and focus for the week
- Specific tasks to complete
- Estimated hours
- Key deliverable

Additional:
- Critical path (must-complete tasks)
- Flexibility notes (what can be adjusted)
- Motivation tips (staying on track)

**File Structure:**
```
backend/app/
├── services/
│   └── timeline_service.py        # Timeline generation orchestration
├── prompts/
│   └── timeline_generation.py     # Timeline prompts and templates
├── models/
│   └── timeline.py                # Pydantic models for timeline
└── api/routes/
    └── analyze.py                 # Updated with four-phase analysis
```

**Data Flow:**
1. Resume analysis completes → results saved
2. Role matching completes → results saved
3. Gap analysis completes → results saved
4. TimelineService loads gap analysis
5. Service calculates timeline parameters (weeks, hours/week)
6. Determines intensity level based on deadline urgency
7. Combined with role description and gap data
8. LLM generates timeline with phases, tasks, milestones
9. Creates weekly breakdown for actionable planning
10. Identifies critical path and flexibility notes
11. Validation ensures timeline is realistic
12. Results saved to `data/sessions/{session_id}/timeline.json`

**Performance:**
- Timeline generation time: 10-30 seconds (after gap analysis)
- Total analysis time: 40-100 seconds (resume + matching + gaps + timeline)
- Token usage: ~10,000-14,000 tokens per complete analysis
- Cost: ~$0.08-0.12 per complete analysis (all four phases)

### Week 5 - LLM Gap Analysis (Completed Jan 15, 2026)

**Key Decisions:**
- Four-category gap system: Technical, Experience, Company Fit, Resume Optimization
- Priority-based recommendations (High, Medium, Low) with reasoning
- Resource-rich recommendations with specific courses, tutorials, projects
- Project ideas for experience gaps with features and technologies
- Quick wins for immediate improvements (2-3 items)
- Long-term development goals (1-2 items)
- Prioritized action plan with 3 phases (Immediate 0-2 weeks, Short-term 2-6 weeks, Medium-term 6+ weeks)
- Gap IDs for cross-referencing between gaps and action items
- Validation recalculates counts to ensure consistency

**Services Created:**
- GapAnalysisService: Orchestrates gap identification (`app/services/gap_analysis_service.py`)
- Gap analysis prompts: Comprehensive templates with examples (`app/prompts/gap_analysis.py`)
- Gap analysis models: Pydantic schemas for all gap types (`app/models/gap_analysis.py`)

**Reusable Patterns:**
- Multi-category gap identification (technical, experience, fit, resume)
- Priority-based recommendation system
- Resource-rich recommendations with URLs and time estimates
- Project-based learning for experience gaps
- Phased action planning (immediate, short-term, medium-term)
- Gap ID cross-referencing system
- Validation with automatic count recalculation
- Lazy service initialization pattern (continued from previous features)

**Common Pitfalls:**
- Large token limit needed (16K) for comprehensive recommendations
- Validation must recalculate counts from actual gaps, not trust LLM
- Gap IDs must be unique across all categories
- Project ideas need specific features and technologies, not generic descriptions
- Quick wins should be truly quick (hours/days), not weeks
- Action plan phases must reference actual gap IDs
- Temperature slightly higher (0.4) for creative recommendations vs scoring (0.3)

**Testing Approach:**
- Backend: 126 total tests passing (99 original + 27 new)
- 15 gap analysis service tests (analysis, parsing, validation, file I/O)
- 12 gap analysis model tests (all Pydantic models)
- Updated analyze endpoint tests to mock all three services
- Gap count validation tests
- Priority level tests
- JSON parsing tests with markdown and invalid responses

**Gap Categories:**

Technical Gaps:
- Category: technical_skills, tools, frameworks, languages
- Current level: none, beginner, intermediate
- Target level: beginner, intermediate, advanced
- Recommendations with resources (courses, tutorials, docs)
- Success criteria and estimated time

Experience Gaps:
- Category: work_experience, project_experience, domain_knowledge
- Project ideas with features and technologies
- Portfolio value assessment
- Difficulty levels and estimated time

Company Fit Gaps:
- Category: leadership, values, culture, communication
- Company value alignment
- Evidence-based recommendations
- Resume improvement suggestions

Resume Optimization Gaps:
- Category: keywords, formatting, content, storytelling
- Before/after examples
- ATS optimization tips
- Specific changes to make

**File Structure:**
```
backend/app/
├── services/
│   └── gap_analysis_service.py    # Gap identification orchestration
├── prompts/
│   └── gap_analysis.py             # Gap analysis prompts and templates
├── models/
│   └── gap_analysis.py             # Pydantic models for gaps
└── api/routes/
    └── analyze.py                  # Updated with three-phase analysis
```

**Data Flow:**
1. Resume analysis completes → results saved
2. Role matching completes → results saved
3. GapAnalysisService loads match analysis
4. Service loads company tenets from file system
5. Match data formatted into summary for prompt
6. Combined with role description and company tenets
7. LLM identifies gaps across four categories
8. Generates recommendations with resources and projects
9. Creates quick wins and long-term goals
10. Builds prioritized action plan with phases
11. Validation recalculates counts
12. Results saved to `data/sessions/{session_id}/gap_analysis.json`

**Performance:**
- Gap analysis time: 10-30 seconds (after role matching)
- Total analysis time: 30-70 seconds (resume + matching + gaps)
- Token usage: ~8,000-12,000 tokens per complete analysis
- Cost: ~$0.06-0.10 per complete analysis (all three phases)

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
