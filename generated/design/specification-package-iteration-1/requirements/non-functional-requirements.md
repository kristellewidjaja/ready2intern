# Non-Functional Requirements - Ready2Intern

## Overview
This document defines the non-functional requirements for the Ready2Intern POC, specifying performance, scalability, security, availability, and operational characteristics appropriate for proof-of-concept scope.

**Project Scope**: POC (Proof of Concept)  
**Infrastructure**: Serverless (AWS Lambda, API Gateway, DynamoDB, S3)  
**Scale**: POC-level (demonstration and validation)

---

## NFR-001: Performance Requirements

### Response Time
- **API Response Time**: 95% of API requests complete within 2 seconds (excluding document processing)
- **Document Upload**: Files under 5MB upload within 5 seconds
- **Document Processing**: PDF text extraction completes within 10 seconds for typical resumes/job descriptions
- **Resume Analysis**: Complete analysis workflow (all agents) completes within 30 seconds
- **Report Generation**: Final report generated within 5 seconds after analysis completion

### Throughput
- **Concurrent Users**: Support 10 concurrent evaluation sessions (POC scale)
- **Daily Evaluations**: Handle 50-100 resume evaluations per day
- **API Request Rate**: 100 requests per minute peak capacity

### Resource Utilization
- **Lambda Memory**: 512MB-1024MB per function (configurable based on workload)
- **Lambda Timeout**: 30 seconds for API functions, 60 seconds for processing functions
- **DynamoDB Read/Write**: 5 RCU / 5 WCU provisioned (with auto-scaling enabled)
- **S3 Storage**: Up to 10GB for POC documents

**Priority**: Medium  
**Source**: Customer context (POC scope), Industry standards for AI applications  
**Assumptions**: POC-level performance acceptable; production would require optimization

---

## NFR-002: Scalability Requirements

### POC Scale Targets
- **User Base**: 20-50 students during POC phase
- **Data Volume**: 100-500 resume evaluations total
- **Document Storage**: 1-10GB S3 storage
- **Session Storage**: 100-500 active sessions in DynamoDB

### Growth Considerations
- **Serverless Auto-Scaling**: Lambda automatically scales with demand
- **DynamoDB Scaling**: Auto-scaling configured for 70% utilization threshold
- **S3 Scalability**: Inherently scalable to production volumes
- **API Gateway**: Rate limiting configured to prevent abuse

### Scaling Triggers
- **Lambda Concurrency**: Increase memory allocation if cold starts >10% of invocations
- **DynamoDB Throttling**: Increase provisioned capacity if throttling detected
- **API Rate Limits**: Adjust based on legitimate usage patterns

**Priority**: Low (POC scope)  
**Source**: Customer context (POC scope), AWS serverless best practices  
**Assumptions**: Production scale-out designed but not implemented for POC

---

## NFR-003: Security Requirements

### Authentication & Authorization
- **API Authentication**: API Key or IAM-based authentication for API Gateway
- **Session Isolation**: Complete isolation between student evaluation sessions
- **Principle of Least Privilege**: Lambda execution roles with minimum required permissions

### Data Encryption
- **Data at Rest**: S3 server-side encryption (SSE-S3) for all uploaded documents
- **Data in Transit**: HTTPS/TLS 1.2+ for all API communications
- **DynamoDB Encryption**: Encryption at rest enabled for session data

### Data Privacy
- **Document Access**: Documents accessible only within associated session
- **PII Protection**: Student names and contact information treated as PII
- **Data Retention**: Documents automatically deleted after 30 days (POC policy)
- **Session Expiration**: Sessions expire after 24 hours of inactivity

### Security Best Practices
- **Input Validation**: All file uploads validated for type, size, malicious content
- **Error Handling**: Error messages do not expose system internals
- **Dependency Management**: Regular dependency vulnerability scans
- **Least Privilege**: S3 bucket policies restrict public access

**Priority**: High  
**Source**: Customer context (standard AWS security), AWS security best practices  
**Assumptions**: POC security appropriate; production would require security audit

---

## NFR-004: Availability Requirements

### POC Availability Targets
- **Uptime**: 95% availability during POC phase (weekdays 9AM-5PM ET)
- **Planned Maintenance**: Maintenance windows announced 24 hours in advance
- **Unplanned Downtime**: Best-effort recovery within 4 hours

### Fault Tolerance
- **Lambda Retries**: Automatic retry for transient failures (3 attempts)
- **DynamoDB Backups**: Point-in-time recovery enabled
- **S3 Durability**: 99.999999999% durability (AWS standard)
- **Error Recovery**: Graceful degradation when non-critical services unavailable

