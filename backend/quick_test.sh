#!/bin/bash
# Quick manual test for LLM resume analysis

echo "=========================================="
echo "Quick Test: LLM Resume Analysis"
echo "=========================================="
echo ""

# Check if backend is running
echo "[1/4] Checking backend health..."
HEALTH=$(curl -s http://localhost:8000/api/health)
if [ $? -eq 0 ]; then
    echo "✓ Backend is running"
else
    echo "✗ Backend is not running. Start it with:"
    echo "  cd backend && source .venv/bin/activate && uvicorn app.main:app --reload --port 8000"
    exit 1
fi

# Check if .env exists
echo ""
echo "[2/4] Checking API key configuration..."
if [ -f .env ]; then
    if grep -q "ANTHROPIC_API_KEY=sk-" .env; then
        echo "✓ API key configured"
    else
        echo "⚠️  .env exists but API key may not be set correctly"
        echo "   Make sure it starts with: ANTHROPIC_API_KEY=sk-ant-..."
    fi
else
    echo "✗ .env file not found"
    echo "  Create it with: echo 'ANTHROPIC_API_KEY=your-key-here' > .env"
    exit 1
fi

# Prepare test resume
echo ""
echo "[3/4] Preparing test resume..."
SESSION_ID="manual-test-$(date +%s)"
cp test_resume_sample.pdf "data/resumes/${SESSION_ID}_test.pdf"
echo "✓ Test resume ready with session ID: $SESSION_ID"

# Run analysis
echo ""
echo "[4/4] Starting analysis (this will call Claude API)..."
echo "⚠️  This may take 10-30 seconds..."
echo ""

RESPONSE=$(curl -s -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d "{
    \"session_id\": \"$SESSION_ID\",
    \"company\": \"amazon\",
    \"role_description\": \"Software Development Engineer Intern - Summer 2025. Amazon is seeking talented Software Development Engineer Interns to join our team. As an intern, you will work on real-world projects that impact millions of customers. Responsibilities include designing and developing scalable software solutions, collaborating with experienced engineers, writing clean maintainable code, and participating in code reviews. Requirements: Currently pursuing Bachelor's or Master's degree in Computer Science, strong programming skills in Java/Python/C++, understanding of data structures and algorithms, experience with web development or cloud technologies is a plus.\"
  }")

echo "$RESPONSE" | jq . 2>/dev/null || echo "$RESPONSE"

# Check if successful
if echo "$RESPONSE" | grep -q "completed"; then
    echo ""
    echo "=========================================="
    echo "✅ SUCCESS! Analysis completed"
    echo "=========================================="
    echo ""
    echo "View results:"
    echo "  cat data/sessions/$SESSION_ID/resume_analysis.json | jq ."
    echo ""
    echo "Or view summary:"
    echo "  cat data/sessions/$SESSION_ID/resume_analysis.json | jq '{name: .personal_info.name, skills: .skills.programming_languages, experience: .experience | length, projects: .projects | length}'"
else
    echo ""
    echo "=========================================="
    echo "❌ Analysis failed"
    echo "=========================================="
    echo ""
    echo "Check backend logs for details"
fi
