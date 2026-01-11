---
description: "Cloud service preferences and local development approach for POC and production deployment"
alwaysApply: true
---

# Cloud Services & Development Approach

## Cloud Provider Preference

**Use AWS exclusively** for cloud services.

### Why AWS
- Deepest service catalog for production needs
- Best enterprise support and documentation
- Strongest ecosystem for AI/ML (Bedrock, SageMaker)
- Most mature IaC tooling (CDK, CloudFormation)

### Core AWS Services by Use Case

**Compute:**
- Lambda (serverless functions)
- ECS/Fargate (containers)
- EC2 (when you need control)

**Storage:**
- S3 (object storage)
- EFS (file system)
- EBS (block storage)

**Database:**
- RDS (PostgreSQL, MySQL)
- DynamoDB (NoSQL)
- Aurora (high-performance SQL)

**AI/ML:**
- Bedrock (LLM access - Claude, etc.)
- SageMaker (custom models)
- Bedrock AgentCore (agent orchestration, runtime, memory)

**API/Networking:**
- API Gateway (REST/WebSocket)
- CloudFront (CDN)
- Route 53 (DNS)

**Observability:**
- CloudWatch (logs, metrics, alarms)
- X-Ray (distributed tracing)

**IaC:**
- CDK (TypeScript/Python - preferred)
- CloudFormation (when CDK not suitable)
- Terraform (multi-cloud scenarios only)

## Development Philosophy

### POC/Local Development First

**Always start local, deploy to cloud later.**

### Why Local First
- ✅ Faster iteration (no deploy wait)
- ✅ No cloud costs during development
- ✅ Easier debugging (local logs, breakpoints)
- ✅ Works offline
- ✅ Simpler onboarding (no AWS credentials needed initially)

### Local Development Stack

**Instead of AWS services, use:**

| AWS Service | Local Alternative | When to Switch |
|-------------|------------------|----------------|
| Lambda | FastAPI/Express locally | When need auto-scaling |
| DynamoDB | SQLite/PostgreSQL | When need global tables |
| S3 | Local file system | When need CDN/durability |
| API Gateway | Local server | When need rate limiting/auth |
| Bedrock | Direct LLM API (Anthropic, OpenAI) | When need VPC/compliance |
| SQS/SNS | In-memory queues | When need reliability |

### AI/LLM Integration

**For local development:**
- Call LLM APIs directly (Anthropic Claude API, OpenAI API)
- Use API keys in `.env` file
- No AWS Bedrock required for POC
- Faster iteration, simpler setup

**For production:**
- Use AWS Bedrock for LLM access
- Benefits: VPC integration, compliance, unified billing
- Migrate when need enterprise features

### Local Development Requirements

**Must have for POC:**
- Run with `npm start` or `python main.py`
- No AWS credentials required
- All data in local files/SQLite
- Environment variables in `.env` (not committed)
- README with setup instructions (< 5 steps)

**Nice to have:**
- Docker Compose for multi-service
- Hot reload for frontend/backend
- Seed data scripts

## When to Move to Cloud

### Triggers for AWS Deployment

Deploy to AWS when you need:
1. **External access** - Share with users outside localhost
2. **Persistence** - Data survives restarts
3. **Scale** - Multiple concurrent users
4. **Production features** - Auth, monitoring, backups
5. **Team collaboration** - Shared environment

### Migration Path

**Phase 1: Local POC**
```
Frontend: React (localhost:3000)
Backend: FastAPI (localhost:8000)
Storage: Local files/SQLite
AI: Direct Anthropic/OpenAI API calls
Agents: Strands Agents SDK
```

**Phase 2: Cloud Deployment**
```
Frontend: S3 + CloudFront
Backend: Lambda + API Gateway
Storage: DynamoDB + S3
AI: Bedrock + AgentCore primitives
Agents: Strands Agents SDK (same code, different gateway)
IaC: AWS CDK
Monitoring: CloudWatch
```

### IaC Approach

**Don't write IaC until you're deploying to cloud.**

When ready:
1. Use AWS CDK (TypeScript or Python)
2. Define infrastructure as code
3. Separate stacks: dev, staging, prod
4. Store state in S3 + DynamoDB lock
5. CI/CD with GitHub Actions

**CDK Structure:**
```
infrastructure/
├── lib/
│   ├── frontend-stack.ts
│   ├── backend-stack.ts
│   ├── database-stack.ts
│   └── monitoring-stack.ts
├── bin/
│   └── app.ts
├── cdk.json
└── package.json
```

## AWS Best Practices

### Security
- Use IAM roles, not access keys
- Principle of least privilege
- Enable CloudTrail logging
- Encrypt at rest (S3, RDS, DynamoDB)
- Use Secrets Manager for credentials

### Cost Optimization
- Use Lambda for variable workload
- Reserved instances for steady state
- S3 lifecycle policies
- DynamoDB on-demand for unpredictable traffic
- Set billing alarms

### Reliability
- Multi-AZ for databases
- CloudFront for global distribution
- Auto-scaling groups
- Health checks and alarms
- Automated backups

### Observability
- Structured logging (JSON)
- CloudWatch dashboards
- X-Ray for distributed tracing
- Alarms with SNS notifications
- Log retention policies

## Anti-Patterns to Avoid

### ❌ Cloud-First Development
Don't require AWS credentials to run locally. Slows development, increases costs, complicates onboarding.

