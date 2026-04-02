from fastapi import HTTPException, status
from sqlalchemy import Select, select
from sqlalchemy.orm import Session, joinedload

from app.models.result import Result, ResultResponse as ResultResponseModel, ReviewFlag
from app.modules.audit_logs.service import AuditLogService
from app.modules.results.schemas import ResultSyncRequest


class ResultService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.audit = AuditLogService(db)

    def list_results(self, exam_id: str | None = None, roll_number: str | None = None) -> list[Result]:
        statement: Select[tuple[Result]] = select(Result).options(joinedload(Result.review_flags)).order_by(Result.created_at.desc())
        if exam_id:
            statement = statement.where(Result.exam_id == exam_id)
        if roll_number:
            statement = statement.where(Result.roll_number == roll_number)
        return list(self.db.scalars(statement).unique())

    def sync_result(self, payload: ResultSyncRequest, actor_id: str | None) -> Result:
        existing = self.db.scalar(select(Result).where(Result.local_attempt_id == payload.local_attempt_id))
        if existing:
            return existing

        result = Result(
            exam_id=payload.exam_id,
            template_id=payload.template_id,
            scanned_by_user_id=actor_id,
            roll_number=payload.roll_number,
            set_code=payload.set_code,
            local_attempt_id=payload.local_attempt_id,
            captured_at=payload.captured_at,
            score=payload.score,
            max_score=payload.max_score,
            correct_count=payload.correct_count,
            wrong_count=payload.wrong_count,
            unattempted_count=payload.unattempted_count,
            needs_review=payload.needs_review,
            sync_status="synced",
            processing_summary=payload.processing_summary,
        )
        self.db.add(result)
        self.db.flush()

        self.db.add_all(
            [
                ResultResponseModel(result_id=result.id, **response.model_dump())
                for response in payload.responses
            ]
        )
        self.db.add_all(
            [
                ReviewFlag(result_id=result.id, **flag.model_dump())
                for flag in payload.review_flags
            ]
        )
        self.audit.log(
            actor_user_id=actor_id,
            action="result.synced",
            entity_type="result",
            entity_id=result.id,
            description=f"Synced result for roll number {result.roll_number}",
            payload={"exam_id": payload.exam_id, "local_attempt_id": payload.local_attempt_id},
        )
        self.db.commit()
        self.db.refresh(result)
        return result

    def mark_reviewed(self, result_id: str, actor_id: str | None) -> Result:
        result = self.db.get(Result, result_id)
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Result not found")
        result.needs_review = False
        self.audit.log(
            actor_user_id=actor_id,
            action="result.reviewed",
            entity_type="result",
            entity_id=result.id,
            description=f"Marked result {result.id} as reviewed",
        )
        self.db.commit()
        self.db.refresh(result)
        return result
