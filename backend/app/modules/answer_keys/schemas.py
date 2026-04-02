from pydantic import BaseModel


class AnswerKeyRow(BaseModel):
    set_code: str
    question_number: int
    correct_option: str


class AnswerKeyUpsertRequest(BaseModel):
    exam_id: str
    rows: list[AnswerKeyRow]


class AnswerKeyResponse(AnswerKeyRow):
    id: str
    exam_id: str
