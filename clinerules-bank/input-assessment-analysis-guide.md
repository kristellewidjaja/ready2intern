---
inclusion: manual
---

# Input Assessment Analysis Methodology

## Overview

This methodology provides a focused approach for conducting input assessment analysis as the foundation for specification package generation. The assessment ensures understanding of key project context, identifies critical information gaps, and establishes generation readiness.

## Purpose
Analyze project documents to establish foundation for specification generation.

### Key Objectives
- Summarize key documents and extract essential context
- Identify critical information gaps
- Map stakeholders and requirements
- Assess generation readiness

## Input Assessment Framework

### 1. Document Inventory and Cataloging

### Document Classification
Systematically catalog all project documents by type and relevance:

**Primary Documents** (Direct project scope and requirements):
- Statement of Work (SOW)
- Opportunity Quality Review (OQR)
- Business Requirements Documents (BRD)
- Technical Requirements Documents (TRD)
- Project proposals and contracts

**Secondary Documents** (Supporting context and background):
- Meeting notes and email threads
- Stakeholder briefing documents
- Presentation materials
- Technical assessments
- Market analysis and competitive intelligence

**Reference Documents** (Standards and guidelines):
- Compliance requirements
- Security standards
- Technical architecture guidelines
- Organizational policies and procedures

#### Document Analysis Template
For each document:

```markdown
### Document: [Document Name]
- **Type**: [Primary/Secondary/Reference]
- **Size**: [Document length]
- **Key Content**: [Essential information summary]
- **Gaps**: [Missing information]
```

### 2. Business Context Analysis
- **Customer**: [Organization and industry]
- **Project Scope**: [Brief description]
- **Key Stakeholders**: [Primary users and decision makers]
- **Business Objectives**: [Top 3 goals]
- **Success Criteria**: [Key measures]
- **Constraints**: [Timeline and budget]

### 3. Technical Context Analysis

#### Current State Assessment
- **Technology Stack**: [Current platforms and systems]
- **Integrations**: [Key dependencies]
- **Constraints**: [Technical limitations and requirements]

#### Proposed Solution Context
- **Architecture**: [Proposed system design]
- **Technology**: [Selected stack and rationale]
- **Implementation**: [Development approach]

### 4. Information Gap Analysis

#### Gap Identification Framework
**Critical Gaps** (Must resolve): [List essential missing information]
**Important Gaps** (Should clarify): [List helpful missing information]
**Nice-to-Have Gaps** (Can defer): [List optional missing information]

#### Gap Impact Assessment
```markdown
### Gap: [Gap Description]
- **Impact**: [High/Medium/Low]
- **Resolution**: [How to address]
- **Assumptions**: [If gap remains]
```

### 5. Generation Readiness Assessment

#### Readiness Assessment
**Information Completeness**: [Score]/100
**Information Quality**: [Score]/100

#### Readiness Decision
- **Ready** (≥80): Proceed with generation
- **Caution** (60–79): Proceed with documented assumptions
- **Discovery Needed** (<60): Address critical gaps first

## Output Generation Guidelines

### Input Assessment Analysis Document Structure

```markdown
# Input Assessment Analysis

## Document Inventory
[List of key documents with type and content summary]

## Business Context
[Organization, scope, stakeholders, objectives, constraints]

## Technical Context
[Current state, proposed solution, implementation approach]

## Information Gaps
[Critical, important, and nice-to-have gaps with resolution approach]

## Generation Readiness
[Readiness score and recommendation]
```

### Quality Standards
- **Completeness**: All documents analyzed, stakeholders identified, gaps assessed
- **Accuracy**: Information correctly extracted and interpreted
- **Actionability**: Clear recommendations and next steps provided

### Integration with Specification Generation
- Business context informs requirements prioritization
- Technical context guides architecture decisions
- Gap management ensures quality specifications
- Readiness assessment confirms generation can proceed

## Success Metrics
- **Completeness**: Documents analyzed and stakeholders mapped
- **Accuracy**: Correct information extraction and interpretation
- **Readiness**: Objective assessment of generation readiness