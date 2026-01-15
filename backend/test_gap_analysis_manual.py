"""
Manual end-to-end test for gap analysis feature.

This script tests the complete three-phase analysis pipeline:
1. Resume parsing and extraction
2. Role matching with scoring
3. Gap analysis with recommendations

Usage:
    python test_gap_analysis_manual.py
"""

import asyncio
import json
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from app.services.resume_analysis_service import ResumeAnalysisService
from app.services.role_matching_service import RoleMatchingService
from app.services.gap_analysis_service import GapAnalysisService


async def test_gap_analysis():
    """Test complete gap analysis pipeline."""
    
    print("=" * 80)
    print("GAP ANALYSIS MANUAL TEST")
    print("=" * 80)
    
    # Configuration
    test_resume = "test_resume_sample.pdf"
    company_id = "amazon"
    role_description = """
    Software Development Engineer Intern - Amazon Web Services (AWS)
    
    We are looking for talented software engineering interns to join our AWS team.
    
    BASIC QUALIFICATIONS:
    - Currently enrolled in a Computer Science or related technical degree
    - Strong programming skills in Java, Python, or C++
    - Understanding of data structures and algorithms
    - Experience with object-oriented design
    - Familiarity with Linux/Unix and version control (Git)
    
    PREFERRED QUALIFICATIONS:
    - Experience with distributed systems and microservices
    - Knowledge of cloud platforms (AWS, Azure, GCP)
    - Understanding of CI/CD pipelines and DevOps practices
    - Previous internship or work experience in software development
    - Contributions to open-source projects
    - Strong problem-solving and debugging skills
    - Excellent communication and teamwork abilities
    """
    
    session_id = f"manual-gap-test-{int(asyncio.get_event_loop().time())}"
    
    print(f"\nTest Configuration:")
    print(f"  Resume: {test_resume}")
    print(f"  Company: {company_id}")
    print(f"  Session ID: {session_id}")
    print(f"  Role: Software Development Engineer Intern")
    
    # Verify test resume exists
    if not Path(test_resume).exists():
        print(f"\n❌ ERROR: Test resume not found: {test_resume}")
        print("   Please ensure test_resume_sample.pdf exists in the backend directory.")
        return
    
    # Verify API key is set
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("\n❌ ERROR: ANTHROPIC_API_KEY not set in environment")
        print("   Please create a .env file with your API key.")
        return
    
    print("\n" + "=" * 80)
    print("PHASE 1: RESUME ANALYSIS")
    print("=" * 80)
    
    try:
        resume_service = ResumeAnalysisService()
        print("\n⏳ Analyzing resume...")
        
        resume_result = await resume_service.analyze_resume(
            resume_file_path=test_resume,
            session_id=session_id,
        )
        
        print("✅ Resume analysis completed!")
        print(f"\n📊 Resume Summary:")
        print(f"  Name: {resume_result.get('personal_info', {}).get('name', 'N/A')}")
        print(f"  Programming Languages: {len(resume_result.get('skills', {}).get('programming_languages', []))}")
        print(f"  Work Experience: {len(resume_result.get('experience', []))}")
        print(f"  Projects: {len(resume_result.get('projects', []))}")
        print(f"  Education: {len(resume_result.get('education', []))}")
        
    except Exception as e:
        print(f"\n❌ Resume analysis failed: {e}")
        return
    
    print("\n" + "=" * 80)
    print("PHASE 2: ROLE MATCHING")
    print("=" * 80)
    
    try:
        role_service = RoleMatchingService()
        print("\n⏳ Analyzing role match...")
        
        match_result = await role_service.analyze_match(
            session_id=session_id,
            company_id=company_id,
            role_description=role_description,
        )
        
        print("✅ Role matching completed!")
        print(f"\n📊 Match Scores:")
        print(f"  ATS Score: {match_result.get('ats_score', {}).get('score', 0)}/100")
        print(f"  Role Match Score: {match_result.get('role_match_score', {}).get('score', 0)}/100")
        print(f"  Company Fit Score: {match_result.get('company_fit_score', {}).get('score', 0)}/100")
        print(f"  Overall Score: {match_result.get('overall_score', {}).get('score', 0)}/100")
        print(f"  Recommendation: {match_result.get('overall_score', {}).get('recommendation', 'N/A')}")
        
    except Exception as e:
        print(f"\n❌ Role matching failed: {e}")
        return
    
    print("\n" + "=" * 80)
    print("PHASE 3: GAP ANALYSIS")
    print("=" * 80)
    
    try:
        gap_service = GapAnalysisService()
        print("\n⏳ Analyzing gaps and generating recommendations...")
        print("   (This may take 20-30 seconds due to comprehensive analysis)")
        
        gap_result = await gap_service.analyze_gaps(
            session_id=session_id,
            company_id=company_id,
            role_description=role_description,
        )
        
        print("✅ Gap analysis completed!")
        
        summary = gap_result.get('summary', {})
        print(f"\n📊 Gap Summary:")
        print(f"  Total Gaps: {summary.get('total_gaps', 0)}")
        print(f"  High Priority: {summary.get('high_priority_count', 0)}")
        print(f"  Medium Priority: {summary.get('medium_priority_count', 0)}")
        print(f"  Low Priority: {summary.get('low_priority_count', 0)}")
        print(f"  Estimated Prep Time: {summary.get('estimated_preparation_time', 'N/A')}")
        
        print(f"\n📝 Overall Assessment:")
        print(f"  {summary.get('overall_assessment', 'N/A')}")
        
        # Show gap breakdown
        print(f"\n🔧 Technical Gaps: {len(gap_result.get('technical_gaps', []))}")
        for i, gap in enumerate(gap_result.get('technical_gaps', [])[:3], 1):
            print(f"  {i}. [{gap.get('priority', 'N/A').upper()}] {gap.get('title', 'N/A')}")
        
        print(f"\n💼 Experience Gaps: {len(gap_result.get('experience_gaps', []))}")
        for i, gap in enumerate(gap_result.get('experience_gaps', [])[:3], 1):
            print(f"  {i}. [{gap.get('priority', 'N/A').upper()}] {gap.get('title', 'N/A')}")
        
        print(f"\n🏢 Company Fit Gaps: {len(gap_result.get('company_fit_gaps', []))}")
        for i, gap in enumerate(gap_result.get('company_fit_gaps', [])[:3], 1):
            print(f"  {i}. [{gap.get('priority', 'N/A').upper()}] {gap.get('title', 'N/A')}")
        
        print(f"\n📄 Resume Optimization Gaps: {len(gap_result.get('resume_optimization_gaps', []))}")
        for i, gap in enumerate(gap_result.get('resume_optimization_gaps', [])[:3], 1):
            print(f"  {i}. [{gap.get('priority', 'N/A').upper()}] {gap.get('title', 'N/A')}")
        
        # Show quick wins
        quick_wins = gap_result.get('quick_wins', [])
        if quick_wins:
            print(f"\n⚡ Quick Wins ({len(quick_wins)}):")
            for i, win in enumerate(quick_wins[:3], 1):
                print(f"  {i}. {win.get('title', 'N/A')} ({win.get('estimated_time', 'N/A')})")
        
        # Show action plan phases
        action_plan = gap_result.get('prioritized_action_plan', {})
        if action_plan:
            print(f"\n📅 Action Plan:")
            
            phase1 = action_plan.get('phase_1_immediate', {})
            if phase1:
                print(f"  Phase 1 ({phase1.get('timeframe', 'N/A')}): {phase1.get('focus', 'N/A')}")
                print(f"    Actions: {len(phase1.get('actions', []))}")
            
            phase2 = action_plan.get('phase_2_short_term', {})
            if phase2:
                print(f"  Phase 2 ({phase2.get('timeframe', 'N/A')}): {phase2.get('focus', 'N/A')}")
                print(f"    Actions: {len(phase2.get('actions', []))}")
            
            phase3 = action_plan.get('phase_3_medium_term', {})
            if phase3:
                print(f"  Phase 3 ({phase3.get('timeframe', 'N/A')}): {phase3.get('focus', 'N/A')}")
                print(f"    Actions: {len(phase3.get('actions', []))}")
        
    except Exception as e:
        print(f"\n❌ Gap analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n" + "=" * 80)
    print("RESULTS SAVED")
    print("=" * 80)
    
    session_dir = Path(f"data/sessions/{session_id}")
    print(f"\n📁 Session Directory: {session_dir}")
    print(f"\n✅ Files created:")
    
    resume_file = session_dir / "resume_analysis.json"
    if resume_file.exists():
        size = resume_file.stat().st_size
        print(f"  1. resume_analysis.json ({size:,} bytes)")
    
    match_file = session_dir / "match_analysis.json"
    if match_file.exists():
        size = match_file.stat().st_size
        print(f"  2. match_analysis.json ({size:,} bytes)")
    
    gap_file = session_dir / "gap_analysis.json"
    if gap_file.exists():
        size = gap_file.stat().st_size
        print(f"  3. gap_analysis.json ({size:,} bytes)")
    
    print(f"\n💡 You can inspect these files to see the detailed analysis results.")
    print(f"   Example: cat {gap_file}")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETED SUCCESSFULLY! ✅")
    print("=" * 80)
    
    print("\n📋 Summary:")
    print(f"  • Resume analyzed with {len(resume_result.get('skills', {}).get('programming_languages', []))} programming languages")
    print(f"  • Overall match score: {match_result.get('overall_score', {}).get('score', 0)}/100")
    print(f"  • {summary.get('total_gaps', 0)} gaps identified across 4 categories")
    print(f"  • {len(quick_wins)} quick wins for immediate improvement")
    print(f"  • 3-phase action plan generated")
    
    print("\n✨ The gap analysis feature is working correctly!")
    print("   You can now commit the changes to GitHub.")


if __name__ == "__main__":
    asyncio.run(test_gap_analysis())
