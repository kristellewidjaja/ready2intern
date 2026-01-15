# Customer Context - Ready2Intern

## Project Goals & Constraints
- **Project Type:** POC (Proof of Concept)
- **Timeline:** Not specified - POC timeframe
- **Budget:** Cost optimization appropriate for POC
- **Compliance:** None - No specific compliance requirements
- **Availability:** POC-level availability acceptable
- **Scale:** POC-level scale - designed for validation and demonstration
- **Success Metrics:** Demonstrate feasibility of multi-agent resume evaluation system with AgentCore
- **Stakeholders:** Internal development team

## Technical Preferences
- **Infrastructure:** Serverless with Amazon Bedrock AgentCore
- **IaC:** AWS CDK (Cloud Development Kit)
- **Development:** Python (FastAPI backend), React + TypeScript (frontend)
- **Data Storage:** AWS services (DynamoDB, S3 as indicated in requirements)
- **Security:** Standard AWS security appropriate for POC
- **Vendor:** AWS-native services, focused on AgentCore primitives
- **AgentCore Focus:** Multi-agent architecture using Strands Agents SDK with Runtime, Memory, Gateway, and Identity primitives

## Organizational Context
- **Team Expertise:** Advanced AWS experience
- **Operational Maturity:** Sufficient for managing serverless and AgentCore implementations
- **Existing Infrastructure:** Not specified - greenfield project
- **Constraints:** None specified
- **Support Model:** Internal team support with advanced AWS capabilities
- **Documentation:** Requirements document provided in project-context folder

## Architecture Implications
- **POC Focus:** Prioritize simplicity and speed to value over enterprise-grade resilience
- **Cost Optimization:** Serverless architecture aligns with POC cost objectives
- **AgentCore Integration:** Architecture must showcase AgentCore primitives (Runtime, Memory, Gateway, Identity)
- **CDK Deployment:** Infrastructure as code using AWS CDK for reproducibility
- **Scalability:** Design with production path in mind but optimize for POC validation
