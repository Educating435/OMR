package com.mycompany.omrscanner.data.repository

import androidx.work.Constraints
import androidx.work.NetworkType
import androidx.work.OneTimeWorkRequestBuilder
import androidx.work.WorkManager
import com.mycompany.omrscanner.data.local.CacheDao
import com.mycompany.omrscanner.data.local.ScanAttemptDao
import com.mycompany.omrscanner.data.local.SecureSessionStore
import com.mycompany.omrscanner.data.local.SyncQueueDao
import com.mycompany.omrscanner.data.local.SyncQueueEntity
import com.mycompany.omrscanner.data.mapper.toCache
import com.mycompany.omrscanner.data.mapper.toDomain
import com.mycompany.omrscanner.data.mapper.toEntity
import com.mycompany.omrscanner.data.remote.LoginRequestDto
import com.mycompany.omrscanner.data.remote.OMRApiService
import com.mycompany.omrscanner.data.remote.RefreshRequestDto
import com.mycompany.omrscanner.domain.model.Exam
import com.mycompany.omrscanner.domain.model.ExamTemplate
import com.mycompany.omrscanner.domain.model.ScanOutcome
import com.mycompany.omrscanner.domain.model.ScanReviewItem
import com.mycompany.omrscanner.domain.model.UserSession
import com.mycompany.omrscanner.domain.repository.AuthRepository
import com.mycompany.omrscanner.domain.repository.ExamRepository
import com.mycompany.omrscanner.domain.repository.ScanRepository
import com.mycompany.omrscanner.sync.ScanSyncWorker
import kotlinx.serialization.json.Json
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class AuthRepositoryImpl @Inject constructor(
    private val apiService: OMRApiService,
    private val secureSessionStore: SecureSessionStore,
) : AuthRepository {
    override suspend fun login(email: String, password: String): UserSession {
        val session = apiService.login(LoginRequestDto(email, password)).toDomain()
        secureSessionStore.save(session)
        return session
    }

    override suspend fun refreshSession(): UserSession? {
        val current = secureSessionStore.read() ?: return null
        val refreshed = apiService.refresh(RefreshRequestDto(current.refreshToken)).toDomain()
        secureSessionStore.save(refreshed)
        return refreshed
    }

    override suspend fun currentSession(): UserSession? = secureSessionStore.read()

    override suspend fun logout() {
        secureSessionStore.clear()
    }
}

@Singleton
class ExamRepositoryImpl @Inject constructor(
    private val apiService: OMRApiService,
    private val cacheDao: CacheDao,
    private val json: Json,
) : ExamRepository {
    override suspend fun fetchExams(): List<Exam> {
        val remote = apiService.exams().items
        cacheDao.upsertExams(remote.map { it.toCache() })
        return remote.map { it.toDomain() }
    }

    override suspend fun fetchTemplates(examId: String): List<ExamTemplate> {
        val remote = apiService.templates(examId)
        cacheDao.upsertTemplates(remote.map { it.toCache(json) })
        return remote.map { it.toDomain() }
    }

    override suspend fun cachedExams(): List<Exam> = cacheDao.cachedExams().map { it.toDomain() }

    override suspend fun cachedTemplates(examId: String): List<ExamTemplate> = cacheDao.cachedTemplates(examId).map { it.toDomain(json) }
}

@Singleton
class ScanRepositoryImpl @Inject constructor(
    private val dao: ScanAttemptDao,
    private val syncQueueDao: SyncQueueDao,
    private val workManager: WorkManager,
    private val json: Json,
    private val apiService: OMRApiService,
) : ScanRepository {
    override suspend fun saveScan(outcome: ScanOutcome) {
        dao.upsert(outcome.toEntity(json))
        syncQueueDao.upsert(
            SyncQueueEntity(
                id = outcome.localAttemptUuid,
                entityType = "omr_result",
                entityId = outcome.localAttemptUuid,
                action = "upload",
            )
        )
    }

    override suspend fun pendingSyncCount(): Int = dao.pendingCount()

    override suspend fun flaggedScans(): List<ScanReviewItem> {
        val local = dao.flagged().map {
            ScanReviewItem(
                id = it.remoteAttemptId ?: it.localAttemptUuid,
                studentIdentifier = it.studentIdentifier,
                score = it.score,
                maxScore = it.maxScore,
                needsReview = it.needsReview,
                reviewStatus = it.reviewStatus,
            )
        }
        return if (local.isNotEmpty()) local else apiService.flaggedScans().map { it.toDomain() }
    }

    override suspend fun markReviewed(attemptId: String) {
        dao.markReviewed(attemptId)
        apiService.markReviewed(
            attemptId = attemptId,
            body = mapOf(
                "needs_review" to false,
                "review_status" to "reviewed",
                "remarks" to "Reviewed on Android device",
            )
        )
    }

    override suspend fun queueCount(): Int = syncQueueDao.count()

    override fun enqueueSync() {
        val request = OneTimeWorkRequestBuilder<ScanSyncWorker>()
            .setConstraints(
                Constraints.Builder()
                    .setRequiredNetworkType(NetworkType.CONNECTED)
                    .build()
            )
            .build()
        workManager.enqueue(request)
    }
}
