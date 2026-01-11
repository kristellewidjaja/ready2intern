# Coding Agent Workflow Guide
**How to Work with AI Coding Agents on Ready2Intern POC**

---

## Overview

This guide explains how to effectively work with coding agents to build features using vertical slices. Each chat session focuses on **one complete feature slice** from start to finish.

---

## Session Structure

### One Feature = One Session
- **Goal:** Complete one vertical slice per session
- **Duration:** 1-3 hours per session
- **Output:** Working, tested, committed feature

### Why One Feature Per Session?
1. **Context Management:** Agent maintains focus on single feature
2. **Clear Boundaries:** Each session has defined start/end
3. **Testable Output:** Feature works end-to-end before moving on
4. **Easy Rollback:** Can revert one feature without affecting others
5. **Knowledge Transfer:** Each session documents what was built

---

## Before Starting a Session

### 1. Review Project Status
```bash
# Read current state
cat PROJECT.md

# Check for known issues
cat ISSUES.md

# Review what's been built
git log --oneline
```

### 2. Choose Next Feature Slice
From `Ready2Intern-Implementation-Plan.md`, select the next feature:
- Feature Slice 1: ✅ Done (foundation)
- Feature Slice 2: 🎯 Next (resume upload)
- Feature Slice 3: ⏳ Pending

### 3. Prepare Session Context
Have these files ready:
- `BUILD-GUIDE.md` - Development patterns
- `Ready2Intern-Implementation-Plan.md` - Feature requirements
- `Ready2Intern-API-Spec.md` - API contracts
- `PROJECT.md` - Current project state
- `ISSUES.md` - Known issues

---

## Session Prompt Template

### Basic Prompt Structure

```
I want to build [FEATURE NAME] for the Ready2Intern POC.

CONTEXT:
- Review PROJECT.md for what's been built so far
- Review ISSUES.md for any known issues to avoid
- Follow the vertical slices approach from BUILD-GUIDE.md

FEATURE TO BUILD:
[Copy the feature slice section from Ready2Intern-Implementation-Plan.md]

APPROACH:
1. Backend first: Create API endpoint with request/response models
2. Test backend: Verify in Swagger UI (/docs)
3. Frontend: Build UI component
4. Integration: Connect frontend to backend
5. Test end-to-end: Verify complete user flow
6. Update PROJECT.md: Document what was built
7. Log any issues in ISSUES.md

ACCEPTANCE CRITERIA:
[List the acceptance criteria from the feature slice]

Please work through this step-by-step, showing your progress at each stage.
```

### Example: Feature Slice 2 (Resume Upload)

```
I want to build the Resume Upload feature for the Ready2Intern POC.

CONTEXT:
- Review PROJECT.md for what's been built so far
- Review ISSUES.md for any known issues to avoid
- Follow the vertical slices approach from BUILD-GUIDE.md
- Backend runs on localhost:8000
- Frontend runs on localhost:5173

FEATURE TO BUILD:
Feature Slice 2: Resume Upload

Goal: Complete end-to-end resume upload functionality

Frontend Tasks:
- Build FileDropzone component (drag & drop)
- Implement file validation (PDF/DOCX, max 5MB)
- Show upload progress indicator
- Display success/error states
- Store uploaded file reference in state

Backend Tasks:
- Create /api/upload endpoint
- Implement file validation logic
- Save uploaded files to data/resumes/ directory
- Generate unique session IDs
- Return file metadata (filename, size, session_id)

File System:
- Create data/resumes/ directory structure
- Implement file naming convention (session_id + timestamp)
- Handle file cleanup for errors

APPROACH:
1. Backend: Create upload endpoint with file validation
2. Test: Upload file via Swagger UI, verify it saves to data/resumes/
3. Frontend: Build FileDropzone component with drag & drop
4. Integration: Connect component to /api/upload endpoint
5. Test: Upload file from UI, verify success/error handling
6. Update PROJECT.md with what was built
7. Log any issues discovered in ISSUES.md

ACCEPTANCE CRITERIA:
✓ Drag & drop works in UI
✓ File validation prevents invalid uploads (only PDF/DOCX, max 5MB)
✓ Backend saves file to file system with unique session ID
✓ Session ID is generated and returned to frontend
✓ Error messages display correctly for invalid files
✓ Upload progress shows during transfer
✓ File persists in data/resumes/ directory

Please work through this step-by-step, showing your progress at each stage.
When complete, commit with message: "feat: add resume upload feature (slice 2)"
```

