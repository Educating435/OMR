from datetime import datetime

from pydantic import BaseModel


class GenerateTemplateRequest(BaseModel):
    exam_id: str


class TemplateResponse(BaseModel):
    id: str
    exam_id: str
    template_code: str
    template_version: int
    qr_payload: dict
    marker_layout: dict
    bubble_layout: dict
    pdf_storage_path: str
    is_official: bool
    created_at: datetime
