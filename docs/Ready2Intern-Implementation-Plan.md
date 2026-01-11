# Implementation Plan: Ready2Intern POC
**Vertical Slices Approach - Feature-by-Feature**

---

## Overview

**Strategy:** Vertical Slices (End-to-End Features)  
**Approach:** Build complete features from UI → API → LLM → Storage  
**Timeline:** 6 weeks (1-week feature cycles)  
**Handoff Method:** Feature-by-feature with working deliverables

---

## Architecture Overview

Each feature slice includes:
1. **Frontend:** UI components + state management
2. **Backend:** API endpoint + request/response handling
3. **Business Logic:** LLM integration + file system operations
4. **Integration:** End-to-end testing of the complete feature

---

## Feature Slice 1: Project Setup & Basic Dashboard (Week 1)

### Goal
Set up the foundation and deliver a working dashboard with theme support.

### Frontend Tasks
- Initialize React + TypeScript + Vite project
- Configure Tailwind CSS with custom theme colors
- Implement theme toggle (light/dark mode)
- Create basic layout (Header, Footer, Main)
- Build empty dashboard shell

### Backend Tasks
- Initialize FastAPI project with uv
- Set up project structure (routers, services, models)
- Create health check endpoint
- Configure CORS for local development
- Set up environment variables (.env)

### Integration
- Frontend can call backend health check
- Theme switching works correctly
- Dashboard displays in both light and dark modes

### Acceptance Criteria
- ✓ Frontend runs on localhost:5173
- ✓ Backend runs on localhost:8000
- ✓ Health check endpoint returns 200
- ✓ Theme toggle switches between light/dark
- ✓ Dashboard layout is responsive

### Deliverables
- Working frontend with theme support
- Working backend with health check
- README with setup instructions

---

## Feature Slice 2: Resume Upload (Week 2)

### Goal
Complete end-to-end resume upload functionality.

### Frontend Tasks
- Build FileDropzone component (drag & drop)
- Implement file validation (PDF/DOCX, max 5MB)
- Show upload progress indicator
- Display success/error states
- Store uploaded file reference in state

### Backend Tasks
- Create `/api/upload` endpoint
- Implement file validation logic
- Save uploaded files to `data/resumes/` directory
- Generate unique session IDs
- Return file metadata (filename, size, session_id)

### File System
- Create `data/resumes/` directory structure
- Implement file naming convention (session_id + timestamp)
- Handle file cleanup for errors

### Integration
- User can drag & drop resume file
- File uploads to backend successfully
- Frontend receives session_id
- File is saved in file system
- Error handling works for invalid files

### Acceptance Criteria
- ✓ Drag & drop works in UI
- ✓ File validation prevents invalid uploads
- ✓ Backend saves file to file system
- ✓ Session ID is generated and returned
- ✓ Error messages display correctly
- ✓ Upload progress shows during transfer

### Deliverables
- Working resume upload feature
- Files persist in data/resumes/
- Session management initialized

---

## Feature Slice 3: Company Selection (Week 2)

### Goal
Allow users to select a target company with logo display.

### Frontend Tasks
- Build CompanyLogoSelector component
- Display company logos (Amazon, Meta, Google)
- Implement single-select interaction
- Show selected state with checkmark
- Store selected company in state

### Backend Tasks
- Create company configuration endpoint `/api/companies`
- Return list of available companies
- Include company metadata (name, logo URL, color)

### File System
- Store company logos in `public/logos/` directory
- Create company tenets files in `data/company-tenets/`
  - `amazon-leadership-principles.txt`
  - `meta-core-values.txt`
  - `google-principles.txt`

### Integration
- Frontend fetches company list from backend
- Company logos display correctly
- User can select one company
- Selected company is stored in state

### Acceptance Criteria
- ✓ Company logos display in UI
- ✓ Single-select works (only one selected)
- ✓ Selected state shows checkmark
- ✓ Backend returns company list
- ✓ Company tenets files exist in file system

### Deliverables
- Working company selection UI
- Company data endpoint
- Company tenets stored in file system

---

## Feature Slice 4: Role Description Input (Week 3)

### Goal
Enable users to paste and validate role descriptions.

### Frontend Tasks
- Build RoleDescriptionInput component (textarea)
- Implement character counter
- Show validation (minimum 50 characters)
- Display validation errors
- Store role description in state

### Backend Tasks
- Add role description validation to analysis endpoint
- Validate minimum length (50 chars)
- Validate maximum length (10,000 chars)
- Return validation errors

