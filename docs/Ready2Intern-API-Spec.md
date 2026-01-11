# API Specification: Ready2Intern POC

**Version:** 1.0  
**Base URL:** `http://localhost:8000/api`  
**Format:** JSON  
**Authentication:** None (POC)

---

## Overview

RESTful API for resume analysis and internship readiness evaluation.

**Request Flow:**
```
1. POST /upload          → Get session_id
2. POST /analyze/{id}    → Start analysis with companies + role descriptions (required)
3. GET /status/{id}      → Poll until complete
4. GET /results/{id}     → Retrieve results
5. GET /download/{id}    → Download PDF report
```

---

## Endpoints

### 1. Upload Resume

**Endpoint:** `POST /upload`

**Purpose:** Upload resume file and create new session

**Request:**
- Content-Type: `multipart/form-data`
- Body:
  - `file`: Resume file (PDF or DOCX)

**Validation:**
- File types: `.pdf`, `.docx` only
- Max size: 5MB
- Required: Yes

**Response (200 OK):**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "uploaded",
  "message": "Resume uploaded successfully"
}
```

**Errors:**
- `400`: Invalid file type or size
- `500`: Upload failed

**Notes:**
- Generates UUID v4 for session_id
- Saves file to `data/uploads/{session_id}/`
- Creates in-memory session

---

### 2. Start Analysis

**Endpoint:** `POST /analyze/{session_id}`

**Purpose:** Start resume analysis for selected companies with role descriptions

**Path Parameters:**
- `session_id`: UUID from upload response

**Request Body:**
```json
{
  "company": "Amazon",
  "role_description": "Amazon is seeking Software Development Engineer Interns...\n\nResponsibilities:\n- Design and implement...\n\nQualifications:\n- Currently pursuing BS in CS...",
  "target_deadline": "2026-09-01"
}
```

**Request Schema:**
- `company`: String (required)
  - Valid values: "Amazon", "Meta", "Google"
- `role_description`: String (required)
  - Must be non-empty string (min 50 characters)
  - Should contain full role posting text
- `target_deadline`: ISO date string (optional)
  - Default: Next September 1st

**Validation Rules:**
- `company` must be one of: "Amazon", "Meta", "Google"
- `role_description` must be at least 50 characters
- Role description cannot be empty or whitespace only

**Note:** Single company analysis per request. User can analyze multiple companies by making separate requests.

**Response (200 OK):**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "analyzing",
  "message": "Analysis started"
}
```

**Errors:**
- `404`: Session not found
- `400`: Validation errors:
  - No resume uploaded
  - Invalid company name
  - Missing role_description field
  - Role description too short (< 50 chars)
  - Role description is empty or whitespace
- `500`: Analysis failed to start

**Error Examples:**
```json
// Invalid company
{
  "error": "Validation error",
  "message": "Invalid company name",
  "details": {
    "company": "Apple",
    "valid_companies": ["Amazon", "Meta", "Google"]
  }
}

// Role description too short
{
  "error": "Validation error", 
  "message": "Role description must be at least 50 characters",
  "details": {
    "length": 25,
    "minimum": 50
  }
}
```

**Notes:**
- Runs analysis as background task
- Updates session status to "analyzing"
- Role description is PRIMARY evaluation criteria
- Company tenets provide supplemental context
- Evaluation focuses on specific role requirements from role posting
- Client should poll `/status/{session_id}` for completion
- Single company per analysis (user can run multiple analyses for different companies)

---

### 3. Check Analysis Status

**Endpoint:** `GET /status/{session_id}`

**Purpose:** Check current analysis status

**Path Parameters:**
- `session_id`: UUID from upload response

