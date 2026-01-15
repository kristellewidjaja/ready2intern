# ADR-002: Serverless Architecture with AWS Lambda

**Status**: Accepted  
**Date**: January 2026  
**Decision Makers**: Architecture Team  
**Technical Story**: POC requires cost-effective, scalable architecture

---

## Context and Problem Statement

Ready2Intern POC must support 20-50 concurrent users with 100-500 evaluations while staying within $50-100/month budget. The system needs to scale automatically with demand without operational overhead.

**Decision**: Should we use serverless or container-based architecture?

---

## Decision Drivers

- **POC Budget**: $50-100/month strict limit
- **Variable Load**: Unpredictable usage patterns during POC
- **Operational Simplicity**: Small team, limited ops resources
- **Team Expertise**: Advanced AWS experience
- **AgentCore Compatibility**: Must work with AgentCore primitives
- **Time to Market**: Fast POC deployment required

---

## Considered Alternatives

### Option 1: AWS Lambda Serverless (Selected)

**Pros**:
- ✅ **Pay-per-Use**: Only pay for actual invocations (~$25/month estimated)
- ✅ **Auto-Scaling**: Automatic scaling, no configuration needed
- ✅ **Zero Ops**: No server management, patching, or scaling
- ✅ **AgentCore Native**: Designed for Lambda deployment
- ✅ **Fast Deployment**: Deploy in minutes with CDK

**Cons**:
- ❌ **Cold Starts**: 1-3 second latency for first request
- ❌ **Timeout Limits**: 15-minute maximum execution time
- ❌ **State Management**: Requires external state storage

**Cost**: ~$25/month for 1000 invocations/day

### Option 2: ECS Fargate Containers

**Pros**:
- ✅ **No Cold Starts**: Always-warm containers
- ✅ **Long-Running**: No timeout limits
- ✅ **Flexibility**: Full control over runtime environment

**Cons**:
- ❌ **Fixed Costs**: Always-on pricing ~$50/month minimum
- ❌ **Ops Overhead**: Must manage task definitions, scaling
- ❌ **Exceeds Budget**: Base cost alone hits budget ceiling
- ❌ **Overkill for POC**: More complexity than needed

**Cost**: ~$50-80/month for 2 tasks

### Option 3: EC2 Instances

**Pros**:
- ✅ **Full Control**: Complete server control
- ✅ **Cost Predictable**: Fixed monthly cost

**Cons**:
- ❌ **High Base Cost**: t3.medium ~$30/month always-on
- ❌ **Ops Burden**: Patching, monitoring, scaling manual
- ❌ **Poor POC Fit**: Over-provisioned or under-provisioned
- ❌ **No Auto-Scaling**: Must configure scaling manually

**Cost**: ~$40-60/month for single instance

---

## Decision Outcome

**Chosen Option**: **AWS Lambda Serverless Architecture**

### Rationale

1. **Perfect Budget Match**: Pay-per-use pricing stays well within $50-100 budget even with usage spikes
2. **Zero Operational Overhead**: No servers to manage allows team to focus on agent logic
3. **AgentCore Integration**: Lambda is primary deployment target for AgentCore agents
4. **Automatic Scaling**: Scales from 0 to thousands without configuration
5. **Fast Iteration**: Deploy updates in seconds, ideal for POC rapid iteration

---

## Implementation Details

### Lambda Function Configuration

**Agent Lambda Functions**:
```yaml
Orchestrator Lambda:
  Memory: 512 MB
  Timeout: 60 seconds
  Concurrency: 10
  Runtime: Python 3.11

Document Agent Lambda:
  Memory: 1024 MB  # Higher for PDF processing
  Timeout: 30 seconds
  Runtime: Python 3.11

Analyzer Agent Lambda:
  Memory: 512 MB
  Timeout: 60 seconds  # LLM calls take time
  Runtime: Python 3.11

Planner Agent Lambda:
  Memory: 512 MB
  Timeout: 30 seconds
  Runtime: Python 3.11
```

### Cold Start Mitigation
- **POC Approach**: Accept cold starts (acceptable for demo)
- **Future**: Provisioned concurrency for critical paths

### State Management
- **DynamoDB**: Session and memory persistence
- **S3**: Document and report storage
- **Lambda Layers**: Shared dependencies to reduce deployment size

---

## Consequences

### Positive

- ✅ **Budget Compliance**: Estimated $25/month Lambda costs
- ✅ **Zero Downtime Deployments**: Blue-green via Lambda aliases
- ✅ **No Capacity Planning**: Auto-scales with demand
- ✅ **Development Speed**: Fast deploy/test cycles

### Negative

- ❌ **Cold Start Latency**: 1-3 second delays on first request
- ❌ **Execution Time Limits**: 60-second agent timeout
- ❌ **Debugging Complexity**: CloudWatch logs only, no shell access

### Risk Mitigation

**Cold Starts**: Acceptable for POC; use provisioned concurrency if needed ($15/month)
**Timeout Limits**: Design agents to complete within 60 seconds; use Step Functions for longer workflows
**Debugging**: CloudWatch Insights and X-Ray for distributed tracing

---

## Related Decisions

- **ADR-001**: AgentCore Platform (requires Lambda)
- **ADR-004**: DynamoDB Storage (complements serverless)
- **ADR-005**: CDK for IaC (serverless-friendly)
