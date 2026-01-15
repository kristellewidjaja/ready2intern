# User Stories - Ready2Intern

## Epic Overview

### Epic 1: Document Upload and Management
Students can upload their resume and target job description to begin the evaluation process

### Epic 2: Document Processing
System processes uploaded documents to extract structured data for analysis

### Epic 3: Company-Specific Evaluation
System evaluates resumes using company-specific organizational principles and criteria

### Epic 4: Analysis Results and Reporting
Students receive comprehensive analysis with probability, strengths, gaps, and actionable feedback

### Epic 5: Development Planning
Students receive personalized timeline-based plans for improving their internship readiness

### Epic 6: Agent Orchestration and Session Management
Multi-agent system coordinates workflow with proper session and state management

### Epic 7: API and Frontend Integration
Frontend application integrates with backend services via REST API

---

## Epic 1: Document Upload and Management

### US-001: Upload Resume
**As a** college student seeking internships  
**I want** to upload my resume in PDF format  
**So that** the system can evaluate my qualifications against internship requirements

#### Acceptance Criteria:
- **Given** I am on the upload page  
  **When** I select a PDF resume file under 10MB  
  **Then** the file uploads successfully within 5 seconds
- **Given** I upload a resume  
  **When** the file is not PDF format  
  **Then** I see a clear error message asking for PDF format
- **Given** I upload a resume over 10MB  
  **When** validation runs  
  **Then** I see an error message about file size limit

#### Definition of Done:
- [ ] File upload component implemented with drag-and-drop
- [ ] PDF validation and size checking functional
- [ ] Clear error messages displayed for invalid files
- [ ] Resume stored securely in S3
- [ ] Upload progress indicator shown

#### Story Points: 3  
#### Dependencies: None

---

### US-002: Upload Job Description
**As a** college student  
**I want** to upload the internship job description  
**So that** my resume can be evaluated against specific job requirements

#### Acceptance Criteria:
- **Given** I have uploaded my resume  
  **When** I upload a job description PDF under 5MB  
  **Then** the file uploads successfully within 5 seconds
- **Given** I upload a job description  
  **When** the system processes it  
  **Then** key requirements are extracted for comparison

#### Definition of Done:
- [ ] Job description upload component implemented
- [ ] PDF validation functional
- [ ] File stored in S3 with session association

#### Story Points: 2  
#### Dependencies: US-001

---

### US-003: Select Target Company
**As a** college student  
**I want** to select which company I'm applying to (Amazon, Meta, or Google)  
**So that** I receive company-specific evaluation and guidance

#### Acceptance Criteria:
- **Given** I have uploaded resume and job description  
  **When** I see company selection options  
  **Then** I can choose Amazon, Meta, or Google
- **Given** I select a company  
  **When** evaluation begins  
  **Then** company-specific sub-agent is triggered

#### Definition of Done:
- [ ] Company selection UI component implemented
- [ ] Selection triggers appropriate evaluation logic
- [ ] Company context passed to analysis agents

#### Story Points: 2  
#### Dependencies: US-001, US-002

---

## Epic 2: Document Processing

### US-004: Process Documents with MCP Tools
**As a** system  
**I want** to extract text and structured data from PDF documents  
**So that** agents can analyze resume and job description content

#### Acceptance Criteria:
- **Given** documents are uploaded  
  **When** Document Agent processes them  
  **Then** text is extracted within 10 seconds
- **Given** PDF has standard format  
  **When** processing occurs  
  **Then** structured sections (education, experience, skills) are identified

#### Definition of Done:
- [ ] MCP tool integration for PDF processing
- [ ] Text extraction functional for common PDF formats
- [ ] Error handling for corrupted or unreadable files
- [ ] Extracted data stored for analysis

#### Story Points: 5  
#### Dependencies: US-001, US-002

---

## Epic 3: Company-Specific Evaluation

### US-005: Load Company Principles
**As a** system  
**I want** to load company organizational principles from file system  
**So that** evaluation can align with company culture and values

#### Acceptance Criteria:
- **Given** company is selected  
  **When** principles loading occurs  
  **Then** document is loaded from `project-doc/organization-context/`
