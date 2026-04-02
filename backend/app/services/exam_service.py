from fastapi import HTTPException, status

from app.models import AnswerKey, Exam
from app.repositories.audit_repository import AuditRepository
from app.repositories.exam_repository import ExamRepository
from app.schemas.common import PageMeta
from app.schemas.exam import AnswerKeyUpdate, ExamCreate, ExamUpdate


class ExamService:
    def __init__(self, repository: ExamRepository, audit_repository: AuditRepository | None = None) -> None:
        self.repository = repository
        self.audit_repository = audit_repository

    def list_exams(self, page: int, page_size: int) -> tuple[list[Exam], PageMeta]:
        offset = (page - 1) * page_size
        items = self.repository.list_exams(offset=offset, limit=page_size)
        total = self.repository.count_exams()
        return items, PageMeta(page=page, page_size=page_size, total=total)

    def create_exam(self, payload: ExamCreate, owner_id: str) -> Exam:
        exam = Exam(owner_id=owner_id, description=payload.description, **payload.model_dump(exclude={"description"}))
        created = self.repository.create_exam(exam)
        if self.audit_repository is not None:
            from app.services.audit_service import AuditService

            AuditService(self.audit_repository).log(owner_id, "create_exam", "exam", created.id, {"title": created.title})
        return created

    def get_exam(self, exam_id: str) -> Exam | None:
        return self.repository.get_exam(exam_id)

    def update_exam(self, exam_id: str, payload: ExamUpdate, actor_user_id: str) -> Exam:
        exam = self.repository.get_exam(exam_id)
        if exam is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")
        for key, value in payload.model_dump().items():
            setattr(exam, "description" if key == "description" else key, value)
        updated = self.repository.save_exam(exam)
        if self.audit_repository is not None:
            from app.services.audit_service import AuditService

            AuditService(self.audit_repository).log(actor_user_id, "update_exam", "exam", updated.id, {"title": updated.title})
        return updated

    def delete_exam(self, exam_id: str, actor_user_id: str) -> None:
        exam = self.repository.get_exam(exam_id)
        if exam is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")
        self.repository.delete_exam(exam)
        if self.audit_repository is not None:
            from app.services.audit_service import AuditService

            AuditService(self.audit_repository).log(actor_user_id, "delete_exam", "exam", exam_id, {})

    def get_answer_keys(self, exam_id: str) -> list[AnswerKey]:
        exam = self.repository.get_exam(exam_id)
        if exam is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")
        return self.repository.list_answer_keys(exam_id)

    def replace_answer_keys(self, exam_id: str, payload: AnswerKeyUpdate, actor_user_id: str) -> list[AnswerKey]:
        exam = self.repository.get_exam(exam_id)
        if exam is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")
        answer_key_json = {str(item.question_no): item.correct_option for item in payload.items}
        exam.answer_key = answer_key_json
        self.repository.save_exam(exam)
        items = [
            AnswerKey(
                exam_id=exam_id,
                set_code=item.set_code,
                question_no=item.question_no,
                correct_option=item.correct_option,
            )
            for item in payload.items
        ]
        saved = self.repository.replace_answer_keys(exam_id, items)
        if self.audit_repository is not None:
            from app.services.audit_service import AuditService

            AuditService(self.audit_repository).log(actor_user_id, "replace_answer_keys", "exam", exam_id, {"count": len(saved)})
        return saved