---

## During the Session

### Agent Works Task-by-Task

The agent should break down the feature into tasks and complete them sequentially:

#### Task 1: Backend Models
- Create Pydantic models for request/response
- Define validation rules
- **Acceptance:** Models defined and importable

#### Task 2: Backend Endpoint
- Create route with file upload logic
- Implement validation
- Save file to file system
- **Acceptance:** Endpoint works in Swagger UI

#### Task 3: Frontend Component
- Create component file
- Build UI with drag & drop
- Add file validation
- **Acceptance:** Component renders without errors

#### Task 4: Frontend API Integration
- Add API function to services/api.ts
- Connect component to API
- Handle loading/error states
- **Acceptance:** API call succeeds

#### Task 5: End-to-End Testing
- Test complete user flow
- Verify file saves correctly
- Test error cases
- **Acceptance:** All acceptance criteria met

#### Task 6: Documentation
- Update PROJECT.md
- Log any issues in ISSUES.md
- **Acceptance:** Documentation updated

#### Task 7: Commit
- Stage all changes
- Commit with descriptive message
- **Acceptance:** Feature committed to git

### Progress Checkpoints

Agent should report progress after each task:
```
✅ Task 1 Complete: Backend models defined
   - Created UploadRequest and UploadResponse models
   - Added file type and size validation
   - Models are in backend/app/models/upload.py

🎯 Next: Task 2 - Create backend endpoint
```

---

## Project Tracking Files

### PROJECT.md (Project State)

**Purpose:** Living document that tracks what's been built and lessons learned

