package com.mycompany.omrscanner.data.repository

import com.mycompany.omrscanner.data.local.CachedExamEntity
import com.mycompany.omrscanner.data.local.CachedTemplateEntity
import com.mycompany.omrscanner.data.local.OmrDatabase
import com.mycompany.omrscanner.data.local.PendingResultEntity
import com.mycompany.omrscanner.data.remote.LoginRequestDto
import com.mycompany.omrscanner.data.remote.OmrApiService
import com.mycompany.omrscanner.data.remote.SyncFlagDto
import com.mycompany.omrscanner.data.remote.SyncResponseDto
import com.mycompany.omrscanner.data.remote.SyncResultRequestDto
import com.mycompany.omrscanner.domain.model.ScanOutcome
import com.mycompany.omrscanner.domain.repository.AuthRepository
import com.mycompany.omrscanner.domain.repository.ExamRepository
import com.mycompany.omrscanner.domain.repository.ResultRepository
import com.mycompany.omrscanner.domain.repository.ScanRepository
import com.mycompany.omrscanner.omr.scoring.ScoredOmrResult
import com.mycompany.omrscanner.omr.template.TemplateDefinition
import kotlinx.serialization.json.Json
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class AuthRepositoryImpl @Inject constructor(
    private val apiService: OmrApiService,
) : AuthRepository {
    override suspend fun login(email: String, password: String): Boolean {
        return apiService.login(LoginRequestDto(email, password)).accessToken.isNotBlank()
    }
}

@Singleton
class ExamRepositoryImpl @Inject constructor(
    private val apiService: OmrApiService,
    private val database: OmrDatabase,
    private val json: Json,
) : ExamRepository {
    override suspend fun refreshCatalog() {
        val exams = apiService.listExams()
        database.examDao().replaceAll(
            exams.map { dto ->
                CachedExamEntity(
                    id = dto.id,
                    title = dto.title,
                    subject = dto.subject,
                    totalQuestions = dto.totalQuestions,
                    updatedAt = System.currentTimeMillis().toString(),
                )
            },
        )
        exams.firstOrNull()?.let { firstExam ->
            val templates = apiService.listTemplates(firstExam.id)
            database.templateDao().replaceAll(
                templates.map { dto ->
                    CachedTemplateEntity(
                        id = dto.id,
                        examId = dto.examId,
                        templateCode = dto.templateCode,
                        bubbleLayoutJson = dto.bubbleLayout.toString(),
                        qrPayloadJson = dto.qrPayload.toString(),
                    )
                },
            )
        }
    }

    override suspend fun getCachedExamTitles(): List<String> {
        return database.examDao().getAll().map { "${it.title} (${it.subject})" }
    }

    override suspend fun getTemplatesForExam(examId: String): List<TemplateDefinition> {
        return database.templateDao().getByExamId(examId).map { entity ->
            TemplateDefinition(
                id = entity.id,
                examId = entity.examId,
                templateCode = entity.templateCode,
                bubbleLayoutJson = entity.bubbleLayoutJson,
                qrPayloadJson = entity.qrPayloadJson,
            )
        }
    }
}

@Singleton
class ResultRepositoryImpl @Inject constructor(
    private val apiService: OmrApiService,
    private val database: OmrDatabase,
    private val json: Json,
) : ResultRepository {
    override suspend fun storeOfflineResult(result: ScoredOmrResult) {
        database.pendingResultDao().upsert(
            PendingResultEntity(
                localAttemptId = result.localAttemptId,
                examId = result.examId,
                templateId = result.templateId,
                rollNumber = result.rollNumber,
                setCode = result.setCode,
                score = result.score,
                maxScore = result.maxScore,
                correctCount = result.correctCount,
                wrongCount = result.wrongCount,
                unattemptedCount = result.unattemptedCount,
                needsReview = result.needsReview,
                capturedAtIso = result.capturedAtIso,
                payloadJson = json.encodeToString(ScoredOmrResult.serializer(), result),
                syncState = "pending",
            ),
        )
    }

    override suspend fun syncPendingResults() {
        database.pendingResultDao().getAll().forEach { entity ->
            val parsed = json.decodeFromString(ScoredOmrResult.serializer(), entity.payloadJson)
            apiService.syncResult(
                SyncResultRequestDto(
                    examId = parsed.examId,
                    templateId = parsed.templateId,
                    rollNumber = parsed.rollNumber,
                    setCode = parsed.setCode,
                    localAttemptId = parsed.localAttemptId,
                    capturedAt = parsed.capturedAtIso,
                    score = parsed.score,
                    maxScore = parsed.maxScore,
                    correctCount = parsed.correctCount,
                    wrongCount = parsed.wrongCount,
                    unattemptedCount = parsed.unattemptedCount,
                    needsReview = parsed.needsReview,
                    processingSummary = parsed.processingSummary,
                    responses = parsed.responses.map {
                        SyncResponseDto(
                            questionNumber = it.questionNumber,
                            selectedOption = it.selectedOption,
                            correctOption = it.correctOption,
                            status = it.status,
                            confidence = it.confidence,
                        )
                    },
                    reviewFlags = parsed.reviewFlags.map {
                        SyncFlagDto(
                            flagType = it.flagType,
                            questionNumber = it.questionNumber,
                            message = it.message,
                        )
                    },
                ),
            )
            database.pendingResultDao().delete(entity.localAttemptId)
        }
    }

    override suspend fun getPendingResultCount(): Int = database.pendingResultDao().getAll().size
}

@Singleton
class ScanRepositoryImpl @Inject constructor(
    private val resultRepository: ResultRepository,
) : ScanRepository {
    override suspend fun saveScan(outcome: ScanOutcome) {
        resultRepository.storeOfflineResult(
            ScoredOmrResult(
                examId = outcome.examId,
                templateId = outcome.templateId,
                rollNumber = outcome.studentIdentifier,
                setCode = outcome.setCode ?: "A",
                localAttemptId = outcome.localAttemptUuid,
                capturedAtIso = java.time.Instant.now().toString(),
                score = outcome.score.toDouble(),
                maxScore = outcome.maxScore.toDouble(),
                correctCount = outcome.gradingSummary["correct"] ?: 0,
                wrongCount = outcome.gradingSummary["incorrect"] ?: 0,
                unattemptedCount = outcome.gradingSummary["blank"] ?: 0,
                needsReview = outcome.flaggedForReview,
                processingSummary = outcome.gradingSummary.mapValues { it.value.toString() },
                responses = outcome.responses.map { entry ->
                    com.mycompany.omrscanner.omr.scoring.ScoredResponse(
                        questionNumber = entry.key.toIntOrNull() ?: 0,
                        selectedOption = entry.value,
                        correctOption = "A",
                        status = if (entry.value == null) "blank" else "detected",
                        confidence = outcome.confidence.toDouble(),
                    )
                },
                reviewFlags = if (outcome.flaggedForReview) {
                    listOf(com.mycompany.omrscanner.omr.scoring.ReviewFlag("shell-review", null, "Requires operator review"))
                } else {
                    emptyList()
                },
            ),
        )
    }

    override suspend fun enqueueSync() {
        resultRepository.syncPendingResults()
    }

    override suspend fun pendingSyncCount(): Int = resultRepository.getPendingResultCount()
}
