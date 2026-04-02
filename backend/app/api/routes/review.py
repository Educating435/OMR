from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, require_roles
from app.models import Exam, ResultAttempt, User, UserRole
from app.schemas.result import ResultRead, ResultReviewUpdate


router = APIRouter(prefix="/review")


@router.get("/flagged", response_model=list[ResultRead])
def list_flagged_scans(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.STAFF, UserRole.VIEWER)),
) -> list[ResultAttempt]:
    del current_user
    exam_ids = db.query(Exam.id).subquery()
    return (
        db.query(ResultAttempt)
        .filter(ResultAttempt.exam_id.in_(exam_ids), ResultAttempt.needs_review.is_(True))
        .order_by(ResultAttempt.created_at.desc())
        .all()
    )


@router.patch("/{attempt_id}", response_model=ResultRead)
def update_review_status(
    attempt_id: str,
    payload: ResultReviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.STAFF)),
) -> ResultAttempt:
    attempt = db.get(ResultAttempt, attempt_id)
    if attempt is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attempt not found")

    exam = db.get(Exam, attempt.exam_id)
    if exam is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attempt not found")

    attempt.needs_review = payload.needs_review
    attempt.review_status = payload.review_status
    attempt.remarks = payload.remarks
    attempt.reviewed_by = current_user.id
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return attempt
