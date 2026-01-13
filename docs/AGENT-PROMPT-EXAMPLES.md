# Agent Prompt Examples
**Concise Prompts Using Reference Documents**

---

## How to Use These Prompts

1. **Create feature branch** before starting:
   ```bash
   git checkout main && git pull origin main
   git checkout -b feature/slice-N-name
   ```
2. **Copy the prompt** for the feature you want to build
3. **Start a new chat session** with your coding agent
4. **Paste the prompt** - Agent will read reference docs for details
5. **Agent works through tasks** following TODO.md
6. **Review and test** the completed feature
7. **Commit, push, and create PR** from feature branch
8. **Move to next feature** in a new session

---

## Quick Reference

All implementation details are in:
- `Ready2Intern-TODO.md` - Sequential task checklist
- `Ready2Intern-Implementation-Plan.md` - Feature slices with acceptance criteria
- `Ready2Intern-PRD.md` - Product requirements
- `Ready2Intern-API-Spec.md` - API endpoint specifications
- `Ready2Intern-UI-UX-MOCKUPS.md` - UI/UX design details

---

## Week 1: Foundation Setup

### Feature Slice 1: Project Setup & Basic Dashboard

```
Build Feature Slice 1: Project Setup & Basic Dashboard

Reference: Ready2Intern-TODO.md (Week 1 section)
Context: Ready2Intern-Implementation-Plan.md (Feature Slice 1)

Set up complete project foundation:
- Frontend: React + TypeScript + Vite + Tailwind
- Backend: FastAPI + Python 3.11+
- Health check endpoint + theme toggle
- Verify frontend-backend integration

Follow TODO checklist in sequence. All acceptance criteria in Implementation Plan.

When complete:
1. Write unit tests (frontend components + backend endpoints)
2. Run all tests and verify they pass
3. Test the feature end-to-end manually
4. Check off completed tasks in Ready2Intern-TODO.md
5. Update PROGRESS.md with what was built and lessons learned
6. Update AGENTS.md with new patterns, services, or key decisions
7. Log any issues or technical debt in ISSUES.md
8. Commit and push: "feat: initial project scaffold with health check (slice 1)"
9. Create pull request from feature branch to main
```

---

## Week 2: Resume Upload & Company Selection

### Feature Slice 2: Resume Upload

```
Build Feature Slice 2: Resume Upload

Reference: Ready2Intern-TODO.md (Week 2 - Resume Upload section)
Context: Ready2Intern-Implementation-Plan.md (Feature Slice 2)

Implement end-to-end resume upload with drag-and-drop, file validation, and session management.

Follow TODO checklist. All details in reference docs.

When complete:
1. Write unit tests (frontend components + backend endpoints)
2. Run all tests and verify they pass
3. Test the feature end-to-end manually
4. Check off completed tasks in Ready2Intern-TODO.md
5. Update PROGRESS.md with what was built and lessons learned
6. Update AGENTS.md with new patterns, services, or key decisions
7. Log any issues or technical debt in ISSUES.md
8. Commit and push:
9. Create pull request: "feat: add resume upload feature (slice 2)"
```

### Feature Slice 3: Company Selection

```
Build Feature Slice 3: Company Selection

Reference: Ready2Intern-TODO.md (Week 2 - Company Selection section)
Context: Ready2Intern-Implementation-Plan.md (Feature Slice 3)

Build company selector with logos for Amazon, Meta, and Google. Create company tenets files.

Follow TODO checklist. All details in reference docs.

When complete:
1. Write unit tests (frontend components + backend endpoints)
2. Run all tests and verify they pass
3. Test the feature end-to-end manually
4. Check off completed tasks in Ready2Intern-TODO.md
5. Update PROGRESS.md with what was built and lessons learned
6. Update AGENTS.md with new patterns, services, or key decisions
7. Log any issues or technical debt in ISSUES.md
8. Commit and push:
9. Create pull request: "feat: add company selection feature (slice 3)"
```

---

## Week 3: Role Description Input & Analyze Button

### Feature Slice 4: Role Description Input

```
Build Feature Slice 4: Role Description Input

Reference: Ready2Intern-TODO.md (Week 3 - Role Description section)
Context: Ready2Intern-Implementation-Plan.md (Feature Slice 4)

Build textarea with character counter and validation (min 50, max 10,000 chars).

Follow TODO checklist. All details in reference docs.

When complete:
1. Write unit tests (frontend components + backend endpoints)
2. Run all tests and verify they pass
3. Test the feature end-to-end manually
4. Check off completed tasks in Ready2Intern-TODO.md
5. Update PROGRESS.md with what was built and lessons learned
6. Update AGENTS.md with new patterns, services, or key decisions
7. Log any issues or technical debt in ISSUES.md
8. Commit and push:
9. Create pull request: "feat: add role description input feature (slice 4)"
```

