# Ready2Intern POC - Issues

**Last Updated:** January 15, 2026

---

## Active Issues

_No active issues. Feature Slice 6 completed successfully._

---

## Resolved Issues

_No issues encountered during Feature Slices 1-3._

---

## Technical Debt

#### TD-1: Frontend Test Infrastructure Not Set Up
**Added:** January 13, 2026 (Feature Slice 3)
**Priority:** Medium

**Description:**
Frontend tests are placeholder files. Need to set up Vitest, React Testing Library, and configure test environment.

**Action Items:**
- Install testing dependencies (vitest, @testing-library/react, etc.)
- Create vitest.config.ts
- Set up test setup file with jest-dom
- Implement actual tests for CompanyLogoSelector and API service
- Add test script to package.json

**Assigned To:** Future sprint (not blocking POC)

---

#### TD-2: FastAPI on_event Deprecation Warnings
**Added:** January 13, 2026 (Feature Slice 3)
**Priority:** Low

**Description:**
Using deprecated `@app.on_event("startup")` and `@app.on_event("shutdown")` decorators. FastAPI recommends using lifespan event handlers instead.

**Action Items:**
- Refactor to use lifespan context manager
- Update main.py to use modern pattern
- Reference: https://fastapi.tiangolo.com/advanced/events/

**Assigned To:** Future cleanup (not blocking POC)

---

#### TD-3: PyPDF2 Deprecation Warning
**Added:** January 15, 2026 (Feature Slice 6)
**Priority:** Low

**Description:**
Using deprecated PyPDF2 library. The library maintainers recommend migrating to pypdf instead.

**Action Items:**
- Replace `PyPDF2` with `pypdf` in requirements.txt
- Update import statement in resume_parser.py: `from pypdf import PdfReader`
- Test PDF extraction still works correctly
- Update documentation

**Assigned To:** Future cleanup (not blocking POC)

---

## Enhancement Ideas

_Enhancement ideas will be captured here for future consideration._

---

## Issue Template

When logging new issues, use this format:

```markdown
#### Issue #[N]: [Brief description]
**Discovered:** [Date] ([Feature Slice])
**Severity:** [High/Medium/Low]
**Impact:** [User impact description]

**Description:**
[Detailed description of the issue]

**Steps to Reproduce:**
1. [Step 1]
2. [Step 2]
3. [Expected vs Actual result]

**Root Cause:** (if known)
[Technical explanation of why this happens]

**Workaround:** (if available)
[Temporary solution users can use]

**Fix Required:**
- [Action item 1]
- [Action item 2]

**Assigned To:** [Next session / Specific feature slice]
**Priority:** [When to fix this]
```

---

## Severity Levels

### 🔴 High Priority
- Blocks development
- Causes data loss
- Security vulnerability
- Critical user flow broken

### 🟡 Medium Priority
- Degrades user experience
- Workaround available
- Affects non-critical features
- Performance issues

### 🟢 Low Priority
- Minor UI issues
- Nice-to-have improvements
- Edge cases
- Cosmetic issues

---

## Notes

- Check this file before starting each feature slice
- Update this file when discovering new issues
- Mark issues as resolved when fixed
- Link issues to git commits when possible
- Use issue numbers (#1, #2, etc.) for easy reference

See AGENT-WORKFLOW.md for how to use this file effectively.
