from datetime import date, datetime
from uuid import uuid4

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.database.base import Base


class Exam(Base):
    __tablename__ = "omr_exams"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    title: Mapped[str] = mapped_column(String(255))
    subject: Mapped[str] = mapped_column(String(120))
    exam_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    total_questions: Mapped[int] = mapped_column(Integer, default=50)
    options_per_question: Mapped[int] = mapped_column(Integer, default=4)
    roll_number_digits: Mapped[int] = mapped_column(Integer, default=6)
    supported_set_codes: Mapped[list[str]] = mapped_column(JSON, default=lambda: ["A", "B", "C", "D"])
    positive_marks: Mapped[float] = mapped_column(Float, default=1.0)
    negative_marks: Mapped[float] = mapped_column(Float, default=0.0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_by: Mapped[str | None] = mapped_column(ForeignKey("omr_users.id"), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    answer_keys: Mapped[list["AnswerKeyItem"]] = relationship(back_populates="exam", cascade="all, delete-orphan")
    templates: Mapped[list["ExamTemplate"]] = relationship(back_populates="exam", cascade="all, delete-orphan")
    results: Mapped[list["Result"]] = relationship(back_populates="exam")


class AnswerKeyItem(Base):
    __tablename__ = "omr_answer_keys"
    __table_args__ = (UniqueConstraint("exam_id", "set_code", "question_number", name="uq_exam_set_question"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    exam_id: Mapped[str] = mapped_column(ForeignKey("omr_exams.id"), index=True)
    set_code: Mapped[str] = mapped_column(String(1), index=True)
    question_number: Mapped[int] = mapped_column(Integer)
    correct_option: Mapped[str] = mapped_column(String(1))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    exam: Mapped["Exam"] = relationship(back_populates="answer_keys")


class ExamTemplate(Base):
    __tablename__ = "omr_exam_templates"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    exam_id: Mapped[str] = mapped_column(ForeignKey("omr_exams.id"), index=True)
    template_code: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    template_version: Mapped[int] = mapped_column(Integer, default=1)
    qr_payload: Mapped[dict] = mapped_column(JSON, default=dict)
    marker_layout: Mapped[dict] = mapped_column(JSON, default=dict)
    bubble_layout: Mapped[dict] = mapped_column(JSON, default=dict)
    pdf_storage_path: Mapped[str] = mapped_column(String(500))
    preview_image_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_official: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    exam: Mapped["Exam"] = relationship(back_populates="templates")
    results: Mapped[list["Result"]] = relationship(back_populates="template")


from app.models.result import Result  # noqa: E402
