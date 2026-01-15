# Manual Testing Guide for LLM Resume Analysis

## Prerequisites

1. **Backend server running** on `localhost:8000`
2. **Anthropic API key** configured in `.env` file
3. **Sample resume** available for testing

## Setup Steps

### 1. Configure API Key

Create a `.env` file in the `backend/` directory:

```bash
cd backend
cp .env.example .env
# Edit .env and add your actual Anthropic API key
```

Your `.env` should look like:
```
ANTHROPIC_API_KEY=sk-ant-api03-...your-key-here...
CORS_ORIGINS=["http://localhost:5173"]

# Optional: Configure LLM settings (defaults shown)
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
LLM_MAX_RETRIES=3
LLM_RETRY_DELAY=1
```

### 2. Ensure Backend is Running

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

Verify it's running:
```bash
curl http://localhost:8000/api/health
```

Expected output:
```json
{"status":"healthy","timestamp":"...","service":"Ready2Intern API"}
```

## Test Option 1: Using the Frontend (Recommended)

This tests the complete user flow:

1. **Open frontend**: Navigate to `http://localhost:5173`
2. **Upload resume**: Drag & drop or click to upload a PDF/DOCX resume
3. **Select company**: Choose Amazon, Meta, or Google
4. **Enter role description**: Paste a job description (minimum 50 characters)
5. **Click "Analyze Resume"**: Wait 10-30 seconds for analysis
6. **Check results**: Look for success message with analysis ID

### Verify Results

Check the saved analysis file:
```bash
# Replace SESSION_ID with the actual session ID from the upload
cat data/sessions/SESSION_ID/resume_analysis.json | jq .
```

## Test Option 2: Using the Python Test Script

Run the automated E2E test:

```bash
cd backend
source .venv/bin/activate
python test_e2e_manual.py
```

This script will:
1. Check backend health
2. Upload a test resume
3. Fetch companies list
4. Start analysis (calls Claude API)
5. Display extracted information

**Expected output:**
```
============================================================
Testing End-to-End Resume Analysis Flow
============================================================

[1/5] Testing health check...
✓ Health check passed

[2/5] Uploading test resume...
✓ Test resume prepared at: data/resumes/test_manual_resume.pdf
✓ Resume uploaded with session ID: test-manual-session-001

[3/5] Fetching available companies...
✓ Found 3 companies: ['amazon', 'meta', 'google']

[4/5] Starting resume analysis...
⚠️  This will call the Anthropic Claude API (requires API key)
⚠️  This may take 10-30 seconds...
✓ Analysis completed in 15.3 seconds
  Analysis ID: abc-123-def-456
  Status: completed
  Message: Resume analysis completed successfully. Results saved.

[5/5] Checking saved analysis results...
✓ Analysis results saved successfully

============================================================
ANALYSIS SUMMARY
============================================================

📋 Personal Info:
  Name: John Doe
  Email: john.doe@email.com

🎓 Education:
  - University of California, Berkeley
    B.S. Computer Science

💻 Skills:
  Languages: Python, Java, JavaScript, TypeScript, C++
  Frameworks: React, Node.js, Express, Django, Flask
  Tools: Git, Docker, AWS

💼 Experience (2 positions):
  - Software Engineering Intern at Tech Startup Inc.
  - Research Assistant at UC Berkeley AI Lab

🚀 Projects (3 projects):
  - E-Commerce Platform
  - Machine Learning Image Classifier

📝 Summary:
  Computer Science student with internship experience...

============================================================
✅ END-TO-END TEST COMPLETED SUCCESSFULLY!
============================================================
```

## Test Option 3: Using cURL

### Step 1: Upload Resume

```bash
# Create a test session
SESSION_ID="test-$(date +%s)"

# Upload resume (using the sample resume)
curl -X POST http://localhost:8000/api/upload \
  -F "file=@test_resume_sample.txt" \
  -F "filename=test_resume.pdf"

# Note the session_id from the response
```

