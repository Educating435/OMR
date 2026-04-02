package com.mycompany.omrscanner.domain.usecases

import com.mycompany.omrscanner.domain.repository.AuthRepository
import com.mycompany.omrscanner.domain.repository.ExamRepository
import com.mycompany.omrscanner.domain.repository.ResultRepository
import com.mycompany.omrscanner.omr.scoring.ScoredOmrResult
import javax.inject.Inject

class LoginUseCase @Inject constructor(
    private val authRepository: AuthRepository,
) {
    suspend operator fun invoke(email: String, password: String): Boolean = authRepository.login(email, password)
}

class RefreshExamCatalogUseCase @Inject constructor(
    private val examRepository: ExamRepository,
) {
    suspend operator fun invoke() = examRepository.refreshCatalog()
}

class StoreOfflineResultUseCase @Inject constructor(
    private val resultRepository: ResultRepository,
) {
    suspend operator fun invoke(result: ScoredOmrResult) = resultRepository.storeOfflineResult(result)
}

class SyncPendingResultsUseCase @Inject constructor(
    private val resultRepository: ResultRepository,
) {
    suspend operator fun invoke() = resultRepository.syncPendingResults()
}