- **Given** principles file is missing  
  **When** loading fails  
  **Then** system falls back to generic evaluation criteria

#### Definition of Done:
- [ ] File system loading mechanism implemented
- [ ] Principles caching for session
- [ ] Graceful fallback for missing files
- [ ] Document-based approach (not knowledge base)

#### Story Points: 3  
#### Dependencies: None

---

### US-006: Analyze Resume Content
**As a** system  
**I want** to analyze resume against job requirements and company criteria  
**So that** I can provide accurate evaluation and feedback

#### Acceptance Criteria:
- **Given** resume and job description are processed  
  **When** Analyzer Agent evaluates  
  **Then** analysis covers GPA, coursework, projects, leadership, experience
- **Given** company principles are loaded  
  **When** evaluation occurs  
  **Then** resume is assessed against company-specific values

#### Definition of Done:
- [ ] Analyzer Agent implemented with Claude 3.7 Sonnet
- [ ] Analysis considers academic level (Freshman-Senior)
- [ ] Structured analysis data generated
- [ ] Company-specific criteria applied

#### Story Points: 8  
#### Dependencies: US-004, US-005

---

### US-010: Provide Company-Specific Feedback
**As a** college student  
**I want** to receive company-specific evaluation  
**So that** I understand how to align my profile with company culture

#### Acceptance Criteria:
- **Given** analysis is complete  
  **When** company specialist sub-agent evaluates  
  **Then** feedback references company principles (e.g., Leadership Principles)
- **Given** company-specific feedback is generated  
  **When** I read the report  
  **Then** I see how my experiences map to company values

#### Definition of Done:
- [ ] Company specialist sub-agents implemented
- [ ] Feedback maps experiences to principles
- [ ] Recommendations explain how to demonstrate values

#### Story Points: 5  
#### Dependencies: US-006, US-005

---

## Epic 4: Analysis Results and Reporting

### US-007: Calculate Acceptance Probability
**As a** college student  
**I want** to see my estimated acceptance probability  
**So that** I can gauge my competitiveness

#### Acceptance Criteria:
- **Given** resume analysis is complete  
  **When** probability calculation runs  
  **Then** I see a percentage (0-100%) with confidence level
- **Given** probability is calculated  
  **When** methodology is applied  
  **Then** calculation is based on resume-job alignment and company criteria

#### Definition of Done:
- [ ] Probability calculation algorithm implemented
- [ ] Percentage displayed with confidence level
- [ ] Calculation methodology documented

#### Story Points: 5  
#### Dependencies: US-006

---

### US-008: Identify Strengths
**As a** college student  
**I want** to see my key strengths  
**So that** I can emphasize them in interviews

#### Acceptance Criteria:
- **Given** analysis is complete  
  **When** strengths are identified  
  **Then** I see 3-5 key strengths with specific examples from my resume
- **Given** strengths are identified  
  **When** I review them  
  **Then** they are presented in student-friendly, encouraging language

#### Definition of Done:
- [ ] Strengths identification logic implemented
- [ ] 3-5 strengths extracted with evidence
- [ ] Student-friendly language used

#### Story Points: 3  
#### Dependencies: US-006

---

### US-009: Identify Improvement Areas
**As a** college student  
**I want** to see areas where I can improve  
**So that** I can strengthen my application

#### Acceptance Criteria:
- **Given** analysis identifies gaps  
  **When** I review feedback  
  **Then** I see 3-5 specific, actionable improvement areas
- **Given** gaps are presented  
  **When** I read them  
  **Then** feedback is constructive and prioritized by importance

#### Definition of Done:
- [ ] Gap identification logic implemented
- [ ] Gaps prioritized by impact
- [ ] Constructive, student-friendly language

#### Story Points: 3  
#### Dependencies: US-006

---

### US-012: Receive Comprehensive Report
**As a** college student  
**I want** to receive a complete analysis report  
**So that** I have all feedback in one accessible document

#### Acceptance Criteria:
- **Given** all analysis is complete  
  **When** report is generated  
  **Then** it includes probability, strengths, gaps, company evaluation, and development plan
