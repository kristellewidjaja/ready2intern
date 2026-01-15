"""
Company service for managing company data and tenets.
"""

import os
from pathlib import Path

from app.models.company import Company


class CompanyService:
    """Service for managing company information and tenets."""

    # Company data configuration
    COMPANIES = [
        {
            "id": "amazon",
            "name": "amazon",
            "display_name": "Amazon",
            "color": "#FF9900",  # Amazon orange
            "logo_url": "/logos/amazon.svg",
            "tenets_file": "amazon-leadership-principles.txt",
            "description": "Evaluated against Amazon's 16 Leadership Principles",
        },
        {
            "id": "meta",
            "name": "meta",
            "display_name": "Meta",
            "color": "#0081FB",  # Meta blue
            "logo_url": "/logos/meta.svg",
            "tenets_file": "meta-core-values.txt",
            "description": "Evaluated against Meta's Core Values and cultural principles",
        },
        {
            "id": "google",
            "name": "google",
            "display_name": "Google",
            "color": "#4285F4",  # Google blue
            "logo_url": "/logos/google.svg",
            "tenets_file": "google-principles.txt",
            "description": "Evaluated against Google's principles and 'Googleyness'",
        },
    ]

    def __init__(self, tenets_dir: str = "data/company-tenets"):
        """
        Initialize the company service.

        Args:
            tenets_dir: Directory containing company tenets files
        """
        self.tenets_dir = Path(tenets_dir)

    def get_all_companies(self) -> list[Company]:
        """
        Get list of all available companies.

        Returns:
            List of Company objects
        """
        return [Company(**company_data) for company_data in self.COMPANIES]

    def get_company_by_id(self, company_id: str) -> Company | None:
        """
        Get a specific company by ID.

        Args:
            company_id: Company identifier (e.g., 'amazon', 'meta', 'google')

        Returns:
            Company object if found, None otherwise
        """
        for company_data in self.COMPANIES:
            if company_data["id"] == company_id:
                return Company(**company_data)
        return None

    def get_company_tenets(self, company_id: str) -> str | None:
        """
        Load company tenets from file.

        Args:
            company_id: Company identifier

        Returns:
            Company tenets as string, or None if not found
        """
        company = self.get_company_by_id(company_id)
        if not company:
            return None

        tenets_path = self.tenets_dir / company.tenets_file
        if not tenets_path.exists():
            return None

        try:
            return tenets_path.read_text(encoding="utf-8")
        except Exception:
            return None

    def validate_company_id(self, company_id: str) -> bool:
        """
        Check if a company ID is valid.

        Args:
            company_id: Company identifier to validate

        Returns:
            True if valid, False otherwise
        """
        return any(c["id"] == company_id for c in self.COMPANIES)