**Response (200 OK):**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "analyzing",
  "message": "Analysis in progress",
  "progress": 60
}
```

**Status Values:**
- `"uploaded"`: Resume uploaded, not yet analyzing
- `"analyzing"`: Analysis in progress
- `"complete"`: Analysis finished successfully
- `"error"`: Analysis failed

**Response Fields:**
- `session_id`: UUID string
- `status`: Current status (required)
- `message`: Human-readable status message (required)
- `progress`: 0-100 percentage (optional)

**Errors:**
- `404`: Session not found

**Notes:**
- Poll every 2-3 seconds while status is "analyzing"
- When status is "complete", call `/results/{session_id}`
- If status is "error", display error message

---

### 4. Get Analysis Results

**Endpoint:** `GET /results/{session_id}`

**Purpose:** Retrieve complete analysis results

**Path Parameters:**
- `session_id`: UUID from upload response

**Response (200 OK):**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2026-01-10T15:30:00Z",
  "student_info": {
    "name": "John Doe",
    "email": "john@example.com",
    "gpa": 3.8,
    "graduation_date": "May 2026",
    "major": "Computer Science"
  },
  "evaluation": {
    "company": "Amazon",
    "role": "Software Development Engineer Intern",
    "overall_score": 75.5,
      "category_scores": [
        {
          "category": "Technical Skills",
          "score": 80.0,
          "feedback": "Strong foundation in data structures...",
          "examples": ["Implemented binary search tree in Java"]
        },
        {
          "category": "Role-Specific Requirements",
          "score": 70.0,
          "feedback": "Meets most requirements from role description...",
          "examples": ["Has required CS degree", "Missing: AWS experience"]
        }
      ],
      "strengths": [
        "Strong academic performance with 3.8 GPA",
        "Relevant coursework in algorithms and systems",
        "Matches 8/10 required qualifications from role posting"
      ],
      "gaps": [
        {
          "category": "projects",
          "description": "Limited distributed systems experience",
          "impact": "high",
          "current_state": "Built small-scale projects",
          "desired_state": "Experience with scalable systems"
        },
        {
          "category": "role_specific",
          "description": "No AWS or cloud platform experience",
          "impact": "medium",
          "current_state": "No cloud experience mentioned",
          "desired_state": "Familiarity with AWS services (from role description)"
        }
      ],
      "company_fit_analysis": "Demonstrates several Amazon Leadership Principles...",
      "role_fit_analysis": "Strong match for core requirements. Missing preferred qualifications around cloud experience...",
      "competitive_positioning": "Above average candidate for SDE intern role..."
  },
  "recommendations": [
    {
      "id": "rec-1",
      "priority": "high",
      "category": "projects",
      "action": "Build a distributed key-value store",
      "rationale": "Demonstrates system design skills valued by all three companies",
      "timeline": "2-3 months",
      "effort_estimate": "8-10 weeks",
      "resources": [
        "MIT 6.824 Distributed Systems course",
        "Designing Data-Intensive Applications book"
      ],
      "companies_benefiting": ["Amazon", "Meta", "Google"]
    }
  ],
  "timeline": {
    "target_deadline": "2026-09-01",
    "created_at": "2026-01-10T15:30:00Z",
    "phases": [
      {
        "name": "Immediate (0-4 weeks)",
        "duration_weeks": 4,
        "start_date": "2026-01-10",
        "end_date": "2026-02-07",
        "goals": [
          "Complete high-priority quick wins",
          "Start distributed systems project"
        ],
        "actions": [
          "Update resume with quantified achievements",
          "Begin MIT 6.824 course"
        ]
      }
    ],
    "milestones": [
      {
        "date": "2026-02-07",
        "title": "Complete Phase 1",
        "deliverables": ["Updated resume", "Course progress"]
      }
    ]
  },
  "summary": {
    "overall_readiness": "Above Average",
    "score": 75.5,
    "key_strengths": ["Strong academics", "Good fundamentals"],
    "critical_gaps": ["System design", "Leadership experience"],
    "recommendation_count": 8
  }
}
```

**Errors:**
- `404`: Session not found
- `400`: Analysis not complete yet
- `500`: Failed to load results

**Notes:**
- Results loaded from filesystem JSON files
- Large response - may be 50-200KB
- Cache on frontend to avoid repeated calls

---

### 5. Download Report

**Endpoint:** `GET /download/{session_id}/report`

**Purpose:** Download PDF report

**Path Parameters:**
- `session_id`: UUID from upload response

**Response (200 OK):**
- Content-Type: `application/pdf`
- Content-Disposition: `attachment; filename="ready2intern_report_{session_id}.pdf"`
- Body: PDF file binary

**Errors:**
- `404`: Report not found
- `400`: Analysis not complete

**Notes:**
- PDF generated during analysis
- Saved to `data/results/{session_id}/report.pdf`
- Typical size: 200-500KB

---

### 6. Delete Session (Optional)

**Endpoint:** `DELETE /session/{session_id}`

