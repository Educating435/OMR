package com.mycompany.omrscanner.omr.pipeline

import com.mycompany.omrscanner.domain.model.ParsedSheet
import com.mycompany.omrscanner.domain.model.ScanCapture
import com.mycompany.omrscanner.domain.model.ScanOutcome
import com.mycompany.omrscanner.omr.alignment.MarkerDetector
import com.mycompany.omrscanner.omr.alignment.PerspectiveCorrector
import com.mycompany.omrscanner.omr.bubble.BubbleReader
import com.mycompany.omrscanner.omr.bubble.RollNumberReader
import com.mycompany.omrscanner.omr.bubble.SetCodeReader
import com.mycompany.omrscanner.omr.detection.SheetDetector
import com.mycompany.omrscanner.omr.qr.QrDecoder
import com.mycompany.omrscanner.omr.scoring.ScoreCalculator
import com.mycompany.omrscanner.omr.template.TemplateResolver
import javax.inject.Inject
import javax.inject.Singleton

interface OMRProcessor {
    suspend fun process(capture: ScanCapture): ScanOutcome
}

@Singleton
class DefaultOMRProcessor @Inject constructor(
    private val sheetDetector: SheetDetector,
    private val perspectiveCorrector: PerspectiveCorrector,
    private val markerDetector: MarkerDetector,
    private val qrDecoder: QrDecoder,
    private val templateResolver: TemplateResolver,
    private val bubbleReader: BubbleReader,
    private val rollNumberReader: RollNumberReader,
    private val setCodeReader: SetCodeReader,
    private val scoreCalculator: ScoreCalculator,
) : OMRProcessor {
    override suspend fun process(capture: ScanCapture): ScanOutcome {
        val detectedSheet = sheetDetector.detect(capture.imagePath)
        require(detectedSheet.validation.sheetFullyVisible) { "Sheet not fully visible" }
        require(!detectedSheet.validation.blurry) { "Image is too blurry" }

        val correctedSheet = perspectiveCorrector.correct(detectedSheet)
        val markers = markerDetector.detect(correctedSheet)
        require(markers.foundAll) { "Corner markers not detected" }

        val qr = qrDecoder.decode(correctedSheet, capture.template)
        val template = templateResolver.resolve(qr.templateId, capture.template)
        val answerReads = bubbleReader.readAnswers(correctedSheet, template)
        val (rollNumber, _) = rollNumberReader.read(correctedSheet)
        val (setCode, _) = setCodeReader.read(correctedSheet)

        val parsedSheet = ParsedSheet(
            templateId = qr.templateId,
            examId = qr.examId,
            rollNumber = rollNumber,
            setCode = setCode,
            responses = answerReads,
            validation = detectedSheet.validation.copy(
                markersDetected = markers.foundAll,
                warnings = detectedSheet.validation.warnings + if (detectedSheet.validation.poorLighting) listOf("Lighting is poor") else emptyList(),
            ),
        )
        return scoreCalculator.calculate(template, parsedSheet, capture.imagePath)
    }
}
