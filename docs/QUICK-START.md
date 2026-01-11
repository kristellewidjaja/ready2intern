# Quick Start Guide
**Get Started with Ready2Intern POC Development**

---

## For Human Developers

### 1. Read These Files (in order)
1. **README.md** - Project overview
2. **BUILD-GUIDE.md** - Complete setup instructions
3. **Ready2Intern-Implementation-Plan.md** - Feature roadmap
4. **AGENT-WORKFLOW.md** - How to work with coding agents

### 2. Set Up Project
Follow BUILD-GUIDE.md Part 1-5 to:
- Create project structure
- Set up backend (FastAPI + uv)
- Set up frontend (React + TypeScript + Vite)
- Verify integration works

### 3. Start Building
- Pick a feature from Implementation Plan
- Follow BUILD-GUIDE.md patterns
- Update PROJECT.md after each feature
- Log issues in ISSUES.md

---

## For Coding Agents

### 1. First Session: Foundation Setup
```
Use this prompt:
- Copy from AGENT-PROMPT-EXAMPLES.md → Feature Slice 1
- Follow BUILD-GUIDE.md step-by-step
- Create PROJECT.md and ISSUES.md
- Verify integration works
```

### 2. Subsequent Sessions: Feature Development
```
For each new session:
1. Read PROJECT.md (what's been built)
2. Read ISSUES.md (what to avoid)
3. Copy prompt from AGENT-PROMPT-EXAMPLES.md for next feature
4. Build feature end-to-end
5. Update PROJECT.md and ISSUES.md
6. Commit
```

### 3. Session Workflow
```
Start → Read Context → Build Feature → Test → Document → Commit → End
```

---

## Document Reference

### Core Documentation
| File | Purpose | When to Use |
|------|---------|-------------|
| **BUILD-GUIDE.md** | Setup & patterns | Setting up project, need code patterns |
| **Ready2Intern-Implementation-Plan.md** | Feature roadmap | Planning what to build next |
| **Ready2Intern-API-Spec.md** | API contracts | Designing endpoints |
| **Ready2Intern-PRD.md** | Product requirements | Understanding business goals |

### Agent Workflow
| File | Purpose | When to Use |
|------|---------|-------------|
| **AGENT-WORKFLOW.md** | How to work with agents | Understanding agent workflow |
| **AGENT-PROMPT-EXAMPLES.md** | Ready-to-use prompts | Starting a new feature |
| **PROJECT.md** | Project state | Every session start |
| **ISSUES.md** | Issue tracking | Every session start |

### Design & Architecture
| File | Purpose | When to Use |
|------|---------|-------------|
| **POC-Architecture-Summary.md** | Architecture overview | Understanding system design |
| **Ready2Intern-TDD-Simple.md** | Technical design | Understanding technical approach |

---

## Typical Development Flow

### Week 1: Foundation
```
Session 1: Foundation Setup (2-3 hours)
→ Complete project scaffold
→ Verify integration
→ Create PROJECT.md and ISSUES.md
```

### Week 2: Input Collection
```
Session 2: Resume Upload (1-2 hours)
→ File upload end-to-end
→ Update PROJECT.md

Session 3: Company Selection (1-2 hours)
→ Company selector end-to-end
→ Update PROJECT.md
```

### Week 3: Analysis Trigger
```
Session 4: Job Description Input (1 hour)
→ Textarea with validation
→ Update PROJECT.md

Session 5: Analyze Button (1 hour)
→ Button + loading states
→ Update PROJECT.md
```

### Weeks 4-6: LLM & Results
Continue with one feature per session...

---

## Quick Commands

### Start Development
```bash
# Terminal 1 - Backend
cd backend && python run.py

# Terminal 2 - Frontend
cd frontend && npm run dev
```

### Check Status
```bash
# View completed features
cat PROJECT.md

# View known issues
cat ISSUES.md

# View git history
git log --oneline
```

### Test Integration
```bash
# Backend health check
curl http://localhost:8000/api/health

# API docs
open http://localhost:8000/docs

# Frontend
open http://localhost:5173
```

---

## Decision Tree

### "Where do I start?"
→ Read BUILD-GUIDE.md and follow Part 1-5

### "What feature should I build next?"
→ Check PROJECT.md, then Ready2Intern-Implementation-Plan.md

### "How do I build a feature?"
→ Follow BUILD-GUIDE.md → Feature Development Workflow

### "What prompt should I use?"
→ Copy from AGENT-PROMPT-EXAMPLES.md

### "How do I know if feature is done?"
→ Check acceptance criteria in Implementation Plan

### "Where do I log issues?"
→ Add to ISSUES.md with template

### "How do I track progress?"
→ Update PROJECT.md after each feature

---

## Success Checklist

### After Foundation Setup
- [ ] Backend runs on localhost:8000
- [ ] Frontend runs on localhost:5173
- [ ] Health check works
- [ ] Theme toggle works
- [ ] PROJECT.md created
- [ ] ISSUES.md created

### After Each Feature
- [ ] All acceptance criteria met
- [ ] Feature tested end-to-end
- [ ] PROJECT.md updated
- [ ] ISSUES.md updated (if issues found)
- [ ] Code committed with clear message

### Before Moving to Next Feature
- [ ] Current feature fully working
- [ ] No blocking issues
- [ ] Documentation updated
- [ ] Ready for next session

---

## Common Questions

### Q: Can I build multiple features in one session?
**A:** Not recommended. One feature per session keeps context clear and ensures quality.

### Q: Do I need to update PROJECT.md every time?
**A:** Yes! It's how you preserve knowledge between sessions.

### Q: What if I find a bug in a previous feature?
**A:** Log it in ISSUES.md, fix it in current session if blocking, otherwise defer to polish phase.

### Q: Can I skip the BUILD-GUIDE patterns?
**A:** No. Patterns ensure consistency and make code easier to maintain.

### Q: What if acceptance criteria are unclear?
**A:** Refer to Ready2Intern-API-Spec.md and Ready2Intern-PRD.md for details.

---

## Getting Help

### If stuck on setup:
→ Review BUILD-GUIDE.md troubleshooting section

### If stuck on feature:
→ Check BUILD-GUIDE.md common patterns

### If unclear on requirements:
→ Check Ready2Intern-PRD.md and API-Spec.md

### If integration fails:
→ Test backend in /docs first, then frontend

---

## Summary

**To start developing:**
1. ✅ Read BUILD-GUIDE.md
2. ✅ Set up project (Part 1-5)
3. ✅ Verify integration works
4. ✅ Create PROJECT.md and ISSUES.md
5. ✅ Start with Feature Slice 2

**For each feature:**
1. ✅ Read PROJECT.md and ISSUES.md
2. ✅ Copy prompt from AGENT-PROMPT-EXAMPLES.md
3. ✅ Build feature end-to-end
4. ✅ Test thoroughly
5. ✅ Update documentation
6. ✅ Commit

**Result:**
- Working software at each step
- Clear progress tracking
- Knowledge preserved
- Smooth development flow

---

**Ready to start? Begin with BUILD-GUIDE.md Part 1!**