### Single Region Deployment
- **AWS Region**: Single region deployment (us-east-1) appropriate for POC
- **No Multi-Region**: Multi-region redundancy deferred to production
- **No DR Site**: Disaster recovery via AWS service durability only

**Priority**: Medium (POC scope)  
**Source**: Customer context (POC availability acceptable)  
**Assumptions**: POC does not require production-grade availability SLAs

---

## NFR-005: Maintainability Requirements

### Code Quality
- **Code Standards**: Follow Python PEP 8 style guidelines
- **Documentation**: Inline comments for complex logic, README for setup
- **Testing**: Unit tests for critical functions (>60% coverage goal)
- **Version Control**: Git repository with meaningful commit messages

### Infrastructure as Code
- **IaC Tool**: AWS CDK (TypeScript or Python)
- **Infrastructure Documentation**: CDK stacks documented and version controlled
- **Configuration Management**: Environment variables for configuration
- **Deployment Automation**: CDK deploy commands for repeatable deployments

### Monitoring & Observability
- **CloudWatch Logs**: All Lambda functions log to CloudWatch
- **CloudWatch Metrics**: Standard Lambda, API Gateway, DynamoDB metrics
- **Error Tracking**: Errors logged with stack traces for debugging
- **Cost Monitoring**: AWS Cost Explorer for POC cost tracking

### Update & Patching
- **Dependency Updates**: Monthly dependency security updates
- **Lambda Runtime**: Use supported Python runtime (3.11+)
- **Bedrock Model**: Claude 3.7 Sonnet model version pinned

**Priority**: Medium  
**Source**: Customer context (advanced AWS team), Development best practices  
**Assumptions**: Advanced team comfortable with CDK and AWS services

---

## NFR-006: Usability Requirements

### User Experience
- **Simple Interface**: Intuitive 3-step workflow (upload resume, upload job description, select company)
- **Clear Feedback**: Progress indicators during document processing and analysis
- **Error Messages**: Clear, actionable error messages for common failures
- **Mobile Responsive**: Interface works on desktop and tablet (mobile optional)

### Accessibility
- **WCAG Compliance**: Basic accessibility (WCAG 2.0 Level A minimum)
- **Keyboard Navigation**: Core functions accessible via keyboard
- **Screen Reader**: Semantic HTML for screen reader compatibility
- **Color Contrast**: Sufficient contrast for text readability

### Documentation
- **User Guide**: Simple guide explaining workflow and interpreting results
- **Help Text**: Inline help for form fields and buttons
- **FAQ**: Common questions about resume evaluation and results

**Priority**: Medium  
**Source**: Requirements.md (student-friendly focus)  
**Assumptions**: Students comfortable with web applications

---

## NFR-007: Portability Requirements

### Platform Independence
- **Frontend**: React application deployable to S3 + CloudFront or any static host
- **Backend**: Serverless functions portable across AWS regions
- **Database**: DynamoDB data exportable to other databases if needed
- **Storage**: S3 documents transferable to other object storage

### Deployment Flexibility
- **CDK Deployment**: Infrastructure deployable to any AWS account
- **Environment Separation**: Dev/Test/Prod environments easily created
- **Configuration**: Environment-specific configuration via .env files

**Priority**: Low (POC scope)  
**Source**: Customer context (CDK preference), Best practices  
**Assumptions**: AWS platform sufficient for foreseeable future

---

## NFR-008: Cost Optimization Requirements

### POC Cost Targets
- **Monthly Budget**: $50-$100/month for POC infrastructure
- **Serverless Pricing**: Pay-per-use model minimizes idle costs
- **Storage Costs**: S3 storage under 10GB keeps costs minimal
- **Bedrock Costs**: Claude 3.7 Sonnet pricing monitored and optimized

### Cost Optimization Strategies
- **Lambda Right-Sizing**: Optimize memory allocation based on actual usage
- **DynamoDB On-Demand**: Consider on-demand pricing for variable workload
- **S3 Lifecycle**: Automatic deletion of old documents after 30 days
- **API Caching**: CloudFront caching for static frontend assets

### Cost Monitoring
- **AWS Cost Explorer**: Weekly cost reviews during POC
- **Budget Alerts**: Alert at 80% and 100% of monthly budget
- **Resource Tagging**: Tag resources for cost allocation tracking

**Priority**: Medium  
**Source**: Customer context (POC cost optimization)  
**Assumptions**: POC infrastructure costs under $100/month acceptable