- **Given** report is ready  
  **When** I view it  
  **Then** content is clear, well-structured, and student-friendly

#### Definition of Done:
- [ ] Report generation implemented
- [ ] All sections included and formatted
- [ ] Report exportable/printable
- [ ] Student-friendly language throughout

#### Story Points: 3  
#### Dependencies: US-007, US-008, US-009, US-010, US-011

---

## Epic 5: Development Planning

### US-011: Receive Development Plan
**As a** college student  
**I want** to receive a timeline-based development plan  
**So that** I can systematically improve my candidacy

#### Acceptance Criteria:
- **Given** gaps are identified  
  **When** Planner Agent creates plan  
  **Then** I receive specific action items with timeline
- **Given** plan is generated  
  **When** I review it  
  **Then** actions are prioritized and aligned with application deadlines

#### Definition of Done:
- [ ] Planner Agent implemented
- [ ] Timeline aligned with internship cycles
- [ ] Actions prioritized by impact
- [ ] Milestone checkpoints included

#### Story Points: 5  
#### Dependencies: US-009

---

## Epic 6: Agent Orchestration and Session Management

### US-013: Manage Evaluation Session
**As a** system  
**I want** to create and manage unique sessions  
**So that** student data is properly isolated and workflow state is maintained

#### Acceptance Criteria:
- **Given** student initiates evaluation  
  **When** session is created  
  **Then** unique session ID is generated and stored in DynamoDB
- **Given** session exists  
  **When** workflow progresses  
  **Then** all documents and analysis are associated with session

#### Definition of Done:
- [ ] Session creation and storage implemented
- [ ] Session data persisted in DynamoDB
- [ ] Session isolation enforced
- [ ] Session expiration after 24 hours

#### Story Points: 5  
#### Dependencies: None

---

### US-014: Orchestrate Multi-Agent Workflow
**As a** system  
**I want** to coordinate workflow across specialized agents  
**So that** evaluation proceeds correctly from document processing to final report

#### Acceptance Criteria:
- **Given** evaluation is initiated  
  **When** Orchestrator Agent runs  
  **Then** agents are invoked in sequence (Document → Analyzer → Planner)
- **Given** agent errors occur  
  **When** Orchestrator handles them  
  **Then** error recovery or graceful degradation is applied

#### Definition of Done:
- [ ] Orchestrator Agent using AgentCore Runtime
- [ ] Sequential agent invocation implemented
- [ ] Error handling and recovery logic
- [ ] Workflow progress tracking

#### Story Points: 8  
#### Dependencies: US-013

---

### US-015: Persist Conversation Memory
**As a** system  
**I want** to persist conversation history using AgentCore Memory  
**So that** context is maintained across agent invocations

#### Acceptance Criteria:
- **Given** agents are invoked  
  **When** Memory primitive is used  
  **Then** messages and analysis persist beyond single request
- **Given** session is active  
  **When** memory is accessed  
  **Then** full conversation context is available

#### Definition of Done:
- [ ] AgentCore Memory integration
- [ ] Conversation history persistence
- [ ] Memory accessible across invocations

#### Story Points: 3  
#### Dependencies: US-013

---

### US-017: Manage Session Identity
**As a** system  
**I want** to associate documents and analysis with session identity  
**So that** data is properly scoped and secure

#### Acceptance Criteria:
- **Given** session is created  
  **When** Identity primitive is used  
  **Then** all operations are associated with session identity
- **Given** multiple sessions exist  
  **When** data is accessed  
  **Then** no cross-session data leakage occurs

#### Definition of Done:
- [ ] AgentCore Identity integration
- [ ] Session-scoped data access
- [ ] Identity integrated with other primitives

#### Story Points: 3  
#### Dependencies: US-013

---

## Epic 7: API and Frontend Integration

### US-016: Provide REST API Endpoints
**As a** frontend application  
**I want** to interact with backend via REST API  
**So that** I can submit evaluation requests and retrieve results

#### Acceptance Criteria:
- **Given** API is deployed  
  **When** frontend calls endpoints  
  **Then** upload, analysis initiation, and results retrieval work correctly
