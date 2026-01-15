# Ready2Intern POC - Development TODO

## Week 1: Project Setup & Basic Dashboard ✅

### Frontend Setup
- [x] Initialize Vite + React + TypeScript project
- [x] Install dependencies: Tailwind CSS, React Router, Axios
- [x] Configure Tailwind with custom theme colors (purple/blue gradient)
- [x] Set up project folder structure (components, pages, hooks, utils, types)
- [x] Create basic layout components: Header, Footer, MainLayout
- [x] Implement theme context and toggle hook
- [x] Build ThemeToggle button component
- [x] Create Dashboard page shell
- [x] Add responsive breakpoints and test mobile layout
- [x] Configure environment variables for API URL

### Backend Setup
- [x] Initialize FastAPI project with uv
- [x] Set up project structure: routers/, services/, models/, utils/
- [x] Create main.py with FastAPI app initialization
- [x] Configure CORS middleware for localhost:5173
- [x] Create .env.example with required variables
- [x] Implement health check endpoint GET /api/health
- [x] Create file system directories: data/resumes/, data/company-tenets/, data/sessions/
- [x] Add logging configuration
- [x] Create requirements.txt or pyproject.toml
- [x] Write README with setup and run instructions

### Integration & Testing
- [x] Test frontend runs on localhost:5173
- [x] Test backend runs on localhost:8000
- [x] Verify frontend can call health check endpoint
- [x] Test theme toggle in light and dark modes
- [x] Verify responsive layout on mobile and desktop

---

## Week 2: Resume Upload & Company Selection

### Resume Upload - Frontend
- [x] Create FileDropzone component
- [x] Add drag-and-drop event handlers
- [x] Implement click-to-upload fallback
- [x] Add file type validation (PDF, DOCX only)
- [x] Add file size validation (max 5MB)
- [x] Build upload progress indicator component
- [x] Create success/error toast notifications
- [x] Add file preview display after upload
- [x] Store session_id in React state/context
- [x] Handle upload errors with user-friendly messages

### Resume Upload - Backend
- [x] Create POST /api/upload endpoint
- [x] Implement file validation middleware
- [x] Generate unique session IDs (UUID)
- [x] Save uploaded files to data/resumes/ with naming convention
- [x] Return file metadata response (filename, size, session_id)
- [x] Add error handling for invalid files
- [x] Implement file cleanup on validation failure
- [x] Add file size limits to endpoint

### Company Selection - Frontend
- [x] Download company logos (Amazon, Meta, Google)
- [x] Create CompanyLogoSelector component
- [x] Implement single-select radio button logic
- [x] Add checkmark overlay for selected state
- [x] Style hover and selected states
- [x] Store selected company in state
- [x] Add company selection validation

### Company Selection - Backend
- [x] Create GET /api/companies endpoint
- [x] Define company data structure (name, logo_url, color, tenets_file)
- [x] Store company logos in public/logos/
- [x] Create company tenets files in data/company-tenets/:
  - [x] amazon-leadership-principles.txt
  - [x] meta-core-values.txt
  - [x] google-principles.txt
- [x] Return company list with metadata

### Integration & Testing
- [x] Test end-to-end resume upload flow
- [x] Verify files persist in data/resumes/
- [x] Test company selection UI interaction
- [x] Verify session management works
- [x] Test error handling for invalid uploads

---

## Week 3: Role Description Input & Analyze Button

### Role Description Input - Frontend
- [x] Create RoleDescriptionInput component (textarea)
- [x] Implement character counter
- [x] Add real-time validation (min 50, max 10000 chars)
- [x] Display validation error messages
- [x] Add placeholder text with example
- [x] Store role description in state
- [x] Style textarea with proper sizing

### Role Description Input - Backend
- [x] Add role description validation to analyze endpoint
- [x] Validate minimum length (50 chars)
- [x] Validate maximum length (10,000 chars)
- [x] Return structured validation errors

### Analyze Button - Frontend
- [x] Create AnalyzeButton component
- [x] Implement disabled state logic (check all required fields)
- [x] Add loading spinner component
- [x] Display progress messages during analysis
- [x] Handle API call to /api/analyze
- [ ] Navigate to results page on success
- [ ] Show error modal on failure

### Analyze Button - Backend
- [x] Create POST /api/analyze endpoint
- [x] Define request schema (session_id, company, role_description, target_deadline)
- [x] Validate all required fields
- [x] Generate analysis_id
- [x] Return immediate response with analysis_id
- [x] Create session directory structure

