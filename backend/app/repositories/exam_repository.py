from sqlalchemy.orm import Session

from app.models import AnswerKey, Exam, ExamTemplate, OMRTemplate, ResultAttempt


class ExamRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_exams(self, offset: int, limit: int) -> list[Exam]:
        return self.db.query(Exam).order_by(Exam.created_at.desc()).offset(offset).limit(limit).all()

    def count_exams(self) -> int:
        return self.db.query(Exam).count()

    def get_exam(self, exam_id: str) -> Exam | None:
        return self.db.get(Exam, exam_id)

    def create_exam(self, exam: Exam) -> Exam:
        self.db.add(exam)
        self.db.commit()
        self.db.refresh(exam)
        return exam

    def save_exam(self, exam: Exam) -> Exam:
        self.db.add(exam)
        self.db.commit()
        self.db.refresh(exam)
        return exam

    def delete_exam(self, exam: Exam) -> None:
        self.db.delete(exam)
        self.db.commit()

    def create_template(self, template: ExamTemplate) -> ExamTemplate:
        self.db.add(template)
        self.db.commit()
        self.db.refresh(template)
        return template

    def get_template_master(self, exam_id: str, template_code: str) -> OMRTemplate | None:
        return (
            self.db.query(OMRTemplate)
            .filter(OMRTemplate.exam_id == exam_id, OMRTemplate.template_code == template_code)
            .first()
        )

    def create_template_master(self, template: OMRTemplate) -> OMRTemplate:
        self.db.add(template)
        self.db.commit()
        self.db.refresh(template)
        return template

    def list_templates(self, exam_id: str) -> list[ExamTemplate]:
        return self.db.query(ExamTemplate).filter(ExamTemplate.exam_id == exam_id).order_by(ExamTemplate.revision.desc()).all()

    def list_all_templates(self, offset: int, limit: int) -> list[ExamTemplate]:
        return self.db.query(ExamTemplate).order_by(ExamTemplate.created_at.desc()).offset(offset).limit(limit).all()

    def count_templates(self) -> int:
        return self.db.query(ExamTemplate).count()

    def get_template(self, template_id: str) -> ExamTemplate | None:
        return self.db.get(ExamTemplate, template_id)

    def list_results(self, exam_id: str, offset: int, limit: int) -> list[ResultAttempt]:
        return self.db.query(ResultAttempt).filter(ResultAttempt.exam_id == exam_id).order_by(ResultAttempt.created_at.desc()).offset(offset).limit(limit).all()

    def count_results(self, exam_id: str) -> int:
        return self.db.query(ResultAttempt).filter(ResultAttempt.exam_id == exam_id).count()

    def replace_answer_keys(self, exam_id: str, items: list[AnswerKey]) -> list[AnswerKey]:
        self.db.query(AnswerKey).filter(AnswerKey.exam_id == exam_id).delete()
        for item in items:
            self.db.add(item)
        self.db.commit()
        return self.db.query(AnswerKey).filter(AnswerKey.exam_id == exam_id).order_by(AnswerKey.question_no.asc()).all()

    def list_answer_keys(self, exam_id: str) -> list[AnswerKey]:
        return self.db.query(AnswerKey).filter(AnswerKey.exam_id == exam_id).order_by(AnswerKey.question_no.asc()).all()