- **Given** API uses AgentCore Gateway  
  **When** requests are routed  
  **Then** appropriate Lambda functions are invoked

#### Definition of Done:
- [ ] API Gateway configured with AgentCore
- [ ] REST endpoints implemented (POST /upload, POST /evaluate, GET /results)
- [ ] Standard HTTP status codes used
- [ ] JSON request/response format

#### Story Points: 5  
#### Dependencies: None

---

## Story Prioritization and Sprint Planning

### Sprint 1: Foundation (Weeks 1-2)
**Priority 1 – Critical Path**
- US-001: Upload Resume (3 points)
- US-002: Upload Job Description (2 points)
- US-003: Select Target Company (2 points)
- US-013: Manage Evaluation Session (5 points)
- US-016: Provide REST API Endpoints (5 points)
- **Total: 17 points**

### Sprint 2: Document Processing and Analysis (Weeks 3-4)
**Priority 1 – Core Functionality**
- US-004: Process Documents with MCP Tools (5 points)
- US-005: Load Company Principles (3 points)
- US-006: Analyze Resume Content (8 points)
- US-014: Orchestrate Multi-Agent Workflow (8 points)
- **Total: 24 points**

### Sprint 3: Analysis Results (Weeks 5-6)
**Priority 2 – User Value Delivery**
- US-007: Calculate Acceptance Probability (5 points)
- US-008: Identify Strengths (3 points)
- US-009: Identify Improvement Areas (3 points)
- US-010: Provide Company-Specific Feedback (5 points)
- US-011: Receive Development Plan (5 points)
- **Total: 21 points**

### Sprint 4: Reporting and Polish (Weeks 7-8)
**Priority 2 – Polish and Complete**
- US-012: Receive Comprehensive Report (3 points)
- US-015: Persist Conversation Memory (3 points)
- US-017: Manage Session Identity (3 points)
- Testing, bug fixes, and polish
- **Total: 9 points + testing**

---

## Acceptance Criteria Summary

### Definition of Ready Checklist
- [ ] User story follows INVEST criteria (Independent, Negotiable, Valuable, Estimable, Small, Testable)
- [ ] Acceptance criteria are specific and testable
- [ ] Dependencies identified and resolved
- [ ] Story points estimated
- [ ] Business value clearly articulated

### Definition of Done Checklist
- [ ] All acceptance criteria met
- [ ] Unit tests written (>60% coverage)
- [ ] Integration testing completed
- [ ] Code reviewed
- [ ] CloudWatch logging implemented
- [ ] Documentation updated
- [ ] POC acceptance by stakeholders

---

## Traceability to Requirements

### Functional Requirements Coverage
- FR-001 → US-001
- FR-002 → US-002
- FR-003 → US-003
- FR-004 → US-004
- FR-005 → US-005
- FR-006 → US-006
- FR-007 → US-007
- FR-008 → US-008
- FR-009 → US-009
- FR-010 → US-010
- FR-011 → US-011
- FR-012 → US-012
- FR-013 → US-013
- FR-014 → US-014
- FR-015 → US-015
- FR-016 → US-016
- FR-017 → US-017

### Non-Functional Requirements Coverage
- NFR-001 (Performance) → All stories (response time requirements)
- NFR-003 (Security) → US-013 (session isolation)
- NFR-006 (Usability) → US-001, US-002, US-003, US-012 (student-friendly)

---

## Success Metrics

### User Experience Metrics
- Time to complete evaluation < 2 minutes
- Student satisfaction score > 4.0/5.0
- Report clarity rating > 4.0/5.0

### Technical Performance Metrics
- API response time < 2 seconds (95th percentile)
- Document processing time < 10 seconds
- Complete analysis time < 30 seconds

### Business Success Metrics
- POC completion within 8 weeks
- All AgentCore primitives demonstrated
- Stakeholder approval for production planning

**Total Story Points**: 71 points  
**Estimated Duration**: 8 weeks (4 sprints)  
**Team Velocity Assumption**: 15-20 points per 2-week sprint
