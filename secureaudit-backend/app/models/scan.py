"""
models/scan.py — SQLAlchemy models for scans and findings tables
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Scan(Base):
    """
    Represents a security scan performed on a URL.
    
    Each scan belongs to a user (via user_id) and
    contains multiple findings (via the findings relationship).
    """

    __tablename__ = "scans"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True  # nullable = anonymous scans allowed
    )

    url = Column(
        String(2048),
        nullable=False  # URL is required
    )

    score = Column(
        Integer,
        nullable=False  # Score 0-100
    )

    score_label = Column(
        String(50),
        nullable=True  # "Excellent", "Good", "Fair", "Poor", "Critical"
    )

    status = Column(
        String(50),
        default="completed"  # pending / completed / failed
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Relationship: one scan has many findings
    findings = relationship(
        "Finding",
        back_populates="scan",
        cascade="all, delete-orphan"  # delete findings when scan is deleted
    )

    def __repr__(self):
        """Human-readable representation for debugging."""
        return f"<Scan id={self.id} url={self.url} score={self.score}>"


class Finding(Base):
    """
    Represents a single security check result within a scan.
    
    Each finding belongs to one scan (via scan_id) and
    contains details about what was found and how to fix it.
    """

    __tablename__ = "findings"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    scan_id = Column(
        Integer,
        ForeignKey("scans.id"),
        nullable=False  # A finding must belong to a scan
    )

    check_name = Column(
        String(100),
        nullable=False  # e.g. "CSP Header", "SSL Certificate"
    )

    status = Column(
        String(20),
        nullable=False  # "pass" or "fail"
    )

    severity = Column(
        String(20),
        nullable=False  # "critical", "medium", "low", "info"
    )

    description = Column(
        Text,
        nullable=True  # What was found
    )

    recommendation = Column(
        Text,
        nullable=True  # How to fix it
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Relationship: each finding belongs to one scan
    scan = relationship("Scan", back_populates="findings")

    def __repr__(self):
        """Human-readable representation for debugging."""
        return f"<Finding id={self.id} check={self.check_name} status={self.status} severity={self.severity}>"