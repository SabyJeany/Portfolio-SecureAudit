"""
routers/scans.py — Scan API routes

Defines 3 routes:
1. POST /api/scans       → launch a new scan on a URL
2. GET  /api/scans       → get all scans for the logged-in user
3. GET  /api/scans/{id}  → get a specific scan with all its findings
4. DELETE /api/scans/{id} → delete a scan

Flow for POST /api/scans:
1. Receive URL from frontend
2. Run ScanEngine on the URL
3. Calculate score with ScoreCalculator
4. Store scan + findings in PostgreSQL
5. Return complete scan result to frontend
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import verify_token
from app.models.scan import Scan, Finding
from app.models.user import User
from app.schemas.scan import ScanCreate, ScanResponse, ScanListItem
from app.scanner.engine import ScanEngine
from app.scanner.score import ScoreCalculator

router = APIRouter(prefix="/api/scans", tags=["Scans"])
security = HTTPBearer(auto_error=False)


def get_current_user_optional(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Get the current user from JWT token if provided.
    Returns None if no token is provided (anonymous scan).
    
    Args:
        credentials: JWT token from Authorization header (optional)
        db: database session
        
    Returns:
        User object if authenticated, None if anonymous
    """
    if credentials is None:
        return None

    user_id = verify_token(credentials.credentials)
    if user_id is None:
        return None

    user = db.query(User).filter(User.id == int(user_id)).first()
    return user


def get_current_user_required(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Get the current user from JWT token — authentication required.
    Raises 401 if no valid token is provided.
    
    Args:
        credentials: JWT token from Authorization header
        db: database session
        
    Returns:
        User object
        
    Raises:
        401 if token is missing or invalid
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )

    user_id = verify_token(credentials.credentials)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.post("", response_model=ScanResponse, status_code=status.HTTP_201_CREATED)
def create_scan(
    scan_data: ScanCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_optional)
):
    """
    Launch a new security scan on a URL.
    
    This is the core endpoint of SecureAudit:
    1. Validates the URL format
    2. Runs the ScanEngine (headers, SSL, redirects, robots)
    3. Calculates the security score (0-100)
    4. Stores scan + findings in PostgreSQL
    5. Returns the complete scan result
    
    Args:
        scan_data: { url } from frontend
        db: database session
        current_user: logged-in user (optional — anonymous scans allowed)
        
    Returns:
        complete ScanResponse with score, findings, severity counts
        
    Raises:
        400 if URL format is invalid
        500 if scan fails unexpectedly
    """
    # Validate URL format
    if not scan_data.url.startswith(('http://', 'https://')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid URL. Must start with http:// or https://"
        )

    try:
        # Run the security scan
        engine = ScanEngine(scan_data.url)
        findings_data = engine.run_scan()

        # Calculate the security score
        calculator = ScoreCalculator(findings_data)
        score = calculator.calculate_score()
        score_label = calculator.get_score_label(score)
        severity_counts = calculator.get_severity_counts()

        # Create the Scan record in database
        scan = Scan(
            url=scan_data.url,
            score=score,
            score_label=score_label,
            status="completed",
            user_id=current_user.id if current_user else None
        )
        db.add(scan)
        db.flush()  # Get the scan.id before committing

        # Create Finding records for each check result
        finding_objects = []
        for f in findings_data:
            finding = Finding(
                scan_id=scan.id,
                check_name=f["check_name"],
                status=f["status"],
                severity=f["severity"],
                description=f.get("description"),
                recommendation=f.get("recommendation")
            )
            db.add(finding)
            finding_objects.append(finding)

        db.commit()
        db.refresh(scan)

        # Build and return the response
        return {
            "id": scan.id,
            "url": scan.url,
            "score": scan.score,
            "score_label": scan.score_label,
            "status": scan.status,
            "created_at": scan.created_at,
            "severity_counts": severity_counts,
            "findings": [
                {
                    "id": f.id,
                    "check_name": f.check_name,
                    "status": f.status,
                    "severity": f.severity,
                    "description": f.description,
                    "recommendation": f.recommendation
                }
                for f in finding_objects
            ]
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Scan failed: {str(e)}"
        )


@router.get("", response_model=List[ScanListItem])
def get_scans(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_required)
):
    """
    Get all scans for the logged-in user (scan history).
    
    Returns a simplified list without full findings details.
    Ordered by most recent first.
    
    Args:
        db: database session
        current_user: logged-in user (required)
        
    Returns:
        list of ScanListItem (id, url, score, score_label, status, created_at)
    """
    scans = (
        db.query(Scan)
        .filter(Scan.user_id == current_user.id)
        .order_by(Scan.created_at.desc())
        .all()
    )
    return scans


@router.get("/{scan_id}", response_model=ScanResponse)
def get_scan(
    scan_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_optional)
):
    """
    Get a specific scan with all its findings.
    
    Args:
        scan_id: ID of the scan to retrieve
        db: database session
        current_user: logged-in user (optional)
        
    Returns:
        complete ScanResponse with all findings
        
    Raises:
        404 if scan not found
    """
    scan = db.query(Scan).filter(Scan.id == scan_id).first()

    if scan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scan not found"
        )

    # Calculate severity counts from existing findings
    calculator = ScoreCalculator([
        {"status": f.status, "severity": f.severity}
        for f in scan.findings
    ])
    severity_counts = calculator.get_severity_counts()

    return {
        "id": scan.id,
        "url": scan.url,
        "score": scan.score,
        "score_label": scan.score_label,
        "status": scan.status,
        "created_at": scan.created_at,
        "severity_counts": severity_counts,
        "findings": scan.findings
    }


@router.delete("/{scan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_scan(
    scan_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_required)
):
    """
    Delete a scan and all its findings.
    
    Only the owner of the scan can delete it.
    
    Args:
        scan_id: ID of the scan to delete
        db: database session
        current_user: logged-in user (required)
        
    Raises:
        404 if scan not found
        403 if user does not own the scan
    """
    scan = db.query(Scan).filter(Scan.id == scan_id).first()

    if scan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scan not found"
        )

    if scan.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete this scan"
        )

    db.delete(scan)
    db.commit()