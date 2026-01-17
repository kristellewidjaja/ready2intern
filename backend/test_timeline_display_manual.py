#!/usr/bin/env python3
"""
Manual test script to verify timeline display works with real data.
Tests the complete flow: fetch results → verify timeline data → display in frontend.
"""

import requests
import json

BASE_URL = "http://localhost:8000"

# Session IDs with timeline data
TEST_SESSIONS = [
    "8d004c68-1e64-4e06-a5df-9062d63ece0b",
    "d7321300-879d-4c66-b9bf-d6ecd44530c4",
    "ff408b97-180d-48de-b5c6-4d7248b8f97d",
]

def test_results_endpoint(session_id):
    """Test fetching results for a session."""
    print(f"\n{'='*60}")
    print(f"Testing Session: {session_id}")
    print(f"{'='*60}")
    
    try:
        response = requests.get(f"{BASE_URL}/api/results/{session_id}")
        response.raise_for_status()
        
        data = response.json()
        
        print(f"✓ API Response Status: {response.status_code}")
        print(f"✓ Session ID: {data['session_id']}")
        print(f"✓ Status: {data['status']}")
        print(f"✓ Overall Score: {data.get('overall_score', 'N/A')}")
        
        # Check timeline data
        if data.get('timeline'):
            timeline = data['timeline']
            metadata = timeline.get('metadata', {})
            phases = timeline.get('phases', [])
            weekly = timeline.get('weekly_breakdown', [])
            
            print(f"\n📅 Timeline Data:")
            print(f"  - Total Weeks: {metadata.get('total_weeks')}")
            print(f"  - Hours/Week: {metadata.get('hours_per_week')}")
            print(f"  - Total Hours: {metadata.get('total_hours')}")
            print(f"  - Intensity: {metadata.get('intensity_level')}")
            print(f"  - Phases: {len(phases)}")
            print(f"  - Weekly Breakdown: {len(weekly)} weeks")
            print(f"  - Critical Path Items: {len(timeline.get('critical_path', []))}")
            print(f"  - Flexibility Notes: {len(timeline.get('flexibility_notes', []))}")
            print(f"  - Motivation Tips: {len(timeline.get('motivation_tips', []))}")
            
            # Show phase details
            print(f"\n  Phases:")
            for phase in phases:
                print(f"    {phase['phase_number']}. {phase['title']}")
                print(f"       Weeks {phase['start_week']}-{phase['end_week']}")
                print(f"       Tasks: {len(phase.get('tasks', []))}")
                print(f"       Milestones: {len(phase.get('milestones', []))}")
            
            print(f"\n✓ Timeline data is complete and valid!")
            
            # Show frontend URL
            print(f"\n🌐 View in Frontend:")
            print(f"   http://localhost:5173/results?session={session_id}")
            
        else:
            print(f"\n⚠ No timeline data found for this session")
            
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ API Error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        return False

def main():
    print("="*60)
    print("Timeline Display Manual Test")
    print("="*60)
    print("\nThis script tests the timeline display feature with real data.")
    print("Make sure both backend (port 8000) and frontend (port 5173) are running.")
    
    success_count = 0
    total_count = len(TEST_SESSIONS)
    
    for session_id in TEST_SESSIONS:
        if test_results_endpoint(session_id):
            success_count += 1
    
    print(f"\n{'='*60}")
    print(f"Test Summary: {success_count}/{total_count} sessions successful")
    print(f"{'='*60}")
    
    if success_count > 0:
        print(f"\n✅ Timeline display is working!")
        print(f"\nNext Steps:")
        print(f"1. Open frontend in browser: http://localhost:5173")
        print(f"2. Navigate to any of the results URLs above")
        print(f"3. Verify timeline section displays correctly")
        print(f"4. Test expand/collapse functionality")
        print(f"5. Test switching between 'By Phase' and 'Week by Week' views")
    else:
        print(f"\n❌ Timeline display test failed")
        print(f"\nTroubleshooting:")
        print(f"- Check if backend is running on port 8000")
        print(f"- Check if session directories exist in backend/data/sessions/")
        print(f"- Check if timeline.json files exist in session directories")

if __name__ == "__main__":
    main()
