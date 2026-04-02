from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, require_roles
from app.models import Exam, User, UserRole
from app.schemas.exam import ExamCreate, ExamRead


router = APIRouter(prefix="/exams")


@router.get("", response_model=list[ExamRead])
def list_exams(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> list[Exam]:
    del current_user
    return db.query(Exam).order_by(Exam.created_at.desc()).all()


@router.post("", response_model=ExamRead, status_code=status.HTTP_201_CREATED)
def create_exam(
    payload: ExamCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPER_ADMIN)),
) -> Exam:
    exam = Exam(owner_id=current_user.id, **payload.model_dump())
    db.add(exam)
    db.commit()
    db.refresh(exam)
    return exam


@router.get("/{exam_id}", response_model=ExamRead)
def get_exam(exam_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> Exam:
    del current_user
    exam = db.get(Exam, exam_id)
    if exam is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")
    return exam
