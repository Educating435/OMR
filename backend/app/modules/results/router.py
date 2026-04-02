from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.results.schemas import ResultResponse, ResultSyncRequest
from app.modules.results.service import ResultService
from app.security.dependencies import CurrentUser

router = APIRouter()


@router.get("", response_model=list[ResultResponse])
def list_results(
    _: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
    exam_id: str | None = Query(default=None),
    roll_number: str | None = Query(default=None),
) -> list[ResultResponse]:
    rows = ResultService(db).list_results(exam_id=exam_id, roll_number=roll_number)
    return [ResultResponse.model_validate(row, from_attributes=True) for row in rows]


@router.post("/sync", response_model=ResultResponse)
def sync_result(
    payload: ResultSyncRequest,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
) -> ResultResponse:
    result = ResultService(db).sync_result(payload, current_user.id)
    return ResultResponse.model_validate(result, from_attributes=True)


@router.post("/{result_id}/review", response_model=ResultResponse)
def mark_reviewed(
    result_id: str,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
) -> ResultResponse:
    result = ResultService(db).mark_reviewed(result_id, current_user.id)
    return ResultResponse.model_validate(result, from_attributes=True)
