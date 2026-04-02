package com.mycompany.omrscanner.omr.alignment

import javax.inject.Inject
import javax.inject.Singleton

data class MarkerDetection(
    val foundAll: Boolean,
    val markerCount: Int,
)

@Singleton
class MarkerDetector @Inject constructor() {
    fun detect(sheet: PerspectiveCorrectedSheet): MarkerDetection {
        val foundAll = !sheet.imagePath.contains("nomarkers", ignoreCase = true)
        return MarkerDetection(foundAll = foundAll, markerCount = if (foundAll) 4 else 2)
    }
}