### ❌ Premature IaC
Don't write CloudFormation before validating POC. Requirements will change, IaC becomes outdated.

### ❌ Multi-Cloud for "Flexibility"
Don't use multiple clouds "just in case." Increases complexity, reduces expertise depth. Pick AWS and commit.

### ❌ Serverless Everything
Don't force Lambda for all workloads. Long-running processes, WebSockets, high memory needs may need containers/EC2.

### ❌ Over-Engineering Locally
Don't replicate AWS architecture locally (LocalStack, etc.). Use simple alternatives, migrate when needed.

## Quick Decision Guide

### "Should I use AWS service X?"

**For POC:** No, use local alternative
**For production:** Evaluate:
- Does it solve real problem?
- Is it managed service? (prefer yes)
- Do we have expertise? (or can learn quickly)
- What's operational burden?
- What's cost at our scale?

### "When to write IaC?"

**Write IaC when:**
- ✅ Deploying to cloud
- ✅ Need reproducible environments
- ✅ Team needs shared infrastructure

**Don't write IaC when:**
- ❌ Still in POC phase
- ❌ Running locally only
- ❌ Requirements still changing rapidly

### "CDK vs CloudFormation vs Terraform?"

**Use CDK** (default choice)
- Type-safe infrastructure
- Reusable constructs
- AWS-native

**Use CloudFormation** (rare)
- Need raw control
- CDK too opinionated

**Use Terraform** (very rare)
- Multi-cloud requirement
- Existing Terraform expertise

## Agentic Framework Preferences

### Agent Framework Selection

**First preference: Strands Agents SDK**
- Purpose-built for production agent systems
- Clean abstractions for agent orchestration
- Native AWS Bedrock integration
- Simpler than LangGraph for most use cases
- Supports both Python and TypeScript

**Second preference: LangGraph (only if needed)**
- Complex state machines with custom graph topologies
- Advanced conditional routing requirements
- When Strands doesn't support specific use case
- More flexibility, more complexity

**Also supported: CrewAI**
- Multi-agent teams with role-based collaboration
- When need agent delegation patterns
- Good for specialized agent roles

### When to Use Each

**Use Strands Agents when:**
- ✅ Building multi-agent systems
- ✅ Standard orchestration patterns
- ✅ AWS Bedrock deployment target
- ✅ Want simplicity and maintainability
- ✅ Need both Python and TypeScript support

**Use LangGraph when:**
- ✅ Need complex graph structures with cycles
- ✅ Advanced conditional routing
- ✅ Strands doesn't support use case
- ✅ Team has LangGraph expertise

**Use CrewAI when:**
- ✅ Need role-based agent teams
- ✅ Agent delegation patterns
- ✅ Collaborative multi-agent workflows

**Avoid:**
- ❌ Building custom agent framework from scratch
- ❌ Using multiple frameworks together
- ❌ LangChain without LangGraph (use Strands instead)

### AWS Agentic Services

**For production agent deployment on AWS:**

**Use Bedrock AgentCore services:**
- **Runtime** - Serverless agent deployment and execution (managed containers)
- **Memory** - Short-term (STM) and long-term (LTM) conversation persistence
- **Gateway** - MCP-compatible tool connectivity and API routing
- **Identity** - OAuth-based session and credential management
- **Browser** - Cloud-based web browsing for agents
- **Code Interpreter** - Secure Python code execution in sandboxes

**Why AgentCore:**
- Fully managed infrastructure (no servers to manage)
- Native AWS integration
- Built-in scaling and session isolation
- Unified monitoring with CloudWatch
- MCP (Model Context Protocol) support

**Architecture pattern:**
```
Local Dev: Strands Agents → Direct Anthropic/OpenAI API
Production: Strands Agents → Bedrock → AgentCore Runtime
```

### Agent Development Workflow

**Phase 1: Local Development**
```python
# Use Strands with direct Anthropic API
from strands import Agent
from strands.models.anthropic import AnthropicModel

model = AnthropicModel(
    client_args={"api_key": os.getenv("ANTHROPIC_API_KEY")},
    model_id="claude-sonnet-4-20250514",
    max_tokens=1028
)

agent = Agent(model=model, tools=[calculator])
response = agent("What is 2+2?")
```

**Phase 2: Production Deployment to AgentCore**
```python
# Use Strands with Bedrock + AgentCore Runtime
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands import Agent

app = BedrockAgentCoreApp()

agent = Agent(
    model="us.anthropic.claude-sonnet-4-20250514-v1:0",  # Bedrock model
    system_prompt="You're a helpful assistant"
)

@app.entrypoint
def invoke(payload, context):
    response = agent(payload.get("prompt", "Hello"))
    return response.message['content'][0]['text']

if __name__ == "__main__":
    app.run()
```

**Deploy with AgentCore CLI:**
```bash
# Configure deployment
agentcore configure -e agent.py

# Deploy to AgentCore Runtime
agentcore deploy

# Test deployed agent
agentcore invoke '{"prompt": "Hello!"}'
```

## Summary

1. **Build POC locally first** - No cloud until validated
2. **Use AWS exclusively** - When ready for cloud
3. **Write IaC with CDK** - When deploying to AWS
4. **Keep local dev simple** - Fast iteration over realism
5. **Migrate incrementally** - Service by service to cloud
6. **Direct LLM APIs locally** - Anthropic/OpenAI for POC
7. **Strands Agents first** - LangGraph only if necessary
8. **AgentCore for production** - AWS-native agent infrastructure
