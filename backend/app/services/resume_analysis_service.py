"""
Resume analysis service that orchestrates resume parsing and LLM analysis.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

from app.services.llm_service import LLMService
from app.services.resume_parser import ResumeParser
from app.prompts.resume_analysis import (
    SYSTEM_PROMPT,
    create_resume_analysis_prompt,
)

logger = logging.getLogger(__name__)


class ResumeAnalysisService:
    """Service for analyzing resumes using LLM."""
    
    def __init__(self):
        """Initialize resume analysis service."""
        self.llm_service = LLMService()
        self.resume_parser = ResumeParser()
        logger.info("ResumeAnalysisService initialized")
    
    async def analyze_resume(
        self,
        resume_file_path: str,
        session_id: str,
    ) -> Dict[str, Any]:
        """
        Analyze a resume and extract structured information.
        
        Args:
            resume_file_path: Path to the resume file
            session_id: Session ID for saving results
            
        Returns:
            Dictionary containing structured resume analysis
            
        Raises:
            Exception: If analysis fails
        """
        logger.info(f"Starting resume analysis for session: {session_id}")
        
        try:
            # Step 1: Extract text from resume
            logger.info("Extracting text from resume...")
            resume_text, error = self.resume_parser.extract_text(resume_file_path)
            
            if error:
                raise Exception(f"Failed to extract text from resume: {error}")
            
            if not resume_text.strip():
                raise Exception("Resume appears to be empty")
            
            logger.info(f"Extracted {len(resume_text)} characters from resume")
            
            # Step 2: Create prompt for LLM
            prompt = create_resume_analysis_prompt(resume_text)
            
            # Step 3: Call LLM for analysis
            logger.info("Calling LLM for resume analysis...")
            llm_response = await self.llm_service.generate_completion(
                prompt=prompt,
                system_prompt=SYSTEM_PROMPT,
                max_tokens=4096,
                temperature=0.3,  # Lower temperature for more consistent extraction
            )
            
            # Step 4: Parse LLM response
            logger.info("Parsing LLM response...")
            analysis_result = self._parse_llm_response(llm_response)
            
            # Step 5: Save results to file system
            logger.info("Saving analysis results...")
            self._save_analysis_results(session_id, analysis_result)
            
            logger.info(f"Resume analysis completed for session: {session_id}")
            return analysis_result
            
        except Exception as e:
            logger.error(f"Resume analysis failed: {e}")
            raise Exception(f"Failed to analyze resume: {str(e)}") from e
    
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
            # Sometimes LLM might wrap JSON in markdown code blocks
            response = llm_response.strip()
            
            # Remove markdown code blocks if present
            if response.startswith("```json"):
                response = response[7:]  # Remove ```json
            elif response.startswith("```"):
                response = response[3:]  # Remove ```
            
            if response.endswith("```"):
                response = response[:-3]  # Remove trailing ```
            
            response = response.strip()
            
            # Parse JSON
            parsed = json.loads(response)
            
            # Validate required fields
            required_fields = [
                "personal_info",
                "education",
                "skills",
                "experience",
                "projects",
                "summary",
            ]
            
            for field in required_fields:
                if field not in parsed:
                    logger.warning(f"Missing required field: {field}")
                    # Add default value
                    if field in ["education", "experience", "projects", "certifications", "awards_honors"]:
                        parsed[field] = []
                    elif field == "skills":
                        parsed[field] = {
                            "programming_languages": [],
                            "frameworks_libraries": [],
                            "tools_technologies": [],
                            "databases": [],
                            "soft_skills": [],
                        }
                    elif field == "personal_info":
                        parsed[field] = {
                            "name": "Not provided",
                            "email": "Not provided",
                            "phone": "Not provided",
                            "location": "Not provided",
                        }
                    elif field == "summary":
                        parsed[field] = "No summary available"
            
            return parsed
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.error(f"Response was: {llm_response[:500]}...")
            raise ValueError(f"Invalid JSON response from LLM: {str(e)}") from e
        except Exception as e:
            logger.error(f"Unexpected error parsing response: {e}")
            raise ValueError(f"Failed to parse LLM response: {str(e)}") from e
    
    def _save_analysis_results(
        self,
        session_id: str,
        analysis_result: Dict[str, Any],
    ) -> None:
        """
        Save analysis results to file system.
        
        Args:
            session_id: Session ID
            analysis_result: Parsed analysis results
        """
        try:
            # Create session directory
            session_dir = Path(f"data/sessions/{session_id}")
            session_dir.mkdir(parents=True, exist_ok=True)
            
            # Save resume analysis
            output_file = session_dir / "resume_analysis.json"
            with open(output_file, "w") as f:
                json.dump(analysis_result, f, indent=2)
            
            logger.info(f"Analysis results saved to: {output_file}")
            
        except Exception as e:
            logger.error(f"Failed to save analysis results: {e}")
            raise Exception(f"Failed to save analysis results: {str(e)}") from e
    
    def load_analysis_results(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Load saved analysis results from file system.
        
        Args:
            session_id: Session ID
            
        Returns:
            Analysis results dictionary or None if not found
        """
        try:
            output_file = Path(f"data/sessions/{session_id}/resume_analysis.json")
            
            if not output_file.exists():
                logger.warning(f"Analysis results not found for session: {session_id}")
                return None
            
            with open(output_file, "r") as f:
                results = json.load(f)
            
            logger.info(f"Loaded analysis results for session: {session_id}")
            return results
            
        except Exception as e:
            logger.error(f"Failed to load analysis results: {e}")
            return None
