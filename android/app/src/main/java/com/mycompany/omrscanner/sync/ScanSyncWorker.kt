package com.mycompany.omrscanner.sync

import androidx.hilt.work.HiltWorker
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import com.mycompany.omrscanner.data.local.ScanAttemptDao
import com.mycompany.omrscanner.data.local.SyncQueueDao
import com.mycompany.omrscanner.data.remote.OMRApiService
import com.mycompany.omrscanner.data.remote.ScanSubmissionRequest
import com.mycompany.omrscanner.core.util.decode
import dagger.assisted.Assisted
import dagger.assisted.AssistedInject
import kotlinx.serialization.json.Json

@HiltWorker
class ScanSyncWorker @AssistedInject constructor(
    @Assisted appContext: android.content.Context,
    @Assisted params: WorkerParameters,
    private val dao: ScanAttemptDao,
    private val syncQueueDao: SyncQueueDao,
    private val api: OMRApiService,
    private val json: Json,
) : CoroutineWorker(appContext, params) {
    override suspend fun doWork(): Result {
        val queueItems = syncQueueDao.pending()
        queueItems.forEach { queueItem ->
            val target = dao.pending().firstOrNull { it.localAttemptUuid == queueItem.entityId } ?: return@forEach
            runCatching {
                api.submitScan(
                    ScanSubmissionRequest(
                        exam_id = target.examId,
                        template_id = target.templateId,
                        student_identifier = target.studentIdentifier,
                        local_attempt_uuid = target.localAttemptUuid,
                        score = target.score,
                        max_score = target.maxScore,
                        responses = json.decode(target.responsesJson),
                        grading_summary = json.decode(target.gradingSummaryJson),
                        image_path = target.imagePath,
                    )
                )
                dao.markSynced(target.localAttemptUuid)
                syncQueueDao.markDone(queueItem.id)
            }.onFailure { error ->
                syncQueueDao.markFailed(queueItem.id, error.message ?: "Upload failed")
                return Result.retry()
            )
        }
        return Result.success()
    }
}
