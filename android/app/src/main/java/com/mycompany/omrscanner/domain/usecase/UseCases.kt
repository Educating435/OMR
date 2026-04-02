package com.mycompany.omrscanner.domain.usecase

import com.mycompany.omrscanner.domain.model.ExamTemplate
import com.mycompany.omrscanner.domain.model.ScanCapture
import com.mycompany.omrscanner.domain.model.ScanOutcome
import com.mycompany.omrscanner.domain.repository.AuthRepository
import com.mycompany.omrscanner.domain.repository.ScanRepository
import com.mycompany.omrscanner.omr.pipeline.OMRProcessor
import javax.inject.Inject

class ProcessScanUseCase @Inject constructor(
    private val omrProcessor: OMRProcessor,
) {
    suspend operator fun invoke(capture: ScanCapture): ScanOutcome {
        return omrProcessor.process(capture)
    }
}

class SaveScanUseCase @Inject constructor(
    private val scanRepository: ScanRepository,
) {
    suspend operator fun invoke(outcome: ScanOutcome) {
        scanRepository.saveScan(outcome)
        scanRepository.enqueueSync()
    }
}

class GetPendingSyncCountUseCase @Inject constructor(
    private val scanRepository: ScanRepository,
) {
    suspend operator fun invoke(): Int = scanRepository.pendingSyncCount()
}

class RefreshSessionUseCase @Inject constructor(
    private val authRepository: AuthRepository,
) {
    suspend operator fun invoke() = authRepository.refreshSession()
}

class GradeScanUseCase @Inject constructor() {
    operator fun invoke(
        template: ExamTemplate,
        studentIdentifier: String,
        responses: Map<String, String?>,
        gradingSummary: Map<String, Int> = emptyMap(),
    ): ScanOutcome {
        var correct = 0
        var incorrect = 0
        var blank = 0

        template.answerKey.forEach { (question, expected) ->
            when (val actual = responses[question]) {
                null -> blank++
                expected -> correct++
                else -> if (actual.isBlank()) blank++ else incorrect++
            }
        }

        val score = (correct * template.positiveMarks) - (incorrect * template.negativeMarks)
        val maxScore = template.answerKey.size * template.positiveMarks

        return ScanOutcome(
            examId = template.examId,
            templateId = template.id,
            studentIdentifier = studentIdentifier,
            responses = responses,
            score = score.toFloat(),
            maxScore = maxScore.toFloat(),
            gradingSummary = mapOf(
                "correct" to correct,
                "incorrect" to incorrect,
                "blank" to blank,
            ) + gradingSummary,
        )
    }
}
