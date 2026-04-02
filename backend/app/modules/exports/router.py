from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.exports.service import ExportService
from app.security.dependencies import CurrentUser

router = APIRouter()


@router.post("/results")
def export_results(
    _: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
    exam_id: str | None = Query(default=None),
) -> dict[str, str]:
    export_path = ExportService(db).export_results_csv(exam_id=exam_id)
    return {"status": "IMPLEMENTED", "export_path": export_path}
