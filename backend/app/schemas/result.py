from pydantic import Field

from app.schemas.common import ORMModel


class ScanSubmission(ORMModel):
    exam_id: str
    template_id: str
    student_identifier: str
    local_attempt_uuid: str
    score: float
    max_score: float
    responses: dict[str, str | None]
    grading_summary: dict
    image_path: str | None = None


class BulkSyncRequest(ORMModel):
    items: list[ScanSubmission]


class ResultRead(ORMModel):
    id: str
    exam_id: str
    template_id: str
    student_identifier: str
    score: float
    max_score: float
    responses: dict[str, str | None]
    grading_summary: dict
    needs_review: bool
    review_status: str


class ResultExportRow(ORMModel):
    student_identifier: str
    score: float
    max_score: float
    percentage: float = Field(ge=0, le=100)


class ResultReviewUpdate(ORMModel):
    needs_review: bool
    review_status: str
    remarks: str | None = None


class AnalyticsSnapshot(ORMModel):
    total_exams: int
    total_attempts: int
    flagged_attempts: int
    average_score: float


class MessageResponse(ORMModel):
    message: str
