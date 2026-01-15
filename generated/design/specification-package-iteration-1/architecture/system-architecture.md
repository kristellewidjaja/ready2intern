# System Architecture - Ready2Intern

## Overview

**Project**: Ready2Intern - AI Internship Readiness Platform  
**Architecture Type**: Multi-Agent Serverless with Amazon Bedrock AgentCore  
**Scope**: POC (Proof of Concept)  
**Last Updated**: January 2026

### Executive Summary

Ready2Intern is a multi-agent resume evaluation system that helps college students assess their internship readiness for top tech companies (Amazon, Meta, Google). The system uses Amazon Bedrock AgentCore with four specialized agents to analyze resumes, provide company-specific feedback, and generate personalized development plans.

**Key Architecture Characteristics**:
- **Multi-Agent Coordination**: 4 specialized agents + company sub-agents orchestrated via AgentCore Runtime
- **Serverless Architecture**: AWS Lambda, API Gateway, DynamoDB, S3
- **AgentCore Primitives**: Showcases all 4 primitives (Runtime, Memory, Gateway, Identity)
- **POC Scale**: 20-50 users, 100-500 evaluations, $50-100/month budget
- **Infrastructure as Code**: AWS CDK for repeatable deployments

---

## High-Level Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend Layer                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  React + TypeScript Application (S3 + CloudFront)        │  │
│  │  - Resume upload interface                                │  │
│  │  - Job description upload interface                       │  │
│  │  - Company selection                                      │  │
│  │  - Results display                                        │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↓ HTTPS
┌─────────────────────────────────────────────────────────────────┐
│                      API Gateway Layer                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  AgentCore Gateway (API Gateway + Lambda)                │  │
│  │  - POST /api/upload-resume                                │  │
│  │  - POST /api/upload-job-description                       │  │
│  │  - POST /api/evaluate                                     │  │
│  │  - GET /api/results/{sessionId}                           │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    AgentCore Runtime Layer                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Orchestrator Agent (Lambda)                  │  │
│  │  - Session management (AgentCore Identity)                │  │
│  │  - Workflow coordination (AgentCore Runtime)              │  │
│  │  - Agent invocation sequencing                            │  │
│  │  - Error handling and recovery                            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              ↓                                   │
│  ┌────────────────┬────────────────────┬────────────────────┐  │
│  │  Document      │  Internship        │  Student Planner   │  │
│  │  Agent         │  Analyzer Agent    │  Agent             │  │
│  │  (Lambda)      │  (Lambda)          │  (Lambda)          │  │
│  │  - PDF parsing │  - Resume analysis │  - Gap analysis    │  │
│  │  - MCP tools   │  - Company eval    │  - Timeline plan   │  │
│  │  - Text extract│  - Sub-agents      │  - Action items    │  │
│  └────────────────┴────────────────────┴────────────────────┘  │
│                              ↓                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │            Company Specialist Sub-Agents                  │  │
│  │  ┌─────────────┬──────────────┬──────────────┐          │  │
│  │  │   Amazon    │    Meta      │   Google     │          │  │
│  │  │ Sub-Agent   │  Sub-Agent   │  Sub-Agent   │          │  │
│  │  │ (Leadership │  (Future)    │  (Future)    │          │  │
│  │  │ Principles) │              │              │          │  │
│  │  └─────────────┴──────────────┴──────────────┘          │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                       AI/ML Layer                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         Amazon Bedrock (Claude 3.7 Sonnet)               │  │
│  │  - Resume content analysis                                │  │
│  │  - Company-specific evaluation                            │  │
│  │  - Natural language generation                            │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                        Data Layer                                │
│  ┌──────────────────┬─────────────────────────────────────┐   │
│  │   DynamoDB       │          S3                          │   │
│  │  - Sessions      │  - Uploaded resumes                  │   │
│  │  - Memory        │  - Job descriptions                  │   │
│  │  - Analysis      │  - Company principles documents      │   │
│  │    results       │  - Generated reports                 │   │
│  └──────────────────┴─────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## AgentCore Primitives Integration

### 1. Runtime Primitive (Agent Orchestration)

**Implementation**: Orchestrator Agent uses AgentCore Runtime for agent coordination

**Capabilities**:
- **Agent Invocation**: Sequential execution of Document → Analyzer → Planner agents
- **Workflow Management**: Manages evaluation workflow state across agent transitions
- **Error Handling**: Graceful failure handling with retry logic
- **Parallel Execution**: Company sub-agents can be invoked in parallel when applicable

