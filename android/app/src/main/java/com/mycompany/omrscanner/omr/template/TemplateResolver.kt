package com.mycompany.omrscanner.omr.template

import com.mycompany.omrscanner.domain.model.ExamTemplate
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class TemplateResolver @Inject constructor() {
    fun resolve(qrTemplateId: String, expectedTemplate: ExamTemplate): ExamTemplate {
        require(qrTemplateId == expectedTemplate.id) { "QR template does not match loaded template" }
        return expectedTemplate
    }
}

