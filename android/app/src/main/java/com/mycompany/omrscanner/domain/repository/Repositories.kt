package com.mycompany.omrscanner.domain.repository

import com.mycompany.omrscanner.domain.model.ScanOutcome
import com.mycompany.omrscanner.omr.scoring.ScoredOmrResult
import com.mycompany.omrscanner.omr.template.TemplateDefinition

interface AuthRepository {
    suspend fun login(email: String, password: String): Boolean
    suspend fun refreshSession(): Boolean = true
}

interface ExamRepository {
    suspend fun refreshCatalog()
    suspend fun getCachedExamTitles(): List<String>
    suspend fun getTemplatesForExam(examId: String): List<TemplateDefinition>
}

interface ResultRepository {
    suspend fun storeOfflineResult(result: ScoredOmrResult)
    suspend fun syncPendingResults()
    suspend fun getPendingResultCount(): Int
}

interface ScanRepository {
    suspend fun saveScan(outcome: ScanOutcome)
    suspend fun enqueueSync()
    suspend fun pendingSyncCount(): Int
}
