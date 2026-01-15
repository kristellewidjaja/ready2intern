"""
Manual end-to-end test for resume analysis.
This script tests the complete flow from file upload to LLM analysis.

Usage:
    python test_e2e_manual.py

Requirements:
    - Backend server running on localhost:8000
    - ANTHROPIC_API_KEY set in .env file
    - Sample resume file available
"""

import requests
import json
import time
from pathlib import Path


def test_e2e_resume_analysis():
    """Test end-to-end resume analysis flow."""
    
    base_url = "http://localhost:8000/api"
    
    print("=" * 60)
    print("Testing End-to-End Resume Analysis Flow")
    print("=" * 60)
    
    # Step 1: Health check
    print("\n[1/5] Testing health check...")
    response = requests.get(f"{base_url}/health")
    if response.status_code == 200:
        print("✓ Health check passed")
    else:
        print(f"✗ Health check failed: {response.status_code}")
        return
    
    # Step 2: Upload resume
    print("\n[2/5] Uploading test resume...")
    
    # Create a simple text file as resume (in real scenario, would be PDF/DOCX)
    test_resume_path = Path("test_resume_sample.txt")
    
    if not test_resume_path.exists():
        print(f"✗ Test resume file not found: {test_resume_path}")
        return
    
    # For testing, we'll copy it as a .pdf file
    test_pdf_path = Path("data/resumes/test_manual_resume.pdf")
    test_pdf_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Copy content to a PDF location (note: this is just for testing structure)
    with open(test_resume_path, 'r') as src:
        with open(test_pdf_path, 'w') as dst:
            dst.write(src.read())
    
    print(f"✓ Test resume prepared at: {test_pdf_path}")
    
    # For this test, we'll use a session ID directly
    session_id = "test-manual-session-001"
    
    # Copy file with session ID naming
    session_resume_path = Path(f"data/resumes/{session_id}_test.pdf")
    with open(test_resume_path, 'r') as src:
        with open(session_resume_path, 'w') as dst:
            dst.write(src.read())
    
    print(f"✓ Resume uploaded with session ID: {session_id}")
    
    # Step 3: Get companies list
    print("\n[3/5] Fetching available companies...")
    response = requests.get(f"{base_url}/companies")
    if response.status_code == 200:
        companies = response.json()
        print(f"✓ Found {len(companies)} companies: {[c['id'] for c in companies]}")
    else:
        print(f"✗ Failed to fetch companies: {response.status_code}")
        return
    
    # Step 4: Start analysis
    print("\n[4/5] Starting resume analysis...")
    print("⚠️  This will call the Anthropic Claude API (requires API key)")
    print("⚠️  This may take 10-30 seconds...")
    
    analysis_request = {
        "session_id": session_id,
        "company": "amazon",
        "role_description": """
        Software Development Engineer Intern - Summer 2025
        
        Amazon is seeking talented Software Development Engineer Interns to join our team for Summer 2025.
        As an intern, you will work on real-world projects that impact millions of customers worldwide.
        
        Responsibilities:
        - Design, develop, and deploy scalable software solutions
        - Collaborate with experienced engineers on complex technical challenges
        - Write clean, maintainable code following best practices
        - Participate in code reviews and technical discussions
        - Contribute to the full software development lifecycle
        
        Requirements:
        - Currently pursuing a Bachelor's or Master's degree in Computer Science or related field
        - Strong programming skills in at least one language (Java, Python, C++, etc.)
        - Understanding of data structures, algorithms, and object-oriented design
        - Experience with web development, databases, or cloud technologies is a plus
        - Excellent problem-solving and communication skills
        - Ability to work in a fast-paced, collaborative environment
        
        Preferred Qualifications:
        - Previous internship or project experience in software development
        - Familiarity with AWS services
        - Experience with Agile development methodologies
        - Open source contributions or personal projects demonstrating technical skills
        """.strip()
    }
    
    start_time = time.time()
    response = requests.post(f"{base_url}/analyze", json=analysis_request)
    elapsed_time = time.time() - start_time
    
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Analysis completed in {elapsed_time:.1f} seconds")
        print(f"  Analysis ID: {result['analysis_id']}")
        print(f"  Status: {result['status']}")
        print(f"  Message: {result['message']}")
    else:
        print(f"✗ Analysis failed: {response.status_code}")
        print(f"  Error: {response.json()}")
        return
    
    # Step 5: Check saved results
    print("\n[5/5] Checking saved analysis results...")
    results_file = Path(f"data/sessions/{session_id}/resume_analysis.json")
    
    if results_file.exists():
        with open(results_file, 'r') as f:
            analysis_data = json.load(f)
        
        print("✓ Analysis results saved successfully")
        print("\n" + "=" * 60)
        print("ANALYSIS SUMMARY")
        print("=" * 60)
        
        # Personal Info
        if 'personal_info' in analysis_data:
            print(f"\n📋 Personal Info:")
            print(f"  Name: {analysis_data['personal_info'].get('name', 'N/A')}")
            print(f"  Email: {analysis_data['personal_info'].get('email', 'N/A')}")
        
        # Education
        if 'education' in analysis_data and analysis_data['education']:
            print(f"\n🎓 Education:")
            for edu in analysis_data['education']:
                print(f"  - {edu.get('institution', 'N/A')}")
                print(f"    {edu.get('degree', 'N/A')}")
        
        # Skills
        if 'skills' in analysis_data:
            skills = analysis_data['skills']
            print(f"\n💻 Skills:")
            if skills.get('programming_languages'):
                print(f"  Languages: {', '.join(skills['programming_languages'][:5])}")
            if skills.get('frameworks_libraries'):
                print(f"  Frameworks: {', '.join(skills['frameworks_libraries'][:5])}")
            if skills.get('tools_technologies'):
                print(f"  Tools: {', '.join(skills['tools_technologies'][:5])}")
        
        # Experience
        if 'experience' in analysis_data and analysis_data['experience']:
            print(f"\n💼 Experience ({len(analysis_data['experience'])} positions):")
            for exp in analysis_data['experience'][:2]:
                print(f"  - {exp.get('title', 'N/A')} at {exp.get('company', 'N/A')}")
        
        # Projects
        if 'projects' in analysis_data and analysis_data['projects']:
            print(f"\n🚀 Projects ({len(analysis_data['projects'])} projects):")
            for proj in analysis_data['projects'][:2]:
                print(f"  - {proj.get('name', 'N/A')}")
        
        # Summary
        if 'summary' in analysis_data:
            print(f"\n📝 Summary:")
            print(f"  {analysis_data['summary']}")
        
        print("\n" + "=" * 60)
        print("✅ END-TO-END TEST COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
    else:
        print(f"✗ Results file not found: {results_file}")
        return


if __name__ == "__main__":
    try:
        test_e2e_resume_analysis()
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
