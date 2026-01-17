# Ready2Intern POC - Issues

**Last Updated:** January 15, 2026

---

## Active Issues

_No active issues. Gap analysis JSON parsing fix implemented._

---

## Resolved Issues

#### Issue #1: Gap Analysis LLM JSON Parsing Failures ✅ RESOLVED
**Discovered:** January 15, 2026 (Feature Slice 10 Testing)
**Resolved:** January 15, 2026
**Severity:** High
**Impact:** Analyze endpoint fails intermittently during gap analysis phase, preventing users from completing analysis

**Description:**
The gap analysis service occasionally received malformed JSON from the LLM (Claude API), causing the analyze endpoint to fail with 500 errors. The JSON parsing error typically occurred around character 53,000-72,000.

**Root Cause:**
- Gap analysis used max_tokens=12000-16384 which could be too high
- Comprehensive prompts asked for very detailed responses
- LLM sometimes generated JSON with syntax errors in large responses

**Resolution Implemented:**
1. ✅ Installed `json-repair==0.55.0` library for robust JSON fixing
2. ✅ Simplified `_parse_llm_response()` to use json-repair library
3. ✅ Added "LIMIT GAPS" instructions to prompt (max 3-5 per category)
4. ✅ Reduced max_tokens from 16384 → 12000 → 10000
5. ✅ Lowered temperature from 0.4 → 0.3 for consistent formatting
6. ✅ Multi-tier repair strategy: standard parse → json-repair → extract+repair
7. ✅ Improved logging to show repair attempts

**Testing:** Ready for testing with full end-to-end analysis flow

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