### Integration
- User can paste role description
- Character counter updates in real-time
- Validation shows before submission
- Invalid descriptions show error messages

### Acceptance Criteria
- ✓ Textarea accepts role description
- ✓ Character counter displays correctly
- ✓ Validation prevents short descriptions
- ✓ Error messages are clear
- ✓ Valid descriptions enable analyze button

### Deliverables
- Working role description input
- Real-time validation
- Clear error messaging

---

## Feature Slice 5: Analyze Button & Loading State (Week 3)

### Goal
Trigger analysis and show loading feedback.

### Frontend Tasks
- Build AnalyzeButton component
- Implement disabled state logic (all fields required)
- Show loading spinner during analysis
- Display progress messages
- Handle API errors gracefully

### Backend Tasks
- Create `/api/analyze` endpoint (POST)
- Accept: session_id, company, role_description, target_deadline
- Validate all required fields
- Return immediate response with analysis_id
- Queue analysis for processing

### Integration
- Button enables only when all fields are valid
- Click triggers API call
- Loading state shows immediately
- Progress messages update user
- Errors display if API fails

### Acceptance Criteria
- ✓ Button disabled until all fields valid
- ✓ Loading spinner shows during analysis
- ✓ API endpoint accepts request
- ✓ Analysis ID is returned
- ✓ Error handling works correctly

### Deliverables
- Working analyze button
- Loading state UI
- Analysis endpoint (stub)

---

## Feature Slice 6: LLM Integration - Resume Analysis (Week 4)

### Goal
Integrate Anthropic Claude to analyze resumes.

### Backend Tasks
- Set up Anthropic API client
- Create prompt templates for resume analysis
- Implement resume parsing logic
- Extract key information (skills, experience, projects)
- Store raw analysis in `data/sessions/{session_id}/resume_analysis.json`

### LLM Prompts
- Resume extraction prompt
- Skills identification prompt
- Experience summarization prompt

### File System
- Create session directories: `data/sessions/{session_id}/`
- Store resume analysis results
- Store intermediate LLM responses

### Integration
- Backend reads uploaded resume file
- Sends resume to Claude API
- Parses LLM response
- Saves structured analysis
- Returns success/failure status

### Acceptance Criteria
- ✓ Resume file is read from file system
- ✓ Claude API call succeeds
- ✓ Resume data is extracted correctly
- ✓ Analysis saved to file system
- ✓ Error handling for API failures

### Deliverables
- Working LLM integration
- Resume analysis logic
- Structured analysis output

---

## Feature Slice 7: LLM Integration - Role Matching (Week 4)

### Goal
Match resume against role description and company tenets.

### Backend Tasks
- Create role matching prompt template
- Load company tenets from file system
- Compare resume vs role requirements
- Compare resume vs company values
- Calculate match scores (ATS, Role Match, Company Fit)
- Store matching results in `data/sessions/{session_id}/match_analysis.json`

### LLM Prompts
- Role requirements matching prompt
- Company culture fit prompt
- ATS score calculation prompt

### Integration
- Backend loads company tenets file
- Combines resume + role description + tenets
- Sends to Claude API for analysis
- Parses match scores
- Saves results to file system

### Acceptance Criteria
- ✓ Company tenets loaded correctly
- ✓ Role matching analysis completes
- ✓ Match scores calculated (0-100)
- ✓ Results saved to file system
- ✓ Overall score computed

### Deliverables
- Role matching logic
- Company fit analysis
- Match score calculation

---

## Feature Slice 8: LLM Integration - Gap Analysis (Week 5)

### Goal
Identify gaps and generate recommendations.

### Backend Tasks
- Create gap analysis prompt template
- Identify missing skills/experience
- Prioritize gaps (High/Medium/Low)
- Generate actionable recommendations
- Provide specific examples
- Store gaps in `data/sessions/{session_id}/gap_analysis.json`

### LLM Prompts
- Gap identification prompt
- Recommendation generation prompt
- Priority assessment prompt

### Integration
- Backend uses match analysis results
- Sends to Claude for gap identification
- Generates prioritized recommendations
- Saves detailed gap analysis
- Returns structured gaps data

### Acceptance Criteria
- ✓ Gaps identified correctly
- ✓ Priorities assigned (High/Med/Low)
- ✓ Recommendations are actionable
- ✓ Examples are specific
- ✓ Results saved to file system

### Deliverables
- Gap analysis logic
- Recommendation generation
- Priority classification

