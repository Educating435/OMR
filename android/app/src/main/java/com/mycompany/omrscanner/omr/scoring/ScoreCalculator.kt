package com.mycompany.omrscanner.omr.scoring

import com.mycompany.omrscanner.domain.model.ExamTemplate
import com.mycompany.omrscanner.domain.model.ParsedSheet
import com.mycompany.omrscanner.domain.model.ScanOutcome
import com.mycompany.omrscanner.domain.usecase.GradeScanUseCase
import kotlinx.serialization.json.Json
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class ScoreCalculator @Inject constructor(
    private val gradeScanUseCase: GradeScanUseCase,
    private val json: Json,
) {
    fun calculate(template: ExamTemplate, parsedSheet: ParsedSheet, imagePath: String): ScanOutcome {
        val responses = parsedSheet.responses.associate { it.questionNo.toString() to it.selectedOption }
        val uncertain = parsedSheet.responses.count { it.status == "uncertain" }
        val multipleMarked = parsedSheet.responses.count { it.status == "multiple_marked" }
        val invalid = parsedSheet.responses.count { it.status != "answered" && it.status != "unattempted" }
        val averageConfidence = if (parsedSheet.responses.isEmpty()) 0f else parsedSheet.responses.map { it.confidence }.average().toFloat()
        return gradeScanUseCase(
            template = template,
            studentIdentifier = parsedSheet.rollNumber ?: "UNKNOWN",
            responses = responses,
            gradingSummary = mapOf(
                "uncertain" to uncertain,
                "multiple_marked" to multipleMarked,
                "invalid" to invalid,
                "poor_lighting" to if (parsedSheet.validation.poorLighting) 1 else 0,
                "blurry" to if (parsedSheet.validation.blurry) 1 else 0,
            ),
        ).copy(
            setCode = parsedSheet.setCode,
            confidence = averageConfidence,
            flaggedForReview = !parsedSheet.validation.sheetFullyVisible ||
                !parsedSheet.validation.markersDetected ||
                parsedSheet.validation.blurry ||
                uncertain > 0 ||
                multipleMarked > 0,
            originalImagePath = imagePath,
            parsedOutputJson = json.encodeToString(parsedSheet),
        )
    }
}

