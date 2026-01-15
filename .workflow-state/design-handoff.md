# Design Agent Workflow - [PROJECT-NAME]

---
## Status Update Protocol

**Workflow Status Values**: `ready` | `in-progress` | `complete` | `gathering_feedback`

**Task Status Values**: `not_started` | `current` | `complete`

**BEFORE task**: Set `status="current"`, update `activeTask`
**AFTER task**: Set `status="complete"`, increment `completed`, recalc `percentage`, set NEXT to `"current"`
**Validate:** JSON valid, counts match, percentage = (completed/total)*100

**Cascading Rules (IMPORTANT)**:
- When first subtask starts ➔ both subtask AND parent must become `current`
- When last subtask completes ➔ both subtask AND parent must become `complete`
- When middle subtask’s previous becomes `complete`, current becomes `current`, parent stays `current`

**Feedback Workflow**:
- When user provides feedback ➔ status becomes `gathering_feedback`
- Feedback iteration number computed by counting existing "Feedback Iteration N" tasks
- Feedback task dynamically injected when user starts feedback workflow
- Agent generates improvement tasks as subtasks below feedback documents
- After feedback complete ➔ status returns to `complete`, new specification package iteration created
**See task-modules/08-incorporate-feedback.md for detailed feedback processing instructions**

*Full protocol in task-modules/00-session-management.md*

---

## Current Status
<workflow-status>
```json
{
  "workflowStage": "Stage 3: Architecture Generation",
  "activeTask": "Task 3.1: Check Intelligence Hub availability",
  "overallProgress": {
    "completed": 6,
    "total": 10,
    "percentage": 60
  },
  "currentFeedbackIteration": 0,
  "currentStageProgress": {
    "stageName": "Architecture Generation",
    "stageCompleted": 0,
    "stageTotal": 5
  },
  "taskDetails": [
    {
        "taskNumber": "0",
        "taskName": "Session Management",
        "status": "complete",
        "subtasks": [
            {
                "taskNumber": "0.1",
                "taskName": "Prepare workflow",
                "status": "complete"
            },
            {
                "taskNumber": "0.2",
                "taskName": "Collect project information",
                "status": "complete"
            },
            {
                "taskNumber": "0.3",
                "taskName": "Verify setup complete",
                "status": "complete"
            }
        ]
    },
    {
        "taskNumber": "1",
        "taskName": "Project Analysis",
        "status": "complete",
        "subtasks": [
            {
                "taskNumber": "1.1",
                "taskName": "Project complexity assessment",
                "status": "complete"
            }
        ]
    },
    {
        "taskNumber": "2",
        "taskName": "Requirements Generation",
        "status": "current",
        "subtasks": [
            {
                "taskNumber": "2.1",
                "taskName": "Analyze project inputs",
                "status": "current"
            },
            {
                "taskNumber": "2.2",
                "taskName": "Generate requirements",
                "status": "not_started"
            },
            {
                "taskNumber": "2.3",
                "taskName": "Verify requirements completeness",
                "status": "not_started"
            },
            {
        "taskNumber": "3",
        "taskName": "Architecture Generation",
        "status": "not_started",
        "subtasks": [
            {
            "taskNumber": "3.1",
            "taskName": "Check Intelligence Hub availability",
            "status": "not_started"
            },
            {
            "taskNumber": "3.2",
            "taskName": "Generate architecture design",
            "status": "not_started"
            },
            {
            "taskNumber": "3.3",
            "taskName": "Create architecture diagrams and specifications",
            "status": "not_started"
            },
            {
            "taskNumber": "3.4",
            "taskName": "Validate architecture completeness",
            "status": "not_started"
            },
            {
            "taskNumber": "3.5",
            "taskName": "Validate AI agent architecture with AgentCore MCP (optional)",
            "status": "not_started"
            }
        ]
    },
    {
        "taskNumber": "4",
        "taskName": "Holistic Quality Assessment",
        "status": "not_started",
        "subtasks": [
            {
                "taskNumber": "4.1",
                "taskName": "Assess specification quality",
                "status": "not_started"
            },
            {
                "taskNumber": "4.2",
                "taskName": "Improve requirements and architecture",
                "status": "not_started"
            },
            {
                "taskNumber": "4.3",
                "taskName": "Verify quality standards met",
                "status": "not_started"
            }
        ],
    },
    {
        "taskNumber": "5",
        "taskName": "Security Assessment",
        "status": "not_started",
        "subtasks": [
            {
                "taskNumber": "5.1",
                "taskName": "Threat model generation",
                "status": "not_started"
            },
            {
                "taskNumber": "5.2",
                "taskName": "Map security controls to threats",
                "status": "not_started"
            },
            {
                "taskNumber": "5.3",
                "taskName": "Integrate security into specification",
                "status": "not_started"
            }
        ]
    },
    {
        "taskNumber": "6",
        "taskName": "Property Identification",
        "status": "not_started",
        "subtasks": [
            {
                "taskNumber": "6.1",
                "taskName": "Requirements Analysis",
                "status": "not_started"
            },
            {
                "taskNumber": "6.2",
                "taskName": "Property Identification",
                "status": "not_started"
            },
            {
                "taskNumber": "6.3",
                "taskName": "Property Documentation",
                "status": "not_started"
            }
        ]
    },
    {
        "taskNumber": "7",
        "taskName": "Documentation Generation",
        "status": "not_started",
        "subtasks": [
            {
                "taskNumber": "7.1",
                "taskName": "Tools prescriptive guidance generation",
                "status": "not_started"
            },
            {
                "taskNumber": "7.2",
                "taskName": "Executive summary and navigation documentation generation",
                "status": "not_started"
            },
            {
                "taskNumber": "7.3",
                "taskName": "Process documentation and change log generation",
                "status": "not_started"
            },
            {
                "taskNumber": "7.4",
                "taskName": "Project risk analysis",
                "status": "not_started"
            },
            {
                "taskNumber": "7.5",
                "taskName": "Documentation quality validation",
                "status": "not_started"
            }
        ]
    },
    {
        "taskNumber": "8",
        "taskName": "Output Organization",
        "status": "not_started",
        "subtasks": [
            {
                "taskNumber": "8.1",
                "taskName": "Create project folders",
                "status": "not_started"
            },
            {
                "taskNumber": "8.2",
                "taskName": "Organize deliverables",
                "status": "not_started"
            },
            {
                "taskNumber": "8.3",
                "taskName": "Structure specialized content",
                "status": "not_started"
            },
            {
                "taskNumber": "8.4",
                "taskName": "Prepare final package",
                "status": "not_started"
            }
        ],
        "lastUpdated": "2025-10-01T00:00:00Z",
        "status": "ready"
    }
}
```
</workflow-status>

