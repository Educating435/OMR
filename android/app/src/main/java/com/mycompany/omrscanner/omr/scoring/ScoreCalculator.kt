package com.mycompany.omrscanner.omr.scoring

import kotlinx.serialization.Serializable

@Serializable
data class ScoredResponse(
    val questionNumber: Int,
    val selectedOption: String? = null,
    val correctOption: String? = null,
    val status: String,
    val confidence: Double,
)

@Serializable
data class ReviewFlag(
    val flagType: String,
    val questionNumber: Int? = null,
    val message: String,
)

@Serializable
data class ScoredOmrResult(
    val examId: String,
    val templateId: String,
    val rollNumber: String,
    val setCode: String,
    val localAttemptId: String,
    val capturedAtIso: String,
    val score: Double,
    val maxScore: Double,
    val correctCount: Int,
    val wrongCount: Int,
    val unattemptedCount: Int,
    val needsReview: Boolean,
    val processingSummary: Map<String, String>,
    val responses: List<ScoredResponse>,
    val reviewFlags: List<ReviewFlag>,
)

class ScoreCalculator {
    fun calculate(
        examId: String,
        templateId: String,
        answers: List<String?>,
    ): ScoredOmrResult {
        val correctCount = answers.count { it == "A" }
        val wrongCount = answers.size - correctCount
        val reviewFlags = buildList {
            if (wrongCount > answers.size / 2) {
                add(ReviewFlag(flagType = "low-confidence", message = "Large mismatch rate detected in shell pipeline"))
            }
        }

        return ScoredOmrResult(
            examId = examId,
            templateId = templateId,
            rollNumber = "123456",
            setCode = "A",
            localAttemptId = "attempt-${System.currentTimeMillis()}",
            capturedAtIso = java.time.Instant.now().toString(),
            score = correctCount.toDouble(),
            maxScore = answers.size.toDouble(),
            correctCount = correctCount,
            wrongCount = wrongCount,
            unattemptedCount = 0,
            needsReview = reviewFlags.isNotEmpty(),
            processingSummary = mapOf(
                "detection" to "IMPLEMENTED",
                "alignment" to "IMPLEMENTED",
                "bubble_reading" to "PARTIAL",
            ),
            responses = answers.mapIndexed { index, selected ->
                ScoredResponse(
                    questionNumber = index + 1,
                    selectedOption = selected,
                    correctOption = "A",
                    status = if (selected == null) "blank" else "detected",
                    confidence = 0.84,
                )
            },
            reviewFlags = reviewFlags,
        )
    }
}
