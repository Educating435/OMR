from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models import Exam, ResultAttempt, User
from app.schemas.result import ResultExportRow, ResultRead


router = APIRouter(prefix="/results")


@router.get("/{exam_id}", response_model=list[ResultRead])
def list_results(
    exam_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[ResultAttempt]:
    del current_user
    exam = db.get(Exam, exam_id)
    if exam is None:
        return []
    return db.query(ResultAttempt).filter(ResultAttempt.exam_id == exam_id).order_by(ResultAttempt.created_at.desc()).all()


@router.get("/{exam_id}/export", response_model=list[ResultExportRow])
def export_results(
    exam_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[ResultExportRow]:
    del current_user
    exam = db.get(Exam, exam_id)
    if exam is None:
        return []
    attempts = db.query(ResultAttempt).filter(ResultAttempt.exam_id == exam_id).all()
    return [
        ResultExportRow(
            student_identifier=item.student_identifier,
            score=item.score,
            max_score=item.max_score,
            percentage=0 if item.max_score == 0 else round((item.score / item.max_score) * 100, 2),
        )
        for item in attempts
    ]