**Structure:**
```markdown
# Ready2Intern POC - Project Status

**Last Updated:** [Date]
**Current Sprint:** Week 2
**Completed Features:** 2/15

---

## Project Overview

AI Internship Readiness Platform that analyzes student resumes against company-specific criteria and provides actionable recommendations.

---

## Completed Features

### ✅ Feature Slice 1: Foundation (Week 1)
**Completed:** 2026-01-11
**Developer:** Agent Session 1

**What Was Built:**
- React + TypeScript + Vite frontend
- FastAPI + Python backend with uv
- Tailwind CSS with custom theme (5 brand colors)
- Theme toggle (light/dark mode)
- Health check endpoint (/api/health)
- CORS configuration
- Basic dashboard layout

**Key Files:**
- Frontend: src/App.tsx, src/services/api.ts
- Backend: app/main.py, app/api/routes/health.py
- Config: tailwind.config.js, app/core/config.py

**Lessons Learned:**
- Tailwind dark mode requires 'class' strategy
- CORS must include localhost:5173 for dev
- Health check useful for verifying integration

**Integration Points:**
- Frontend successfully calls backend health check
- Theme switching works in both modes
- API docs accessible at /docs

---

### ✅ Feature Slice 2: Resume Upload (Week 2)
**Completed:** 2026-01-12
**Developer:** Agent Session 2

**What Was Built:**
- FileDropzone component with drag & drop
- File validation (PDF/DOCX, max 5MB)
- Backend /api/upload endpoint
- Session ID generation (UUID)
- File storage in data/resumes/
- Upload progress indicator
- Error handling for invalid files

**Key Files:**
- Frontend: src/components/dashboard/FileDropzone.tsx
- Backend: app/api/routes/upload.py, app/models/upload.py
- Services: app/services/file_service.py

**Lessons Learned:**
- FormData required for multipart file upload
- File.size is in bytes (5MB = 5 * 1024 * 1024)
- Session IDs should be UUID4 for uniqueness
- Need to create data/resumes/ directory if not exists
- Content-Type header must be multipart/form-data

**Integration Points:**
- Frontend sends file via FormData
- Backend validates and saves to file system
- Session ID returned and stored in frontend state
- Error messages propagate to UI

**State Management:**
- Added sessionId to app state (useState)
- File reference stored locally in component

---

## In Progress

### 🎯 Feature Slice 3: Company Selection (Week 2)
**Started:** 2026-01-13
**Developer:** Agent Session 3

**Current Status:**
- Backend /api/companies endpoint created
- Company logos added to public/logos/
- Working on CompanySelector component

---

## Pending Features

### ⏳ Feature Slice 4: Job Description Input
- Not started
- Depends on: Feature Slice 3

### ⏳ Feature Slice 5: Analyze Button
- Not started
- Depends on: Feature Slices 2, 3, 4

[... list remaining features ...]

---

## Technical Decisions

### Architecture
- **Frontend:** React 18 + TypeScript + Vite
- **Backend:** FastAPI + Python 3.11+ with uv
- **Styling:** Tailwind CSS with custom theme
- **State:** Zustand (to be added in slice 5)
- **LLM:** Anthropic Claude API (to be added in slice 6)
- **Storage:** File system (POC only)

### Design Choices
- **Vertical Slices:** Build features end-to-end
- **API First:** Define contracts before implementation
- **Theme Support:** Light and dark modes from start
- **No Database:** File system storage for POC simplicity

### File Naming Conventions
- **Resumes:** `{session_id}_{timestamp}.{ext}`
- **Sessions:** `data/sessions/{session_id}/`
- **Components:** PascalCase (e.g., FileDropzone.tsx)
- **Routes:** snake_case (e.g., upload.py)

---

## Dependencies

### Frontend
```json
{
  "react": "^18.2.0",
  "typescript": "^5.2.2",
  "vite": "^5.0.0",
  "tailwindcss": "^3.4.0",
  "axios": "^1.6.0",
  "zustand": "^4.4.0",
  "lucide-react": "^0.300.0"
}
```

### Backend
```toml
dependencies = [
    "fastapi>=0.109.0",
    "uvicorn[standard]>=0.27.0",
    "python-multipart>=0.0.6",
    "anthropic>=0.18.0",
    "python-dotenv>=1.0.0",
    "pydantic>=2.5.0",
]
```

---

## Environment Variables

### Backend (.env)
```
ANTHROPIC_API_KEY=sk-ant-...
API_PORT=8000
CORS_ORIGINS=["http://localhost:5173"]
DATA_DIR=../data
MAX_FILE_SIZE_MB=5
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000
```

---

## Known Patterns

### File Upload Pattern
- Frontend: FormData with Content-Type multipart/form-data
- Backend: UploadFile with File(...) dependency
- Validation: Check content_type and size before saving

### API Call Pattern
- Frontend: axios with try/catch
- Backend: Pydantic models for validation
- Errors: HTTPException with status codes

### Component Pattern
- Props interface defined
- Loading/error states managed
- API calls in async handlers

---

## Next Steps

1. Complete Feature Slice 3 (Company Selection)
2. Start Feature Slice 4 (Job Description Input)
3. Consider adding Zustand for global state (before slice 5)
4. Plan LLM integration architecture (before slice 6)

---

## Metrics

- **Features Completed:** 2/15 (13%)
- **Lines of Code:** ~1,200 (estimated)
- **Test Coverage:** Manual testing only
- **Known Issues:** 1 (see ISSUES.md)
```

### ISSUES.md (Issue Tracking)

**Purpose:** Track bugs, technical debt, and improvements

