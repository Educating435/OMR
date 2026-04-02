from io import BytesIO

from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse, StreamingResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from app.api.deps import DBSession, get_current_user
from app.models import User
from app.repositories.exam_repository import ExamRepository
from app.schemas.result import ResultExportRow
from app.services.export_service import ExportService


router = APIRouter(prefix="/exports")


@router.get("/results.csv", response_class=PlainTextResponse)
def export_results_csv(exam_id: str, db: DBSession, current_user: User = Depends(get_current_user)) -> str:
    del current_user
    rows = ExportService(ExamRepository(db)).export_results(exam_id)
    lines = ["student_identifier,score,max_score,percentage"]
    lines.extend(f"{row.student_identifier},{row.score},{row.max_score},{row.percentage}" for row in rows)
    return "\n".join(lines)


@router.get("/results.pdf")
def export_results_pdf(exam_id: str, db: DBSession, current_user: User = Depends(get_current_user)) -> StreamingResponse:
    del current_user
    rows = ExportService(ExamRepository(db)).export_results(exam_id)
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    y = 800
    pdf.setTitle("Results Export")
    pdf.drawString(40, y, f"Results Export for Exam {exam_id}")
    y -= 30
    for row in rows[:40]:
        pdf.drawString(40, y, f"{row.student_identifier}  Score {row.score}/{row.max_score}  Percentage {row.percentage}")
        y -= 18
    pdf.save()
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="application/pdf")
