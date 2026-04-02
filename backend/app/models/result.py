from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.database.base import Base


class Result(Base):
    __tablename__ = "omr_results"
    __table_args__ = (UniqueConstraint("exam_id", "roll_number", "local_attempt_id", name="uq_exam_roll_attempt"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    exam_id: Mapped[str] = mapped_column(ForeignKey("omr_exams.id"), index=True)
    template_id: Mapped[str] = mapped_column(ForeignKey("omr_exam_templates.id"), index=True)
    scanned_by_user_id: Mapped[str | None] = mapped_column(ForeignKey("omr_users.id"), nullable=True, index=True)
    roll_number: Mapped[str] = mapped_column(String(20), index=True)
    set_code: Mapped[str] = mapped_column(String(1))
    local_attempt_id: Mapped[str] = mapped_column(String(80), index=True)
    captured_at: Mapped[datetime] = mapped_column(DateTime)
    score: Mapped[float] = mapped_column(Float)
    max_score: Mapped[float] = mapped_column(Float)
    correct_count: Mapped[int] = mapped_column(Integer)
    wrong_count: Mapped[int] = mapped_column(Integer)
    unattempted_count: Mapped[int] = mapped_column(Integer)
    needs_review: Mapped[bool] = mapped_column(Boolean, default=False)
    sync_status: Mapped[str] = mapped_column(String(20), default="synced")
    scan_image_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    processing_summary: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    exam: Mapped["Exam"] = relationship(back_populates="results")
    template: Mapped["ExamTemplate"] = relationship(back_populates="results")
    responses: Mapped[list["ResultResponse"]] = relationship(back_populates="result", cascade="all, delete-orphan")
    review_flags: Mapped[list["ReviewFlag"]] = relationship(back_populates="result", cascade="all, delete-orphan")


class ResultResponse(Base):
    __tablename__ = "omr_result_responses"
    __table_args__ = (UniqueConstraint("result_id", "question_number", name="uq_result_response_question"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    result_id: Mapped[str] = mapped_column(ForeignKey("omr_results.id"), index=True)
    question_number: Mapped[int] = mapped_column(Integer)
    selected_option: Mapped[str | None] = mapped_column(String(1), nullable=True)
    correct_option: Mapped[str | None] = mapped_column(String(1), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="detected")
    confidence: Mapped[float] = mapped_column(Float, default=0.0)

    result: Mapped["Result"] = relationship(back_populates="responses")


class ReviewFlag(Base):
    __tablename__ = "omr_review_flags"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    result_id: Mapped[str] = mapped_column(ForeignKey("omr_results.id"), index=True)
    flag_type: Mapped[str] = mapped_column(String(80))
    question_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    message: Mapped[str] = mapped_column(Text)
    resolved: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    result: Mapped["Result"] = relationship(back_populates="review_flags")


from app.models.exam import Exam, ExamTemplate  # noqa: E402
