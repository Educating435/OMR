from pydantic import Field

from app.schemas.common import ORMModel


class ExamCreate(ORMModel):
    title: str
    subject: str
    description: str | None = None
    total_questions: int = Field(gt=0, le=300)
    options_per_question: int = Field(default=4, ge=2, le=6)
    positive_marks: int = 1
    negative_marks: int = 0
    answer_key: dict[str, str]


class ExamUpdate(ORMModel):
    title: str
    subject: str
    description: str | None = None
    total_questions: int = Field(gt=0, le=300)
    options_per_question: int = Field(default=4, ge=2, le=6)
    positive_marks: int = 1
    negative_marks: int = 0
    answer_key: dict[str, str]


class ExamRead(ExamCreate):
    id: str


class AnswerKeyItem(ORMModel):
    question_no: int
    correct_option: str
    set_code: str = "A"


class AnswerKeyUpdate(ORMModel):
    items: list[AnswerKeyItem]


class TemplateGenerateRequest(ORMModel):
    exam_id: str


class TemplateRead(ORMModel):
    id: str
    exam_id: str
    revision: int
    pdf_path: str
    qr_payload: dict
    geometry_json: dict
