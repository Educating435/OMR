package com.mycompany.omrscanner.scanner

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.mycompany.omrscanner.camera.CameraCoordinator
import com.mycompany.omrscanner.omr.alignment.PageAligner
import com.mycompany.omrscanner.omr.bubble.BubbleInterpreter
import com.mycompany.omrscanner.omr.detection.SheetDetector
import com.mycompany.omrscanner.omr.scoring.ScoreCalculator

@Composable
fun ScannerScreen(modifier: Modifier = Modifier) {
    val status = remember { mutableStateOf("Ready to scan.") }
    val cameraCoordinator = remember { CameraCoordinator() }
    val sheetDetector = remember { SheetDetector() }
    val pageAligner = remember { PageAligner() }
    val bubbleInterpreter = remember { BubbleInterpreter() }
    val scoreCalculator = remember { ScoreCalculator() }

    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        Text("Scanner", style = MaterialTheme.typography.headlineMedium)
        Text(cameraCoordinator.captureGuidance())
        Text(status.value)
        Button(
            onClick = {
                val detection = sheetDetector.detect()
                val alignment = pageAligner.align()
                val answers = bubbleInterpreter.readAnswers(questionCount = 50)
                val result = scoreCalculator.calculate(
                    examId = "local-demo-exam",
                    templateId = "local-template-v1",
                    answers = answers,
                )
                status.value =
                    "${detection.guidance}\n${alignment.note}\nScored ${result.score}/${result.maxScore} for roll ${result.rollNumber}."
            },
        ) {
            Text("Run on-device OMR shell")
        }
    }
}
