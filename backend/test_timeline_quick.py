"""
Quick timeline test using existing session from UI upload.

This continues from where the UI left off and completes:
2. Role matching
3. Gap analysis  
4. Timeline generation

Usage:
    python test_timeline_quick.py <session_id>
"""

import asyncio
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from app.services.role_matching_service import RoleMatchingService
from app.services.gap_analysis_service import GapAnalysisService
from app.services.timeline_service import TimelineService


async def continue_analysis(session_id: str):
    """Continue analysis from existing session."""
    
    print("=" * 80)
    print("TIMELINE GENERATION - QUICK TEST")
    print("=" * 80)
    print()
    print(f"📋 Session ID: {session_id}")
    print()
    
    # Configuration
    company_id = "amazon"
    role_description = """
    Software Development Engineer Intern - Summer 2026
    
    We are looking for talented software engineering interns to join our team.
    
    Required Skills:
    - Strong programming skills in Python, Java, or C++
    - Data structures and algorithms knowledge
    - Experience with web development (React, Node.js)
    - Understanding of databases (SQL, NoSQL)
    - Cloud computing experience (AWS preferred)
    - Version control with Git
    
    Responsibilities:
    - Design and implement scalable software solutions
    - Collaborate with cross-functional teams
    - Write clean, maintainable code
    - Participate in code reviews
    - Debug and optimize existing systems
    
    Preferred Qualifications:
    - Experience with microservices architecture
    - Knowledge of containerization (Docker, Kubernetes)
    - Previous internship experience
    - Open source contributions
    """
    
    # Target deadline: 8 weeks from now
    target_deadline = (datetime.now().date() + timedelta(weeks=8)).isoformat()
    
    print(f"🏢 Company: {company_id}")
    print(f"📅 Target Deadline: {target_deadline}")
    print()
    
    try:
        # Phase 2: Role Matching
        print("-" * 80)
        print("PHASE 2: ROLE MATCHING")
        print("-" * 80)
        
        matching_service = RoleMatchingService()
        print("⏳ Analyzing role match...")
        
        match_result = await matching_service.analyze_match(
            session_id=session_id,
            company_id=company_id,
            role_description=role_description,
        )
        
        print("✅ Role matching complete!")
        print(f"   - ATS Score: {match_result.get('ats_score', {}).get('score', 0)}/100")
        print(f"   - Role Match Score: {match_result.get('role_match_score', {}).get('score', 0)}/100")
        print(f"   - Company Fit Score: {match_result.get('company_fit_score', {}).get('score', 0)}/100")
        print(f"   - Overall Score: {match_result.get('overall_score', {}).get('score', 0)}/100")
        print(f"   - Recommendation: {match_result.get('overall_score', {}).get('recommendation', 'N/A')}")
        print()
        
        # Phase 3: Gap Analysis
        print("-" * 80)
        print("PHASE 3: GAP ANALYSIS")
        print("-" * 80)
        
        gap_service = GapAnalysisService()
        print("⏳ Identifying gaps...")
        
        gap_result = await gap_service.analyze_gaps(
            session_id=session_id,
            company_id=company_id,
            role_description=role_description,
        )
        
        print("✅ Gap analysis complete!")
        summary = gap_result.get('summary', {})
        print(f"   - Total Gaps: {summary.get('total_gaps', 0)}")
        print(f"   - High Priority: {summary.get('high_priority_count', 0)}")
        print(f"   - Medium Priority: {summary.get('medium_priority_count', 0)}")
        print(f"   - Low Priority: {summary.get('low_priority_count', 0)}")
        print()
        
        # Phase 4: Timeline Generation
        print("-" * 80)
        print("PHASE 4: TIMELINE GENERATION ⭐")
        print("-" * 80)
        
        timeline_service = TimelineService()
        print("⏳ Generating development timeline...")
        
        timeline_result = await timeline_service.generate_timeline(
            session_id=session_id,
            role_description=role_description,
            target_deadline=target_deadline,
        )
        
        print("✅ Timeline generation complete!")
        metadata = timeline_result.get('metadata', {})
        print(f"   - Total Weeks: {metadata.get('total_weeks', 0)}")
        print(f"   - Total Hours: {metadata.get('total_hours', 0)}")
        print(f"   - Hours/Week: {metadata.get('hours_per_week', 0)}")
        print(f"   - Intensity: {metadata.get('intensity_level', 'N/A')}")
        print(f"   - Phases: {len(timeline_result.get('phases', []))}")
        print()
        
        # Display Timeline Phases
        print("-" * 80)
        print("TIMELINE PHASES")
        print("-" * 80)
        print()
        
        phases = timeline_result.get('phases', [])
        for phase in phases:
            print(f"📌 Phase {phase.get('phase_number', 0)}: {phase.get('title', 'Untitled')}")
            print(f"   Weeks {phase.get('start_week', 0)}-{phase.get('end_week', 0)}")
            print(f"   Focus: {', '.join(phase.get('focus_areas', [])[:3])}")
            print(f"   Tasks: {len(phase.get('tasks', []))}")
            if phase.get('milestones'):
                milestone = phase['milestones'][0]
                print(f"   Milestone: {milestone.get('title', 'N/A')}")
            print()
        
        # Display first week
        print("-" * 80)
        print("WEEK 1 PLAN")
        print("-" * 80)
        print()
        
        weekly = timeline_result.get('weekly_breakdown', [])
        if weekly:
            week1 = weekly[0]
            print(f"📅 Week {week1.get('week_number', 0)}")
            print(f"   Phase: {week1.get('phase', 'N/A')}")
            print(f"   Focus: {week1.get('focus', 'N/A')}")
            print(f"   Hours: {week1.get('estimated_hours', 0)}")
            print(f"   Key Deliverable: {week1.get('key_deliverable', 'N/A')}")
            print()
            print("   Tasks:")
            for task in week1.get('tasks', [])[:5]:
                print(f"     • {task}")
            print()
        
        # Success
        print("=" * 80)
        print("✅ SUCCESS! Timeline generated for your resume!")
        print("=" * 80)
        print()
        print(f"📁 View complete results at:")
        print(f"   data/sessions/{session_id}/")
        print()
        print("Files created:")
        print("  ✅ resume_analysis.json (already existed)")
        print("  ✅ match_analysis.json (NEW)")
        print("  ✅ gap_analysis.json (NEW)")
        print("  ✅ timeline.json (NEW) ⭐")
        print()
        
    except Exception as e:
        print()
        print("=" * 80)
        print("❌ TEST FAILED")
        print("=" * 80)
        print()
        print(f"Error: {str(e)}")
        print()
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_timeline_quick.py <session_id>")
        print()
        print("Most recent session: 8d004c68-1e64-4e06-a5df-9062d63ece0b")
        print()
        print("Run with:")
        print("  python test_timeline_quick.py 8d004c68-1e64-4e06-a5df-9062d63ece0b")
        sys.exit(1)
    
    session_id = sys.argv[1]
    print()
    asyncio.run(continue_analysis(session_id))