---

## Feature Slice 9: LLM Integration - Development Timeline (Week 5)

### Goal
Generate personalized development timeline.

### Backend Tasks
- Create timeline generation prompt template
- Calculate time to deadline
- Break into phases (Immediate, Short-term, Medium-term)
- Assign tasks to each phase
- Create milestone checkpoints
- Store timeline in `data/sessions/{session_id}/timeline.json`

### LLM Prompts
- Timeline generation prompt
- Task prioritization prompt
- Milestone creation prompt

### Integration
- Backend uses gap analysis + deadline
- Sends to Claude for timeline generation
- Structures timeline by phases
- Saves timeline to file system
- Returns complete timeline data

### Acceptance Criteria
- ✓ Timeline respects target deadline
- ✓ Phases are logical and sequential
- ✓ Tasks are specific and actionable
- ✓ Milestones are measurable
- ✓ Results saved to file system

### Deliverables
- Timeline generation logic
- Phase-based planning
- Milestone tracking

---

## Feature Slice 10: Results Display - Overall Score (Week 6)

### Goal
Display overall match score with visual feedback.

### Frontend Tasks
- Build OverallScoreCard component
- Implement animated progress bar
- Show score with gradient background
- Display status message based on score
- Animate score counting on load

### Backend Tasks
- Create `/api/results/{session_id}` endpoint
- Load all analysis files from session directory
- Combine into single response object
- Return complete analysis results

### Integration
- Frontend polls for results (or uses WebSocket)
- Backend returns complete analysis
- Overall score displays with animation
- Status message shows appropriate feedback

### Acceptance Criteria
- ✓ Overall score displays prominently
- ✓ Progress bar animates smoothly
- ✓ Gradient matches score range
- ✓ Status message is encouraging
- ✓ Results endpoint returns all data

### Deliverables
- Working overall score display
- Results retrieval endpoint
- Animated UI components

---

## Feature Slice 11: Results Display - Score Breakdown (Week 6)

### Goal
Show detailed score breakdown (ATS, Role Match, Company Fit).

### Frontend Tasks
- Build CategoryScoreCard component
- Display three score cards side-by-side
- Show individual progress bars
- Add hover tooltips with details
- Implement responsive layout

### Backend Tasks
- Ensure score breakdown included in results
- Add tooltip data for each category
- Include score explanations

### Integration
- Frontend receives score breakdown
- Three cards display correctly
- Hover shows detailed breakdown
- Responsive on mobile (stacked)

### Acceptance Criteria
- ✓ Three score cards display
- ✓ Individual scores show correctly
- ✓ Progress bars animate
- ✓ Tooltips provide details
- ✓ Responsive layout works

### Deliverables
- Score breakdown display
- Tooltip implementation
- Responsive card layout

---

## Feature Slice 12: Results Display - Strengths & Gaps (Week 6)

### Goal
Display strengths and gaps with expandable details.

### Frontend Tasks
- Build StrengthsSection component
- Build GapsSection component
- Implement expandable cards
- Show priority badges for gaps
- Display evidence and recommendations

### Backend Tasks
- Format strengths data for display
- Format gaps data with priorities
- Include all recommendation details

### Integration
- Frontend receives strengths and gaps
- Sections display with proper formatting
- Cards expand/collapse correctly
- Priority badges show colors
- All details are readable

### Acceptance Criteria
- ✓ Strengths display with evidence
- ✓ Gaps show with priorities
- ✓ Cards expand/collapse smoothly
- ✓ Recommendations are actionable
- ✓ Examples are specific

### Deliverables
- Strengths display section
- Gaps display section
- Expandable card UI

---

## Feature Slice 13: Results Display - Timeline (Week 6)

### Goal
Show development timeline with phases and tasks.

### Frontend Tasks
- Build TimelineSection component
- Display timeline visualization
- Show phases with tasks
- Implement expandable phases
- Display milestones

### Backend Tasks
- Format timeline data for display
- Include all phases and tasks
- Add milestone information

### Integration
- Frontend receives timeline data
- Timeline visualization displays
- Phases expand/collapse
- Tasks are clearly listed
- Milestones are highlighted

### Acceptance Criteria
- ✓ Timeline visualization shows
- ✓ Phases display correctly
- ✓ Tasks are actionable
- ✓ Milestones are clear
- ✓ Expandable sections work

### Deliverables
- Timeline visualization
- Phase-based display
- Interactive timeline UI

---

## Feature Slice 14: PDF Export (Week 6)

