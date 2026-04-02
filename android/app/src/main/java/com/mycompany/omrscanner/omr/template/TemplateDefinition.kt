package com.mycompany.omrscanner.omr.template

data class TemplateDefinition(
    val id: String,
    val examId: String,
    val templateCode: String,
    val bubbleLayoutJson: String,
    val qrPayloadJson: String,
)