**Technology**:
- Strands Agents SDK Runtime API
- AWS Lambda for agent execution
- Step Functions (future) for complex workflows

### 2. Memory Primitive (Conversation Persistence)

**Implementation**: AgentCore Memory for session state and analysis results

**Storage Strategy**:
- **Short-term Memory**: In-memory during single evaluation session
- **Long-term Memory**: DynamoDB for conversation history and analysis results
- **Session Scope**: Memory isolated per student session (no cross-session leakage)

**Data Stored**:
- Uploaded document references
- Processed resume and job description content
- Intermediate analysis results
- Final evaluation and development plan
- Session metadata and timestamps

### 3. Gateway Primitive (API Routing)

**Implementation**: AgentCore Gateway for frontend-backend communication

**API Endpoints**:
- **POST /api/upload-resume**: Resume file upload with validation
- **POST /api/upload-job-description**: Job description upload
- **POST /api/evaluate**: Initiate evaluation with company selection
- **GET /api/results/{sessionId}**: Retrieve evaluation results

**Features**:
- API Key authentication (POC)
- Request/response logging
- Rate limiting (100 req/min)
- CORS configuration for frontend

### 4. Identity Primitive (Session Management)

**Implementation**: AgentCore Identity for session tracking and data isolation

**Session Management**:
- **Session Creation**: Unique session ID generated on first upload
- **Session Association**: All documents and analysis tied to session ID
- **Session Expiration**: 24-hour session timeout
- **Data Isolation**: Complete isolation between student sessions

**Security**:
- Session ID as authentication token
- S3 bucket policies enforce session-scoped access
- DynamoDB queries filtered by session ID

---

## Agent Specifications

### Orchestrator Agent

**Purpose**: Coordinate multi-agent workflow and manage evaluation sessions

**Responsibilities**:
1. **Session Management**: Create/manage sessions using AgentCore Identity
2. **Workflow Coordination**: Invoke agents in correct sequence
3. **Error Recovery**: Handle agent failures gracefully
4. **Progress Tracking**: Monitor evaluation progress
5. **Result Aggregation**: Combine agent outputs into final report

**Technology Stack**:
- AWS Lambda (Python 3.11)
- Strands Agents SDK
- AgentCore Runtime primitive
- DynamoDB for state management

**Inputs**: Session ID, company selection
**Outputs**: Orchestration status, error messages
**Invokes**: Document Agent → Analyzer Agent → Planner Agent

---

### Document Agent

**Purpose**: Process PDF documents and extract structured data

**Responsibilities**:
1. **PDF Processing**: Extract text from resume and job description PDFs
2. **MCP Tool Integration**: Use MCP tools for document processing
3. **Content Parsing**: Identify resume sections (education, experience, skills, projects)
4. **Job Requirements Extraction**: Parse key requirements from job description
5. **Error Handling**: Handle malformed or unreadable PDFs

**Technology Stack**:
- AWS Lambda (Python 3.11)
- MCP Tools for PDF processing
- S3 for document retrieval
- Structured output for downstream agents

**Inputs**: S3 paths to resume and job description
**Outputs**: Structured resume data, extracted job requirements
**Processing Time**: <10 seconds per document

---

### Internship Analyzer Agent

**Purpose**: Evaluate resume against job requirements and company criteria

**Responsibilities**:
1. **Resume Analysis**: Analyze GPA, coursework, projects, leadership, experience
2. **Job Alignment**: Compare resume content against job description requirements
3. **Company Evaluation**: Invoke company specialist sub-agent for principles-based assessment
4. **Probability Calculation**: Estimate internship acceptance probability
5. **Strengths Identification**: Identify 3-5 key strengths with evidence
6. **Gap Identification**: Identify 3-5 improvement areas

**Technology Stack**:
- AWS Lambda (Python 3.11)
- Amazon Bedrock (Claude 3.7 Sonnet)
- Strands Agents SDK for sub-agent invocation
- Company principles documents (file system)

**Inputs**: Structured resume data, job requirements, company selection
**Outputs**: Acceptance probability, strengths, gaps, company-specific feedback
**LLM Model**: anthropic.claude-3-7-sonnet-20250219-v1:0

**Sub-Agents**:
- **Amazon Sub-Agent**: Evaluates against Leadership Principles
- **Meta Sub-Agent**: (Future) Evaluates against Meta values
- **Google Sub-Agent**: (Future) Evaluates against Google principles

---

### Student Planner Agent

**Purpose**: Create personalized development plan based on identified gaps

