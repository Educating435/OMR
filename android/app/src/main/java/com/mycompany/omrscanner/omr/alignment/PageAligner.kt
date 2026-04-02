package com.mycompany.omrscanner.omr.alignment

class PageAligner {
    fun align(): AlignmentResult {
        return AlignmentResult(
            isAligned = true,
            note = "Four-corner marker alignment shell is IMPLEMENTED. Perspective warping and marker confidence tuning are TODO NEXT.",
        )
    }
}

data class AlignmentResult(
    val isAligned: Boolean,
    val note: String,
)
