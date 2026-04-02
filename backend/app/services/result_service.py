from fastapi import HTTPException, status

from app.models import ResultAttempt
from app.repositories.exam_repository import ExamRepository
from app.repositories.result_repository import ResultRepository
from app.schemas.common import PageMeta
from app.schemas.result import AnalyticsSnapshot, ResultReviewUpdate, ScanSubmission


class ResultService:
    def __init__(self, exam_repository: ExamRepository, result_repository: ResultRepository) -> None:
        self.exam_repository = exam_repository
        self.result_repository = result_repository

    def submit_scan(self, payload: ScanSubmission) -> ResultAttempt:
        existing = self.result_repository.get_by_local_attempt_uuid(payload.local_attempt_uuid)
        if existing:
            return existing
        summary = payload.grading_summary
        needs_review = bool(summary.get("uncertain", 0)) or bool(summary.get("multiple_marked", 0))
        attempt = ResultAttempt(**payload.model_dump(), needs_review=needs_review)
        return self.result_repository.create(attempt)

    def list_results(self, exam_id: str, page: int, page_size: int) -> tuple[list[ResultAttempt], PageMeta]:
        exam = self.exam_repository.get_exam(exam_id)
        if exam is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")
        offset = (page - 1) * page_size
        items = self.exam_repository.list_results(exam_id, offset=offset, limit=page_size)
        total = self.exam_repository.count_results(exam_id)
        return items, PageMeta(page=page, page_size=page_size, total=total)

    def flagged_results(self) -> list[ResultAttempt]:
        return self.result_repository.flagged()

    def review_result(self, attempt_id: str, payload: ResultReviewUpdate, reviewer_id: str) -> ResultAttempt:
        attempt = self.result_repository.get(attempt_id)
        if attempt is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attempt not found")
        attempt.needs_review = payload.needs_review
        attempt.review_status = payload.review_status
        attempt.remarks = payload.remarks
        attempt.reviewed_by = reviewer_id
        return self.result_repository.save(attempt)

    def analytics(self) -> AnalyticsSnapshot:
        total_exams, total_attempts, flagged_attempts, average_score = self.result_repository.analytics_summary()
        return AnalyticsSnapshot(
            total_exams=total_exams,
            total_attempts=total_attempts,
            flagged_attempts=flagged_attempts,
            average_score=round(average_score, 2),
        )

    def list_all_results(self, page: int, page_size: int) -> tuple[list[ResultAttempt], PageMeta]:
        offset = (page - 1) * page_size
        items = self.result_repository.list(offset=offset, limit=page_size)
        total = self.result_repository.count()
        return items, PageMeta(page=page, page_size=page_size, total=total)

    def get_result(self, result_id: str) -> ResultAttempt:
        attempt = self.result_repository.get(result_id)
        if attempt is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Result not found")
        return attempt