**Responsibilities**:
1. **Gap Prioritization**: Prioritize gaps by impact on internship success
2. **Action Item Generation**: Create specific, actionable improvement steps
3. **Timeline Planning**: Align actions with internship application cycles
4. **Milestone Definition**: Define checkpoints for progress tracking
5. **Resource Recommendations**: Suggest courses, projects, activities

**Technology Stack**:
- AWS Lambda (Python 3.11)
- Amazon Bedrock (Claude 3.7 Sonnet)
- Standard internship timeline knowledge

**Inputs**: Identified gaps, student academic level, target company
**Outputs**: Timeline-based development plan with prioritized actions
**Plan Horizon**: 3-12 months depending on application timeline

---

### Company Specialist Sub-Agents

**Purpose**: Provide company-specific evaluation and guidance

**Amazon Sub-Agent**:
- **Principles Source**: Amazon Leadership Principles document (`project-doc/organization-context/amazon-leadership-principles.md`)
- **Loading Strategy**: File system read, cached for session
- **Evaluation Approach**: Map resume experiences to Leadership Principles
- **Feedback Format**: Specific examples of how to demonstrate each principle

**Meta/Google Sub-Agents** (Future):
- Similar structure with company-specific principles
- Separate evaluation logic per company culture

**Fallback Strategy**:
- If principles document missing: Generic evaluation criteria
- Log missing principles for debugging
- Continue evaluation with reduced company-specificity

---

## Data Flow

### Evaluation Workflow Sequence

```
1. Student uploads resume (PDF) → S3
   ↓
2. Student uploads job description (PDF) → S3
   ↓
3. Student selects company (Amazon/Meta/Google)
   ↓
4. Frontend calls POST /api/evaluate
   ↓
5. API Gateway invokes Orchestrator Agent
   ↓
6. Orchestrator creates session (AgentCore Identity)
   ↓
7. Orchestrator invokes Document Agent
   - Document Agent retrieves PDFs from S3
   - Extracts text using MCP tools
   - Returns structured data
   ↓
8. Orchestrator invokes Analyzer Agent
   - Analyzer evaluates resume vs job requirements
   - Invokes company sub-agent for principles-based evaluation
   - Calculates probability, identifies strengths/gaps
   - Returns analysis results
   ↓
9. Orchestrator invokes Planner Agent
   - Planner creates development plan from gaps
   - Returns timeline-based action plan
   ↓
10. Orchestrator aggregates results
    - Combines probability, strengths, gaps, evaluation, plan
    - Stores in DynamoDB (AgentCore Memory)
    - Returns final report
   ↓
11. Frontend retrieves results via GET /api/results/{sessionId}
   ↓
12. Student views comprehensive analysis report
```

### Data Storage Pattern

**DynamoDB Schema**:
```json
{
  "PK": "SESSION#{sessionId}",
  "SK": "METADATA",
  "sessionId": "uuid",
  "studentId": "session-based-id",
  "company": "Amazon|Meta|Google",
  "status": "uploading|processing|complete|error",
  "createdAt": "ISO-8601 timestamp",
  "expiresAt": "ISO-8601 timestamp (24 hours)",
  "resumeS3Path": "s3://bucket/sessions/{sessionId}/resume.pdf",
  "jobDescS3Path": "s3://bucket/sessions/{sessionId}/job-desc.pdf"
}

{
  "PK": "SESSION#{sessionId}",
  "SK": "ANALYSIS",
  "probability": 75,
  "strengths": ["strength1", "strength2", "strength3"],
  "gaps": ["gap1", "gap2", "gap3"],
  "companyEvaluation": "detailed feedback text",
  "developmentPlan": {...}
}
```

**S3 Structure**:
```
s3://ready2intern-documents-{accountId}/
├── sessions/
│   ├── {sessionId}/
│   │   ├── resume.pdf
│   │   ├── job-description.pdf
│   │   └── analysis-report.json
├── company-principles/
│   ├── amazon-leadership-principles.md
│   ├── meta-values.md (future)
│   └── google-principles.md (future)
```

---

## Technology Stack

### Frontend
- **Framework**: React 18+ with TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Context API
- **HTTP Client**: Axios
- **File Upload**: react-dropzone
- **Deployment**: S3 + CloudFront

### Backend (Agent Layer)
- **Runtime**: Python 3.11
- **Agent Framework**: Strands Agents SDK
- **AgentCore**: Amazon Bedrock AgentCore primitives
- **LLM**: Claude 3.7 Sonnet (anthropic.claude-3-7-sonnet-20250219-v1:0)
- **Document Processing**: MCP Tools
- **Compute**: AWS Lambda (512MB-1GB memory, 30-60s timeout)

