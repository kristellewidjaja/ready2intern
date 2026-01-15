# ADR-003: Document-Based Company Principles Loading

**Status**: Accepted  
**Date**: January 2026  
**Decision Makers**: Architecture Team  
**Technical Story**: Company specialist sub-agents need access to organizational principles

---

## Context and Problem Statement

The Internship Analyzer Agent must evaluate resumes against company-specific organizational principles (e.g., Amazon Leadership Principles). The system needs a way to store and load these principles for use by company specialist sub-agents.

**Key Requirements**:
- Store company-specific evaluation criteria (Amazon Leadership Principles initially)
- Easy updates when principles change
- Version control for principles documents
- Direct access by agents without complex infrastructure
- Support for multiple companies (Amazon, Meta, Google)

**Decision**: How should we store and load company organizational principles?

---

## Decision Drivers

- **Simplicity**: POC requires straightforward implementation
- **Version Control**: Principles should be tracked in git
- **Easy Updates**: Non-technical updates should be possible
- **No Complex Infrastructure**: Minimize additional services
- **AgentCore Compatibility**: Work with AgentCore session management
- **Multi-Company Support**: Support Amazon now, Meta/Google future

---

## Considered Alternatives

### Option 1: File System Documents (Selected)

**Description**: Store principles as markdown files in `project-doc/organization-context/`, load directly by agents

**Pros**:
- ✅ **Simplicity**: No additional infrastructure required
- ✅ **Version Control**: Files tracked in git automatically
- ✅ **Easy Updates**: Edit markdown files directly
- ✅ **Fast Access**: Direct file system reads, no API calls
- ✅ **Developer Friendly**: Markdown easy to read and edit
- ✅ **Zero Cost**: No storage or database costs

**Cons**:
- ❌ **Manual Deployment**: Must redeploy to update principles
- ❌ **No Runtime Updates**: Cannot update without redeployment
- ❌ **Lambda Package Size**: Principles bundled in deployment package

**Cost**: $0 (included in Lambda deployment)

### Option 2: DynamoDB Table

**Description**: Store principles in DynamoDB table, query at runtime

**Pros**:
- ✅ **Runtime Updates**: Update principles without redeployment
- ✅ **Centralized**: Single source of truth
- ✅ **Queryable**: Complex queries possible

**Cons**:
- ❌ **Additional Cost**: ~$5/month for table
- ❌ **Complexity**: Requires CRUD operations, schema design
- ❌ **No Version Control**: Manual tracking of changes
- ❌ **Latency**: Network call adds 10-50ms per evaluation
- ❌ **Overkill for POC**: More infrastructure than needed

**Cost**: ~$5/month

### Option 3: S3 Bucket

**Description**: Store principles as files in S3, download at runtime

**Pros**:
- ✅ **Runtime Updates**: Update files without Lambda redeploy
- ✅ **Version Control**: S3 versioning available
- ✅ **Low Cost**: Minimal storage costs

**Cons**:
- ❌ **Latency**: S3 API call adds 50-100ms per load
- ❌ **Complexity**: Requires S3 client, bucket policies
- ❌ **Cache Management**: Must cache to avoid repeated downloads
- ❌ **Git Separation**: Files separate from code repository

**Cost**: ~$0.50/month

### Option 4: Amazon Bedrock Knowledge Base

**Description**: Use Bedrock Knowledge Base for principles storage and retrieval

**Pros**:
- ✅ **Semantic Search**: Can query principles by relevance
- ✅ **AWS Managed**: Fully managed service
- ✅ **Scalable**: Handles large principle sets

**Cons**:
- ❌ **Complexity**: Knowledge base setup, ingestion, indexing
- ❌ **Cost**: ~$10-20/month for POC scale
- ❌ **Overkill**: Semantic search not required for principles
- ❌ **Latency**: Additional API calls for retrieval
- ❌ **Requirements Conflict**: Requirements explicitly state "NOT knowledge base"

**Cost**: ~$15/month

---

## Decision Outcome

**Chosen Option**: **File System Documents (Markdown Files)**

### Rationale

1. **Requirements Alignment**: Requirements.md explicitly states "Document-based approach (NOT knowledge base)"

2. **POC Simplicity**: Zero additional infrastructure aligns with POC scope and budget constraints

3. **Version Control**: Git tracks all principle changes automatically with full history

4. **Fast Access**: Direct file reads (microseconds) vs network calls (50-100ms)

5. **Developer Experience**: Markdown files easy to edit, review in PRs, and understand