### Feature Slice 5: Analyze Button & Loading State

```
Build Feature Slice 5: Analyze Button & Loading State

Reference: Ready2Intern-TODO.md (Week 3 - Analyze Button section)
Context: Ready2Intern-Implementation-Plan.md (Feature Slice 5)

Create analyze button with loading states and progress indicators. Set up /api/analyze endpoint.

Follow TODO checklist. All details in reference docs.

When complete:
1. Write unit tests (frontend components + backend endpoints)
2. Run all tests and verify they pass
3. Test the feature end-to-end manually
4. Check off completed tasks in Ready2Intern-TODO.md
5. Update PROGRESS.md with what was built and lessons learned
6. Update AGENTS.md with new patterns, services, or key decisions
7. Log any issues or technical debt in ISSUES.md
8. Commit and push:
9. Create pull request: "feat: add analyze button and loading state (slice 5)"
```

---

## Week 4: LLM Integration (Resume & Role Matching)

### Feature Slice 6: LLM - Resume Analysis

```
Build Feature Slice 6: LLM Resume Analysis

Reference: Ready2Intern-TODO.md (Week 4 - Resume Analysis section)
Context: Ready2Intern-Implementation-Plan.md (Feature Slice 6)

Integrate Anthropic Claude API for resume parsing. Extract skills, experience, education, and projects.

Follow TODO checklist. All details in reference docs.

When complete:
1. Write unit tests (frontend components + backend endpoints)
2. Run all tests and verify they pass
3. Test the feature end-to-end manually
4. Check off completed tasks in Ready2Intern-TODO.md
5. Update PROGRESS.md with what was built and lessons learned
6. Update AGENTS.md with new patterns, services, or key decisions
7. Log any issues or technical debt in ISSUES.md
8. Commit and push:
9. Create pull request: "feat: add LLM resume analysis (slice 6)"
```

### Feature Slice 7: LLM - Role Matching

```
Build Feature Slice 7: LLM Role Matching

Reference: Ready2Intern-TODO.md (Week 4 - Role Matching section)
Context: Ready2Intern-Implementation-Plan.md (Feature Slice 7)

Implement role matching with company tenets. Calculate ATS, Role Match, and Company Fit scores.

Follow TODO checklist. All details in reference docs.

When complete:
1. Write unit tests (frontend components + backend endpoints)
2. Run all tests and verify they pass
3. Test the feature end-to-end manually
4. Check off completed tasks in Ready2Intern-TODO.md
5. Update PROGRESS.md with what was built and lessons learned
6. Update AGENTS.md with new patterns, services, or key decisions
7. Log any issues or technical debt in ISSUES.md
8. Commit and push:
9. Create pull request: "feat: add LLM role matching analysis (slice 7)"
```

---

## Week 5: Gap Analysis & Timeline Generation

### Feature Slice 8: LLM - Gap Analysis

```
Build Feature Slice 8: Gap Analysis

Reference: Ready2Intern-TODO.md (Week 5 - Gap Analysis section)
Context: Ready2Intern-Implementation-Plan.md (Feature Slice 8)

Identify skill gaps with priority levels and generate actionable recommendations.

Follow TODO checklist. All details in reference docs.

When complete:
1. Write unit tests (frontend components + backend endpoints)
2. Run all tests and verify they pass
3. Test the feature end-to-end manually
4. Check off completed tasks in Ready2Intern-TODO.md
5. Update PROGRESS.md with what was built and lessons learned
6. Update AGENTS.md with new patterns, services, or key decisions
7. Log any issues or technical debt in ISSUES.md
8. Commit and push:
9. Create pull request: "feat: add gap analysis with recommendations (slice 8)"
```

### Feature Slice 9: LLM - Timeline Generation

```
Build Feature Slice 9: Timeline Generation

Reference: Ready2Intern-TODO.md (Week 5 - Timeline Generation section)
Context: Ready2Intern-Implementation-Plan.md (Feature Slice 9)

Generate personalized development timeline with phases and milestones based on target deadline.

Follow TODO checklist. All details in reference docs.

When complete:
1. Write unit tests (frontend components + backend endpoints)
2. Run all tests and verify they pass
3. Test the feature end-to-end manually
4. Check off completed tasks in Ready2Intern-TODO.md
5. Update PROGRESS.md with what was built and lessons learned
6. Update AGENTS.md with new patterns, services, or key decisions
7. Log any issues or technical debt in ISSUES.md
8. Commit and push:
9. Create pull request: "feat: add timeline generation (slice 9)"
```

---

## Week 6: Results Display & Export

### Feature Slice 10: Overall Score Display

