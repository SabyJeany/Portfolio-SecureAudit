"""
routers/reports.py — PDF report generation routes

Defines 2 routes:
1. GET /api/scans/{id}/pdf   → generate and download PDF report
2. POST /api/scans/{id}/email → send PDF report by email

Uses WeasyPrint to convert HTML template to PDF.
Uses Jinja2 to render the HTML template with scan data.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa
from io import BytesIO
import os

from app.core.database import get_db
from app.core.security import verify_token
from app.models.scan import Scan
from app.models.user import User
from app.scanner.score import ScoreCalculator

router = APIRouter(prefix="/api/reports", tags=["Reports"])
security = HTTPBearer(auto_error=False)

# Path to HTML templates folder
TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")


def get_current_user_optional(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Get current user from JWT token if provided.
    Returns None if no token (anonymous access).
    """
    if credentials is None:
        return None
    user_id = verify_token(credentials.credentials)
    if user_id is None:
        return None
    return db.query(User).filter(User.id == int(user_id)).first()


def get_score_color(score: int) -> str:
    """
    Get hex color based on score value.
    Used in the PDF template for the score circle color.
    
    Args:
        score: integer between 0 and 100
    Returns:
        hex color string
    """
    if score >= 90:
        return '#1D9E75'
    elif score >= 70:
        return '#22c55e'
    elif score >= 50:
        return '#eab308'
    elif score >= 30:
        return '#f97316'
    else:
        return '#ef4444'


@router.get("/{scan_id}")
def generate_pdf(
    scan_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_optional)
):
    """
    Generate and download a PDF security report for a scan.
    
    1. Fetches scan + findings from database
    2. Renders HTML template with scan data using Jinja2
    3. Converts HTML to PDF using WeasyPrint
    4. Returns PDF as downloadable file
    
    Args:
        scan_id: ID of the scan to generate PDF for
        db: database session
        current_user: logged-in user (optional)
        
    Returns:
        PDF file as binary response
        
    Raises:
        404 if scan not found
        500 if PDF generation fails
    """
    # Fetch scan from database
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scan not found"
        )

    try:
        # Calculate severity counts
        calculator = ScoreCalculator([
            {"status": f.status, "severity": f.severity}
            for f in scan.findings
        ])
        severity_counts = calculator.get_severity_counts()
        passed_count = sum(1 for f in scan.findings if f.status == 'pass')

        # Load and render HTML template with Jinja2
        env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
        template = env.get_template("report.html")

        html_content = template.render(
            scan_id=scan.id,
            url=scan.url,
            score=scan.score,
            score_label=scan.score_label,
            score_color=get_score_color(scan.score),
            scan_date=scan.created_at.strftime("%d %b %Y, %H:%M"),
            critical_count=severity_counts.get("critical", 0),
            medium_count=severity_counts.get("medium", 0),
            low_count=severity_counts.get("low", 0),
            passed_count=passed_count,
            total_checks=len(scan.findings),
            findings=scan.findings
        )

        # Convert HTML to PDF using WeasyPrint
        pdf_buffer = BytesIO()
        pisa.CreatePDF(html_content, dest=pdf_buffer)
        pdf_bytes = pdf_buffer.getvalue()

        # Return PDF as downloadable file
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=secureaudit-report-{scan_id}.pdf"
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"PDF generation failed: {str(e)}"
        )