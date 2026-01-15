# ADR-001: Amazon Bedrock AgentCore Platform Selection

**Status**: Accepted  
**Date**: January 2026  
**Decision Makers**: Architecture Team  
**Technical Story**: Multi-agent system requires robust orchestration platform

---

## Context and Problem Statement

Ready2Intern requires a multi-agent architecture with 4 specialized agents (Orchestrator, Document, Analyzer, Planner) plus company specialist sub-agents. The system must showcase modern agentic AI patterns while remaining maintainable for a POC-scope project.

**Key Requirements**:
- Multi-agent orchestration and coordination
- Session management and state persistence
- API routing for frontend integration
- Identity and session isolation
- Serverless deployment compatibility
- POC-appropriate complexity

**Decision**: Which platform should we use for implementing the multi-agent architecture?

---

## Decision Drivers

- **AgentCore Showcase**: Project specifically requires demonstrating AgentCore primitives (Runtime, Memory, Gateway, Identity)
- **Serverless Compatibility**: Must work with serverless architecture (AWS Lambda)
- **Development Speed**: POC timeline requires fast development
- **Team Expertise**: Team has advanced AWS experience
- **Cost**: Must stay within $50-100/month POC budget
- **Production Path**: Should support future production scale

---

## Considered Alternatives

### Option 1: Amazon Bedrock AgentCore (Selected)
**Description**: Use Bedrock AgentCore with Strands Agents SDK for all agent coordination

**Pros**:
- ✅ **Perfect Requirements Match**: Directly addresses project requirement to showcase AgentCore primitives
- ✅ **Integrated Primitives**: Runtime, Memory, Gateway, Identity all provided
- ✅ **AWS Native**: Deep integration with Lambda, DynamoDB, API Gateway
- ✅ **Serverless First**: Designed for serverless deployment
- ✅ **Managed Service**: Reduces operational complexity
- ✅ **Team Familiarity**: Team experienced with AWS services

**Cons**:
- ❌ **Newer Platform**: Less mature than custom orchestration
- ❌ **Learning Curve**: Strands Agents SDK requires initial learning
- ❌ **Vendor Lock-in**: Tied to AWS Bedrock ecosystem

**Cost Estimate**: Included in Bedrock API costs (~$30/month for POC)

### Option 2: Custom Lambda Orchestration
**Description**: Build custom orchestration using Lambda functions and Step Functions

**Pros**:
- ✅ **Full Control**: Complete control over orchestration logic
- ✅ **AWS Native**: Familiar AWS services (Lambda, Step Functions, SQS)
- ✅ **Flexibility**: Can customize any aspect of coordination
- ✅ **Well-Documented**: Extensive documentation and examples

**Cons**:
- ❌ **Doesn't Meet Requirements**: Project specifically requires AgentCore primitives
- ❌ **Development Time**: Significant time to build orchestration from scratch
- ❌ **Operational Complexity**: Must manage state, retries, error handling manually
- ❌ **Missing Primitives**: Would need to build Memory, Gateway, Identity separately

**Cost Estimate**: $20/month (Lambda + Step Functions)

### Option 3: LangChain with LangGraph
**Description**: Use LangChain framework with LangGraph for agent orchestration

**Pros**:
- ✅ **Rich Ecosystem**: Large community and extensive tools
- ✅ **Agent Abstractions**: Built-in agent patterns and tools
- ✅ **Flexibility**: Works with multiple LLM providers
- ✅ **Development Speed**: Pre-built components accelerate development

**Cons**:
- ❌ **Doesn't Meet Requirements**: Doesn't showcase AgentCore primitives
- ❌ **External Dependency**: Open-source framework with breaking changes
- ❌ **Integration Work**: Must integrate with AWS services manually
- ❌ **State Management**: Must implement Memory and Gateway separately

**Cost Estimate**: $30/month (Bedrock API costs + Lambda)

### Option 4: Semantic Kernel
**Description**: Microsoft's Semantic Kernel for agent orchestration

**Pros**:
- ✅ **Agent Framework**: Purpose-built for agentic AI
- ✅ **Multi-Platform**: Works with Azure, AWS, others
- ✅ **Plugin System**: Extensible with custom plugins

**Cons**:
- ❌ **Doesn't Meet Requirements**: Doesn't showcase AgentCore primitives
- ❌ **Microsoft Ecosystem**: Less natural fit for AWS-native project
- ❌ **Team Familiarity**: Team less experienced with .NET/C# ecosystem
- ❌ **Integration Complexity**: Must integrate with AWS services

**Cost Estimate**: $30/month (Bedrock API costs + Lambda)

