"""
Gap analysis service that identifies skill/experience gaps and generates recommendations.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from json_repair import repair_json

from app.services.llm_service import LLMService
from app.services.company_service import CompanyService
from app.prompts.gap_analysis import (
    SYSTEM_PROMPT,
    create_gap_analysis_prompt,
)

logger = logging.getLogger(__name__)


class GapAnalysisService:
    """Service for identifying gaps and generating recommendations."""
    
    def __init__(self):
        """Initialize gap analysis service."""
        self.llm_service = LLMService()
        self.company_service = CompanyService()
        logger.info("GapAnalysisService initialized")
    
    async def analyze_gaps(
        self,
        session_id: str,
        company_id: str,
        role_description: str,
    ) -> Dict[str, Any]:
        """
        Analyze gaps between candidate profile and target role.
        
        Args:
            session_id: Session ID for loading match analysis
            company_id: Company ID (amazon, meta, google)
            role_description: Job role description
            
        Returns:
            Dictionary containing gap analysis with recommendations
            
        Raises:
            Exception: If analysis fails
        """
        logger.info(f"Starting gap analysis for session: {session_id}")
        
        try:
            # Step 1: Load match analysis results
            logger.info("Loading match analysis...")
            match_data = self._load_match_analysis(session_id)
            
            if not match_data:
                raise Exception(f"Match analysis not found for session: {session_id}")
            
            # Step 2: Load company tenets
            logger.info(f"Loading company tenets for: {company_id}")
            company_tenets = self.company_service.get_company_tenets(company_id)
            
            if not company_tenets:
                raise Exception(f"Company tenets not found for: {company_id}")
            
            # Step 3: Create prompt for LLM
            prompt = create_gap_analysis_prompt(
                match_analysis=match_data,
                role_description=role_description,
                company_tenets=company_tenets,
            )
            
            # Step 4: Call LLM for gap analysis
            logger.info("Calling LLM for gap analysis...")
            llm_response = await self.llm_service.generate_completion(
                prompt=prompt,
                system_prompt=SYSTEM_PROMPT,
                max_tokens=10000,  # Reduced to prevent incomplete JSON (was 16384)
                temperature=0.3,  # Lower for more consistent formatting
            )
            
            # Step 5: Parse LLM response
            logger.info("Parsing LLM response...")
            gap_result = self._parse_llm_response(llm_response)
            
            # Step 6: Validate gap data
            logger.info("Validating gap analysis...")
            gap_result = self._validate_gap_data(gap_result)
            
            # Step 7: Save results to file system
            logger.info("Saving gap analysis results...")
            self._save_gap_results(session_id, gap_result)
            
            logger.info(f"Gap analysis completed for session: {session_id}")
            logger.info(f"Total gaps identified: {gap_result.get('summary', {}).get('total_gaps', 0)}")
            
            return gap_result
            
        except Exception as e:
            logger.error(f"Gap analysis failed: {e}")
            raise Exception(f"Failed to analyze gaps: {str(e)}") from e
    
    def _load_match_analysis(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Load match analysis results from file system.
        
        Args:
            session_id: Session ID
            
        Returns:
            Match analysis dictionary or None if not found
        """
        try:
            analysis_file = Path(f"data/sessions/{session_id}/match_analysis.json")
            
            if not analysis_file.exists():
                logger.warning(f"Match analysis not found for session: {session_id}")
                return None
            
            with open(analysis_file, "r") as f:
                data = json.load(f)
            
            logger.info(f"Loaded match analysis for session: {session_id}")
            return data
            
        except Exception as e:
            logger.error(f"Failed to load match analysis: {e}")
            return None
    
    def _parse_llm_response(self, llm_response: str) -> Dict[str, Any]:
        """
        Parse LLM response into structured format using json-repair library.
        
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
            
            # Try standard JSON parsing first
            try:
                parsed = json.loads(response)
                logger.info("Successfully parsed JSON on first attempt")
            except json.JSONDecodeError as e:
                logger.warning(f"Initial JSON parse failed at position {e.pos}: {e.msg}")
                logger.info("Attempting to repair JSON using json-repair library...")
                
                try:
                    # Use json-repair library to fix malformed JSON
                    repaired_json = repair_json(response)
                    parsed = json.loads(repaired_json)
                    logger.info("Successfully repaired and parsed JSON")
                except Exception as repair_error:
                    logger.error(f"JSON repair failed: {repair_error}")
                    
                    # Last resort: try to extract just the JSON object
                    start_idx = response.find('{')
                    end_idx = response.rfind('}')
                    
                    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                        response = response[start_idx:end_idx + 1]
                        logger.info(f"Extracted JSON boundaries from {start_idx} to {end_idx}")
                        
                        try:
                            repaired_json = repair_json(response)
                            parsed = json.loads(repaired_json)
                            logger.info("Successfully repaired extracted JSON")
                        except Exception:
                            logger.error("All JSON repair attempts failed")
                            raise ValueError(f"Invalid JSON response from LLM: {e.msg}")
                    else:
                        raise ValueError(f"Invalid JSON response from LLM: {e.msg}")
            
            # Validate required fields
            required_fields = [
                "summary",
                "technical_gaps",
                "experience_gaps",
                "company_fit_gaps",
                "resume_optimization_gaps",
            ]
            
            for field in required_fields:
                if field not in parsed:
                    logger.warning(f"Missing required field: {field}")
                    # Add default structure
                    if field == "summary":
                        parsed[field] = {
                            "total_gaps": 0,
                            "high_priority_count": 0,
                            "medium_priority_count": 0,
                            "low_priority_count": 0,
                            "estimated_preparation_time": "Unknown",
                            "overall_assessment": "Gap analysis incomplete",
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
    
    def _validate_gap_data(self, gap_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and enrich gap analysis data.
        
        Args:
            gap_data: Parsed gap analysis data
            
        Returns:
            Validated gap data
        """
        # Count gaps by priority
        high_count = 0
        medium_count = 0
        low_count = 0
        total_count = 0
        
        # Count gaps across all categories
        for category in ["technical_gaps", "experience_gaps", "company_fit_gaps", "resume_optimization_gaps"]:
            gaps = gap_data.get(category, [])
            total_count += len(gaps)
            
            for gap in gaps:
                priority = gap.get("priority", "medium").lower()
                if priority == "high":
                    high_count += 1
                elif priority == "medium":
                    medium_count += 1
                elif priority == "low":
                    low_count += 1
        
        # Update summary counts
        if "summary" not in gap_data:
            gap_data["summary"] = {}
        
        gap_data["summary"]["total_gaps"] = total_count
        gap_data["summary"]["high_priority_count"] = high_count
        gap_data["summary"]["medium_priority_count"] = medium_count
        gap_data["summary"]["low_priority_count"] = low_count
        
        logger.info(
            f"Gap counts - Total: {total_count}, "
            f"High: {high_count}, Medium: {medium_count}, Low: {low_count}"
        )
        
        return gap_data
    
    def _save_gap_results(
        self,
        session_id: str,
        gap_result: Dict[str, Any],
    ) -> None:
        """
        Save gap analysis results to file system.
        
        Args:
            session_id: Session ID
            gap_result: Gap analysis results
        """
        try:
            # Create session directory
            session_dir = Path(f"data/sessions/{session_id}")
            session_dir.mkdir(parents=True, exist_ok=True)
            
            # Save gap analysis
            output_file = session_dir / "gap_analysis.json"
            with open(output_file, "w") as f:
                json.dump(gap_result, f, indent=2)
            
            logger.info(f"Gap analysis results saved to: {output_file}")
            
        except Exception as e:
            logger.error(f"Failed to save gap results: {e}")
            raise Exception(f"Failed to save gap results: {str(e)}") from e
    
    def load_gap_results(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Load saved gap analysis results from file system.
        
        Args:
            session_id: Session ID
            
        Returns:
            Gap analysis results dictionary or None if not found
        """
        try:
            output_file = Path(f"data/sessions/{session_id}/gap_analysis.json")
            
            if not output_file.exists():
                logger.warning(f"Gap analysis results not found for session: {session_id}")
                return None
            
            with open(output_file, "r") as f:
                results = json.load(f)
            
            logger.info(f"Loaded gap analysis results for session: {session_id}")
            return results
            
        except Exception as e:
            logger.error(f"Failed to load gap results: {e}")
            return None
