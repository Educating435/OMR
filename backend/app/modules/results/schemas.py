from datetime import datetime

from pydantic import BaseModel, Field


class ResultResponseItem(BaseModel):
    question_number: int
    selected_option: str | None = None
    correct_option: str | None = None
    status: str = "detected"
    confidence: float = 0.0


class ReviewFlagItem(BaseModel):
    flag_type: str
    question_number: int | None = None
    message: str


class ResultSyncRequest(BaseModel):
    exam_id: str
    template_id: str
    roll_number: str
    set_code: str
    local_attempt_id: str
    captured_at: datetime
    score: float
    max_score: float
    correct_count: int
    wrong_count: int
    unattempted_count: int
    needs_review: bool = False
    processing_summary: dict = Field(default_factory=dict)
    responses: list[ResultResponseItem] = Field(default_factory=list)
    review_flags: list[ReviewFlagItem] = Field(default_factory=list)


class ResultResponse(BaseModel):
    id: str
    exam_id: str
    template_id: str
    roll_number: str
    set_code: str
    local_attempt_id: str
    score: float
    max_score: float
    correct_count: int
    wrong_count: int
    unattempted_count: int
    needs_review: bool
    sync_status: str
    created_at: datetime
