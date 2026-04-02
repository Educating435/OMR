package com.mycompany.omrscanner.data.remote

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.JsonObject

@Serializable
data class LoginRequestDto(
    val email: String,
    val password: String,
)

@Serializable
data class LoginResponseDto(
    @SerialName("access_token") val accessToken: String,
    val role: String,
    @SerialName("user_id") val userId: String,
)

@Serializable
data class ExamDto(
    val id: String,
    val title: String,
    val subject: String,
    @SerialName("total_questions") val totalQuestions: Int,
    @SerialName("supported_set_codes") val supportedSetCodes: List<String>,
    @SerialName("roll_number_digits") val rollNumberDigits: Int,
)

@Serializable
data class TemplateDto(
    val id: String,
    @SerialName("exam_id") val examId: String,
    @SerialName("template_code") val templateCode: String,
    @SerialName("bubble_layout") val bubbleLayout: JsonObject,
    @SerialName("qr_payload") val qrPayload: JsonObject,
)

@Serializable
data class SyncResultRequestDto(
    @SerialName("exam_id") val examId: String,
    @SerialName("template_id") val templateId: String,
    @SerialName("roll_number") val rollNumber: String,
    @SerialName("set_code") val setCode: String,
    @SerialName("local_attempt_id") val localAttemptId: String,
    @SerialName("captured_at") val capturedAt: String,
    val score: Double,
    @SerialName("max_score") val maxScore: Double,
    @SerialName("correct_count") val correctCount: Int,
    @SerialName("wrong_count") val wrongCount: Int,
    @SerialName("unattempted_count") val unattemptedCount: Int,
    @SerialName("needs_review") val needsReview: Boolean,
    @SerialName("processing_summary") val processingSummary: Map<String, String>,
    val responses: List<SyncResponseDto>,
    @SerialName("review_flags") val reviewFlags: List<SyncFlagDto>,
)

@Serializable
data class SyncResponseDto(
    @SerialName("question_number") val questionNumber: Int,
    @SerialName("selected_option") val selectedOption: String? = null,
    @SerialName("correct_option") val correctOption: String? = null,
    val status: String,
    val confidence: Double,
)

@Serializable
data class SyncFlagDto(
    @SerialName("flag_type") val flagType: String,
    @SerialName("question_number") val questionNumber: Int? = null,
    val message: String,
)