### Infrastructure
- **API Gateway**: REST API with API Key auth
- **Lambda**: Serverless compute for agents
- **DynamoDB**: Session and memory storage (5 RCU/WCU with auto-scaling)
- **S3**: Document and principles storage (10GB limit)
- **Bedrock**: Claude 3.7 Sonnet via AWS SDK
- **CloudWatch**: Logging and monitoring

### Infrastructure as Code
- **IaC Tool**: AWS CDK (TypeScript or Python)
- **Deployment**: `cdk deploy` command
- **Environment Management**: Dev/Test/Prod separation via CDK contexts
- **Configuration**: Environment variables for model IDs, bucket names, table names

---

## Security Architecture

### Authentication & Authorization
- **API Authentication**: API Key (POC) or IAM Sig V4
- **Session-Based Access**: All operations scoped to session ID
- **Principle of Least Privilege**: Lambda execution roles with minimal permissions

### Data Encryption
- **In Transit**: HTTPS/TLS 1.2+ for all API calls
- **At Rest**: 
  - S3 SSE-S3 encryption for documents
  - DynamoDB encryption at rest
- **Document Access**: Pre-signed URLs with 15-minute expiration

### Data Privacy
- **Session Isolation**: Complete isolation between student sessions
- **Data Retention**: 30-day automatic deletion policy
- **PII Protection**: Student names and contact info treated as PII
- **No Cross-Session Access**: S3/DynamoDB policies prevent cross-session reads

### Network Security
- **VPC**: Not required for POC (public endpoints acceptable)
- **Security Groups**: Lambda in VPC (future) with restrictive egress
- **API Rate Limiting**: 100 requests/minute per API key

---

## Performance & Scalability

### Performance Targets (POC)
- **API Response Time**: <2 seconds (95th percentile, excluding document processing)
- **Document Processing**: <10 seconds per document
- **Complete Analysis**: <30 seconds end-to-end
- **Report Generation**: <5 seconds

### Throughput Targets (POC)
- **Concurrent Users**: 10 concurrent evaluation sessions
- **Daily Evaluations**: 50-100 resume evaluations per day
- **Peak Request Rate**: 100 requests per minute

### Scalability Strategy
- **Lambda Auto-Scaling**: Automatic scaling with demand (no config needed)
- **DynamoDB Auto-Scaling**: Configured at 70% utilization threshold
- **S3 Scalability**: Inherently scalable (no action needed)
- **Bedrock Throttling**: Monitor and request quota increases if needed

### Optimization Strategies
- **Lambda Memory**: Right-size based on profiling (start 512MB)
- **Cold Start Mitigation**: Provisioned concurrency for critical functions (future)
- **Caching**: Company principles cached in Lambda memory during session
- **Parallel Processing**: Company sub-agents can run in parallel

---

## Deployment Architecture

### Environment Strategy
- **Development**: Personal AWS account for testing
- **Production POC**: Shared account with tagging for cost tracking

### CDK Stack Structure
```
ready2intern-cdk/
├── lib/
│   ├── frontend-stack.ts          # S3 + CloudFront
│   ├── api-gateway-stack.ts       # API Gateway + Lambda integration
│   ├── agent-stack.ts             # Lambda functions for agents
│   ├── data-stack.ts              # DynamoDB + S3 buckets
│   └── iam-stack.ts               # Roles and policies
├── bin/
│   └── ready2intern-cdk.ts        # CDK app entry point
├── cdk.json                        # CDK configuration
└── package.json
```

### Deployment Commands
```bash
# Install dependencies
npm install

# Bootstrap CDK (first time only)
cdk bootstrap

# Deploy all stacks
cdk deploy --all

# Deploy specific stack
cdk deploy Ready2InternApiGatewayStack

# Destroy all resources
cdk destroy --all
```

### Configuration Management
```bash
# .env file
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-3-7-sonnet-20250219-v1:0
S3_BUCKET_NAME=ready2intern-documents-${AWS::AccountId}
DYNAMODB_TABLE_NAME=ready2intern-sessions
API_KEY=<generated-api-key>
SESSION_EXPIRATION_HOURS=24
```

---

## Monitoring & Observability

### CloudWatch Logs
- **Log Groups**:
  - `/aws/lambda/orchestrator-agent`
  - `/aws/lambda/document-agent`
  - `/aws/lambda/analyzer-agent`
  - `/aws/lambda/planner-agent`
