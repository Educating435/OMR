from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, require_roles
from app.models import Exam, ExamTemplate, User, UserRole
from app.schemas.exam import TemplateRead
from app.services.omr.pdf_generator import generate_template_geometry, render_exam_template_pdf
from app.services.omr.qr_payload import build_qr_payload
from app.services.storage.local import LocalStorageService


router = APIRouter(prefix="/templates")


@router.post("/{exam_id}", response_model=TemplateRead, status_code=status.HTTP_201_CREATED)
def generate_template(
    exam_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPER_ADMIN)),
) -> ExamTemplate:
    exam = db.get(Exam, exam_id)
    if exam is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")

    revision = len(exam.templates) + 1
    geometry = generate_template_geometry(exam.total_questions, exam.options_per_question)
    qr_payload = build_qr_payload(exam_id=exam.id, revision=revision, questions=exam.total_questions)

    storage = LocalStorageService()
    file_name = f"template-{exam.id}-r{revision}.pdf"
    relative_path = Path("templates") / file_name
    absolute_path = storage.resolve(relative_path)
    absolute_path.parent.mkdir(parents=True, exist_ok=True)
    render_exam_template_pdf(exam, qr_payload, geometry, absolute_path)

    template = ExamTemplate(
        exam_id=exam.id,
        revision=revision,
        pdf_path=str(relative_path),
        qr_payload=qr_payload,
        geometry_json=geometry,
    )
    db.add(template)
    db.commit()
    db.refresh(template)
    return template


@router.get("/{exam_id}", response_model=list[TemplateRead])
def list_templates(
    exam_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[ExamTemplate]:
    del current_user
    return db.query(ExamTemplate).filter(ExamTemplate.exam_id == exam_id).order_by(ExamTemplate.revision.desc()).all()