---

## NFR-009: Compliance Requirements

### General Compliance
- **No Specific Regulations**: POC exempt from HIPAA, FERPA, GDPR compliance
- **Data Handling**: Follow general data privacy best practices
- **Student Data**: Treat student information responsibly even without regulatory requirements

### Future Compliance Considerations
- **Production Planning**: Architecture designed to support compliance requirements if needed
- **Data Classification**: Framework for classifying and protecting sensitive data
- **Audit Trail**: CloudWatch logs provide basic audit trail capability

**Priority**: Low (POC scope)  
**Source**: Customer context (no compliance requirements)  
**Assumptions**: Production deployment may require compliance certifications

---

## NFR-010: Interoperability Requirements

### AWS Service Integration
- **Bedrock AgentCore**: Primary integration for agent orchestration
- **Strands Agents SDK**: Python SDK for AgentCore integration
- **MCP Tools**: Integration for document processing
- **AWS Services**: Lambda, API Gateway, DynamoDB, S3, CloudWatch

### API Standards
- **REST API**: Standard REST conventions for frontend-backend communication
- **JSON Format**: JSON for all API request/response bodies
- **HTTP Status Codes**: Standard HTTP status codes for API responses

### Data Formats
- **Input**: PDF documents (resume and job descriptions)
- **Output**: JSON (API responses), Markdown/HTML (reports)
- **Storage**: JSON (DynamoDB), Binary (S3)

**Priority**: Medium  
**Source**: Requirements.md (technology stack)  
**Assumptions**: Standard formats sufficient for POC

---

## Requirements Summary by Category

### Performance (NFR-001)
- Response times: 2s API, 30s analysis, 10s document processing
- Throughput: 10 concurrent users, 100 evaluations/day
- Resource limits: 512MB-1GB Lambda, 30-60s timeouts

### Scalability (NFR-002)
- POC scale: 20-50 users, 100-500 evaluations
- Serverless auto-scaling configured
- Production scale-out designed but not implemented

### Security (NFR-003)
- API authentication, session isolation
- Encryption at rest (S3, DynamoDB) and in transit (HTTPS)
- Data retention 30 days, session expiration 24 hours

### Availability (NFR-004)
- 95% uptime during business hours
- Single region, fault-tolerant within region
- Best-effort recovery for POC

### Maintainability (NFR-005)
- Python standards, CDK infrastructure
- CloudWatch monitoring, >60% test coverage
- Monthly security updates

### Usability (NFR-006)
- Simple 3-step workflow
- Student-friendly language and interface
- Basic accessibility (WCAG 2.0 Level A)

### Portability (NFR-007)
- CDK deployment to any AWS account
- Environment separation (dev/test/prod)
- AWS platform focus

### Cost (NFR-008)
- $50-100/month POC budget
- Serverless pay-per-use model
- Automated cost monitoring and optimization

### Compliance (NFR-009)
- No regulatory requirements for POC
- General data privacy practices
- Architecture supports future compliance needs

### Interoperability (NFR-010)
- AWS service integration via SDKs
- REST API, JSON format
- PDF input, JSON/Markdown output

---

## Trade-offs and Constraints

### POC Scope Trade-offs
- **Availability vs Cost**: 95% uptime vs 99.9% to reduce cost
- **Scale vs Simplicity**: POC scale vs production-ready scalability
- **Security vs Speed**: Basic security vs comprehensive security audit
- **Features vs Timeline**: Core features vs advanced features

### Technical Constraints
- **Bedrock Model**: Limited to Claude 3.7 Sonnet capabilities
- **AgentCore**: Dependent on Strands Agents SDK maturity
- **Serverless Limits**: AWS Lambda execution time and memory limits
- **Single Region**: No multi-region redundancy for POC

### Resource Constraints
- **Budget**: $50-100/month infrastructure budget
- **Timeline**: POC timeframe constrains feature complexity
- **Team**: Advanced AWS team but limited to POC scope

---

## Validation and Acceptance

### Performance Validation
- Load testing with 10 concurrent users
- Response time measurements under typical load
- Document processing time benchmarks

### Security Validation
- Security best practices checklist review
- Penetration testing (basic, not comprehensive)
- Data encryption verification

### Usability Validation
- User testing with 5-10 students
- Feedback on interface clarity and report usefulness
- Accessibility spot checks

**Acceptance Criteria**: All HIGH priority non-functional requirements met; MEDIUM priority NFRs substantially met with documented exceptions
