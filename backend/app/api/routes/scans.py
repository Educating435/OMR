from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models import ResultAttempt, User
from app.schemas.result import ResultRead, ScanSubmission


router = APIRouter(prefix="/scans")


@router.post("/submit", response_model=ResultRead, status_code=status.HTTP_201_CREATED)
def submit_scan(
    payload: ScanSubmission,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ResultAttempt:
    del current_user
    existing = db.query(ResultAttempt).filter(ResultAttempt.local_attempt_uuid == payload.local_attempt_uuid).first()
    if existing:
        return existing

    grading_summary = payload.grading_summary
    needs_review = bool(grading_summary.get("uncertain", 0)) or bool(grading_summary.get("multiple_marked", 0))
    attempt = ResultAttempt(**payload.model_dump(), needs_review=needs_review)
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return attempt
