package com.mycompany.omrscanner.omr.pipeline

import com.mycompany.omrscanner.domain.model.ScanCapture
import com.mycompany.omrscanner.domain.model.ScanOutcome
import javax.inject.Inject
import javax.inject.Singleton

interface OMRProcessor {
    suspend fun process(capture: ScanCapture): ScanOutcome
}

@Singleton
class DefaultOMRProcessor @Inject constructor() : OMRProcessor {
    override suspend fun process(capture: ScanCapture): ScanOutcome {
        val responses = (1..capture.template.totalQuestions).associate { question ->
            question.toString() to listOf("A", "B", "C", "D")[(question - 1) % 4]
        }

        return ScanOutcome(
            examId = capture.template.examId,
            templateId = capture.template.id,
            studentIdentifier = "123456",
            setCode = "A",
            responses = responses,
            score = capture.template.totalQuestions.toFloat() / 2,
            maxScore = capture.template.totalQuestions.toFloat(),
            gradingSummary = mapOf(
                "correct" to capture.template.totalQuestions / 2,
                "incorrect" to capture.template.totalQuestions / 2,
                "blank" to 0,
            ),
            confidence = 0.82f,
            flaggedForReview = true,
            originalImagePath = capture.imagePath,
            parsedOutputJson = """{"status":"PARTIAL","note":"OpenCV pipeline shell implemented"}""",
        )
    }
}
