from app.models.entities import (
    AnswerKey,
    AuditLog,
    Exam,
    ExamSet,
    Export,
    OMRResponse,
    OMRResult,
    OMRTemplate,
    Organization,
    ReviewFlag,
    Role,
    ScanImage,
    ScanSession,
    Student,
    TemplateVersion,
    User,
    UserRole,
)

ExamTemplate = TemplateVersion
ResultAttempt = OMRResult

__all__ = [
    "Organization",
    "Role",
    "User",
    "UserRole",
    "Exam",
    "ExamSet",
    "AnswerKey",
    "OMRTemplate",
    "TemplateVersion",
    "ExamTemplate",
    "Student",
    "ScanSession",
    "ScanImage",
    "OMRResult",
    "ResultAttempt",
    "OMRResponse",
    "ReviewFlag",
    "Export",
    "AuditLog",
]
