"""initial mysql schema

Revision ID: 20260402_01
Revises:
Create Date: 2026-04-02 22:20:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260402_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "omr_users",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=30), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_omr_users_email", "omr_users", ["email"], unique=True)

    op.create_table(
        "omr_exams",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("subject", sa.String(length=120), nullable=False),
        sa.Column("exam_date", sa.Date(), nullable=True),
        sa.Column("total_questions", sa.Integer(), nullable=False),
        sa.Column("options_per_question", sa.Integer(), nullable=False),
        sa.Column("roll_number_digits", sa.Integer(), nullable=False),
        sa.Column("supported_set_codes", sa.JSON(), nullable=False),
        sa.Column("positive_marks", sa.Float(), nullable=False),
        sa.Column("negative_marks", sa.Float(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_by", sa.String(length=36), sa.ForeignKey("omr_users.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "omr_answer_keys",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("exam_id", sa.String(length=36), sa.ForeignKey("omr_exams.id"), nullable=False),
        sa.Column("set_code", sa.String(length=1), nullable=False),
        sa.Column("question_number", sa.Integer(), nullable=False),
        sa.Column("correct_option", sa.String(length=1), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("exam_id", "set_code", "question_number", name="uq_exam_set_question"),
    )

    op.create_table(
        "omr_exam_templates",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("exam_id", sa.String(length=36), sa.ForeignKey("omr_exams.id"), nullable=False),
        sa.Column("template_code", sa.String(length=80), nullable=False),
        sa.Column("template_version", sa.Integer(), nullable=False),
        sa.Column("qr_payload", sa.JSON(), nullable=False),
        sa.Column("marker_layout", sa.JSON(), nullable=False),
        sa.Column("bubble_layout", sa.JSON(), nullable=False),
        sa.Column("pdf_storage_path", sa.String(length=500), nullable=False),
        sa.Column("preview_image_path", sa.String(length=500), nullable=True),
        sa.Column("is_official", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_omr_exam_templates_template_code", "omr_exam_templates", ["template_code"], unique=True)

    op.create_table(
        "omr_results",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("exam_id", sa.String(length=36), sa.ForeignKey("omr_exams.id"), nullable=False),
        sa.Column("template_id", sa.String(length=36), sa.ForeignKey("omr_exam_templates.id"), nullable=False),
        sa.Column("scanned_by_user_id", sa.String(length=36), sa.ForeignKey("omr_users.id"), nullable=True),
        sa.Column("roll_number", sa.String(length=20), nullable=False),
        sa.Column("set_code", sa.String(length=1), nullable=False),
        sa.Column("local_attempt_id", sa.String(length=80), nullable=False),
        sa.Column("captured_at", sa.DateTime(), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("max_score", sa.Float(), nullable=False),
        sa.Column("correct_count", sa.Integer(), nullable=False),
        sa.Column("wrong_count", sa.Integer(), nullable=False),
        sa.Column("unattempted_count", sa.Integer(), nullable=False),
        sa.Column("needs_review", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("sync_status", sa.String(length=20), nullable=False),
        sa.Column("scan_image_path", sa.String(length=500), nullable=True),
        sa.Column("processing_summary", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("exam_id", "roll_number", "local_attempt_id", name="uq_exam_roll_attempt"),
    )

    op.create_table(
        "omr_result_responses",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("result_id", sa.String(length=36), sa.ForeignKey("omr_results.id"), nullable=False),
        sa.Column("question_number", sa.Integer(), nullable=False),
        sa.Column("selected_option", sa.String(length=1), nullable=True),
        sa.Column("correct_option", sa.String(length=1), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.UniqueConstraint("result_id", "question_number", name="uq_result_response_question"),
    )

    op.create_table(
        "omr_review_flags",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("result_id", sa.String(length=36), sa.ForeignKey("omr_results.id"), nullable=False),
        sa.Column("flag_type", sa.String(length=80), nullable=False),
        sa.Column("question_number", sa.Integer(), nullable=True),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("resolved", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "omr_audit_logs",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("actor_user_id", sa.String(length=36), sa.ForeignKey("omr_users.id"), nullable=True),
        sa.Column("action", sa.String(length=100), nullable=False),
        sa.Column("entity_type", sa.String(length=100), nullable=False),
        sa.Column("entity_id", sa.String(length=36), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_index("ix_omr_answer_keys_exam_id", "omr_answer_keys", ["exam_id"], unique=False)
    op.create_index("ix_omr_answer_keys_set_code", "omr_answer_keys", ["set_code"], unique=False)
    op.create_index("ix_omr_audit_logs_actor_user_id", "omr_audit_logs", ["actor_user_id"], unique=False)
    op.create_index("ix_omr_audit_logs_action", "omr_audit_logs", ["action"], unique=False)
    op.create_index("ix_omr_audit_logs_entity_id", "omr_audit_logs", ["entity_id"], unique=False)
    op.create_index("ix_omr_audit_logs_entity_type", "omr_audit_logs", ["entity_type"], unique=False)
    op.create_index("ix_omr_exam_templates_exam_id", "omr_exam_templates", ["exam_id"], unique=False)
    op.create_index("ix_omr_results_exam_id", "omr_results", ["exam_id"], unique=False)
    op.create_index("ix_omr_results_local_attempt_id", "omr_results", ["local_attempt_id"], unique=False)
    op.create_index("ix_omr_results_roll_number", "omr_results", ["roll_number"], unique=False)
    op.create_index("ix_omr_results_scanned_by_user_id", "omr_results", ["scanned_by_user_id"], unique=False)
    op.create_index("ix_omr_results_template_id", "omr_results", ["template_id"], unique=False)
    op.create_index("ix_omr_review_flags_result_id", "omr_review_flags", ["result_id"], unique=False)
    op.create_index("ix_omr_result_responses_result_id", "omr_result_responses", ["result_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_omr_result_responses_result_id", table_name="omr_result_responses")
    op.drop_index("ix_omr_review_flags_result_id", table_name="omr_review_flags")
    op.drop_index("ix_omr_results_template_id", table_name="omr_results")
    op.drop_index("ix_omr_results_scanned_by_user_id", table_name="omr_results")
    op.drop_index("ix_omr_results_roll_number", table_name="omr_results")
    op.drop_index("ix_omr_results_local_attempt_id", table_name="omr_results")
    op.drop_index("ix_omr_results_exam_id", table_name="omr_results")
    op.drop_index("ix_omr_exam_templates_exam_id", table_name="omr_exam_templates")
    op.drop_index("ix_omr_audit_logs_entity_type", table_name="omr_audit_logs")
    op.drop_index("ix_omr_audit_logs_entity_id", table_name="omr_audit_logs")
    op.drop_index("ix_omr_audit_logs_action", table_name="omr_audit_logs")
    op.drop_index("ix_omr_audit_logs_actor_user_id", table_name="omr_audit_logs")
    op.drop_index("ix_omr_answer_keys_set_code", table_name="omr_answer_keys")
    op.drop_index("ix_omr_answer_keys_exam_id", table_name="omr_answer_keys")
    op.drop_index("ix_omr_exam_templates_template_code", table_name="omr_exam_templates")
    op.drop_index("ix_omr_users_email", table_name="omr_users")
    op.drop_table("omr_audit_logs")
    op.drop_table("omr_review_flags")
    op.drop_table("omr_result_responses")
    op.drop_table("omr_results")
    op.drop_table("omr_exam_templates")
    op.drop_table("omr_answer_keys")
    op.drop_table("omr_exams")
    op.drop_table("omr_users")
