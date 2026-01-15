"""
Tests for resume parser service.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
from app.services.resume_parser import ResumeParser


@pytest.fixture
def resume_parser():
    """Create a ResumeParser instance."""
    return ResumeParser()


@pytest.fixture
def sample_pdf_text():
    """Sample text that would be extracted from a PDF."""
    return """John Doe
Software Engineer
john.doe@example.com | (555) 123-4567

EDUCATION
University of California, Berkeley
B.S. Computer Science, Expected May 2024
GPA: 3.8/4.0

SKILLS
Programming Languages: Python, Java, JavaScript, C++
Frameworks: React, Django, Flask
Tools: Git, Docker, AWS

EXPERIENCE
Software Engineering Intern | Tech Company | Summer 2023
- Built scalable web application using React and Django
- Improved API performance by 40%

PROJECTS
E-commerce Platform
- Developed full-stack application with React and Node.js
- Implemented payment integration with Stripe"""


@pytest.fixture
def sample_docx_paragraphs():
    """Sample paragraphs that would be extracted from a DOCX."""
    return [
        "Jane Smith",
        "Data Scientist",
        "jane.smith@example.com",
        "",
        "EDUCATION",
        "Stanford University",
        "M.S. Computer Science, 2024",
        "",
        "SKILLS",
        "Python, R, TensorFlow, PyTorch",
        "",
        "EXPERIENCE",
        "ML Intern | AI Startup | 2023",
        "- Built recommendation system",
        "- Improved model accuracy by 25%",
    ]


class TestResumeParser:
    """Test suite for ResumeParser."""
    
    def test_init(self, resume_parser):
        """Test ResumeParser initialization."""
        assert resume_parser is not None
    
    def test_extract_text_file_not_found(self, resume_parser):
        """Test extract_text with non-existent file."""
        with pytest.raises(FileNotFoundError):
            resume_parser.extract_text("nonexistent.pdf")
    
    def test_extract_text_unsupported_format(self, resume_parser, tmp_path):
        """Test extract_text with unsupported file format."""
        # Create a temporary file with unsupported extension
        test_file = tmp_path / "test.txt"
        test_file.write_text("Some content")
        
        # extract_text returns (text, error) tuple, not raises exception
        text, error = resume_parser.extract_text(str(test_file))
        
        assert text == ""
        assert error != ""
        assert "Unsupported file format" in error
    
    @patch("app.services.resume_parser.PyPDF2.PdfReader")
    @patch("builtins.open", new_callable=mock_open, read_data=b"fake pdf content")
    def test_extract_from_pdf_success(
        self, mock_file, mock_pdf_reader, resume_parser, sample_pdf_text, tmp_path
    ):
        """Test successful PDF text extraction."""
        # Create a temporary PDF file
        test_file = tmp_path / "test.pdf"
        test_file.write_bytes(b"fake pdf content")
        
        # Mock PDF reader
        mock_page = Mock()
        mock_page.extract_text.return_value = sample_pdf_text
        mock_reader_instance = Mock()
        mock_reader_instance.pages = [mock_page]
        mock_pdf_reader.return_value = mock_reader_instance
        
        # Extract text
        text, error = resume_parser.extract_text(str(test_file))
        
        assert error == ""
        assert "John Doe" in text
        assert "Software Engineer" in text
        assert "Python" in text
    
    @patch("app.services.resume_parser.PyPDF2.PdfReader")
    @patch("builtins.open", new_callable=mock_open, read_data=b"fake pdf content")
    def test_extract_from_pdf_empty(
        self, mock_file, mock_pdf_reader, resume_parser, tmp_path
    ):
        """Test PDF extraction with empty content."""
        test_file = tmp_path / "empty.pdf"
        test_file.write_bytes(b"fake pdf content")
        
        # Mock PDF reader with empty text
        mock_page = Mock()
        mock_page.extract_text.return_value = ""
        mock_reader_instance = Mock()
        mock_reader_instance.pages = [mock_page]
        mock_pdf_reader.return_value = mock_reader_instance
        
        # Extract text should raise error for empty PDF
        text, error = resume_parser.extract_text(str(test_file))
        
        assert error != ""
        assert "empty" in error.lower()
    
    @patch("app.services.resume_parser.Document")
    def test_extract_from_docx_success(
        self, mock_document, resume_parser, sample_docx_paragraphs, tmp_path
    ):
        """Test successful DOCX text extraction."""
        test_file = tmp_path / "test.docx"
        test_file.write_bytes(b"fake docx content")
        
        # Mock Document
        mock_doc_instance = Mock()
        mock_paragraphs = [Mock(text=text) for text in sample_docx_paragraphs]
        mock_doc_instance.paragraphs = mock_paragraphs
        mock_doc_instance.tables = []  # No tables
        mock_document.return_value = mock_doc_instance
        
        # Extract text
        text, error = resume_parser.extract_text(str(test_file))
        
        assert error == ""
        assert "Jane Smith" in text
        assert "Data Scientist" in text
        assert "Python" in text
    
    @patch("app.services.resume_parser.Document")
    def test_extract_from_docx_with_tables(
        self, mock_document, resume_parser, tmp_path
    ):
        """Test DOCX extraction with tables."""
        test_file = tmp_path / "test_with_tables.docx"
        test_file.write_bytes(b"fake docx content")
        
        # Mock Document with tables
        mock_doc_instance = Mock()
        mock_doc_instance.paragraphs = [Mock(text="Header Text")]
        
        # Mock table
        mock_cell1 = Mock(text="Skill")
        mock_cell2 = Mock(text="Python")
        mock_row = Mock(cells=[mock_cell1, mock_cell2])
        mock_table = Mock(rows=[mock_row])
        mock_doc_instance.tables = [mock_table]
        
        mock_document.return_value = mock_doc_instance
        
        # Extract text
        text, error = resume_parser.extract_text(str(test_file))
        
        assert error == ""
        assert "Header Text" in text
        assert "Skill" in text
        assert "Python" in text
    
    @patch("app.services.resume_parser.Document")
    def test_extract_from_docx_empty(self, mock_document, resume_parser, tmp_path):
        """Test DOCX extraction with empty content."""
        test_file = tmp_path / "empty.docx"
        test_file.write_bytes(b"fake docx content")
        
        # Mock Document with empty paragraphs
        mock_doc_instance = Mock()
        mock_doc_instance.paragraphs = [Mock(text=""), Mock(text="   ")]
        mock_doc_instance.tables = []
        mock_document.return_value = mock_doc_instance
        
        # Extract text should return error for empty DOCX
        text, error = resume_parser.extract_text(str(test_file))
        
        assert error != ""
        assert "empty" in error.lower()
    
    @patch("app.services.resume_parser.PyPDF2.PdfReader")
    @patch("builtins.open", new_callable=mock_open, read_data=b"fake pdf content")
    def test_extract_from_pdf_exception(
        self, mock_file, mock_pdf_reader, resume_parser, tmp_path
    ):
        """Test PDF extraction with exception."""
        test_file = tmp_path / "corrupt.pdf"
        test_file.write_bytes(b"fake pdf content")
        
        # Mock PDF reader to raise exception
        mock_pdf_reader.side_effect = Exception("Corrupt PDF")
        
        # Extract text should return error
        text, error = resume_parser.extract_text(str(test_file))
        
        assert text == ""
        assert error != ""
        assert "Corrupt PDF" in error
