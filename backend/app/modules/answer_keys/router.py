from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.answer_keys.schemas import AnswerKeyResponse, AnswerKeyUpsertRequest
from app.modules.answer_keys.service import AnswerKeyService
from app.security.dependencies import CurrentUser

router = APIRouter()


@router.get("/exam/{exam_id}", response_model=list[AnswerKeyResponse])
def list_answer_keys(
    exam_id: str,
    _: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
) -> list[AnswerKeyResponse]:
    rows = AnswerKeyService(db).list_for_exam(exam_id)
    return [AnswerKeyResponse.model_validate(row, from_attributes=True) for row in rows]


@router.put("", response_model=list[AnswerKeyResponse], status_code=status.HTTP_200_OK)
def replace_answer_keys(
    payload: AnswerKeyUpsertRequest,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
) -> list[AnswerKeyResponse]:
    rows = AnswerKeyService(db).replace_for_exam(payload, current_user.id)
    return [AnswerKeyResponse.model_validate(row, from_attributes=True) for row in rows]
