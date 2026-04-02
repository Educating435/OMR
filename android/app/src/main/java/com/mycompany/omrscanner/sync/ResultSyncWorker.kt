package com.mycompany.omrscanner.sync

import android.content.Context
import androidx.hilt.work.HiltWorker
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import com.mycompany.omrscanner.domain.repository.ResultRepository
import dagger.assisted.Assisted
import dagger.assisted.AssistedInject

@HiltWorker
class ResultSyncWorker @AssistedInject constructor(
    @Assisted appContext: Context,
    @Assisted workerParams: WorkerParameters,
    private val resultRepository: ResultRepository,
) : CoroutineWorker(appContext, workerParams) {
    override suspend fun doWork(): Result {
        resultRepository.syncPendingResults()
        return Result.success()
    }
}
