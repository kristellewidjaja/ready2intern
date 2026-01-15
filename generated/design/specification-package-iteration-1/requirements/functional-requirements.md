# Functional Requirements - Ready2Intern

## Overview
This document defines the functional requirements for the Ready2Intern AI Internship Readiness Platform, a multi-agent resume evaluation system built with Amazon Bedrock AgentCore and Claude 3.7 Sonnet.

**Project Scope**: POC (Proof of Concept)  
**Target Users**: College students (CS/Software Engineering, Freshman to Senior)  
**Target Companies**: Amazon, Meta, Google internship programs

---

## FR-001: Resume Document Upload
- **Description**: Students must be able to upload their resume in PDF format for evaluation
- **Business Justification**: Core capability enabling resume analysis workflow
- **Acceptance Criteria**:
  - System accepts PDF files up to 10MB
  - System validates file format before processing
  - System provides clear error messages for invalid files
  - System stores uploaded resumes securely in S3
  - Upload completes within 5 seconds for files under 5MB
- **Priority**: High
- **Dependencies**: None
- **Assumptions**: Students have resumes in PDF format
- **Source**: requirements.md - Workflow section

## FR-002: Job Description Upload
- **Description**: Students must be able to upload internship job descriptions in PDF format
- **Business Justification**: Enables targeted evaluation against specific internship requirements
- **Acceptance Criteria**:
  - System accepts PDF files up to 5MB
  - System validates file format before processing
  - System extracts key requirements from job description
  - System stores job descriptions securely in S3
  - Upload completes within 5 seconds
- **Priority**: High
- **Dependencies**: None
- **Assumptions**: Job descriptions are available in PDF format from company career sites
- **Source**: requirements.md - Workflow section

## FR-003: Company Selection
- **Description**: Students must be able to select target company for evaluation (Amazon, Meta, or Google)
- **Business Justification**: Enables company-specific evaluation criteria and feedback
- **Acceptance Criteria**:
  - System presents three company options: Amazon, Meta, Google
  - System allows single company selection per evaluation session
  - Selection triggers appropriate company specialist sub-agent
  - System loads company-specific evaluation criteria
- **Priority**: High
- **Dependencies**: FR-005 (Company Principles Loading)
- **Assumptions**: Company evaluation criteria available at selection time
- **Source**: requirements.md - Target Users section

## FR-004: Document Processing with MCP Tools
- **Description**: System must process PDF documents (resumes and job descriptions) using MCP tools to extract text and structured data
- **Business Justification**: Foundation for resume analysis and evaluation
- **Acceptance Criteria**:
  - Document Agent successfully extracts text from PDF files
  - System handles common PDF formats and encoding
  - System extracts structured data (sections, headings, key information)
  - Processing completes within 10 seconds for typical documents
  - System handles processing errors gracefully with retry logic
- **Priority**: High
- **Dependencies**: FR-001, FR-002
- **Assumptions**: MCP tools provide reliable PDF text extraction capabilities
- **Source**: requirements.md - Key Features, Architecture

## FR-005: Company Principles Loading
- **Description**: System must load company-specific organizational principles from file system documents
- **Business Justification**: Enables principles-based resume evaluation aligned with company culture
- **Acceptance Criteria**:
  - System loads principles document from `project-doc/organization-context/` directory
  - System caches principles data for evaluation session
  - System handles missing principles file gracefully (fallback to generic criteria)
  - Principles loaded before evaluation begins
  - Document-based approach (not knowledge base)
- **Priority**: High
- **Dependencies**: None (design requirement for future implementation)
- **Assumptions**: Amazon Leadership Principles document will be provided
- **Source**: requirements.md - Design Requirements section

## FR-006: Resume Analysis
- **Description**: Internship Analyzer Agent must evaluate resume against internship requirements and company-specific criteria
- **Business Justification**: Core value proposition - providing actionable resume feedback
- **Acceptance Criteria**:
  - System analyzes resume content (GPA, coursework, projects, leadership, experience)
  - System identifies alignment with internship requirements from job description
  - System evaluates against company-specific principles (when available)
  - Analysis considers student academic level (Freshman to Senior)
  - System generates structured analysis data for reporting
- **Priority**: High
- **Dependencies**: FR-004, FR-005
- **Assumptions**: Standard resume sections can be identified and extracted
- **Source**: requirements.md - Key Features, Architecture

