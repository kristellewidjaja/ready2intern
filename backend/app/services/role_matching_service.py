"""
Role matching service that analyzes resume fit for job roles and company culture.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

from app.services.llm_service import LLMService
from app.services.company_service import CompanyService
from app.prompts.role_matching import (
    SYSTEM_PROMPT,
    create_role_matching_prompt,
)

logger = logging.getLogger(__name__)


class RoleMatchingService:
    """Service for matching resumes against job roles and company culture."""
    
    def __init__(self):
        """Initialize role matching service."""
        self.llm_service = LLMService()
        self.company_service = CompanyService()
        logger.info("RoleMatchingService initialized")
    
    async def analyze_match(
        self,
        session_id: str,
        company_id: str,
        role_description: str,
    ) -> Dict[str, Any]:
        """
        Analyze how well a resume matches a role and company.
        
        Args:
            session_id: Session ID for loading resume analysis
            company_id: Company ID (amazon, meta, google)
            role_description: Job role description
            
        Returns:
            Dictionary containing match analysis with scores
            
        Raises:
            Exception: If analysis fails
        """
        logger.info(f"Starting role matching analysis for session: {session_id}")
        
        try:
            # Step 1: Load resume analysis results
            logger.info("Loading resume analysis...")
            resume_data = self._load_resume_analysis(session_id)
            
            if not resume_data:
                raise Exception(f"Resume analysis not found for session: {session_id}")
            
            # Step 2: Load company tenets
            logger.info(f"Loading company tenets for: {company_id}")
            company_tenets = self.company_service.get_company_tenets(company_id)
            
            if not company_tenets:
                raise Exception(f"Company tenets not found for: {company_id}")
            
            # Step 3: Create prompt for LLM
            prompt = create_role_matching_prompt(
                resume_summary=resume_data,
                role_description=role_description,
                company_tenets=company_tenets,
            )
            
            # Step 4: Call LLM for matching analysis
            logger.info("Calling LLM for role matching analysis...")
            llm_response = await self.llm_service.generate_completion(
                prompt=prompt,
                system_prompt=SYSTEM_PROMPT,
                max_tokens=8192,  # Increased for complete JSON response
                temperature=0.1,  # Lower temperature for consistent scoring
            )
            
            # Step 5: Parse LLM response
            logger.info("Parsing LLM response...")
            match_result = self._parse_llm_response(llm_response)
            
            # Step 6: Validate and calculate scores
            logger.info("Validating scores...")
            match_result = self._validate_and_calculate_scores(match_result)
            
            # Step 7: Save results to file system
            logger.info("Saving match analysis results...")
            self._save_match_results(session_id, match_result)
            
            logger.info(f"Role matching analysis completed for session: {session_id}")
            logger.info(f"Overall score: {match_result.get('overall_score', {}).get('score', 0)}")
            
            return match_result
            
        except Exception as e:
            logger.error(f"Role matching analysis failed: {e}")
            raise Exception(f"Failed to analyze role match: {str(e)}") from e
    
    def _load_resume_analysis(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Load resume analysis results from file system.
        
        Args:
            session_id: Session ID
            
        Returns:
            Resume analysis dictionary or None if not found
        """
        try:
            analysis_file = Path(f"data/sessions/{session_id}/resume_analysis.json")
            
            if not analysis_file.exists():
                logger.warning(f"Resume analysis not found for session: {session_id}")
                return None
            
            with open(analysis_file, "r") as f:
                data = json.load(f)
            
            logger.info(f"Loaded resume analysis for session: {session_id}")
            return data
            
        except Exception as e:
            logger.error(f"Failed to load resume analysis: {e}")
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
                "ats_score",
                "role_match_score",
                "company_fit_score",
                "overall_score",
            ]
            
            for field in required_fields:
                if field not in parsed:
                    logger.warning(f"Missing required field: {field}")
                    # Add default structure
                    parsed[field] = {
                        "score": 0,
                        "explanation": "Not provided",
                    }
            
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
    
    def _validate_and_calculate_scores(self, match_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate scores and calculate overall score if needed.
        
        Args:
            match_data: Parsed match analysis data
            
        Returns:
            Validated match data with calculated overall score
        """
        # Extract individual scores
        ats_score = match_data.get("ats_score", {}).get("score", 0)
        role_match_score = match_data.get("role_match_score", {}).get("score", 0)
        company_fit_score = match_data.get("company_fit_score", {}).get("score", 0)
        
        # Validate scores are in range 0-100
        ats_score = max(0, min(100, ats_score))
        role_match_score = max(0, min(100, role_match_score))
        company_fit_score = max(0, min(100, company_fit_score))
        
        # Update validated scores
        match_data["ats_score"]["score"] = ats_score
        match_data["role_match_score"]["score"] = role_match_score
        match_data["company_fit_score"]["score"] = company_fit_score
        
        # Calculate weighted overall score
        # ATS: 20%, Role Match: 50%, Company Fit: 30%
        calculated_overall = round(
            (ats_score * 0.20) +
            (role_match_score * 0.50) +
            (company_fit_score * 0.30)
        )
        
        # Update overall score
        if "overall_score" not in match_data:
            match_data["overall_score"] = {}
        
        match_data["overall_score"]["score"] = calculated_overall
        match_data["overall_score"]["calculation"] = (
            "Weighted average: ATS ({}) × 20% + "
            "Role Match ({}) × 50% + "
            "Company Fit ({}) × 30% = {}".format(
                ats_score, role_match_score, company_fit_score, calculated_overall
            )
        )
        
        # Determine recommendation level
        if calculated_overall >= 85:
            recommendation = "strong_match"
        elif calculated_overall >= 70:
            recommendation = "good_match"
        elif calculated_overall >= 55:
            recommendation = "moderate_match"
        elif calculated_overall >= 40:
            recommendation = "weak_match"
        else:
            recommendation = "poor_match"
        
        match_data["overall_score"]["recommendation"] = recommendation
        
        logger.info(f"Validated scores - ATS: {ats_score}, Role: {role_match_score}, Company: {company_fit_score}, Overall: {calculated_overall}")
        
        return match_data
    
    def _save_match_results(
        self,
        session_id: str,
        match_result: Dict[str, Any],
    ) -> None:
        """
        Save match analysis results to file system.
        
        Args:
            session_id: Session ID
            match_result: Match analysis results
        """
        try:
            # Create session directory
            session_dir = Path(f"data/sessions/{session_id}")
            session_dir.mkdir(parents=True, exist_ok=True)
            
            # Save match analysis
            output_file = session_dir / "match_analysis.json"
            with open(output_file, "w") as f:
                json.dump(match_result, f, indent=2)
            
            logger.info(f"Match analysis results saved to: {output_file}")
            
        except Exception as e:
            logger.error(f"Failed to save match results: {e}")
            raise Exception(f"Failed to save match results: {str(e)}") from e
    
    def load_match_results(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Load saved match analysis results from file system.
        
        Args:
            session_id: Session ID
            
        Returns:
            Match analysis results dictionary or None if not found
        """
        try:
            output_file = Path(f"data/sessions/{session_id}/match_analysis.json")
            
            if not output_file.exists():
                logger.warning(f"Match analysis results not found for session: {session_id}")
                return None
            
            with open(output_file, "r") as f:
                results = json.load(f)
            
            logger.info(f"Loaded match analysis results for session: {session_id}")
            return results
            
        except Exception as e:
            logger.error(f"Failed to load match results: {e}")
            return None