**Structure:**
```markdown
# Ready2Intern POC - Issues

**Last Updated:** [Date]

---

## Active Issues

### 🔴 High Priority

#### Issue #1: File upload fails for files with special characters in name
**Discovered:** 2026-01-12 (Feature Slice 2)
**Severity:** High
**Impact:** Users cannot upload files with names like "resume (final).pdf"

**Description:**
When uploading files with special characters (parentheses, spaces, etc.), the backend saves the file but returns an error. Frontend shows upload failed even though file is saved.

**Steps to Reproduce:**
1. Select file named "resume (final).pdf"
2. Upload via FileDropzone
3. Backend saves file but returns 500 error
4. Frontend shows error message

**Root Cause:**
File naming logic doesn't sanitize special characters. Session ID concatenation breaks with certain characters.

**Workaround:**
Rename files to remove special characters before upload.

**Fix Required:**
- Sanitize filename in backend before saving
- Use only session_id + extension for storage
- Return original filename in metadata

**Assigned To:** Next session
**Priority:** Fix in Feature Slice 3 session

---

### 🟡 Medium Priority

#### Issue #2: No loading indicator during file upload
**Discovered:** 2026-01-12 (Feature Slice 2)
**Severity:** Medium
**Impact:** User doesn't know if large file is uploading

**Description:**
When uploading large files (>2MB), there's a delay but no visual feedback. User might think app is frozen.

**Fix Required:**
- Add upload progress bar
- Show percentage complete
- Add cancel button

**Assigned To:** Feature Slice 2 polish (Week 6)
**Priority:** Nice to have

---

### 🟢 Low Priority

#### Issue #3: Dark mode colors need adjustment
**Discovered:** 2026-01-11 (Feature Slice 1)
**Severity:** Low
**Impact:** Some text hard to read in dark mode

**Description:**
Secondary text color (Mint #9DBEBB) has low contrast on Deep Ocean background in dark mode. Passes WCAG AA but could be better.

**Fix Required:**
- Test all color combinations
- Adjust if needed for AAA compliance

**Assigned To:** Feature Slice 15 (Polish)
**Priority:** Low

---

## Resolved Issues

### ✅ Issue #0: CORS error on initial setup
**Discovered:** 2026-01-11 (Feature Slice 1)
**Resolved:** 2026-01-11
**Resolution:** Added localhost:5173 to CORS_ORIGINS in backend .env

---

## Technical Debt

### TD-1: No automated tests
**Created:** 2026-01-11
**Impact:** Manual testing only, risk of regressions
**Plan:** Add tests in Feature Slice 15 (Week 6)

### TD-2: No error logging
**Created:** 2026-01-12
**Impact:** Hard to debug production issues
**Plan:** Add logging service in Feature Slice 6 (LLM integration)

### TD-3: No rate limiting
**Created:** 2026-01-12
**Impact:** API could be abused
**Plan:** Add rate limiting in Feature Slice 15 (Polish)

---

## Enhancement Ideas

### 💡 Idea #1: Add file preview before upload
**Suggested:** 2026-01-12
**Description:** Show PDF preview in modal before uploading
**Effort:** Medium
**Value:** High
**Status:** Backlog

### 💡 Idea #2: Support multiple file formats
**Suggested:** 2026-01-12
**Description:** Accept TXT, RTF in addition to PDF/DOCX
**Effort:** Low
**Value:** Medium
**Status:** Backlog

---

## Issue Template

When logging new issues, use this format:

```
#### Issue #[N]: [Brief description]
**Discovered:** [Date] ([Feature Slice])
**Severity:** [High/Medium/Low]
**Impact:** [User impact description]

**Description:**
[Detailed description]

**Steps to Reproduce:**
1. [Step 1]
2. [Step 2]
3. [Expected vs Actual]

**Root Cause:** (if known)
[Technical explanation]

**Workaround:** (if available)
[Temporary solution]

**Fix Required:**
- [Action item 1]
- [Action item 2]

**Assigned To:** [Next session / Specific feature slice]
**Priority:** [When to fix]
```
```

---

## Recommendations

