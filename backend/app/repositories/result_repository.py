from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import Exam, ResultAttempt


class ResultRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_local_attempt_uuid(self, local_attempt_uuid: str) -> ResultAttempt | None:
        return self.db.query(ResultAttempt).filter(ResultAttempt.local_attempt_uuid == local_attempt_uuid).first()

    def create(self, attempt: ResultAttempt) -> ResultAttempt:
        self.db.add(attempt)
        self.db.commit()
        self.db.refresh(attempt)
        return attempt

    def flagged(self) -> list[ResultAttempt]:
        exam_ids = self.db.query(Exam.id).subquery()
        return (
            self.db.query(ResultAttempt)
            .filter(ResultAttempt.exam_id.in_(exam_ids), ResultAttempt.needs_review.is_(True))
            .order_by(ResultAttempt.created_at.desc())
            .all()
        )

    def get(self, attempt_id: str) -> ResultAttempt | None:
        return self.db.get(ResultAttempt, attempt_id)

    def list(self, offset: int, limit: int) -> list[ResultAttempt]:
        return self.db.query(ResultAttempt).order_by(ResultAttempt.created_at.desc()).offset(offset).limit(limit).all()

    def count(self) -> int:
        return self.db.query(ResultAttempt).count()

    def save(self, attempt: ResultAttempt) -> ResultAttempt:
        self.db.add(attempt)
        self.db.commit()
        self.db.refresh(attempt)
        return attempt

    def analytics_summary(self) -> tuple[int, int, int, float]:
        total_exams = self.db.query(func.count(Exam.id)).scalar() or 0
        total_attempts = self.db.query(func.count(ResultAttempt.id)).scalar() or 0
        flagged_attempts = self.db.query(func.count(ResultAttempt.id)).filter(ResultAttempt.needs_review.is_(True)).scalar() or 0
        average_score = self.db.query(func.avg(ResultAttempt.score)).scalar() or 0
        return total_exams, total_attempts, flagged_attempts, float(average_score)
