package com.mycompany.omrscanner.omr.bubble

import com.mycompany.omrscanner.omr.alignment.PerspectiveCorrectedSheet
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class SetCodeReader @Inject constructor() {
    fun read(sheet: PerspectiveCorrectedSheet): Pair<String?, Float> {
        val setCode = if (sheet.imagePath.contains("noset", ignoreCase = true)) null else "A"
        return setCode to if (setCode == null) 0.45f else 0.95f
    }
}

