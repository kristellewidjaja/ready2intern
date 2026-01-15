# Ready2Intern


AI Internship Readiness Platform for college students pursuing tech internships at top companies.


## Overview


Ready2Intern is a multi-agent resume evaluation system built with Amazon Bedrock AgentCore and Claude 3.7 Sonnet. It analyzes student resumes against internship requirements and provides actionable career guidance.


## Target Users


College students (Freshman to Senior) in CS/Software Engineering programs seeking internships at:
- Amazon (SDE Intern, AWS)
- Meta (Software Engineer Intern)
- Google (Software Engineering Intern, STEP)


## Key Features


- Internship-focused resume analysis tailored for student profiles
- Multi-agent architecture using AgentCore primitives
- Company-specific evaluation criteria for top tech companies
- Student-friendly reports focusing on GPA, coursework, projects, and leadership
- Timeline-based development plans aligned with application deadlines
- Document processing with MCP tools


## Technology Stack


**Backend:**
- Strands Agents SDK with Amazon Bedrock AgentCore
- Anthropic Claude 3.7 Sonnet (via Amazon Bedrock)
- Python (FastAPI)
- AWS (Lambda, API Gateway, DynamoDB, S3)


**Frontend:**
- React + TypeScript
- Tailwind CSS


**AgentCore Primitives:**
- Runtime (agent orchestration)
- Memory (conversation persistence)
- Gateway (API routing)
- Identity (session management)


## Architecture


The system employs four specialized agents:


1. **Orchestrator Agent** - Coordinates workflow and manages student sessions
2. **Document Agent** - Processes resumes and job descriptions using MCP tools
3. **Internship Analyzer Agent** - Evaluates resumes with company-specific criteria
4. **Student Planner Agent** - Creates timeline-based development plans


Each company has a specialist sub-agent that understands specific internship requirements and evaluation criteria.


## Design Requirements

### Company Organization Principles

**Requirement**: The system shall incorporate company-specific organizational principles and cultural tenets to evaluate candidate resumes.

**Implementation Approach**:
- Principles stored as documents in the file system (`project-doc/organization-context/`)
- Document-based approach (NOT knowledge base)
- Each company has a dedicated principles document
- Documents are loaded by specialist sub-agents during evaluation

**Initial Implementation**:
- Amazon Leadership Principles document (`amazon-leadership-principles.md`)
- Future expansion for Meta and Google

**Rationale**: File system storage provides version control, easy updates, and direct agent access without requiring knowledge base infrastructure.


## Installation


```bash
# Clone repository
git clone https://github.com/yourusername/ready2intern.git
cd ready2intern


# Backend setup
cd backend
pip install -r requirements.txt


# Frontend setup
cd ../frontend
npm install


# Configure AWS credentials
aws configure
```


## Configuration


Create `.env` file in backend directory:


```
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-3-7-sonnet-20250219-v1:0
S3_BUCKET_NAME=ready2intern-documents
DYNAMODB_TABLE_NAME=ready2intern-sessions
```


## Usage


```bash
# Start backend
cd backend
uvicorn main:app --reload


# Start frontend
cd frontend
npm start
```


Access the application at `http://localhost:3000`


## Workflow


1. Upload student resume (PDF)
2. Upload internship job description (PDF)
3. Select target company
4. Receive comprehensive analysis including:
  - Acceptance probability
  - Strengths and gaps
  - Company-specific evaluation
  - Timeline-based development plan


## Project Structure


```
ready2intern/
├── backend/
│   ├── agents/           # Agent implementations
│   ├── tools/            # MCP tools
│   ├── api/              # FastAPI routes
│   └── config/           # Configuration
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   └── services/     # API services
├── infrastructure/       # AWS CDK/Terraform
└── docs/                 # Documentation
```


## License


MIT License - see LICENSE file for details


## Contributing


Contributions welcome. Please open an issue first to discuss proposed changes.


## Contact


For questions or feedback, please open an issue on GitHub.


