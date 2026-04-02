from pathlib import Path

from app.models import Exam
from app.services.omr.pdf_generator import generate_template_geometry, render_exam_template_pdf, resolve_template_spec
from app.services.omr.qr_payload import build_qr_payload


class PdfService:
    def generate_exam_pdf(self, exam: Exam, revision: int, output_path: Path, template_code: str) -> tuple[dict, dict]:
        spec = resolve_template_spec(exam)
        geometry = generate_template_geometry(exam.total_questions, exam.options_per_question, exam=exam)
        qr_payload = build_qr_payload(
            template_id=template_code,
            exam_id=exam.id,
            version=revision,
            total_questions=spec.questions,
            options_count=spec.options_count,
        )
        render_exam_template_pdf(exam, qr_payload, geometry, output_path)
        return geometry, qr_payload
