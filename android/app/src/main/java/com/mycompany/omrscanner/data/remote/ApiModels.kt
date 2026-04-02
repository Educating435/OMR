package com.mycompany.omrscanner.data.remote

import kotlinx.serialization.Serializable

@Serializable
data class LoginRequestDto(
    val email: String,
    val password: String,
)

@Serializable
data class RefreshRequestDto(
    val refresh_token: String,
)

@Serializable
data class TokenResponseDto(
    val access_token: String,
    val refresh_token: String,
    val user_role: String,
)

@Serializable
data class PaginatedResponseDto<T>(
    val items: List<T>,
)

@Serializable
data class ExamDto(
    val id: String,
    val title: String,
    val subject: String,
    val total_questions: Int,
)

@Serializable
data class TemplateDto(
    val id: String,
    val exam_id: String,
    val revision: Int,
    val qr_payload: Map<String, String> = emptyMap(),
    val geometry_json: Map<String, String> = emptyMap(),
)

@Serializable
data class ScanSubmissionRequest(
    val exam_id: String,
    val template_id: String,
    val student_identifier: String,
    val local_attempt_uuid: String,
    val score: Float,
    val max_score: Float,
    val responses: Map<String, String?>,
    val grading_summary: Map<String, Int>,
    val image_path: String? = null,
)

@Serializable
data class ReviewItemDto(
    val id: String,
    val student_identifier: String,
    val score: Float,
    val max_score: Float,
    val needs_review: Boolean,
    val review_status: String,
)