---

## Decision Outcome

**Chosen Option**: **Amazon Bedrock AgentCore with Strands Agents SDK**

### Rationale

1. **Perfect Requirements Alignment**: Project explicitly requires showcasing AgentCore primitives (Runtime, Memory, Gateway, Identity). No other option directly satisfies this requirement.

2. **AWS Native Integration**: Deep integration with Lambda, DynamoDB, API Gateway, and S3 provides seamless serverless deployment without custom integration work.

3. **Reduced Complexity**: Managed service model reduces operational overhead for POC, allowing team to focus on agent logic rather than infrastructure.

4. **Team Expertise**: Team's advanced AWS experience directly translates to AgentCore success. No need to learn external frameworks.

5. **Cost Efficiency**: AgentCore costs included in Bedrock API pricing with no additional platform fees. Total estimate ~$63/month well within budget.

6. **Production Path**: Managed service provides clear path to production scale with AWS support and SLAs.

---

## Implementation Details

### AgentCore Primitive Usage

**Runtime Primitive** (Agent Orchestration):
```python
from strands_agents import Runtime

runtime = Runtime.create()
orchestrator = runtime.create_agent("orchestrator")
document_agent = runtime.create_agent("document")
analyzer_agent = runtime.create_agent("analyzer")
planner_agent = runtime.create_agent("planner")

# Sequential invocation
orchestrator.invoke(document_agent)
orchestrator.invoke(analyzer_agent)
orchestrator.invoke(planner_agent)
```

**Memory Primitive** (Session Persistence):
```python
from strands_agents import Memory

memory = Memory.create(backend="dynamodb")
session = memory.create_session(session_id=uuid.uuid4())
session.store("resume_data", resume)
session.store("analysis_results", results)
```

**Gateway Primitive** (API Routing):
```python
from strands_agents import Gateway

gateway = Gateway.create(api_gateway_id="xyz")
gateway.route("/api/evaluate", orchestrator_agent)
gateway.route("/api/results/{sessionId}", results_handler)
```

**Identity Primitive** (Session Management):
```python
from strands_agents import Identity

identity = Identity.create()
session = identity.create_session()
identity.associate_resource(session, s3_object)
identity.enforce_isolation(session_id)
```

### Integration with Existing AWS Services

- **Lambda Functions**: Each agent implemented as Lambda function, invoked via AgentCore Runtime
- **DynamoDB**: Used by AgentCore Memory for session persistence
- **API Gateway**: Integrated with AgentCore Gateway for routing
- **S3**: Session-scoped access enforced by AgentCore Identity

---

## Consequences

### Positive Consequences

- ✅ **Requirement Satisfaction**: Directly demonstrates all 4 AgentCore primitives as required
- ✅ **Faster Development**: Managed primitives reduce custom code by ~40%
- ✅ **Operational Simplicity**: AWS manages platform, team focuses on agent logic
- ✅ **Scalability**: Serverless-native design scales automatically with demand
- ✅ **Cost Predictability**: Pay-per-use pricing aligns with POC variability
- ✅ **Future-Proof**: Production-ready platform with AWS support

### Negative Consequences

- ❌ **Platform Lock-in**: Deep integration with AgentCore limits portability
- ❌ **Learning Curve**: Team must learn Strands Agents SDK (estimated 1-2 weeks)
- ❌ **Debugging Complexity**: Managed service may complicate debugging vs custom code
- ❌ **Version Dependencies**: Must stay compatible with AgentCore updates

### Risk Mitigation

**Risk 1: AgentCore Breaking Changes**
- **Mitigation**: Pin Strands Agents SDK version, test before upgrading
- **Fallback**: Can implement critical paths with direct Bedrock API if needed

**Risk 2: Platform Limitations**
- **Mitigation**: Validate all required features in early POC phase
- **Fallback**: Custom Lambda orchestration as documented alternative

**Risk 3: Cost Overruns**
- **Mitigation**: Set CloudWatch alarms at 80% and 100% of $100/month budget
- **Fallback**: Reduce evaluation frequency or implement caching

---

## Related Decisions

- **ADR-002**: Serverless Architecture Choice (AgentCore requires serverless)
- **ADR-003**: Document-Based Principles Approach (complements AgentCore session management)
- **ADR-004**: Multi-Agent Architecture Pattern (enabled by AgentCore Runtime)

---

## Notes

- AgentCore showcase is primary project requirement - this decision was effectively pre-determined
- Alternative frameworks evaluated for completeness but cannot satisfy core requirement
- Team's AWS expertise makes AgentCore the natural choice regardless of alternatives