## Stage Completion Status
- [ ] Stage 0: Session Management
- [ ] Stage 1: Project Analysis
- [ ] Stage 2: Requirements Generation
- [ ] Stage 3: Architecture Generation
- [ ] Stage 4: Holistic Quality Assessment
- [ ] Stage 5: Security Assessment
- [ ] Stage 6: Property Identification
- [ ] Stage 7: Documentation Generation
- [ ] Stage 8: Output Organization
- [ ] Stage 9+: Feedback Integration (when feedback provided)

## Project Context and Initialization
- **Project Name:** ready2intern
- **Project Folder:** `generated/design/ready2intern/`
- **Input Scenario:** Existing Documents (Simple)

**Input Source Analysis:**
- **project-context/**: 1 file (requirements.md) - Project requirements and context
- **organization-context/**: Empty - No organizational policies provided yet
- **technical-knowledge/**: Empty - No external reference materials provided yet
- **project-code/**: Empty - No existing codebase to analyze
- **Complexity Assessment:** Simple (single file, markdown, small size)

## Files Created/Updated
- `.workflow-state/design-handoff.md` - Updated with Task 0.1 progress and input scenario

## Key Insights & Decisions
**Task 0.1 Completed:**
- Input scenario identified: Existing Documents (Simple complexity)
- Project name extracted: ready2intern (AI Internship Readiness Platform)
- Single requirements document exists in project-context folder
- Organization-context, technical-knowledge, and project-code folders are empty

**Task 0.2 Completed:**
- Customer context captured and documented in `.workflow-state/customer-context.md`
- Project Type: POC (Proof of Concept)
- Infrastructure: Serverless with Amazon Bedrock AgentCore
- IaC Preference: AWS CDK
- Team Experience: Advanced AWS
- Execution Mode: Full workflow (user requested "please continue")

**Task 0.3 Verification:**
- ✓ Prerequisites met: design-handoff.md and customer-context.md exist
- ✓ Handoff protocol understood: BEFORE/AFTER updates, cascading rules
- ✓ Ready for Stage 1: Project Analysis

**Task 1.1: Project Complexity Assessment**

**Complexity Level**: Simple

**Input Analysis**:
- **Input Scenario**: Existing Documents (Simple)
- **Documents** (`project-doc/` folder): 1 file, <0.1 MB, markdown format
  - `project-context/requirements.md` - Project requirements and context document
- **User Context** (from `.workflow-state/customer-context.md`): Comprehensive POC context captured
  - Project Type: POC (Proof of Concept)
  - Infrastructure: Serverless with Amazon Bedrock AgentCore
  - IaC: AWS CDK, Team: Advanced AWS experience
- **Additional Context** (from current prompt): User requested full workflow execution ("please continue")

**Code Project Detection** (MANDATORY):
- **Project-Code Folder Status**: Exists but empty
- **Code Projects Detected**: No code projects provided
- **Ingestion Status**: Skipped - no code projects to ingest

**Codebase Analysis**: N/A - No existing codebases provided

**Time Estimate**: 2-3 hours total workflow time

**Recommendations**:
- **Execution Strategy**: Full workflow (auto-proceed) - Simple complexity with single requirements file
- **Session Management**: Single session recommended - low complexity, no timeout risk
- **Risk Factors**: None identified - straightforward POC with clear requirements
- **AgentCore Focus**: Architecture must showcase AgentCore primitives per customer context

**Next Steps**: Proceed to Stage 2 (Requirements Generation) to analyze requirements document and generate comprehensive specification package

## Architecture Generation Path Selection
**Task 3.1 Completed - Path Selection Determined**

**Selected Path**:
- [ ] Path A: Intelligence Hub Integration (when Intelligence Hub available)
- [x] Path B: Standard Architecture Generation (when Intelligence Hub unavailable)

**Path Selection Rationale**:
- **MCP Configuration Check**: Examined `.vscode/mcp.json` configuration file
- **Intelligence Hub Status**: NOT CONFIGURED - No "intelligence-hub" server entry found in MCP configuration
- **Configuration Contents**: Only "fetch" server is configured in MCP settings
- **Availability Determination**: Intelligence Hub unavailable due to missing configuration
- **Selected Approach**: Path B (Standard Architecture Generation) will be executed
- **Execution Strategy**: Systematic architecture generation using architecture guidance selection framework, reference architectures, and customer context analysis

**Note:** Task 3.2 will execute Path B steps exclusively based on this selection.

**Task 3.2 - Step B2: Architecture Guidance Selection**

**Decision Hierarchy Evaluation Results**:
1. **ProServe Solutions**: ❌ NO MATCH (Seed-Farmer: not multi-account, ADDf: not automotive)
2. **Prescriptive Guidance - Agentic AI**: ✅ STRONG MATCH (multi-agent system, AgentCore primitives, serverless)
3. **AWS Documentation Search**: ⊘ SKIPPED (MCP server not configured)
4. **Well-Architected Framework**: ✅ SUPPLEMENTARY (GenAI Lens, Serverless Lens for validation)

**Selected Guidance Approach**:
- **Primary**: Prescriptive Guidance - Agentic AI (`prescriptive-guidance/agentic-ai/`)
- **Supplementary**: Well-Architected Framework - Generative AI Lens + Serverless Applications Lens

**Selection Rationale**:
- Multi-agent architecture with 4 specialized agents perfectly matches agentic AI patterns
- AgentCore primitives (Runtime, Memory, Gateway, Identity) require agentic AI guidance
- Serverless architecture aligns with serverless agentic AI patterns in prescriptive guidance
- POC scope benefits from proven agentic AI implementation patterns
- Well-Architected lenses provide best practices validation for AI/ML and serverless

## Reference Architecture Repositories
No reference architecture repositories identified - selected guidance is documentation-based (prescriptive guidance documents and Well-Architected lenses).

**Task 3.2 - Steps B3-B5: Execution Summary**

**Step B3: Reference Architecture Analysis** - ✅ SKIPPED
- **Enforcement Check**: No reference architectures selected in B2 and no existing codebases
- **Decision**: Step B3 can be skipped per framework rules

**Step B4: Reference Architecture Integration Design** - ✅ SKIPPED  
- **Enforcement Check**: Step B3 was skipped
- **Decision**: Step B4 can be skipped per framework rules (only mandatory if B3 executed)

**Step B5: Context-Aware Architecture Design** - ✅ COMPLETE
- **Mode Selection**: POC Mode (based on customer context analysis)
- **Architecture Approach**: Streamlined architecture for core functionality validation
- **Key Focus Areas**:
  - Multi-agent serverless architecture using Amazon Bedrock AgentCore
  - Showcase all 4 AgentCore primitives (Runtime, Memory, Gateway, Identity)
  - 4 specialized agents: Orchestrator, Document, Analyzer, Planner
  - Company specialist sub-agents for company-specific evaluation
  - Document-based company principles loading mechanism
  - Simple 3-step workflow (upload resume, upload job description, select company)
  - AWS services: Lambda, API Gateway, DynamoDB, S3, Bedrock
  - Infrastructure as Code: AWS CDK
  - POC-appropriate targets: 20-50 users, 100-500 evaluations, $50-100/month budget
- **Design Strategy**: Prioritize simplicity, speed to value, and AgentCore demonstration over enterprise complexity

**Task 3.2 Status**: All Path B steps (B1-B5) complete and verified
**Next Task**: Task 3.3 - Create Architecture Diagrams and Specifications

## Issues Encountered
*Workflow not started*

## Next Stage Details
- **Stage**: Ready to begin with Stage 0: Session Management
- **Objective**: Initialize workflow, capture context, determine execution mode
- **Dependencies**: None - Workflow initialization

## Session Instructions

### To Start: Execute design agent workflow – will read this handoff and begin with Stage 0

### Progress Updates: Update taskDetails status when completing each stage (not_started → current → complete)