### Integration & Testing
- [x] Test analyze button enable/disable logic
- [x] Verify all form fields are validated
- [x] Test loading state displays correctly
- [x] Verify API endpoint accepts requests
- [x] Test error handling for missing fields

---

## Week 4: LLM Integration (Resume & Role Matching)

### LLM Setup
- [ ] Install Anthropic SDK
- [ ] Configure API key in environment variables
- [ ] Create LLM service class/module
- [ ] Implement retry logic for API failures
- [ ] Add timeout handling
- [ ] Create prompt template utilities

### Resume Analysis - Backend
- [ ] Create resume parsing service
- [ ] Implement PDF text extraction (PyPDF2 or pdfplumber)
- [ ] Implement DOCX text extraction (python-docx)
- [ ] Create resume analysis prompt template
- [ ] Call Claude API with resume text
- [ ] Parse LLM response into structured format
- [ ] Extract: skills, experience, education, projects
- [ ] Save results to data/sessions/{session_id}/resume_analysis.json
- [ ] Add error handling for parsing failures

### Role Matching - Backend
- [ ] Create role matching service
- [ ] Load company tenets from file system
- [ ] Create role matching prompt template
- [ ] Combine resume + role description + company tenets
- [ ] Call Claude API for matching analysis
- [ ] Calculate ATS score (0-100)
- [ ] Calculate role match score (0-100)
- [ ] Calculate company fit score (0-100)
- [ ] Compute overall score (weighted average)
- [ ] Save results to data/sessions/{session_id}/match_analysis.json
- [ ] Add detailed explanations for each score

### Integration & Testing
- [ ] Test resume file reading from file system
- [ ] Verify Claude API calls succeed
- [ ] Test resume data extraction accuracy
- [ ] Verify match scores are calculated correctly
- [ ] Test error handling for API failures
- [ ] Verify all results saved to file system

---

## Week 5: LLM Integration (Gap Analysis & Timeline)

### Gap Analysis - Backend
- [ ] Create gap analysis service
- [ ] Load match analysis results
- [ ] Create gap identification prompt template
- [ ] Call Claude API to identify gaps
- [ ] Extract missing skills
- [ ] Extract missing experience areas
- [ ] Assign priority levels (High, Medium, Low)
- [ ] Generate actionable recommendations for each gap
- [ ] Provide specific examples and resources
- [ ] Save results to data/sessions/{session_id}/gap_analysis.json

### Timeline Generation - Backend
- [ ] Create timeline generation service
- [ ] Load gap analysis results
- [ ] Calculate days until target deadline
- [ ] Create timeline generation prompt template
- [ ] Call Claude API to generate timeline
- [ ] Structure timeline into phases:
  - [ ] Immediate (0-2 weeks)
  - [ ] Short-term (2-6 weeks)
  - [ ] Medium-term (6+ weeks)
- [ ] Assign specific tasks to each phase
- [ ] Create milestone checkpoints
- [ ] Add estimated hours per task
- [ ] Save results to data/sessions/{session_id}/timeline.json

### Integration & Testing
- [ ] Test gap analysis identifies relevant gaps
- [ ] Verify priorities are assigned correctly
- [ ] Test recommendations are actionable
- [ ] Verify timeline respects deadline
- [ ] Test timeline phases are logical
- [ ] Verify all results saved correctly

---

## Week 6: Results Display & Export

### Results Retrieval - Backend
- [ ] Create GET /api/results/{session_id} endpoint
- [ ] Load all analysis JSON files from session directory
- [ ] Combine into single response object
- [ ] Add error handling for missing files
- [ ] Return complete analysis results

### Overall Score Display - Frontend
- [ ] Create ResultsPage component
- [ ] Create OverallScoreCard component
- [ ] Implement animated circular progress bar
- [ ] Add score counting animation on mount
- [ ] Display gradient background based on score range
- [ ] Show status message (Excellent/Good/Needs Work)
- [ ] Add confetti animation for high scores (optional)

### Score Breakdown Display - Frontend
- [ ] Create CategoryScoreCard component
- [ ] Display three score cards: ATS, Role Match, Company Fit
- [ ] Implement individual progress bars
- [ ] Add hover tooltips with score explanations
- [ ] Make layout responsive (stacked on mobile)
- [ ] Add icons for each category

