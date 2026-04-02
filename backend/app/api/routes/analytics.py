from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models import Exam, ResultAttempt, User
from app.schemas.result import AnalyticsSnapshot


router = APIRouter(prefix="/analytics")


@router.get("/summary", response_model=AnalyticsSnapshot)
def get_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AnalyticsSnapshot:
    del current_user
    total_exams = db.query(func.count(Exam.id)).scalar() or 0
    exam_ids = db.query(Exam.id).subquery()
    total_attempts = db.query(func.count(ResultAttempt.id)).filter(ResultAttempt.exam_id.in_(exam_ids)).scalar() or 0
    flagged_attempts = (
        db.query(func.count(ResultAttempt.id))
        .filter(ResultAttempt.exam_id.in_(exam_ids), ResultAttempt.needs_review.is_(True))
        .scalar()
        or 0
    )
    average_score = db.query(func.avg(ResultAttempt.score)).filter(ResultAttempt.exam_id.in_(exam_ids)).scalar() or 0
    return AnalyticsSnapshot(
        total_exams=total_exams,
        total_attempts=total_attempts,
        flagged_attempts=flagged_attempts,
        average_score=round(float(average_score), 2),
    )
