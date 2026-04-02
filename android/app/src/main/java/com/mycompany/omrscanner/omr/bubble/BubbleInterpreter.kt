package com.mycompany.omrscanner.omr.bubble

class BubbleInterpreter {
    fun readRollNumber(): String = "123456"

    fun readSetCode(): String = "A"

    fun readAnswers(questionCount: Int): List<String?> {
        return List(questionCount) { index ->
            listOf("A", "B", "C", "D")[index % 4]
        }
    }
}