### Strengths & Gaps Display - Frontend
- [ ] Create StrengthsSection component
- [ ] Display list of strengths with evidence
- [ ] Create GapsSection component
- [ ] Display gaps with priority badges
- [ ] Implement expandable cards for details
- [ ] Show recommendations for each gap
- [ ] Add color coding for priority levels
- [ ] Include specific examples and resources

### Timeline Display - Frontend
- [ ] Create TimelineSection component
- [ ] Build timeline visualization (vertical or horizontal)
- [ ] Display phases with date ranges
- [ ] Show tasks within each phase
- [ ] Implement expandable phase sections
- [ ] Highlight milestones
- [ ] Add progress indicators (optional for POC)

### PDF Export - Backend
- [ ] Install PDF generation library (ReportLab or WeasyPrint)
- [ ] Create PDF template with branding
- [ ] Create POST /api/export/{session_id} endpoint
- [ ] Generate PDF with all sections:
  - [ ] Overall score
  - [ ] Score breakdown
  - [ ] Strengths
  - [ ] Gaps with recommendations
  - [ ] Timeline
- [ ] Format PDF with proper styling
- [ ] Return PDF file for download

### PDF Export - Frontend
- [ ] Add "Download PDF" button to results header
- [ ] Trigger API call on button click
- [ ] Show download progress indicator
- [ ] Handle download errors
- [ ] Provide success feedback

### Integration & Testing
- [ ] Test results endpoint returns complete data
- [ ] Verify all UI components display correctly
- [ ] Test animations and interactions
- [ ] Verify PDF generates with all content
- [ ] Test PDF download works
- [ ] Test responsive layout on all screen sizes

---

## Week 6: Error Handling, Polish & Deployment

### Error Handling - Frontend
- [ ] Add React error boundaries
- [ ] Implement toast notification system
- [ ] Create loading skeleton components
- [ ] Improve all error messages to be user-friendly
- [ ] Add "Start New Analysis" button
- [ ] Implement session cleanup on new analysis
- [ ] Add 404 page for invalid routes
- [ ] Add network error handling

### Error Handling - Backend
- [ ] Add comprehensive try-catch blocks
- [ ] Implement request validation with Pydantic
- [ ] Add structured logging (JSON format)
- [ ] Handle LLM API failures gracefully
- [ ] Add rate limiting middleware
- [ ] Implement request timeout handling
- [ ] Add health check for dependencies
- [ ] Create error response schemas

### Testing
- [ ] Write frontend unit tests for components
- [ ] Write frontend integration tests for user flows
- [ ] Write backend unit tests for services
- [ ] Write backend integration tests for endpoints
- [ ] Test all error paths
- [ ] Test edge cases (empty files, malformed data)
- [ ] Run accessibility audit
- [ ] Test cross-browser compatibility

### Polish & Optimization
- [ ] Optimize images and assets
- [ ] Add meta tags for SEO
- [ ] Implement loading states everywhere
- [ ] Add micro-interactions and transitions
- [ ] Optimize API response times
- [ ] Add request caching where appropriate
- [ ] Minify and bundle frontend assets
- [ ] Add favicon and app icons

### Documentation
- [ ] Update README with complete setup instructions
- [ ] Document API endpoints
- [ ] Add architecture diagram
- [ ] Document environment variables
- [ ] Create deployment guide
- [ ] Add troubleshooting section

### Deployment Preparation
- [ ] Create production environment config
- [ ] Set up environment variables for production
- [ ] Configure CORS for production domain
- [ ] Test production build locally
- [ ] Create deployment scripts
- [ ] Set up file system directories on server
- [ ] Configure Anthropic API key on server
- [ ] Test end-to-end in production environment

---

## Success Checklist

### Functionality
- [ ] Users can upload resume (PDF/DOCX)
- [ ] Users can select target company
- [ ] Users can paste role description
- [ ] Analysis completes in < 2 minutes
- [ ] Results display all sections correctly
- [ ] PDF export works with all content
- [ ] Users can start new analysis

### Performance
- [ ] Page load time < 2 seconds
- [ ] API response time < 3 seconds
- [ ] No memory leaks
- [ ] Smooth animations (60fps)

### Quality
- [ ] No console errors
- [ ] No linter warnings
- [ ] 80%+ test coverage
- [ ] All acceptance criteria met
- [ ] Responsive on mobile and desktop
- [ ] Accessible (keyboard navigation, screen readers)

### User Experience
- [ ] Clear feedback at every step
- [ ] Helpful error messages
- [ ] Intuitive workflow
- [ ] Professional visual design
- [ ] Loading states prevent confusion