```
Build Feature Slice 10: Overall Score Display

Reference: Ready2Intern-TODO.md (Week 6 - Overall Score section)
Context: Ready2Intern-Implementation-Plan.md (Feature Slice 10)

Create results page with animated overall score display and /api/results endpoint.

Follow TODO checklist. All details in reference docs.

When complete:
1. Write unit tests (frontend components + backend endpoints)
2. Run all tests and verify they pass
3. Test the feature end-to-end manually
4. Check off completed tasks in Ready2Intern-TODO.md
5. Update PROGRESS.md with what was built and lessons learned
6. Update AGENTS.md with new patterns, services, or key decisions
7. Log any issues or technical debt in ISSUES.md
8. Commit and push:
9. Create pull request: "feat: add overall score display (slice 10)"
```

### Feature Slice 11: Score Breakdown Display

```
Build Feature Slice 11: Score Breakdown

Reference: Ready2Intern-TODO.md (Week 6 - Score Breakdown section)
Context: Ready2Intern-Implementation-Plan.md (Feature Slice 11)

Display three score cards: ATS, Role Match, Company Fit with tooltips and progress bars.

Follow TODO checklist. All details in reference docs.

When complete:
1. Write unit tests (frontend components + backend endpoints)
2. Run all tests and verify they pass
3. Test the feature end-to-end manually
4. Check off completed tasks in Ready2Intern-TODO.md
5. Update PROGRESS.md with what was built and lessons learned
6. Update AGENTS.md with new patterns, services, or key decisions
7. Log any issues or technical debt in ISSUES.md
8. Commit and push:
9. Create pull request: "feat: add score breakdown display (slice 11)"
```

### Feature Slice 12: Strengths & Gaps Display

```
Build Feature Slice 12: Strengths & Gaps Display

Reference: Ready2Intern-TODO.md (Week 6 - Strengths & Gaps section)
Context: Ready2Intern-Implementation-Plan.md (Feature Slice 12)

Display strengths and gaps with expandable cards, priority badges, and recommendations.

Follow TODO checklist. All details in reference docs.

When complete:
1. Write unit tests (frontend components + backend endpoints)
2. Run all tests and verify they pass
3. Test the feature end-to-end manually
4. Check off completed tasks in Ready2Intern-TODO.md
5. Update PROGRESS.md with what was built and lessons learned
6. Update AGENTS.md with new patterns, services, or key decisions
7. Log any issues or technical debt in ISSUES.md
8. Commit and push:
9. Create pull request: "feat: add strengths and gaps display (slice 12)"
```

### Feature Slice 13: Timeline Display

```
Build Feature Slice 13: Timeline Display

Reference: Ready2Intern-TODO.md (Week 6 - Timeline section)
Context: Ready2Intern-Implementation-Plan.md (Feature Slice 13)

Build timeline visualization with phases, tasks, and milestones.

Follow TODO checklist. All details in reference docs.

When complete:
1. Write unit tests (frontend components + backend endpoints)
2. Run all tests and verify they pass
3. Test the feature end-to-end manually
4. Check off completed tasks in Ready2Intern-TODO.md
5. Update PROGRESS.md with what was built and lessons learned
6. Update AGENTS.md with new patterns, services, or key decisions
7. Log any issues or technical debt in ISSUES.md
8. Commit and push:
9. Create pull request: "feat: add timeline visualization (slice 13)"
```

### Feature Slice 14: PDF Export

```
Build Feature Slice 14: PDF Export

Reference: Ready2Intern-TODO.md (Week 6 - PDF Export section)
Context: Ready2Intern-Implementation-Plan.md (Feature Slice 14)

Implement PDF generation and download with all analysis sections.

Follow TODO checklist. All details in reference docs.

When complete:
1. Write unit tests (frontend components + backend endpoints)
2. Run all tests and verify they pass
3. Test the feature end-to-end manually
4. Check off completed tasks in Ready2Intern-TODO.md
5. Update PROGRESS.md with what was built and lessons learned
6. Update AGENTS.md with new patterns, services, or key decisions
7. Log any issues or technical debt in ISSUES.md
8. Commit and push:
9. Create pull request: "feat: add PDF export functionality (slice 14)"
```

### Feature Slice 15: Error Handling & Polish

```
Build Feature Slice 15: Error Handling & Polish

Reference: Ready2Intern-TODO.md (Week 6 - Error Handling section)
Context: Ready2Intern-Implementation-Plan.md (Feature Slice 15)

Add comprehensive error handling, loading states, testing, and final polish.

Follow TODO checklist. All details in reference docs.

When complete:
1. Write unit tests (frontend components + backend endpoints)
2. Run all tests and verify they pass
3. Test the feature end-to-end manually
4. Check off completed tasks in Ready2Intern-TODO.md
5. Update PROGRESS.md with what was built and lessons learned
6. Update AGENTS.md with new patterns, services, or key decisions
7. Log any issues or technical debt in ISSUES.md
8. Commit and push:
9. Create pull request: "feat: add error handling and polish (slice 15)"
```

