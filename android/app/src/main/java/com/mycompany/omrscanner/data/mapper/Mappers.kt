package com.mycompany.omrscanner.data.mapper

import com.mycompany.omrscanner.core.model.SyncStatus
import com.mycompany.omrscanner.core.model.UserRole
import com.mycompany.omrscanner.data.local.CachedExamEntity
import com.mycompany.omrscanner.data.local.CachedTemplateEntity
import com.mycompany.omrscanner.data.local.ScanAttemptEntity
import com.mycompany.omrscanner.data.remote.ExamDto
import com.mycompany.omrscanner.data.remote.ReviewItemDto
import com.mycompany.omrscanner.data.remote.TemplateDto
import com.mycompany.omrscanner.data.remote.TokenResponseDto
import com.mycompany.omrscanner.domain.model.Exam
import com.mycompany.omrscanner.domain.model.ExamTemplate
import com.mycompany.omrscanner.domain.model.ScanOutcome
import com.mycompany.omrscanner.domain.model.ScanReviewItem
import com.mycompany.omrscanner.domain.model.UserSession
import kotlinx.serialization.json.Json

fun TokenResponseDto.toDomain(): UserSession = UserSession(
    accessToken = access_token,
    refreshToken = refresh_token,
    role = UserRole.valueOf(user_role.uppercase()),
)

fun ExamDto.toDomain(): Exam = Exam(
    id = id,
    title = title,
    subject = subject,
    totalQuestions = total_questions,
)

fun ExamDto.toCache(): CachedExamEntity = CachedExamEntity(
    id = id,
    title = title,
    subject = subject,
    totalQuestions = total_questions,
)

fun CachedExamEntity.toDomain(): Exam = Exam(
    id = id,
    title = title,
    subject = subject,
    totalQuestions = totalQuestions,
)

fun TemplateDto.toDomain(): ExamTemplate = ExamTemplate(
    id = id,
    examId = exam_id,
    revision = revision,
    totalQuestions = qr_payload["total_questions"]?.toIntOrNull() ?: 0,
    optionsCount = qr_payload["options_count"]?.toIntOrNull() ?: 4,
    qrPayload = qr_payload,
    layoutJson = Json.encodeToString(geometry_json),
    answerKey = emptyMap(),
    positiveMarks = 1,
    negativeMarks = 0,
)

fun TemplateDto.toCache(json: Json): CachedTemplateEntity = CachedTemplateEntity(
    id = id,
    examId = exam_id,
    revision = revision,
    totalQuestions = qr_payload["total_questions"]?.toIntOrNull() ?: 0,
    optionsCount = qr_payload["options_count"]?.toIntOrNull() ?: 4,
    qrPayloadJson = json.encodeToString(qr_payload),
    layoutJson = json.encodeToString(geometry_json),
    answerKeyJson = "{}",
    positiveMarks = 1,
    negativeMarks = 0,
)

fun CachedTemplateEntity.toDomain(json: Json): ExamTemplate = ExamTemplate(
    id = id,
    examId = examId,
    revision = revision,
    totalQuestions = totalQuestions,
    optionsCount = optionsCount,
    qrPayload = json.decodeFromString(qrPayloadJson),
    layoutJson = layoutJson,
    answerKey = json.decodeFromString(answerKeyJson),
    positiveMarks = positiveMarks,
    negativeMarks = negativeMarks,
)

fun ScanOutcome.toEntity(json: Json): ScanAttemptEntity = ScanAttemptEntity(
    localAttemptUuid = localAttemptUuid,
    examId = examId,
    templateId = templateId,
    studentIdentifier = studentIdentifier,
    setCode = setCode,
    score = score,
    maxScore = maxScore,
    confidence = confidence,
    responsesJson = json.encodeToString(responses),
    gradingSummaryJson = json.encodeToString(gradingSummary),
    parsedOutputJson = parsedOutputJson,
    needsReview = flaggedForReview,
    reviewStatus = if (flaggedForReview) "pending" else "clear",
    imagePath = originalImagePath,
    synced = syncStatus == SyncStatus.SYNCED,
)

fun ReviewItemDto.toDomain(): ScanReviewItem = ScanReviewItem(
    id = id,
    studentIdentifier = student_identifier,
    score = score,
    maxScore = max_score,
    needsReview = needs_review,
    reviewStatus = review_status,
)
