package com.mycompany.omrscanner.omr.detection

class SheetDetector {
    fun detect(): DetectionResult {
        return DetectionResult(
            sheetFound = true,
            guidance = "Controlled-template detection shell is IMPLEMENTED. OpenCV contour detection refinement is TODO NEXT.",
        )
    }
}

data class DetectionResult(
    val sheetFound: Boolean,
    val guidance: String,
)
