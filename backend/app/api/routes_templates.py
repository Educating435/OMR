from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse

from app.api.deps import DBSession, get_current_user, get_pagination, require_roles
from app.core.storage import StorageManager
from app.models import User, UserRole
from app.repositories.audit_repository import AuditRepository
from app.repositories.exam_repository import ExamRepository
from app.schemas.exam import TemplateGenerateRequest, TemplateRead
from app.services.pdf_service import PdfService
from app.services.template_service import TemplateService


router = APIRouter(prefix="/templates")


@router.get("")
def list_templates(
    db: DBSession,
    pagination=Depends(get_pagination),
    current_user: User = Depends(get_current_user),
) -> dict:
    del current_user
    repo = ExamRepository(db)
    offset = (pagination.page - 1) * pagination.page_size
    items = repo.list_all_templates(offset=offset, limit=pagination.page_size)
    total = repo.count_templates()
    return {"items": [TemplateRead.model_validate(item).model_dump() for item in items], "meta": {"page": pagination.page, "page_size": pagination.page_size, "total": total}}


@router.post("/generate", response_model=TemplateRead, status_code=status.HTTP_201_CREATED)
def create_template(
    payload: TemplateGenerateRequest,
    db: DBSession,
    current_user: User = Depends(require_roles(UserRole.SUPER_ADMIN)),
) -> TemplateRead:
    del current_user
    service = TemplateService(ExamRepository(db), PdfService(), StorageManager(), AuditRepository(db))
    return TemplateRead.model_validate(service.create_template(payload.exam_id))


@router.get("/{template_id}", response_model=TemplateRead)
def get_template(template_id: str, db: DBSession, current_user: User = Depends(get_current_user)) -> TemplateRead:
    del current_user
    item = ExamRepository(db).get_template(template_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template not found")
    return TemplateRead.model_validate(item)


@router.get("/{template_id}/pdf")
def get_template_pdf(template_id: str, db: DBSession, current_user: User = Depends(get_current_user)) -> FileResponse:
    del current_user
    item = ExamRepository(db).get_template(template_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template not found")
    file_path = StorageManager().resolve(Path(item.pdf_path))
    return FileResponse(path=file_path, filename=file_path.name, media_type="application/pdf")
