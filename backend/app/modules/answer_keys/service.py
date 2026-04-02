from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models.exam import AnswerKeyItem
from app.modules.answer_keys.schemas import AnswerKeyUpsertRequest
from app.modules.audit_logs.service import AuditLogService


class AnswerKeyService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.audit = AuditLogService(db)

    def list_for_exam(self, exam_id: str) -> list[AnswerKeyItem]:
        statement = select(AnswerKeyItem).where(AnswerKeyItem.exam_id == exam_id).order_by(
            AnswerKeyItem.set_code,
            AnswerKeyItem.question_number,
        )
        return list(self.db.scalars(statement))

    def replace_for_exam(self, payload: AnswerKeyUpsertRequest, actor_id: str | None) -> list[AnswerKeyItem]:
        self.db.execute(delete(AnswerKeyItem).where(AnswerKeyItem.exam_id == payload.exam_id))
        rows = [AnswerKeyItem(exam_id=payload.exam_id, **row.model_dump()) for row in payload.rows]
        self.db.add_all(rows)
        self.audit.log(
            actor_user_id=actor_id,
            action="answer_key.replaced",
            entity_type="exam",
            entity_id=payload.exam_id,
            description=f"Uploaded {len(rows)} answer key rows",
        )
        self.db.commit()
        return self.list_for_exam(payload.exam_id)
