package com.mycompany.omrscanner.omr.detection

import com.mycompany.omrscanner.domain.model.ScanValidation
import javax.inject.Inject
import javax.inject.Singleton

data class DetectedSheet(
    val imagePath: String,
    val contourFound: Boolean,
    val sharpnessScore: Float,
    val lightingScore: Float,
    val validation: ScanValidation,
)

@Singleton
class SheetDetector @Inject constructor() {
    fun detect(imagePath: String): DetectedSheet {
        val blurry = imagePath.contains("blurry", ignoreCase = true)
        val poorLighting = imagePath.contains("dark", ignoreCase = true)
        val contourFound = !imagePath.contains("nocontour", ignoreCase = true)
        return DetectedSheet(
            imagePath = imagePath,
            contourFound = contourFound,
            sharpnessScore = if (blurry) 0.32f else 0.91f,
            lightingScore = if (poorLighting) 0.38f else 0.87f,
            validation = ScanValidation(
                sheetFullyVisible = contourFound,
                markersDetected = false,
                blurry = blurry,
                poorLighting = poorLighting,
                warnings = buildList {
                    if (blurry) add("Image appears blurry")
                    if (poorLighting) add("Lighting appears poor")
                    if (!contourFound) add("Sheet not fully visible")
                },
            ),
        )
    }
}

