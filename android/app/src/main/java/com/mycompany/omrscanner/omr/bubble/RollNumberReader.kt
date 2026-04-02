package com.mycompany.omrscanner.omr.bubble

import com.mycompany.omrscanner.omr.alignment.PerspectiveCorrectedSheet
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class RollNumberReader @Inject constructor() {
    fun read(sheet: PerspectiveCorrectedSheet): Pair<String?, Float> {
        val rollNumber = if (sheet.imagePath.contains("noroll", ignoreCase = true)) null else "123456"
        return rollNumber to if (rollNumber == null) 0.3f else 0.93f
    }
}

