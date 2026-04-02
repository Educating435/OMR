package com.mycompany.omrscanner.omr.template

data class TemplateDefinition(
    val templateId: String,
    val examId: String,
    val revision: Int,
    val questionCount: Int,
)

