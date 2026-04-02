package com.mycompany.omrscanner.domain.model

import com.mycompany.omrscanner.core.model.SyncStatus
import com.mycompany.omrscanner.core.model.UserRole
import java.util.UUID
import kotlinx.serialization.Serializable

@Serializable
data class UserSession(
    val accessToken: String,
    val refreshToken: String,
    val role: UserRole,
)

@Serializable
data class Exam(
    val id: String,
    val title: String,
    val subject: String,
    val totalQuestions: Int,
)

@Serializable
data class ExamTemplate(
    val id: String,
    val examId: String,
    val revision: Int,
    val totalQuestions: Int = 0,
    val optionsCount: Int = 4,
    val qrPayload: Map<String, String> = emptyMap(),
    val layoutJson: String = "{}",
    val answerKey: Map<String, String>,
    val positiveMarks: Int,
    val negativeMarks: Int,
)

@Serializable
data class ScanCapture(
    val template: ExamTemplate,
    val imagePath: String,
)

@Serializable
data class ScanValidation(
    val sheetFullyVisible: Boolean,
    val markersDetected: Boolean,
    val blurry: Boolean,
    val poorLighting: Boolean,
    val warnings: List<String> = emptyList(),
)

@Serializable
data class BubbleMark(
    val label: String,
    val fillScore: Float,
    val confidence: Float,
)

@Serializable
data class ResponseRead(
    val questionNo: Int,
    val selectedOption: String?,
    val status: String,
    val confidence: Float,
    val optionScores: List<BubbleMark>,
)

@Serializable
data class ParsedSheet(
    val templateId: String,
    val examId: String,
    val rollNumber: String?,
    val setCode: String?,
    val responses: List<ResponseRead>,
    val validation: ScanValidation,
)

@Serializable
data class ScanOutcome(
    val examId: String,
    val templateId: String,
    val studentIdentifier: String,
    val setCode: String? = null,
    val localAttemptUuid: String = UUID.randomUUID().toString(),
    val responses: Map<String, String?>,
    val score: Float,
    val maxScore: Float,
    val gradingSummary: Map<String, Int>,
    val confidence: Float = 0f,
    val flaggedForReview: Boolean = false,
    val originalImagePath: String? = null,
    val parsedOutputJson: String = "{}",
    val syncStatus: SyncStatus = SyncStatus.PENDING,
)

@Serializable
data class ScanReviewItem(
    val id: String,
    val studentIdentifier: String,
    val score: Float,
    val maxScore: Float,
    val needsReview: Boolean,
    val reviewStatus: String,
)
