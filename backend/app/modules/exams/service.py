from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.exam import Exam, ExamTemplate
from app.models.result import Result
from app.modules.audit_logs.service import AuditLogService
from app.modules.exams.schemas import ExamCreate


class ExamService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.audit = AuditLogService(db)

    def list_exams(self) -> list[Exam]:
        return list(self.db.scalars(select(Exam).order_by(Exam.created_at.desc())))

    def create_exam(self, payload: ExamCreate, actor_id: str | None) -> Exam:
        exam = Exam(**payload.model_dump())
        self.db.add(exam)
        self.db.flush()
        self.audit.log(
            actor_user_id=actor_id,
            action="exam.created",
            entity_type="exam",
            entity_id=exam.id,
            description=f"Created exam {exam.title}",
            payload={"subject": exam.subject},
        )
        self.db.commit()
        self.db.refresh(exam)
        return exam

    def get_exam(self, exam_id: str) -> Exam:
        exam = self.db.get(Exam, exam_id)
        if exam is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")
        return exam

    def exam_stats(self, exam_id: str) -> dict[str, int]:
        template_count = self.db.scalar(select(func.count(ExamTemplate.id)).where(ExamTemplate.exam_id == exam_id)) or 0
        result_count = self.db.scalar(select(func.count(Result.id)).where(Result.exam_id == exam_id)) or 0
        return {"template_count": template_count, "result_count": result_count}
