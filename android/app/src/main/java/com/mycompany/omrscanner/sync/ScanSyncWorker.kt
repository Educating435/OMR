package com.mycompany.omrscanner.sync

import android.content.Context
import androidx.hilt.work.HiltWorker
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import com.mycompany.omrscanner.domain.repository.ResultRepository
import dagger.assisted.Assisted
import dagger.assisted.AssistedInject

@HiltWorker
class ScanSyncWorker @AssistedInject constructor(
    @Assisted appContext: Context,
    @Assisted params: WorkerParameters,
    private val resultRepository: ResultRepository,
) : CoroutineWorker(appContext, params) {
    override suspend fun doWork(): Result {
        resultRepository.syncPendingResults()
        return Result.success()
    }
}