## FR-007: Acceptance Probability Calculation
- **Description**: System must calculate and present estimated acceptance probability for selected internship
- **Business Justification**: Provides students with clear, actionable metric
- **Acceptance Criteria**:
  - System calculates probability percentage (0-100%)
  - Calculation based on resume alignment with job requirements
  - Calculation considers company-specific criteria
  - Probability presented with confidence level
  - Calculation methodology documented and repeatable
- **Priority**: Medium
- **Dependencies**: FR-006
- **Assumptions**: Sufficient data from resume and job description to estimate probability
- **Source**: requirements.md - Workflow section

## FR-008: Strengths Identification
- **Description**: System must identify and present student's strengths relevant to selected internship
- **Business Justification**: Builds confidence and highlights competitive advantages
- **Acceptance Criteria**:
  - System identifies 3-5 key strengths from resume
  - Strengths aligned with internship requirements
  - Strengths mapped to company principles (when available)
  - Strengths presented in student-friendly language
  - Specific examples cited from resume
- **Priority**: High
- **Dependencies**: FR-006
- **Assumptions**: Resumes contain identifiable strength indicators
- **Source**: requirements.md - Key Features, Workflow section

## FR-009: Gaps Identification
- **Description**: System must identify and present gaps or areas for improvement in student's profile
- **Business Justification**: Provides actionable feedback for improvement
- **Acceptance Criteria**:
  - System identifies 3-5 key gaps or improvement areas
  - Gaps specific to internship requirements
  - Gaps mapped to company expectations (when available)
  - Gaps presented constructively in student-friendly language
  - Gaps prioritized by importance for internship success
- **Priority**: High
- **Dependencies**: FR-006
- **Assumptions**: Gap identification possible from resume content and job requirements
- **Source**: requirements.md - Key Features, Workflow section

## FR-010: Company-Specific Evaluation
- **Description**: System must provide company-specific evaluation feedback based on organizational principles
- **Business Justification**: Differentiates platform with tailored, company-aligned guidance
- **Acceptance Criteria**:
  - Evaluation references company-specific principles (e.g., Amazon Leadership Principles)
  - Feedback maps resume experiences to company values
  - Evaluation explains how to demonstrate specific principles
  - Company specialist sub-agent provides targeted recommendations
  - Evaluation distinguishes between different companies' expectations
- **Priority**: High
- **Dependencies**: FR-005, FR-006
- **Assumptions**: Company principles documents available and loaded successfully
- **Source**: requirements.md - Key Features, Architecture, Design Requirements

## FR-011: Timeline-Based Development Plan
- **Description**: Student Planner Agent must create personalized timeline-based development plan aligned with application deadlines
- **Business Justification**: Provides actionable roadmap for improving candidacy
- **Acceptance Criteria**:
  - Plan includes specific action items addressing identified gaps
  - Timeline aligned with typical internship application cycles
  - Plan considers student's current academic level
  - Action items prioritized by impact and timeline feasibility
  - Plan includes milestone checkpoints
- **Priority**: High
- **Dependencies**: FR-009
- **Assumptions**: Standard internship application timelines are known
- **Source**: requirements.md - Key Features, Architecture

## FR-012: Student-Friendly Report Generation
- **Description**: System must generate comprehensive, student-friendly analysis report
- **Business Justification**: Ensures students can understand and act on feedback
- **Acceptance Criteria**:
  - Report includes acceptance probability, strengths, gaps, evaluation, and plan
  - Language appropriate for college students (clear, non-jargon)
  - Report structured with clear sections and headings
  - Visual elements enhance readability (when applicable)
  - Report exportable or printable
- **Priority**: High
- **Dependencies**: FR-007, FR-008, FR-009, FR-010, FR-011
- **Assumptions**: Students prefer comprehensive written reports
- **Source**: requirements.md - Key Features, Workflow section

## FR-013: Session Management
- **Description**: Orchestrator Agent must coordinate workflow and manage student evaluation sessions
- **Business Justification**: Ensures reliable multi-agent coordination and state management
- **Acceptance Criteria**:
  - System creates unique session for each evaluation request
  - Session state persisted in DynamoDB
  - Session includes all uploaded documents and generated analysis
  - Session recoverable in case of interruption
  - Session data accessible throughout agent workflow
  - Session properly closed after analysis completion
- **Priority**: High
- **Dependencies**: None
- **Assumptions**: DynamoDB provides adequate session persistence
- **Source**: requirements.md - Architecture, Configuration

