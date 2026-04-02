package com.mycompany.omrscanner.omr.pipeline

import com.mycompany.omrscanner.domain.model.ExamTemplate
import com.mycompany.omrscanner.omr.template.TemplateResolver
import org.junit.Assert.assertEquals
import org.junit.Test

class TemplateResolverTest {
    @Test
    fun rejects_invalid_template_id() {
        val resolver = TemplateResolver()
        val template = ExamTemplate(
            id = "template-1",
            examId = "exam-1",
            revision = 1,
            totalQuestions = 50,
            optionsCount = 4,
            qrPayload = emptyMap(),
            layoutJson = "{}",
            answerKey = emptyMap(),
            positiveMarks = 1,
            negativeMarks = 0,
        )
        val resolved = resolver.resolve("template-1", template)
        assertEquals("template-1", resolved.id)
    }
}
