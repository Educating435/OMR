from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.exams.schemas import ExamCreate, ExamDetailResponse, ExamResponse
from app.modules.exams.service import ExamService
from app.security.dependencies import CurrentUser

router = APIRouter()


@router.get("", response_model=list[ExamResponse])
def list_exams(
    _: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
) -> list[ExamResponse]:
    exams = ExamService(db).list_exams()
    return [ExamResponse.model_validate(exam, from_attributes=True) for exam in exams]


@router.post("", response_model=ExamResponse, status_code=status.HTTP_201_CREATED)
def create_exam(
    payload: ExamCreate,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
) -> ExamResponse:
    exam = ExamService(db).create_exam(payload, current_user.id)
    return ExamResponse.model_validate(exam, from_attributes=True)


@router.get("/{exam_id}", response_model=ExamDetailResponse)
def get_exam(
    exam_id: str,
    _: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
) -> ExamDetailResponse:
    service = ExamService(db)
    exam = service.get_exam(exam_id)
    stats = service.exam_stats(exam_id)
    return ExamDetailResponse(
        **ExamResponse.model_validate(exam, from_attributes=True).model_dump(),
        template_count=stats["template_count"],
        result_count=stats["result_count"],
    )
