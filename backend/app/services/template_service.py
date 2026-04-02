from pathlib import Path

from fastapi import HTTPException, status

from app.core.storage import StorageManager
from app.models import ExamTemplate, OMRTemplate
from app.repositories.audit_repository import AuditRepository
from app.repositories.exam_repository import ExamRepository
from app.services.pdf_service import PdfService
from app.services.omr.pdf_generator import resolve_template_spec


class TemplateService:
    def __init__(
        self,
        repository: ExamRepository,
        pdf_service: PdfService,
        storage: StorageManager,
        audit_repository: AuditRepository | None = None,
    ) -> None:
        self.repository = repository
        self.pdf_service = pdf_service
        self.storage = storage
        self.audit_repository = audit_repository

    def create_template(self, exam_id: str) -> ExamTemplate:
        exam = self.repository.get_exam(exam_id)
        if exam is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")
        spec = resolve_template_spec(exam)
        template_master = self.repository.get_template_master(exam.id, spec.key)
        if template_master is None:
            template_master = self.repository.create_template_master(
                OMRTemplate(
                    exam_id=exam.id,
                    template_code=spec.key,
                    is_active=True,
                )
            )

        revision = len(exam.templates) + 1
        relative_path = Path("templates") / f"{spec.key}-{exam.id}-r{revision}.pdf"
        output_path = self.storage.resolve(relative_path)
        geometry, qr_payload = self.pdf_service.generate_exam_pdf(exam, revision, output_path, template_code=template_master.template_code)
        template = ExamTemplate(
            exam_id=exam.id,
            omr_template_id=template_master.id,
            revision=revision,
            page_width_px=geometry["page"]["width_px"],
            page_height_px=geometry["page"]["height_px"],
            marker_spec_json=geometry["marker_spec_json"],
            pdf_path=str(relative_path),
            qr_payload=qr_payload,
            geometry_json=geometry,
            is_active=True,
        )
        created = self.repository.create_template(template)
        if self.audit_repository is not None:
            from app.services.audit_service import AuditService

            AuditService(self.audit_repository).log(exam.owner_id, "create_template", "template_version", created.id, {"exam_id": exam.id})
        return created

    def list_templates(self, exam_id: str) -> list[ExamTemplate]:
        return self.repository.list_templates(exam_id)