6. **Zero Cost**: No additional AWS services or storage costs

---

## Implementation Details

### File Structure

```
project-doc/organization-context/
├── amazon-leadership-principles.md
├── meta-values.md (future)
└── google-principles.md (future)
```

### Document Format

**Example: amazon-leadership-principles.md**
```markdown
# Amazon Leadership Principles

## Customer Obsession
Leaders start with the customer and work backwards...

## Ownership
Leaders are owners. They think long term...

## Invent and Simplify
Leaders expect and require innovation...

[Continue for all 16 principles]
```

### Loading Strategy

**Agent Code**:
```python
import os
from pathlib import Path

class CompanyPrinciplesLoader:
    def __init__(self):
        self.principles_dir = Path("project-doc/organization-context")
        self.cache = {}
    
    def load_principles(self, company: str) -> str:
        """Load company principles with caching"""
        if company in self.cache:
            return self.cache[company]
        
        filename = f"{company.lower()}-principles.md"
        filepath = self.principles_dir / filename
        
        try:
            with open(filepath, 'r') as f:
                principles = f.read()
            self.cache[company] = principles
            return principles
        except FileNotFoundError:
            # Graceful fallback
            return self._get_generic_principles()
    
    def _get_generic_principles(self) -> str:
        """Fallback when company principles missing"""
        return "Use general internship evaluation criteria..."
```

### Deployment Process

1. **Development**: Edit markdown files in git repository
2. **Review**: Code review via Pull Request
3. **Deploy**: CDK packages principles in Lambda deployment
4. **Runtime**: Agents read from file system, cache in memory

### Cache Strategy

- **Load Once Per Lambda Instance**: Principles loaded when Lambda starts
- **Cache in Memory**: Store principles in agent memory for session duration
- **Cold Start Impact**: Initial 10-20ms to read file (acceptable)
- **Memory Usage**: ~10KB per principles document (negligible)

---

## Consequences

### Positive Consequences

- ✅ **Zero Additional Cost**: No database or storage costs
- ✅ **Fast Performance**: Sub-millisecond file reads
- ✅ **Version Control**: Full git history of principle changes
- ✅ **Simple Deployment**: No separate deployment step for principles
- ✅ **Easy Updates**: Edit markdown, commit, deploy
- ✅ **Code Proximity**: Principles live with code in same repository

### Negative Consequences

- ❌ **Deployment Required**: Must redeploy Lambda to update principles
- ❌ **No Hot Updates**: Cannot update principles while system running
- ❌ **Package Size**: Principles add to Lambda deployment package (~50KB)

### Trade-offs Accepted

**Trade-off**: Redeployment required for principle updates  
**Rationale**: POC scope, principles change infrequently (quarterly at most)  
**Mitigation**: Fast CDK deployment (<2 minutes) acceptable for POC

**Trade-off**: No runtime principle updates  
**Rationale**: Principles are stable, don't require hot updates  
**Mitigation**: Can move to S3 if frequent updates needed in production

---

## Future Considerations

### Production Evolution Path

**If principles require frequent updates** (>monthly):
- **Option A**: Move to S3 with Lambda caching
- **Option B**: DynamoDB with version tracking
- **Cost Impact**: +$5/month for either option

**If semantic search becomes valuable**:
- **Option**: Bedrock Knowledge Base
- **Use Case**: "Find principles related to customer service"
- **Cost Impact**: +$15/month

### Multi-Region Deployment

Current file-based approach works for multi-region:
- Principles bundled in each region's Lambda deployment
- No cross-region data transfer costs
- No synchronization issues

---

## Related Decisions

- **ADR-001**: AgentCore Platform (principles integrate with session management)
- **ADR-002**: Serverless Architecture (file system read fits Lambda model)
- **ADR-004**: Company Sub-Agent Design (sub-agents consume principles)

---

## Validation

**Requirements Traceability**:
- ✅ FR-005: Company Principles Loading (satisfied)
- ✅ Requirements.md Design Requirements: Document-based approach (satisfied)
- ✅ Cost Constraint: $0 additional cost (satisfied)

**Success Criteria**:
- Principles loadable by agents ✅
- Version controlled in git ✅
- Easy to update ✅
- No knowledge base ✅

---

## Notes

- **Requirements Mandate**: This was not a free choice - requirements explicitly specified document-based approach
- **POC Appropriate**: File system approach perfect for POC; production may evolve to S3 if update frequency increases
- **Git-Friendly**: Markdown files enable collaborative editing and PR reviews
