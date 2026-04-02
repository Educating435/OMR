package com.mycompany.omrscanner.omr.scoring

import com.mycompany.omrscanner.domain.model.ExamTemplate
import com.mycompany.omrscanner.domain.model.ParsedSheet
import com.mycompany.omrscanner.domain.model.ResponseRead
import com.mycompany.omrscanner.domain.model.ScanValidation
import com.mycompany.omrscanner.domain.usecase.GradeScanUseCase
import kotlinx.serialization.json.Json
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class ScoreCalculatorTest {
    private val calculator = ScoreCalculator(GradeScanUseCase(), Json { ignoreUnknownKeys = true })

    @Test
    fun marks_unattempted_and_multiple_marked_for_review() {
        val template = ExamTemplate(
            id = "template-1",
            examId = "exam-1",
            revision = 1,
            totalQuestions = 3,
            optionsCount = 4,
            qrPayload = mapOf("template_id" to "template-1", "version" to "1"),
            layoutJson = "{}",
            answerKey = mapOf("1" to "A", "2" to "B", "3" to "C"),
            positiveMarks = 1,
            negativeMarks = 0,
        )
        val parsed = ParsedSheet(
            templateId = "template-1",
            examId = "exam-1",
            rollNumber = "123456",
            setCode = "A",
            responses = listOf(
                ResponseRead(1, "A", "answered", 0.95f, emptyList()),
                ResponseRead(2, null, "multiple_marked", 0.25f, emptyList()),
                ResponseRead(3, null, "uncertain", 0.30f, emptyList()),
            ),
            validation = ScanValidation(true, true, false, false),
        )

        val outcome = calculator.calculate(template, parsed, "scan.jpg")
        assertEquals(1f, outcome.score)
        assertTrue(outcome.flaggedForReview)
    }
}

