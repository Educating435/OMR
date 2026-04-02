package com.mycompany.omrscanner.omr.alignment

import com.mycompany.omrscanner.omr.detection.DetectedSheet
import javax.inject.Inject
import javax.inject.Singleton

data class PerspectiveCorrectedSheet(
    val imagePath: String,
    val normalizedWidth: Int = 2480,
    val normalizedHeight: Int = 3508,
)

@Singleton
class PerspectiveCorrector @Inject constructor() {
    fun correct(sheet: DetectedSheet): PerspectiveCorrectedSheet {
        return PerspectiveCorrectedSheet(imagePath = sheet.imagePath)
    }
}