- **Log Retention**: 7 days (POC)
- **Log Level**: INFO (ERROR for production)

### CloudWatch Metrics
- **Lambda Metrics**: Duration, errors, throttles, concurrent executions
- **API Gateway Metrics**: Request count, latency, 4xx/5xx errors
- **DynamoDB Metrics**: Read/write capacity, throttles
- **Bedrock Metrics**: Model invocation count, latency, errors

### Alarms (Future)
- Lambda error rate > 5%
- API Gateway 5xx rate > 1%
- DynamoDB throttling detected
- S3 bucket approaching 10GB limit

### Cost Monitoring
- **AWS Cost Explorer**: Weekly cost reviews
- **Budget Alerts**: 80% and 100% of $100/month
- **Resource Tagging**: All resources tagged with `Project:Ready2Intern`

---

## Operational Considerations

### Error Handling
- **Retry Logic**: 3 retries with exponential backoff for transient failures
- **Graceful Degradation**: Continue evaluation without company sub-agent if principles missing
- **User-Friendly Errors**: Clear error messages for common failures (invalid PDF, file too large)

### Testing Strategy
- **Unit Tests**: Python pytest for agent logic (>60% coverage goal)
- **Integration Tests**: End-to-end evaluation workflow tests
- **Load Testing**: Simulate 10 concurrent users for performance validation

### Disaster Recovery
- **DynamoDB Backups**: Point-in-time recovery enabled
- **S3 Durability**: 99.999999999% (11 nines) AWS guarantee
- **Lambda**: Stateless, redeploy from CDK if needed
- **RTO/RPO**: Best-effort for POC (no SLA)

### Maintenance
- **Dependency Updates**: Monthly security updates
- **Lambda Runtime**: Python 3.11+ (supported runtime)
- **Model Updates**: Pin Claude 3.7 Sonnet version, update intentionally

---

## Cost Estimation (POC)

### Monthly Cost Breakdown

| Service | Usage | Unit Cost | Monthly Cost |
|---------|-------|-----------|--------------|
| Lambda | 1000 invocations/day, 512MB, 30s avg | $0.0000166667/GB-second | $25 |
| Bedrock (Claude 3.7 Sonnet) | 100 evaluations/day, ~2000 tokens each | $0.003/1K input, $0.015/1K output | $30 |
| API Gateway | 3000 requests/day | $3.50/million | $0.35 |
| DynamoDB | 5 RCU/WCU, 1GB storage | On-Demand pricing | $5 |
| S3 | 10GB storage, 3000 requests/day | $0.023/GB, $0.0004/1K requests | $0.60 |
| CloudWatch | 5GB logs, basic metrics | $0.50/GB | $2.50 |
| **Total** | | | **~$63/month** |

**Cost Optimization Notes**:
- Stay within free tier where possible
- DynamoDB on-demand reduces costs for variable workload
- S3 lifecycle policy deletes old documents after 30 days
- Right-size Lambda memory based on profiling

---

## Future Enhancements (Post-POC)

### Scalability Improvements
- Multi-region deployment for global availability
- Step Functions for complex workflows with parallel execution
- Provisioned concurrency for Lambda to eliminate cold starts
- ElastiCache for company principles caching

### Feature Enhancements
- Multi-turn conversation support for clarification questions
- Resume improvement suggestions with before/after examples
- Interview preparation guidance based on evaluation
- Progress tracking across multiple evaluation sessions

### Security Enhancements
- Cognito for user authentication and authorization
- WAF for API Gateway protection
- VPC deployment for Lambda functions
- Secrets Manager for API keys and credentials

### Operational Improvements
- CloudWatch dashboards for real-time monitoring
- X-Ray tracing for distributed debugging
- Automated testing pipeline (CI/CD)
- Comprehensive alerting and on-call

---

## Conclusion

This architecture provides a solid foundation for the Ready2Intern POC, demonstrating:

✅ **Multi-Agent Coordination**: 4 specialized agents working together  
✅ **AgentCore Showcase**: All 4 primitives (Runtime, Memory, Gateway, Identity) integrated  
✅ **Serverless Scalability**: Auto-scaling with demand, pay-per-use pricing  
✅ **POC-Appropriate**: Streamlined for validation, designed for future production scale  
✅ **Cost-Optimized**: ~$63/month well within $50-100 budget  
✅ **Production Path**: Clear roadmap for scaling beyond POC

The architecture balances POC simplicity with production-ready patterns, ensuring the system can validate the multi-agent approach while maintaining a clear path to production deployment.
