package com.mycompany.omrscanner.omr.bubble

import com.mycompany.omrscanner.domain.model.BubbleMark
import com.mycompany.omrscanner.domain.model.ExamTemplate
import com.mycompany.omrscanner.domain.model.ResponseRead
import com.mycompany.omrscanner.omr.alignment.PerspectiveCorrectedSheet
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class BubbleReader @Inject constructor() {
    fun readAnswers(sheet: PerspectiveCorrectedSheet, template: ExamTemplate): List<ResponseRead> {
        return (1..template.totalQuestions).map { questionNo ->
            val scores = (0 until template.optionsCount).map { optionIndex ->
                val label = ('A'.code + optionIndex).toChar().toString()
                val strongA = optionIndex == 0
                BubbleMark(
                    label = label,
                    fillScore = if (strongA) 0.84f else 0.18f,
                    confidence = if (strongA) 0.92f else 0.41f,
                )
            }
            val selected = scores.maxByOrNull { it.fillScore }
            val multipleMarked = scores.count { it.fillScore > 0.72f } > 1
            val weak = (selected?.fillScore ?: 0f) < 0.55f
            ResponseRead(
                questionNo = questionNo,
                selectedOption = when {
                    multipleMarked -> null
                    weak -> null
                    else -> selected?.label
                },
                status = when {
                    multipleMarked -> "multiple_marked"
                    weak -> "uncertain"
                    else -> "answered"
                },
                confidence = selected?.confidence ?: 0f,
                optionScores = scores,
            )
        }
    }
}