**Purpose:** Delete session and all associated files

**Path Parameters:**
- `session_id`: UUID from upload response

**Response (200 OK):**
```json
{
  "message": "Session deleted successfully"
}
```

**Errors:**
- `404`: Session not found

**Notes:**
- Removes from in-memory sessions
- Deletes all files from filesystem
- Use for cleanup after user downloads report

---

## Data Models

### Student Info
```
{
  name: string
  email: string (optional)
  phone: string (optional)
  linkedin: string (optional)
  github: string (optional)
  location: string (optional)
  gpa: number (0.0-4.0, optional)
  graduation_date: string
  major: string
  minor: string (optional)
}
```

### Education
```
{
  institution: string
  degree: string
  major: string
  minor: string (optional)
  gpa: number (optional)
  graduation_date: string
  relevant_coursework: string[]
  honors: string[]
}
```

### Experience
```
{
  company: string
  title: string
  location: string (optional)
  start_date: string
  end_date: string (optional, null if current)
  description: string[]
  technologies: string[]
  achievements: string[]
}
```

### Project
```
{
  name: string
  description: string
  technologies: string[]
  url: string (optional)
  github_url: string (optional)
  highlights: string[]
  date: string (optional)
}
```

### Category Score
```
{
  category: string
  score: number (0-100)
  feedback: string
  examples: string[]
}
```

### Gap
```
{
  category: string
  description: string
  impact: "high" | "medium" | "low"
  current_state: string
  desired_state: string
}
```

### Recommendation
```
{
  id: string
  priority: "high" | "medium" | "low"
  category: string
  action: string
  rationale: string
  timeline: string
  effort_estimate: string
  resources: string[]
  companies_benefiting: string[]
}
```

### Timeline Phase
```
{
  name: string
  duration_weeks: number
  start_date: string (ISO date)
  end_date: string (ISO date)
  goals: string[]
  actions: string[]
}
```

### Milestone
```
{
  date: string (ISO date)
  title: string
  deliverables: string[]
}
```

---

## Error Response Format

**All errors follow this structure:**
```json
{
  "error": "Error type",
  "message": "Human-readable error message",
  "details": {
    "field": "Additional context"
  }
}
```

**Common HTTP Status Codes:**
- `200`: Success
- `400`: Bad request (validation error)
- `404`: Resource not found
- `500`: Internal server error

---

## Rate Limits

**POC (No limits):**
- Unlimited requests
- Single user assumed

**Future (MVP):**
- 10 uploads per hour per user
- 100 API calls per hour per user

---

## CORS Configuration

**Allowed Origins:**
- `http://localhost:5173` (Vite dev server)
- `http://localhost:3000` (Alternative)

**Allowed Methods:**
- GET, POST, DELETE

**Allowed Headers:**
- Content-Type, Authorization (future)

---

## File Upload Specifications

### Supported Formats
- **PDF**: `.pdf` (preferred)
- **DOCX**: `.docx` (Microsoft Word)

### Constraints
- **Max Size**: 5MB
- **Max Pages**: No limit (but affects processing time)
- **Encoding**: UTF-8 text extraction

### Validation Rules
1. File extension must be `.pdf` or `.docx`
2. File size must be ≤ 5MB
3. File must contain extractable text
4. Filename sanitized (special chars removed)

---

## Analysis Process

### Background Task Flow
```
1. Extract text from resume (5-10 seconds)
2. Document Agent: Parse resume (10-15 seconds)
3. Evaluation Agent: Score for each company (10-15 seconds each)
4. Recommendation Agent: Generate suggestions (10-15 seconds)
5. Planner Agent: Create timeline (10-15 seconds)
6. Save results to filesystem (1-2 seconds)
7. Update session status to "complete"
```

**Total Time:** 45-75 seconds for 3 companies

### Status Updates
- Client should poll `/status/{session_id}` every 2-3 seconds
- Backend updates status after each agent completes
- Progress percentage calculated based on completed agents

---

## Response Times (Target)

| Endpoint | Target | Max Acceptable |
|----------|--------|----------------|
| POST /upload | < 2s | 5s |
| POST /analyze | < 1s | 2s |
| GET /status | < 500ms | 1s |
| GET /results | < 1s | 3s |
| GET /download | < 2s | 5s |

---

