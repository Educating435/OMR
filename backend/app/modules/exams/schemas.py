from datetime import date, datetime

from pydantic import BaseModel, Field


class ExamCreate(BaseModel):
    title: str
    subject: str
    exam_date: date | None = None
    total_questions: int = 50
    options_per_question: int = 4
    roll_number_digits: int = 6
    supported_set_codes: list[str] = Field(default_factory=lambda: ["A", "B", "C", "D"])
    positive_marks: float = 1.0
    negative_marks: float = 0.0


class ExamResponse(BaseModel):
    id: str
    title: str
    subject: str
    exam_date: date | None
    total_questions: int
    options_per_question: int
    roll_number_digits: int
    supported_set_codes: list[str]
    positive_marks: float
    negative_marks: float
    is_active: bool
    created_at: datetime


class ExamDetailResponse(ExamResponse):
    template_count: int
    result_count: int
