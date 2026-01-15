"""
Timeline generation service that creates personalized development timelines.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

from app.services.llm_service import LLMService
from app.prompts.timeline_generation import (
    SYSTEM_PROMPT,
    create_timeline_prompt,
)

logger = logging.getLogger(__name__)


class TimelineService:
    """Service for generating personalized development timelines."""
    
    def __init__(self):
        """Initialize timeline service."""
        self.llm_service = LLMService()
        logger.info("TimelineService initialized")
    
    async def generate_timeline(
        self,
        session_id: str,
        role_description: str,
        target_deadline: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Generate a personalized development timeline.
        
        Args:
            session_id: Session ID for loading gap analysis
            role_description: Job role description
            target_deadline: Target deadline (ISO date string YYYY-MM-DD), defaults to 12 weeks from now
            
        Returns:
            Dictionary containing timeline with phases, tasks, and milestones
            
        Raises:
            Exception: If timeline generation fails
        """
        logger.info(f"Starting timeline generation for session: {session_id}")
        
        try:
            # Step 1: Load gap analysis results
            logger.info("Loading gap analysis...")
            gap_data = self._load_gap_analysis(session_id)
            
            if not gap_data:
                raise Exception(f"Gap analysis not found for session: {session_id}")
            
            # Step 2: Calculate timeline parameters
            logger.info("Calculating timeline parameters...")
            start_date = datetime.now().date()
            
            if target_deadline:
                # Parse target deadline
                try:
                    deadline_date = datetime.fromisoformat(target_deadline).date()
                except ValueError:
                    logger.warning(f"Invalid deadline format: {target_deadline}, using default 12 weeks")
                    deadline_date = start_date + timedelta(weeks=12)
            else:
                # Default to 12 weeks from now
                deadline_date = start_date + timedelta(weeks=12)
            
            # Calculate weeks available
            days_available = (deadline_date - start_date).days
            weeks_available = max(1, days_available // 7)  # At least 1 week
            
            # Determine recommended hours per week based on timeline length
            if weeks_available < 4:
                hours_per_week = 20  # Intensive
            elif weeks_available < 8:
                hours_per_week = 15  # Moderate
            else:
                hours_per_week = 12  # Light
            
            logger.info(f"Timeline parameters: {weeks_available} weeks, {hours_per_week} hours/week")
            logger.info(f"Start: {start_date.isoformat()}, Deadline: {deadline_date.isoformat()}")
            
            # Step 3: Create prompt for LLM
            prompt = create_timeline_prompt(
                gap_analysis=gap_data,
                role_description=role_description,
                target_deadline=deadline_date.isoformat(),
                start_date=start_date.isoformat(),
                weeks_available=weeks_available,
                hours_per_week=hours_per_week,
            )
            
            # Step 4: Call LLM for timeline generation
            logger.info("Calling LLM for timeline generation...")
            llm_response = await self.llm_service.generate_completion(
                prompt=prompt,
                system_prompt=SYSTEM_PROMPT,
                max_tokens=16384,  # Large token limit for comprehensive timeline
                temperature=0.4,  # Slightly higher for creative planning
            )
            
            # Step 5: Parse LLM response
            logger.info("Parsing LLM response...")
            timeline_result = self._parse_llm_response(llm_response)
            
            # Step 6: Validate timeline data
            logger.info("Validating timeline...")
            timeline_result = self._validate_timeline_data(
                timeline_result,
                start_date.isoformat(),
                deadline_date.isoformat(),
                weeks_available,
            )
            
            # Step 7: Save results to file system
            logger.info("Saving timeline results...")
            self._save_timeline_results(session_id, timeline_result)
            
            logger.info(f"Timeline generation completed for session: {session_id}")
            logger.info(f"Phases: {len(timeline_result.get('phases', []))}")
            logger.info(f"Total tasks: {sum(len(phase.get('tasks', [])) for phase in timeline_result.get('phases', []))}")
            logger.info(f"Total hours: {timeline_result.get('metadata', {}).get('total_hours', 0)}")
            
            return timeline_result
            
        except Exception as e:
            logger.error(f"Timeline generation failed: {e}")
            raise Exception(f"Failed to generate timeline: {str(e)}") from e
    
    def _load_gap_analysis(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Load gap analysis results from file system.
        
        Args:
            session_id: Session ID
            
        Returns:
            Gap analysis dictionary or None if not found
        """
        try:
            analysis_file = Path(f"data/sessions/{session_id}/gap_analysis.json")
            
            if not analysis_file.exists():
                logger.warning(f"Gap analysis not found for session: {session_id}")
                return None
            
            with open(analysis_file, "r") as f:
                data = json.load(f)
            
            logger.info(f"Loaded gap analysis for session: {session_id}")
            return data
            
        except Exception as e:
            logger.error(f"Failed to load gap analysis: {e}")
            return None
    
    def _parse_llm_response(self, llm_response: str) -> Dict[str, Any]:
        """
        Parse LLM response into structured format.
        
        Args:
            llm_response: Raw response from LLM
            
        Returns:
            Parsed dictionary
            
        Raises:
            ValueError: If response cannot be parsed
        """
        try:
            # Try to extract JSON from response
            response = llm_response.strip()
            
            # Remove markdown code blocks if present
            if response.startswith("```json"):
                response = response[7:]
            elif response.startswith("```"):
                response = response[3:]
            
            if response.endswith("```"):
                response = response[:-3]
            
            response = response.strip()
            
            # Try to find JSON object boundaries if parsing fails
            try:
                parsed = json.loads(response)
            except json.JSONDecodeError as e:
                logger.warning(f"Initial JSON parse failed: {e}")
                logger.warning("Attempting to extract JSON object from response...")
                
                # Try to find the first { and last }
                start_idx = response.find('{')
                end_idx = response.rfind('}')
                
                if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                    response = response[start_idx:end_idx + 1]
                    logger.info(f"Extracted JSON from position {start_idx} to {end_idx}")
                    parsed = json.loads(response)
                else:
                    raise
            
            # Validate required fields
            required_fields = [
                "metadata",
                "phases",
                "weekly_breakdown",
            ]
            
            for field in required_fields:
                if field not in parsed:
                    logger.warning(f"Missing required field: {field}")
                    # Add default structure
                    if field == "metadata":
                        parsed[field] = {
                            "total_weeks": 0,
                            "total_hours": 0,
                            "hours_per_week": 12,
                            "intensity_level": "moderate",
                            "feasibility_assessment": "Timeline generation incomplete",
                        }
                    else:
                        parsed[field] = []
            
            return parsed
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.error(f"Response length: {len(llm_response)} characters")
            logger.error(f"Response preview: {llm_response[:500]}...")
            logger.error(f"Response end: ...{llm_response[-500:]}")
            raise ValueError(f"Invalid JSON response from LLM: {str(e)}") from e
        except Exception as e:
            logger.error(f"Unexpected error parsing response: {e}")
            raise ValueError(f"Failed to parse LLM response: {str(e)}") from e
    
    def _validate_timeline_data(
        self,
        timeline_data: Dict[str, Any],
        start_date: str,
        target_deadline: str,
        weeks_available: int,
    ) -> Dict[str, Any]:
        """
        Validate and enrich timeline data.
        
        Args:
            timeline_data: Parsed timeline data
            start_date: Start date (ISO string)
            target_deadline: Target deadline (ISO string)
            weeks_available: Number of weeks available
            
        Returns:
            Validated timeline data
        """
        # Ensure metadata exists
        if "metadata" not in timeline_data:
            timeline_data["metadata"] = {}
        
        metadata = timeline_data["metadata"]
        
        # Update metadata with actual values
        metadata["start_date"] = start_date
        metadata["target_deadline"] = target_deadline
        metadata["total_weeks"] = weeks_available
        
        # Calculate total hours from tasks
        total_hours = 0
        phases = timeline_data.get("phases", [])
        
        for phase in phases:
            tasks = phase.get("tasks", [])
            for task in tasks:
                total_hours += task.get("estimated_hours", 0)
        
        metadata["total_hours"] = total_hours
        
        # Validate hours per week is reasonable
        if "hours_per_week" not in metadata or metadata["hours_per_week"] <= 0:
            metadata["hours_per_week"] = 12
        
        # Ensure critical_path exists
        if "critical_path" not in timeline_data:
            timeline_data["critical_path"] = []
        
        # Ensure flexibility_notes exists
        if "flexibility_notes" not in timeline_data:
            timeline_data["flexibility_notes"] = []
        
        # Ensure motivation_tips exists
        if "motivation_tips" not in timeline_data:
            timeline_data["motivation_tips"] = []
        
        logger.info(
            f"Timeline validation - Phases: {len(phases)}, "
            f"Total hours: {total_hours}, Hours/week: {metadata['hours_per_week']}"
        )
        
        return timeline_data
    
    def _save_timeline_results(
        self,
        session_id: str,
        timeline_result: Dict[str, Any],
    ) -> None:
        """
        Save timeline results to file system.
        
        Args:
            session_id: Session ID
            timeline_result: Timeline results
        """
        try:
            # Create session directory
            session_dir = Path(f"data/sessions/{session_id}")
            session_dir.mkdir(parents=True, exist_ok=True)
            
            # Save timeline
            output_file = session_dir / "timeline.json"
            with open(output_file, "w") as f:
                json.dump(timeline_result, f, indent=2)
            
            logger.info(f"Timeline results saved to: {output_file}")
            
        except Exception as e:
            logger.error(f"Failed to save timeline results: {e}")
            raise Exception(f"Failed to save timeline results: {str(e)}") from e
    
    def load_timeline_results(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Load saved timeline results from file system.
        
        Args:
            session_id: Session ID
            
        Returns:
            Timeline results dictionary or None if not found
        """
        try:
            output_file = Path(f"data/sessions/{session_id}/timeline.json")
            
            if not output_file.exists():
                logger.warning(f"Timeline results not found for session: {session_id}")
                return None
            
            with open(output_file, "r") as f:
                results = json.load(f)
            
            logger.info(f"Loaded timeline results for session: {session_id}")
            return results
            
        except Exception as e:
            logger.error(f"Failed to load timeline results: {e}")
            return None