## Example Usage Flow

### Happy Path
```
1. Upload resume
   POST /upload
   → {session_id: "abc-123", status: "uploaded"}

2. Start analysis with role description (required)
   POST /analyze/abc-123
   Body: {
     company: "Amazon",
     role_description: "Software Development Engineer Intern\n\nWe are seeking...\n\nRequired:\n- BS in CS\n- Data structures\n- Algorithms\n\nPreferred:\n- AWS experience\n- Distributed systems"
   }
   → {status: "analyzing"}

3. Poll status (repeat until complete)
   GET /status/abc-123
   → {status: "analyzing", progress: 30}
   ... wait 2 seconds ...
   GET /status/abc-123
   → {status: "analyzing", progress: 60}
   ... wait 2 seconds ...
   GET /status/abc-123
   → {status: "complete"}

4. Get results
   GET /results/abc-123
   → {evaluation: {...}, recommendations: [...], timeline: {...}}
   → Results include role-specific evaluation based on role description

5. Download report
   GET /download/abc-123/report
   → PDF file
```

### Error Handling
```
1. Upload invalid file
   POST /upload (with .txt file)
   → 400 {error: "Invalid file type", message: "Only PDF and DOCX allowed"}

2. Analyze without role description
   POST /analyze/abc-123
   Body: {company: "Amazon"}
   → 400 {error: "Validation error", message: "Role description is required"}

3. Analyze with invalid company
   POST /analyze/abc-123
   Body: {
     company: "Apple",
     role_description: "..."
   }
   → 400 {error: "Validation error", message: "Invalid company name", details: {valid_companies: ["Amazon", "Meta", "Google"]}}

4. Analyze with short role description
   POST /analyze/abc-123
   Body: {
     company: "Amazon",
     role_description: "SDE Intern"
   }
   → 400 {error: "Validation error", message: "Role description must be at least 50 characters", details: {length: 10, minimum: 50}}

5. Analyze non-existent session
   POST /analyze/invalid-id
   → 404 {error: "Session not found", message: "Session invalid-id does not exist"}

6. Get results before complete
   GET /results/abc-123 (while status is "analyzing")
   → 400 {error: "Analysis not complete", message: "Status: analyzing"}
```

---

## Frontend Integration Guide

### State Management
```
1. Store session_id after upload
2. Store selected company (single)
3. Store role description for selected company
4. Validate company selected and role description provided
5. Poll status during analysis
6. Store results after completion
7. Allow new analysis without page reload
```

### Dashboard UI Flow
```
Single Page Dashboard:

┌──────────────────────────────────────────────────────────┐
│ Ready2Intern                                             │
├────────────────────┬─────────────────────────────────────┤
│ LEFT PANEL         │ RIGHT PANEL                         │
│                    │                                     │
│ 1. Upload Resume   │ [Empty State]                       │
│ ┌────────────────┐ │                                     │
│ │ Drag & Drop    │ │ Upload your resume and select      │
│ │ or Click       │ │ a company to begin analysis        │
│ └────────────────┘ │                                     │
│ ✓ resume.pdf       │                                     │
│                    │                                     │
│ 2. Select Company  │                                     │
│ ┌───┐ ┌───┐ ┌───┐ │                                     │
│ │AWS│ │META│ │GOO│ │  ← Company logos (clickable)       │
│ └─●─┘ └───┘ └───┘ │                                     │
│   Selected         │                                     │
│                    │                                     │
│ 3. Role Description │                                     │
│ ┌────────────────┐ │                                     │
│ │ Paste Amazon   │ │                                     │
│ │ SDE Intern role │ │                                     │
│ │ description... │ │                                     │
│ │                │ │                                     │
│ └────────────────┘ │                                     │
│ ✓ 250 characters   │                                     │
│                    │                                     │
│ [Analyze Resume]   │                                     │
│                    │                                     │
└────────────────────┴─────────────────────────────────────┘

After clicking "Analyze Resume":

┌──────────────────────────────────────────────────────────┐
│ Ready2Intern                                             │
├────────────────────┬─────────────────────────────────────┤
│ LEFT PANEL         │ RIGHT PANEL                         │
│ (locked during     │                                     │
│  analysis)         │ [Loading State]                     │
│                    │                                     │
│ ✓ resume.pdf       │     [Spinner Animation]             │
│ ✓ Amazon selected  │                                     │
│ ✓ Role description  │  Analyzing your resume...           │
│                    │                                     │
│                    │  ████████░░░░░░░░░ 60%              │
│                    │                                     │
│                    │  Evaluating against Amazon          │
│                    │  criteria...                        │
│                    │                                     │
└────────────────────┴─────────────────────────────────────┘

After analysis complete:

┌──────────────────────────────────────────────────────────┐
│ Ready2Intern                                             │
├────────────────────┬─────────────────────────────────────┤
│ LEFT PANEL         │ RIGHT PANEL                         │
│                    │                                     │
│ [New Analysis]     │ [Results State]                     │
│ button to reset    │                                     │
│                    │ Amazon - SDE Intern                 │
│ Or change company  │ ┌─────┐                             │
│ to analyze same    │ │ 75  │ Above Average Fit           │
│ resume for         │ └─────┘                             │
│ different company  │                                     │
│                    │ ▼ Gap Analysis                      │
│                    │ ▼ Recommendations (8)               │
│                    │ ▼ Timeline                          │
│                    │                                     │
│                    │ [Download Report]                   │
│                    │                                     │
└────────────────────┴─────────────────────────────────────┘
```

