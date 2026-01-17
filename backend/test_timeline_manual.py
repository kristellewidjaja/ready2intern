"""
Manual test script for timeline generation feature.

This script tests the complete four-phase analysis pipeline:
1. Resume analysis
2. Role matching
3. Gap analysis
4. Timeline generation

Usage:
    python test_timeline_manual.py
"""

import asyncio
import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from app.services.resume_analysis_service import ResumeAnalysisService
from app.services.role_matching_service import RoleMatchingService
from app.services.gap_analysis_service import GapAnalysisService
from app.services.timeline_service import TimelineService


async def test_timeline_generation():
    """Test the complete timeline generation pipeline."""
    
    print("=" * 80)
    print("TIMELINE GENERATION MANUAL TEST")
    print("=" * 80)
    print()
    
    # Configuration
    session_id = f"manual-timeline-test-{int(datetime.now().timestamp())}"
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
    
    # Use existing test resume
    resume_file = Path("test_resume_sample.pdf")
    if not resume_file.exists():
        print("❌ Error: test_resume_sample.pdf not found")
        print("Please ensure the test resume file exists in the backend directory")
        return
    
    print(f"📋 Session ID: {session_id}")
    print(f"🏢 Company: {company_id}")
    print(f"📅 Target Deadline: {target_deadline}")
    print(f"📄 Resume: {resume_file}")
    print()
    
    try:
        # Phase 1: Resume Analysis
        print("-" * 80)
        print("PHASE 1: RESUME ANALYSIS")
        print("-" * 80)
        
        resume_service = ResumeAnalysisService()
        print("⏳ Analyzing resume...")
        
        resume_result = await resume_service.analyze_resume(
            resume_file_path=str(resume_file),
            session_id=session_id,
        )
        
        print("✅ Resume analysis complete!")
        print(f"   - Name: {resume_result.get('personal_info', {}).get('name', 'N/A')}")
        print(f"   - Programming Languages: {len(resume_result.get('skills', {}).get('programming_languages', []))}")
        print(f"   - Work Experiences: {len(resume_result.get('experience', []))}")
        print(f"   - Projects: {len(resume_result.get('projects', []))}")
        print()
        
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
        print(f"   - Estimated Prep Time: {summary.get('estimated_preparation_time', 'N/A')}")
        print()
        
        # Phase 4: Timeline Generation
        print("-" * 80)
        print("PHASE 4: TIMELINE GENERATION")
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
        print(f"   - Weekly Breakdown: {len(timeline_result.get('weekly_breakdown', []))} weeks")
        print(f"   - Critical Path Tasks: {len(timeline_result.get('critical_path', []))}")
        print()
        
        # Display Timeline Summary
        print("-" * 80)
        print("TIMELINE SUMMARY")
        print("-" * 80)
        print()
        
        phases = timeline_result.get('phases', [])
        for phase in phases:
            print(f"📌 {phase.get('title', 'Untitled Phase')}")
            print(f"   Weeks {phase.get('start_week', 0)}-{phase.get('end_week', 0)}")
            print(f"   Focus: {', '.join(phase.get('focus_areas', []))}")
            print(f"   Tasks: {len(phase.get('tasks', []))}")
            print(f"   Milestones: {len(phase.get('milestones', []))}")
            print()
        
        # Display Weekly Breakdown (first 3 weeks)
        print("-" * 80)
        print("WEEKLY BREAKDOWN (First 3 Weeks)")
        print("-" * 80)
        print()
        
        weekly = timeline_result.get('weekly_breakdown', [])
        for week in weekly[:3]:
            print(f"📅 Week {week.get('week_number', 0)}: {week.get('focus', 'N/A')}")
            print(f"   Phase: {week.get('phase', 'N/A')}")
            print(f"   Hours: {week.get('estimated_hours', 0)}")
            print(f"   Key Deliverable: {week.get('key_deliverable', 'N/A')}")
            tasks = week.get('tasks', [])
            if tasks:
                print(f"   Tasks:")
                for task in tasks[:3]:  # Show first 3 tasks
                    print(f"     - {task}")
            print()
        
        # Display Flexibility Notes
        print("-" * 80)
        print("FLEXIBILITY & MOTIVATION")
        print("-" * 80)
        print()
        
        flexibility = timeline_result.get('flexibility_notes', [])
        if flexibility:
            print("💡 Flexibility Notes:")
            for note in flexibility[:3]:
                print(f"   - {note}")
            print()
        
        motivation = timeline_result.get('motivation_tips', [])
        if motivation:
            print("🎯 Motivation Tips:")
            for tip in motivation[:3]:
                print(f"   - {tip}")
            print()
        
        # Save location
        print("-" * 80)
        print("RESULTS SAVED")
        print("-" * 80)
        print()
        print(f"📁 Session Directory: data/sessions/{session_id}/")
        print(f"   - resume_analysis.json")
        print(f"   - match_analysis.json")
        print(f"   - gap_analysis.json")
        print(f"   - timeline.json ⭐ NEW!")
        print()
        
        # Success summary
        print("=" * 80)
        print("✅ TIMELINE GENERATION TEST COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print()
        print("All four phases completed:")
        print("  ✅ Phase 1: Resume Analysis")
        print("  ✅ Phase 2: Role Matching")
        print("  ✅ Phase 3: Gap Analysis")
        print("  ✅ Phase 4: Timeline Generation")
        print()
        print(f"Review the complete timeline at:")
        print(f"  data/sessions/{session_id}/timeline.json")
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
        print()


if __name__ == "__main__":
    print()
    print("Starting timeline generation test...")
    print()
    asyncio.run(test_timeline_generation())
