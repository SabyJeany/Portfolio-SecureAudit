
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

"""
schemas/scan.py — Pydantic schemas for scans and findings
"""

class ScanCreate(BaseModel):
    """
    Data received from the frontend to start a new scan.
    
    Example JSON received:
    {
        "url": "https://example.com"
    }
    """
    url: str


class FindingResponse(BaseModel):
    """
    Structure of a single security finding returned to the frontend.
    
    Example JSON returned:
    {
        "id": 1,
        "check_name": "CSP Header",
        "status": "fail",
        "severity": "critical",
        "description": "Content-Security-Policy header is missing.",
        "recommendation": "Add: Content-Security-Policy: default-src 'self'"
    }
    """
    id: int
    check_name: str
    status: str
    severity: str
    description: Optional[str] = None
    recommendation: Optional[str] = None

    class Config:
        """Allow reading data from SQLAlchemy objects."""
        from_attributes = True


class ScanResponse(BaseModel):
    """
    Complete scan result returned to the frontend.
    
    Example JSON returned:
    {
        "id": 42,
        "url": "https://example.com",
        "score": 78,
        "score_label": "Good",
        "status": "completed",
        "created_at": "2026-05-28T10:00:00",
        "severity_counts": {
            "critical": 2,
            "medium": 3,
            "low": 1,
            "info": 0
        },
        "findings": [...]
    }
    """
    id: int
    url: str
    score: int
    score_label: Optional[str] = None
    status: str
    created_at: datetime
    findings: List[FindingResponse] = []
    severity_counts: Optional[dict] = None

    class Config:
        """Allow reading data from SQLAlchemy objects."""
        from_attributes = True


class ScanListItem(BaseModel):
    """
    Simplified scan item for the history list.
    Does not include the full findings list — only summary data.
    
    Example JSON returned:
    {
        "id": 42,
        "url": "https://example.com",
        "score": 78,
        "score_label": "Good",
        "status": "completed",
        "created_at": "2026-05-28T10:00:00"
    }
    """
    id: int
    url: str
    score: int
    score_label: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        """Allow reading data from SQLAlchemy objects."""
        from_attributes = True