---

## Ultra-Minimal Format (Alternative)

If your agent is familiar with the project:

```
Slice [N]: [Feature Name]
→ Ready2Intern-TODO.md (Week [N])
→ Ready2Intern-Implementation-Plan.md (Slice [N])
```

**Examples:**

```
Slice 1: Setup
→ Ready2Intern-TODO.md (Week 1)
→ Ready2Intern-Implementation-Plan.md (Slice 1)
```

```
Slice 2: Resume Upload
→ Ready2Intern-TODO.md (Week 2, Resume Upload)
→ Ready2Intern-Implementation-Plan.md (Slice 2)
```

```
Slice 6: LLM Resume Analysis
→ Ready2Intern-TODO.md (Week 4, Resume Analysis)
→ Ready2Intern-Implementation-Plan.md (Slice 6)
```

---

## Session Management

### Start of Session
```
Read Ready2Intern-TODO.md and Ready2Intern-Implementation-Plan.md for [Feature Slice N].
Confirm understanding before starting.
```

### During Session
```
Show progress after each major task:
✅ [Task] Complete
🎯 Next: [Task]
```

### End of Session
```
Verify all acceptance criteria met.
Run tests.
Commit with specified message.
```

---

## When to Add More Detail

Only expand the prompt if:
- ❌ Deviating from documented plan
- ❌ Special considerations or blockers
- ❌ Agent needs clarification
- ❌ Testing specific edge cases

Otherwise, **trust your documentation** and keep prompts minimal.

---

## Tips for Success

### ✅ DO:
- Point to specific sections in reference docs
- Let agent read details from TODO.md
- Keep prompts under 10 lines
- Trust the documentation

### ❌ DON'T:
- Repeat information already in docs
- List all tasks in prompt
- Copy acceptance criteria
- Over-specify implementation details

---

## Testing Requirements

After implementing each feature, the agent must:

### 1. Write Unit Tests
**Backend:**
```bash
# Test API endpoints, services, models
pytest tests/test_[feature].py -v
```

**Frontend:**
```bash
# Test components, hooks, utilities
npm test -- [ComponentName]
```

### 2. Run All Tests
```bash
# Backend
cd backend && pytest tests/ -v

# Frontend
cd frontend && npm test
```

### 3. Manual End-to-End Testing
- Test the complete user flow in browser
- Verify all acceptance criteria met
- Test error cases and edge cases
- Check responsive design (mobile/desktop)

---

## Documentation Updates

After completing each feature slice, the agent must:

### 1. Update Ready2Intern-TODO.md
```markdown
Change: - [ ] Task description
To:     - [x] Task description
```

### 2. Update PROGRESS.md
Add to the appropriate section:
```markdown
### ✅ Feature Slice N: [Feature Name] (Completed)
**Completed:** [Date]

**What Was Built:**
- Component/file names created
- API endpoints implemented
- Key functionality delivered

**Key Decisions:**
- Technical choices made
- Patterns established
- Libraries/tools used

**Lessons Learned:**
- What worked well
- What to improve
- Gotchas to remember

**Integration Points:**
- How it connects to other features
- State management approach
- API contracts established

**Tests Added:**
- Unit tests written
- Test coverage percentage
- Manual testing completed
```

### 3. Update AGENTS.md
Add new knowledge acquired during implementation:
```markdown
**Status Update:**
- Change ⏳ to 🚧 when starting
- Change 🚧 to ✅ when complete

**Add Implementation Notes:**
- New services/utilities created
- Reusable patterns established
- API client methods added
- Important configuration changes
- Common pitfalls discovered
```

Keep updates concise - 1-3 lines per item.

### 4. Update ISSUES.md (if needed)
Document any blockers, bugs, or technical debt:
```markdown
### Issue #N: [Brief Title]
**Type:** Bug | Technical Debt | Blocker
**Feature:** Slice N - [Feature Name]
**Description:** [What's wrong or needs improvement]
**Workaround:** [Temporary solution if any]
**Priority:** High | Medium | Low
```

---

## Summary

**Key Principle:** Your reference documents contain all the details. Prompts should just point the agent to the right section.

**Result:**
- Faster prompting (< 1 minute per feature)
- Consistent implementation (follows documented plan)
- Less repetition (single source of truth)
- Clearer communication (reference-based)

**Remember:** If it's in the docs, don't put it in the prompt.

**After Each Feature (Required):**
1. ✅ Write and run unit tests (frontend + backend)
2. ✅ Test feature end-to-end manually
3. ✅ Update TODO.md (check off completed tasks)
4. ✅ Update PROGRESS.md (what was built + lessons learned)
5. ✅ Update AGENTS.md (new patterns/services/decisions - keep concise)
6. ✅ Update ISSUES.md (if bugs or technical debt found)
7. ✅ Commit with proper message