### Step 2: Start Analysis

```bash
# Replace SESSION_ID with the actual ID from upload response
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "YOUR_SESSION_ID_HERE",
    "company": "amazon",
    "role_description": "Software Development Engineer Intern - Summer 2025. Amazon is seeking talented SDE Interns. Responsibilities include designing and developing scalable software solutions, collaborating with engineers, and participating in code reviews. Requirements: CS degree, strong programming skills in Java/Python/C++, understanding of data structures and algorithms."
  }'
```

Expected response:
```json
{
  "analysis_id": "abc-123-def-456",
  "session_id": "YOUR_SESSION_ID_HERE",
  "status": "completed",
  "message": "Resume analysis completed successfully. Results saved."
}
```

### Step 3: View Results

```bash
cat data/sessions/YOUR_SESSION_ID_HERE/resume_analysis.json | jq .
```

## What to Verify

### ✅ Success Indicators

1. **API Response**: Status 200 with `"status": "completed"`
2. **Analysis File**: JSON file created in `data/sessions/{session_id}/resume_analysis.json`
3. **Extracted Data**: File contains all expected fields:
   - `personal_info` (name, email, etc.)
   - `education` (array of education entries)
   - `skills` (programming languages, frameworks, tools)
   - `experience` (array of work experiences)
   - `projects` (array of projects)
   - `summary` (candidate summary)

4. **Data Quality**:
   - Skills are correctly categorized (languages vs frameworks vs tools)
   - Experience includes achievements and technologies
   - Projects include descriptions and highlights
   - Summary is concise and accurate

### ❌ Common Issues

**Issue**: `ValueError: ANTHROPIC_API_KEY environment variable not set`
- **Fix**: Create `.env` file with your API key

**Issue**: `Rate limit exceeded`
- **Fix**: Wait a few seconds and try again (retry logic will handle this)

**Issue**: `Failed to extract text from resume`
- **Fix**: Ensure resume is a valid PDF or DOCX file (not image-based PDF)

**Issue**: `Invalid JSON response from LLM`
- **Fix**: This is rare - check logs for details, may need to retry

## Performance Expectations

- **PDF Extraction**: < 1 second
- **DOCX Extraction**: < 1 second  
- **LLM API Call**: 5-15 seconds
- **Total Analysis Time**: 10-30 seconds

## Sample Resume

A sample resume is provided in `test_resume_sample.txt` with:
- Personal information
- Education (UC Berkeley, CS degree)
- Skills (Python, Java, JavaScript, React, Node.js, AWS, etc.)
- Experience (2 internships)
- Projects (3 projects)
- Certifications and awards

## Troubleshooting

### Check Backend Logs

The backend logs will show:
- Resume text extraction progress
- LLM API calls and responses
- Any errors during analysis

### Verify File System

```bash
# Check resume was uploaded
ls -lh data/resumes/

# Check session directory was created
ls -lh data/sessions/

# Check analysis results
cat data/sessions/YOUR_SESSION_ID/resume_analysis.json
```

### Test Individual Components

```bash
# Test LLM service directly (requires API key)
cd backend
source .venv/bin/activate
python -c "
from app.services.llm_service import LLMService
import asyncio

async def test():
    service = LLMService()
    result = await service.generate_completion('Say hello!')
    print(result)

asyncio.run(test())
"
```

## Next Steps After Testing

Once manual testing is successful:

1. ✅ Verify all 75 backend tests pass: `pytest tests/ -v`
2. ✅ Check documentation is updated: `AGENTS.md`, `PROGRESS.md`, `TODO.md`
3. ✅ Review code changes
4. ✅ Commit changes: `git add . && git commit -m "feat: add LLM resume analysis (slice 6)"`
5. ✅ Push to remote: `git push`
6. ✅ Create pull request

## Questions?

- Check `AGENTS.md` for implementation details
- Check `PROGRESS.md` for what was built
- Check `ISSUES.md` for known issues
- Check backend logs for debugging