### ✅ Recommended Approach

**Use PROJECT.md + ISSUES.md** - This is a GOOD approach because:

1. **Context Preservation:** Each session can quickly understand project state
2. **Knowledge Transfer:** Lessons learned are documented
3. **Issue Tracking:** Problems don't get forgotten
4. **Progress Visibility:** Clear view of what's done vs pending
5. **Pattern Library:** Successful patterns are recorded
6. **Onboarding:** New agents (or humans) can get up to speed quickly

### 📊 Alternative Approaches (Not Recommended)

#### ❌ Git Commit Messages Only
**Problem:** Hard to get high-level overview, must read many commits

#### ❌ Separate Issue Tracker (Jira, GitHub Issues)
**Problem:** Context switching, agent can't easily access external tools

#### ❌ No Documentation
**Problem:** Each session starts from scratch, repeated mistakes

### 🎯 Optimal Workflow

```
Session Start
    ↓
Read PROJECT.md (what's built)
    ↓
Read ISSUES.md (what to avoid)
    ↓
Choose Feature Slice
    ↓
Build Feature (tasks with acceptance criteria)
    ↓
Test End-to-End
    ↓
Update PROJECT.md (what was built + lessons)
    ↓
Update ISSUES.md (new issues found)
    ↓
Commit Feature
    ↓
Session End
```

---

## Session End Checklist

Before ending a session, agent should:

- [ ] All acceptance criteria met
- [ ] Feature tested end-to-end
- [ ] PROJECT.md updated with:
  - Feature marked complete
  - Key files listed
  - Lessons learned documented
  - Integration points noted
- [ ] ISSUES.md updated with:
  - Any new issues discovered
  - Any issues resolved
- [ ] Code committed with clear message
- [ ] Next feature identified

---

## Example Session Flow

### Session Start
```
Agent: I've reviewed PROJECT.md and see that Feature Slice 1 (Foundation) 
is complete. I've also checked ISSUES.md and see one known issue about 
file naming with special characters - I'll keep that in mind.

I'm ready to build Feature Slice 2: Resume Upload. Let me start with the 
backend API endpoint.
```

### During Session
```
Agent: ✅ Task 1 Complete: Backend models created
- UploadRequest and UploadResponse models defined
- Validation rules added (file type, size)
- Models in backend/app/models/upload.py

Testing in Swagger UI... ✅ Endpoint works!

Moving to Task 2: Frontend component...
```

### Session End
```
Agent: ✅ Feature Slice 2 Complete!

All acceptance criteria met:
✓ Drag & drop works
✓ File validation working
✓ Files save to data/resumes/
✓ Session IDs generated
✓ Error handling works

I've updated:
- PROJECT.md: Added Feature Slice 2 section with lessons learned
- ISSUES.md: Logged Issue #1 about special characters in filenames

Committed as: "feat: add resume upload feature (slice 2)"

Ready for Feature Slice 3: Company Selection in next session.
```

---

## Tips for Effective Sessions

### 1. Start with Context
Always have agent read PROJECT.md and ISSUES.md first

### 2. One Feature at a Time
Don't try to build multiple features in one session

### 3. Test as You Go
Don't wait until the end to test integration

### 4. Document Immediately
Update PROJECT.md and ISSUES.md before committing

### 5. Clear Acceptance Criteria
Agent knows exactly when feature is "done"

### 6. Commit Working Code
Only commit when all acceptance criteria met

### 7. Learn from Issues
Review ISSUES.md before starting to avoid known problems

---

## Summary

**Best Practice:**
- One feature slice per session
- Work task-by-task with acceptance criteria
- Maintain PROJECT.md for state
- Maintain ISSUES.md for problems
- Test end-to-end before committing
- Document lessons learned

This approach ensures:
- ✅ Clear progress tracking
- ✅ Knowledge preservation
- ✅ Issue awareness
- ✅ Smooth handoffs between sessions
- ✅ Working software at each step
