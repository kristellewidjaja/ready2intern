"""Tests for resume upload endpoint"""
import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import io

from app.main import app

client = TestClient(app)


def test_upload_valid_pdf():
    """Test uploading a valid PDF file"""
    # Create a mock PDF file
    pdf_content = b"%PDF-1.4\n%test content\n%%EOF"
    files = {"file": ("test_resume.pdf", io.BytesIO(pdf_content), "application/pdf")}
    
    response = client.post("/api/upload", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert data["status"] == "uploaded"
    assert data["filename"] == "test_resume.pdf"
    assert data["file_size"] > 0


def test_upload_valid_docx():
    """Test uploading a valid DOCX file"""
    # Create a mock DOCX file (minimal valid DOCX structure)
    docx_content = b"PK\x03\x04" + b"\x00" * 100  # Simplified ZIP header
    files = {"file": ("test_resume.docx", io.BytesIO(docx_content), 
                      "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
    
    response = client.post("/api/upload", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert data["status"] == "uploaded"
    assert data["filename"] == "test_resume.docx"


def test_upload_invalid_file_type():
    """Test uploading an invalid file type"""
    txt_content = b"This is a text file"
    files = {"file": ("test.txt", io.BytesIO(txt_content), "text/plain")}
    
    response = client.post("/api/upload", files=files)
    
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert "Invalid file type" in data["message"]


def test_upload_empty_file():
    """Test uploading an empty file"""
    files = {"file": ("empty.pdf", io.BytesIO(b""), "application/pdf")}
    
    response = client.post("/api/upload", files=files)
    
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert "empty" in data["message"].lower()


def test_upload_file_too_large():
    """Test uploading a file that exceeds size limit"""
    # Create a file larger than 5MB
    large_content = b"x" * (6 * 1024 * 1024)  # 6MB
    files = {"file": ("large_resume.pdf", io.BytesIO(large_content), "application/pdf")}
    
    response = client.post("/api/upload", files=files)
    
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert "exceeds maximum" in data["message"].lower()


def test_upload_no_file():
    """Test upload endpoint without providing a file"""
    response = client.post("/api/upload")
    
    assert response.status_code == 422  # Unprocessable Entity


def test_session_id_is_unique():
    """Test that each upload generates a unique session ID"""
    pdf_content = b"%PDF-1.4\n%test content\n%%EOF"
    files1 = {"file": ("resume1.pdf", io.BytesIO(pdf_content), "application/pdf")}
    files2 = {"file": ("resume2.pdf", io.BytesIO(pdf_content), "application/pdf")}
    
    response1 = client.post("/api/upload", files=files1)
    response2 = client.post("/api/upload", files=files2)
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    session_id1 = response1.json()["session_id"]
    session_id2 = response2.json()["session_id"]
    
    assert session_id1 != session_id2


def test_uploaded_file_exists():
    """Test that uploaded file is saved to disk"""
    pdf_content = b"%PDF-1.4\n%test content\n%%EOF"
    files = {"file": ("test_file.pdf", io.BytesIO(pdf_content), "application/pdf")}
    
    response = client.post("/api/upload", files=files)
    
    assert response.status_code == 200
    session_id = response.json()["session_id"]
    
    # Check if file exists in data/resumes directory
    upload_dir = Path("data/resumes")
    uploaded_files = list(upload_dir.glob(f"{session_id}_*.pdf"))
    
    assert len(uploaded_files) > 0, "Uploaded file not found in data/resumes"
    
    # Cleanup
    for file in uploaded_files:
        file.unlink()