### Validation
- Client-side: Check resume uploaded
- Client-side: Check company selected
- Client-side: Check role description >= 50 characters
- Server-side: Validate same rules, return 400 if invalid
- Show inline validation feedback in left panel
- "Analyze Resume" button disabled until all valid
```

### Error Display
- Show validation errors inline (file upload)
- Show toast/alert for API errors
- Show retry button for 500 errors
- Show helpful message for 404 errors

### Loading States
- Upload: Show progress bar
- Analysis: Show animated loader with status message
- Results: Show skeleton while loading
- Download: Show download progress

---

## Testing Checklist

### Upload Endpoint
- ✅ Valid PDF upload succeeds
- ✅ Valid DOCX upload succeeds
- ✅ Invalid file type rejected (400)
- ✅ File too large rejected (400)
- ✅ Returns valid UUID session_id

### Analysis Endpoint
- ✅ Valid companies accepted
- ✅ 1-3 companies allowed
- ✅ Invalid company name rejected (400)
- ✅ Missing role_descriptions rejected (400)
- ✅ Missing role description for company rejected (400)
- ✅ Role description too short rejected (400)
- ✅ Empty/whitespace role description rejected (400)
- ✅ Non-existent session rejected (404)
- ✅ Analysis starts in background

### Status Endpoint
- ✅ Returns current status
- ✅ Status updates during analysis
- ✅ Progress increases over time
- ✅ Non-existent session rejected (404)

### Results Endpoint
- ✅ Returns complete results when ready
- ✅ Rejects if analysis not complete (400)
- ✅ All required fields present
- ✅ Valid JSON structure

### Download Endpoint
- ✅ Returns PDF file
- ✅ Correct content-type header
- ✅ Correct filename
- ✅ Rejects if report not ready (404)

---

## Implementation Notes

### Backend
- Use FastAPI for automatic OpenAPI docs
- Use Pydantic models for request/response validation
- Use background tasks for analysis
- Use structured logging for debugging

### Frontend
- Use Axios for HTTP client
- Implement exponential backoff for polling
- Cache results to avoid repeated calls
- Handle network errors gracefully

### File Storage
- Create session directories on upload
- Save all results as JSON files
- Clean up old sessions periodically (future)

### LLM Integration
- Each agent makes 1-3 Claude API calls
- Use extended thinking for better results
- Implement retry logic for API failures
- Parse JSON responses carefully

---

## Future Enhancements (MVP)

### Authentication
- Add JWT tokens
- User registration/login
- Session ownership validation

### Additional Endpoints
- `GET /history` - List past evaluations
- `POST /compare` - Compare multiple resumes
- `GET /analytics` - Usage statistics

### Webhooks
- Notify when analysis complete
- Email report to user

### Batch Processing
- Upload multiple resumes
- Compare against peers

---

## API Versioning

**Current:** v1 (implicit in `/api` prefix)

**Future:** Add version to path
- `/api/v1/upload`
- `/api/v2/upload` (when breaking changes needed)

---

**This API specification provides everything needed to implement the backend and integrate the frontend without prescribing implementation details.**