### Goal
Allow users to download analysis as PDF.

### Frontend Tasks
- Add "Download PDF" button to header
- Trigger PDF generation on click
- Show download progress
- Handle download errors

### Backend Tasks
- Create `/api/export/{session_id}` endpoint
- Generate PDF from analysis results
- Format PDF with branding
- Include all sections (scores, gaps, timeline)
- Return PDF file for download

### Integration
- User clicks download button
- Backend generates PDF
- PDF downloads to user's device
- PDF contains all analysis data

### Acceptance Criteria
- ✓ Download button works
- ✓ PDF generates successfully
- ✓ PDF includes all sections
- ✓ PDF is well-formatted
- ✓ Download completes

### Deliverables
- PDF generation logic
- Export endpoint
- Download functionality

---

## Feature Slice 15: Error Handling & Polish (Week 6)

### Goal
Add comprehensive error handling and UI polish.

### Frontend Tasks
- Add error boundaries
- Implement toast notifications
- Add loading skeletons
- Improve error messages
- Add "Start New Analysis" functionality

### Backend Tasks
- Add comprehensive error handling
- Implement request validation
- Add logging for debugging
- Handle LLM API failures gracefully
- Add rate limiting

### Integration
- All error paths tested
- User-friendly error messages
- Graceful degradation
- Clear recovery paths

### Acceptance Criteria
- ✓ Errors display user-friendly messages
- ✓ API failures handled gracefully
- ✓ Loading states show everywhere
- ✓ Users can start new analysis
- ✓ No crashes on edge cases

### Deliverables
- Comprehensive error handling
- Polished user experience
- Production-ready application

---

## Testing Strategy (Continuous)

### Per Feature Slice
- **Unit Tests:** Test individual functions/components
- **Integration Tests:** Test feature end-to-end
- **Manual Testing:** Verify in browser/API client

### Test Coverage Goals
- Frontend: 70%+ coverage
- Backend: 80%+ coverage
- Critical paths: 100% coverage

### Testing Checklist (Per Slice)
- ✓ Happy path works
- ✓ Error cases handled
- ✓ Edge cases covered
- ✓ Responsive design verified
- ✓ Accessibility checked

---

## Deployment Checklist (Final)

### Frontend
- ✓ Build optimized production bundle
- ✓ Environment variables configured
- ✓ Assets optimized (images, fonts)
- ✓ Service worker (optional)

### Backend
- ✓ Environment variables set
- ✓ File system directories created
- ✓ Anthropic API key configured
- ✓ CORS configured for production
- ✓ Logging enabled

### File System Structure
```
data/
├── resumes/           # Uploaded resume files
├── company-tenets/    # Company values/principles
│   ├── amazon-leadership-principles.txt
│   ├── meta-core-values.txt
│   └── google-principles.txt
└── sessions/          # Analysis results by session
    └── {session_id}/
        ├── resume_analysis.json
        ├── match_analysis.json
        ├── gap_analysis.json
        └── timeline.json
```

---

## Success Metrics

### Technical Metrics
- All features working end-to-end
- < 3 second response time for analysis
- 0 critical bugs
- 80%+ test coverage

### User Experience Metrics
- Intuitive single-page workflow
- Clear feedback at every step
- Helpful error messages
- Professional visual design

### Business Metrics
- Complete analysis in < 2 minutes
- Actionable recommendations
- Downloadable PDF report
- Support for 3 companies (Amazon, Meta, Google)

---

## Feature Completion Order

1. ✓ Project Setup & Dashboard (Week 1)
2. ✓ Resume Upload (Week 2)
3. ✓ Company Selection (Week 2)
4. ✓ Role Description Input (Week 3)
5. ✓ Analyze Button & Loading (Week 3)
6. ✓ LLM - Resume Analysis (Week 4)
7. ✓ LLM - Role Matching (Week 4)
8. ✓ LLM - Gap Analysis (Week 5)
9. ✓ LLM - Timeline Generation (Week 5)
10. ✓ Results - Overall Score (Week 6)
11. ✓ Results - Score Breakdown (Week 6)
12. ✓ Results - Strengths & Gaps (Week 6)
13. ✓ Results - Timeline (Week 6)
14. ✓ PDF Export (Week 6)
15. ✓ Error Handling & Polish (Week 6)

---

**This implementation plan uses vertical slices to deliver working features incrementally. Each slice is independently testable and provides immediate value. The approach allows for early feedback and course correction while maintaining momentum.**
