from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.exam import Exam, ExamTemplate
from app.modules.audit_logs.service import AuditLogService
from app.modules.pdf_generation.service import OMRPdfService
from app.storage.local import LocalStorageProvider


class TemplateService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.audit = AuditLogService(db)
        self.storage = LocalStorageProvider()
        self.pdf_service = OMRPdfService()

    def list_templates(self, exam_id: str | None = None) -> list[ExamTemplate]:
        statement = select(ExamTemplate).order_by(ExamTemplate.created_at.desc())
        if exam_id:
            statement = statement.where(ExamTemplate.exam_id == exam_id)
        return list(self.db.scalars(statement))

    def generate_template(self, exam_id: str, actor_id: str | None) -> ExamTemplate:
        exam = self.db.get(Exam, exam_id)
        if exam is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")

        existing_count = self.db.scalar(
            select(func.count(ExamTemplate.id)).where(ExamTemplate.exam_id == exam_id)
        )
        template_version = (existing_count or 0) + 1
        template_code = f"EXAM-{exam_id[:8]}-V{template_version}"
        pdf_bytes, metadata = self.pdf_service.build_template_document(exam.id, template_code, exam.total_questions)
        relative_path = f"templates/{exam.id}/{template_code}.pdf"
        pdf_path = self.storage.save_bytes(relative_path, pdf_bytes)

        template = ExamTemplate(
            exam_id=exam.id,
            template_code=template_code,
            template_version=template_version,
            qr_payload=metadata["qr_payload"],
            marker_layout=metadata["layout"]["markers"],
            bubble_layout=metadata["layout"],
            pdf_storage_path=pdf_path,
            is_official=True,
        )
        self.db.add(template)
        self.db.flush()
        self.audit.log(
            actor_user_id=actor_id,
            action="template.generated",
            entity_type="exam_template",
            entity_id=template.id,
            description=f"Generated A4 OMR template {template.template_code}",
        )
        self.db.commit()
        self.db.refresh(template)
        return template
