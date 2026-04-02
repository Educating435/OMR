package com.mycompany.omrscanner.feature_scan

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.mycompany.omrscanner.camera.CameraCaptureCoordinator
import com.mycompany.omrscanner.domain.model.ExamTemplate
import com.mycompany.omrscanner.domain.model.ScanCapture
import com.mycompany.omrscanner.domain.usecase.GetPendingSyncCountUseCase
import com.mycompany.omrscanner.domain.usecase.ProcessScanUseCase
import com.mycompany.omrscanner.domain.usecase.SaveScanUseCase
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.launch
import javax.inject.Inject

data class ScanUiState(
    val pendingSyncCount: Int = 0,
    val queueCount: Int = 0,
    val lastSummary: String = "No scans yet",
    val isProcessing: Boolean = false,
    val warning: String? = null,
)

@HiltViewModel
class ScanViewModel @Inject constructor(
    private val processScanUseCase: ProcessScanUseCase,
    private val saveScanUseCase: SaveScanUseCase,
    private val getPendingSyncCountUseCase: GetPendingSyncCountUseCase,
    private val cameraCaptureCoordinator: CameraCaptureCoordinator,
) : ViewModel() {
    var uiState by mutableStateOf(ScanUiState())
        private set

    fun processDemoScan() {
        viewModelScope.launch {
            uiState = uiState.copy(isProcessing = true, warning = null)
            val template = ExamTemplate(
                id = "template-demo",
                examId = "exam-demo",
                revision = 1,
                totalQuestions = 50,
                optionsCount = 4,
                qrPayload = mapOf(
                    "template_id" to "template-demo",
                    "exam_id" to "exam-demo",
                    "total_questions" to "50",
                    "options_count" to "4",
                    "version" to "1",
                ),
                layoutJson = "{}",
                answerKey = (1..50).associate { it.toString() to "A" },
                positiveMarks = 1,
                negativeMarks = 0,
            )
            val imagePath = cameraCaptureCoordinator.latestCapturedImagePath()
            val capture = ScanCapture(
                template = template,
                imagePath = imagePath,
            )
            runCatching {
                val outcome = processScanUseCase(capture)
                saveScanUseCase(outcome)
                val pendingCount = getPendingSyncCountUseCase()
                uiState = uiState.copy(
                    isProcessing = false,
                    pendingSyncCount = pendingCount,
                    queueCount = pendingCount,
                    lastSummary = "Score ${outcome.score}/${outcome.maxScore} | ${outcome.studentIdentifier} | ${outcome.setCode ?: "-"}",
                    warning = if (outcome.flaggedForReview) "Flagged for review due to uncertain read or validation issue" else null,
                )
            }.onFailure { throwable ->
                uiState = uiState.copy(
                    isProcessing = false,
                    warning = throwable.message ?: "Scan failed",
                )
            }
        }
    }
}
