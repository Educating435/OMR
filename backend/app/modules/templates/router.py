from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.templates.schemas import GenerateTemplateRequest, TemplateResponse
from app.modules.templates.service import TemplateService
from app.security.dependencies import CurrentUser

router = APIRouter()


@router.get("", response_model=list[TemplateResponse])
def list_templates(
    _: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
    exam_id: str | None = Query(default=None),
) -> list[TemplateResponse]:
    templates = TemplateService(db).list_templates(exam_id)
    return [TemplateResponse.model_validate(template, from_attributes=True) for template in templates]


@router.post("/generate", response_model=TemplateResponse, status_code=status.HTTP_201_CREATED)
def generate_template(
    payload: GenerateTemplateRequest,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
) -> TemplateResponse:
    template = TemplateService(db).generate_template(payload.exam_id, current_user.id)
    return TemplateResponse.model_validate(template, from_attributes=True)
