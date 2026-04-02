import enum
import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.core.database import Base


JSONType = JSONB().with_variant(JSON(), "sqlite")


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class UserRole(str, enum.Enum):
    SUPER_ADMIN = "super_admin"
    STAFF = "staff"
    VIEWER = "viewer"


class ExamStatus(str, enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"


class ResultStatus(str, enum.Enum):
    PROCESSED = "processed"
    FLAGGED = "flagged"
    REVIEWED = "reviewed"
    SYNCED = "synced"


class Organization(TimestampMixin, Base):
    __tablename__ = "organizations"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    code: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    users: Mapped[list["User"]] = relationship(back_populates="organization")
    exams: Mapped[list["Exam"]] = relationship(back_populates="organization")


class Role(TimestampMixin, Base):
    __tablename__ = "roles"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    users: Mapped[list["User"]] = relationship(back_populates="role_record")


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id: Mapped[str | None] = mapped_column(ForeignKey("organizations.id"), nullable=True, index=True)
    role_id: Mapped[str | None] = mapped_column(ForeignKey("roles.id"), nullable=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column("password_hash", String(255))
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.SUPER_ADMIN)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    organization: Mapped["Organization | None"] = relationship(back_populates="users")
    role_record: Mapped["Role | None"] = relationship(back_populates="users")
    exams: Mapped[list["Exam"]] = relationship(back_populates="owner")
    scan_sessions: Mapped[list["ScanSession"]] = relationship(back_populates="operator")
    scanned_results: Mapped[list["OMRResult"]] = relationship(
        back_populates="scanner",
        foreign_keys="OMRResult.scanner_user_id",
    )
    reviewed_flags: Mapped[list["ReviewFlag"]] = relationship(back_populates="resolver")
    audit_logs: Mapped[list["AuditLog"]] = relationship(back_populates="actor")


class Exam(TimestampMixin, Base):
    __tablename__ = "exams"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id: Mapped[str | None] = mapped_column(ForeignKey("organizations.id"), nullable=True, index=True)
    owner_id: Mapped[str | None] = mapped_column("created_by", ForeignKey("users.id"), nullable=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    subject: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    total_questions: Mapped[int] = mapped_column(Integer)
    options_per_question: Mapped[int] = mapped_column("options_count", Integer, default=4)
    negative_marking_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    negative_marks: Mapped[float] = mapped_column("negative_marks_per_wrong", Float, default=0)
    positive_marks: Mapped[float] = mapped_column("positive_marks_per_correct", Float, default=1)
    status: Mapped[ExamStatus] = mapped_column(Enum(ExamStatus), default=ExamStatus.DRAFT)
    answer_key: Mapped[dict] = mapped_column(JSONType, default=dict)
    metadata_json: Mapped[dict] = mapped_column(JSONType, default=dict)

    organization: Mapped["Organization | None"] = relationship(back_populates="exams")
    owner: Mapped["User | None"] = relationship(back_populates="exams")
    exam_sets: Mapped[list["ExamSet"]] = relationship(back_populates="exam")
    answer_keys: Mapped[list["AnswerKey"]] = relationship(back_populates="exam")
    omr_templates: Mapped[list["OMRTemplate"]] = relationship(back_populates="exam")
    templates: Mapped[list["TemplateVersion"]] = relationship(back_populates="exam")
    results: Mapped[list["OMRResult"]] = relationship(back_populates="exam")
    scan_sessions: Mapped[list["ScanSession"]] = relationship(back_populates="exam")


class ExamSet(Base):
    __tablename__ = "exam_sets"
    __table_args__ = (UniqueConstraint("exam_id", "set_code", name="uq_exam_set_exam_code"),)

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    exam_id: Mapped[str] = mapped_column(ForeignKey("exams.id"), index=True)
    set_code: Mapped[str] = mapped_column(String(32), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    exam: Mapped["Exam"] = relationship(back_populates="exam_sets")
    answer_keys: Mapped[list["AnswerKey"]] = relationship()


class AnswerKey(Base):
    __tablename__ = "answer_keys"
    __table_args__ = (UniqueConstraint("exam_id", "set_code", "question_no", name="uq_answer_key_question"),)

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    exam_id: Mapped[str] = mapped_column(ForeignKey("exams.id"), index=True)
    set_code: Mapped[str] = mapped_column(String(32), index=True)
    question_no: Mapped[int] = mapped_column(Integer)
    correct_option: Mapped[str] = mapped_column(String(8))

    exam: Mapped["Exam"] = relationship(back_populates="answer_keys")


class OMRTemplate(TimestampMixin, Base):
    __tablename__ = "omr_templates"
    __table_args__ = (UniqueConstraint("exam_id", "template_id", name="uq_template_exam_code"),)

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    exam_id: Mapped[str] = mapped_column(ForeignKey("exams.id"), index=True)
    template_code: Mapped[str] = mapped_column("template_id", String(128), index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    exam: Mapped["Exam"] = relationship(back_populates="omr_templates")
    versions: Mapped[list["TemplateVersion"]] = relationship(back_populates="template")


class TemplateVersion(TimestampMixin, Base):
    __tablename__ = "template_versions"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    exam_id: Mapped[str] = mapped_column(ForeignKey("exams.id"), index=True)
    omr_template_id: Mapped[str | None] = mapped_column(ForeignKey("omr_templates.id"), nullable=True, index=True)
    revision: Mapped[int] = mapped_column("version", Integer, default=1)
    page_width_px: Mapped[int] = mapped_column(Integer, default=2480)
    page_height_px: Mapped[int] = mapped_column(Integer, default=3508)
    marker_spec_json: Mapped[dict] = mapped_column(JSONType, default=dict)
    geometry_json: Mapped[dict] = mapped_column("layout_json", JSONType, default=dict)
    qr_payload: Mapped[dict] = mapped_column("qr_payload_schema_json", JSONType, default=dict)
    pdf_path: Mapped[str] = mapped_column(String(500))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    exam: Mapped["Exam"] = relationship(back_populates="templates")
    template: Mapped["OMRTemplate | None"] = relationship(back_populates="versions")
    results: Mapped[list["OMRResult"]] = relationship(back_populates="template_version")


class Student(TimestampMixin, Base):
    __tablename__ = "students"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id: Mapped[str | None] = mapped_column(ForeignKey("organizations.id"), nullable=True, index=True)
    roll_number: Mapped[str] = mapped_column(String(64), index=True)
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    external_metadata_json: Mapped[dict] = mapped_column(JSONType, default=dict)


class ScanSession(Base):
    __tablename__ = "scan_sessions"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    exam_id: Mapped[str] = mapped_column(ForeignKey("exams.id"), index=True)
    operator_user_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    device_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    exam: Mapped["Exam"] = relationship(back_populates="scan_sessions")
    operator: Mapped["User | None"] = relationship(back_populates="scan_sessions")
    scan_images: Mapped[list["ScanImage"]] = relationship(back_populates="scan_session")
    results: Mapped[list["OMRResult"]] = relationship(back_populates="scan_session")


class ScanImage(TimestampMixin, Base):
    __tablename__ = "scan_images"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    scan_session_id: Mapped[str | None] = mapped_column(ForeignKey("scan_sessions.id"), nullable=True, index=True)
    result_id: Mapped[str | None] = mapped_column(ForeignKey("omr_results.id"), nullable=True, index=True)
    image_path: Mapped[str] = mapped_column(String(500))
    image_type: Mapped[str] = mapped_column(String(32), default="original")
    captured_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    scan_session: Mapped["ScanSession | None"] = relationship(back_populates="scan_images")
    result: Mapped["OMRResult | None"] = relationship(back_populates="scan_images")


class OMRResult(TimestampMixin, Base):
    __tablename__ = "omr_results"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    exam_id: Mapped[str] = mapped_column(ForeignKey("exams.id"), index=True)
    template_id: Mapped[str] = mapped_column(ForeignKey("template_versions.id"), index=True)
    scan_session_id: Mapped[str | None] = mapped_column(ForeignKey("scan_sessions.id"), nullable=True, index=True)
    set_code: Mapped[str | None] = mapped_column(String(32), nullable=True)
    student_identifier: Mapped[str] = mapped_column("roll_number", String(128), index=True)
    student_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    local_attempt_uuid: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    scanner_user_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    total_questions: Mapped[int] = mapped_column(Integer, default=0)
    correct_count: Mapped[int] = mapped_column(Integer, default=0)
    wrong_count: Mapped[int] = mapped_column(Integer, default=0)
    unattempted_count: Mapped[int] = mapped_column(Integer, default=0)
    invalid_count: Mapped[int] = mapped_column(Integer, default=0)
    score: Mapped[float] = mapped_column(Float, default=0)
    max_score: Mapped[float] = mapped_column(Float, default=0)
    percentage: Mapped[float] = mapped_column(Float, default=0)
    confidence: Mapped[float] = mapped_column(Float, default=0)
    status: Mapped[ResultStatus] = mapped_column(Enum(ResultStatus), default=ResultStatus.PROCESSED)
    grading_summary: Mapped[dict] = mapped_column(JSONType, default=dict)
    responses: Mapped[dict] = mapped_column(JSONType, default=dict)
    image_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    sync_source: Mapped[str] = mapped_column(String(32), default="android")
    remarks: Mapped[str | None] = mapped_column(Text, nullable=True)
    needs_review: Mapped[bool] = mapped_column(Boolean, default=False)
    review_status: Mapped[str] = mapped_column(String(32), default="pending")
    reviewed_by: Mapped[str | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    synced_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    exam: Mapped["Exam"] = relationship(back_populates="results")
    template_version: Mapped["TemplateVersion"] = relationship(back_populates="results")
    scan_session: Mapped["ScanSession | None"] = relationship(back_populates="results")
    scanner: Mapped["User | None"] = relationship(back_populates="scanned_results", foreign_keys=[scanner_user_id])
    response_rows: Mapped[list["OMRResponse"]] = relationship(back_populates="result")
    review_flags: Mapped[list["ReviewFlag"]] = relationship(back_populates="result")
    scan_images: Mapped[list["ScanImage"]] = relationship(back_populates="result")


class OMRResponse(Base):
    __tablename__ = "omr_responses"
    __table_args__ = (UniqueConstraint("result_id", "question_no", name="uq_result_question"),)

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    result_id: Mapped[str] = mapped_column(ForeignKey("omr_results.id"), index=True)
    question_no: Mapped[int] = mapped_column(Integer)
    selected_option: Mapped[str | None] = mapped_column(String(8), nullable=True)
    correct_option: Mapped[str | None] = mapped_column(String(8), nullable=True)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False)
    confidence: Mapped[float] = mapped_column(Float, default=0)
    response_status: Mapped[str] = mapped_column(String(32), default="detected")

    result: Mapped["OMRResult"] = relationship(back_populates="response_rows")


class ReviewFlag(Base):
    __tablename__ = "review_flags"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    result_id: Mapped[str] = mapped_column(ForeignKey("omr_results.id"), index=True)
    question_no: Mapped[int | None] = mapped_column(Integer, nullable=True)
    flag_type: Mapped[str] = mapped_column(String(64))
    message: Mapped[str] = mapped_column(Text)
    severity: Mapped[str] = mapped_column(String(32), default="medium")
    resolved_by: Mapped[str | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    result: Mapped["OMRResult"] = relationship(back_populates="review_flags")
    resolver: Mapped["User | None"] = relationship(back_populates="reviewed_flags")


class Export(TimestampMixin, Base):
    __tablename__ = "exports"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id: Mapped[str | None] = mapped_column(ForeignKey("organizations.id"), nullable=True, index=True)
    exam_id: Mapped[str | None] = mapped_column(ForeignKey("exams.id"), nullable=True, index=True)
    requested_by: Mapped[str | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    export_type: Mapped[str] = mapped_column(String(32), default="csv")
    status: Mapped[str] = mapped_column(String(32), default="queued")
    file_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    metadata_json: Mapped[dict] = mapped_column(JSONType, default=dict)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    actor_user_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    action: Mapped[str] = mapped_column(String(128))
    entity_type: Mapped[str] = mapped_column(String(64))
    entity_id: Mapped[str] = mapped_column(String(128), index=True)
    metadata_json: Mapped[dict] = mapped_column(JSONType, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    actor: Mapped["User | None"] = relationship(back_populates="audit_logs")
