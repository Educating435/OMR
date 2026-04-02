package com.mycompany.omrscanner.omr.qr

import com.mycompany.omrscanner.domain.model.ExamTemplate
import com.mycompany.omrscanner.omr.alignment.PerspectiveCorrectedSheet
import javax.inject.Inject
import javax.inject.Singleton

data class QrMetadata(
    val templateId: String,
    val examId: String,
    val totalQuestions: Int,
    val optionsCount: Int,
    val version: Int,
)

@Singleton
class QrDecoder @Inject constructor() {
    fun decode(sheet: PerspectiveCorrectedSheet, fallbackTemplate: ExamTemplate): QrMetadata {
        val imagePath = sheet.imagePath
        return QrMetadata(
            templateId = fallbackTemplate.qrPayload["template_id"] ?: fallbackTemplate.id,
            examId = fallbackTemplate.examId,
            totalQuestions = fallbackTemplate.totalQuestions,
            optionsCount = fallbackTemplate.optionsCount,
            version = fallbackTemplate.qrPayload["version"]?.toIntOrNull() ?: fallbackTemplate.revision,
        )
    }
}