## FR-014: Agent Orchestration
- **Description**: Orchestrator Agent must coordinate workflow across all specialized agents (Document, Analyzer, Planner)
- **Business Justification**: Core technical requirement for multi-agent architecture
- **Acceptance Criteria**:
  - Orchestrator invokes agents in correct sequence
  - Orchestrator passes data between agents correctly
  - Orchestrator handles agent errors gracefully
  - Orchestrator tracks workflow progress
  - Orchestrator uses AgentCore Runtime primitive
- **Priority**: High
- **Dependencies**: FR-013
- **Assumptions**: AgentCore Runtime provides necessary orchestration capabilities
- **Source**: requirements.md - Architecture, AgentCore Primitives

## FR-015: Conversation Memory
- **Description**: System must persist conversation history and session data using AgentCore Memory primitive
- **Business Justification**: Supports multi-turn interactions and session recovery
- **Acceptance Criteria**:
  - System stores all messages and analysis results
  - Memory accessible across agent invocations
  - Memory persisted beyond single request
  - Memory includes conversation context
  - Memory uses AgentCore Memory primitive correctly
- **Priority**: Medium
- **Dependencies**: FR-013
- **Assumptions**: AgentCore Memory provides adequate persistence mechanisms
- **Source**: requirements.md - AgentCore Primitives

## FR-016: API Gateway Integration
- **Description**: System must provide REST API endpoints using AgentCore Gateway primitive for frontend integration
- **Business Justification**: Enables frontend-backend communication
- **Acceptance Criteria**:
  - API endpoints for document upload, analysis initiation, results retrieval
  - API uses standard REST conventions
  - API Gateway configured with appropriate routes
  - API Gateway integrated with Lambda functions
  - API uses AgentCore Gateway primitive correctly
- **Priority**: High
- **Dependencies**: None
- **Assumptions**: Standard REST API patterns sufficient for POC
- **Source**: requirements.md - Technology Stack, AgentCore Primitives

## FR-017: Identity and Session Management
- **Description**: System must manage student identity and sessions using AgentCore Identity primitive
- **Business Justification**: Ensures proper session association and data security
- **Acceptance Criteria**:
  - System associates uploaded documents with session identity
  - System maintains session context throughout workflow
  - System prevents session data leakage between students
  - Identity primitive used for session tracking
  - Session identity integrated with other AgentCore primitives
- **Priority**: High
- **Dependencies**: FR-013
- **Assumptions**: AgentCore Identity provides adequate session management
- **Source**: requirements.md - AgentCore Primitives

---

## Requirements Summary by Domain

### User Interface (Frontend)
- FR-001: Resume Document Upload
- FR-002: Job Description Upload
- FR-003: Company Selection
- FR-012: Student-Friendly Report Generation

### Business Logic (Agent Processing)
- FR-004: Document Processing with MCP Tools
- FR-006: Resume Analysis
- FR-007: Acceptance Probability Calculation
- FR-008: Strengths Identification
- FR-009: Gaps Identification
- FR-010: Company-Specific Evaluation
- FR-011: Timeline-Based Development Plan

### Data Management
- FR-005: Company Principles Loading
- FR-013: Session Management
- FR-015: Conversation Memory

### Integration & Infrastructure
- FR-014: Agent Orchestration
- FR-016: API Gateway Integration
- FR-017: Identity and Session Management

---

## Requirements Traceability to Business Objectives

**Objective 1: Demonstrate Feasibility**
- FR-001, FR-002, FR-003, FR-012: Complete student workflow
- FR-013, FR-014: Multi-agent coordination
- FR-006, FR-007, FR-008, FR-009: Resume evaluation capabilities

**Objective 2: Showcase AgentCore Primitives**
- FR-014: Runtime primitive (agent orchestration)
- FR-015: Memory primitive (conversation persistence)
- FR-016: Gateway primitive (API routing)
- FR-017: Identity primitive (session management)

**Objective 3: Provide Student Value**
- FR-006, FR-007, FR-008, FR-009: Actionable resume analysis
- FR-010: Company-specific guidance
- FR-011: Timeline-based development plan
- FR-012: Student-friendly reporting

---

## Implementation Notes

**POC Scope Considerations**:
- FR-005: Document-based principles loading architecture established; content TBD
- FR-010: Company specialist sub-agents for Amazon initially; Meta/Google future
- FR-007: Probability calculation uses heuristic model appropriate for POC
- FR-015: Basic memory persistence sufficient for POC; advanced features deferred
- All requirements designed for POC-level scale and availability
