package com.mycompany.omrscanner.domain.repository

import com.mycompany.omrscanner.domain.model.Exam
import com.mycompany.omrscanner.domain.model.ExamTemplate
import com.mycompany.omrscanner.domain.model.ScanOutcome
import com.mycompany.omrscanner.domain.model.ScanReviewItem
import com.mycompany.omrscanner.domain.model.UserSession

interface AuthRepository {
    suspend fun login(email: String, password: String): UserSession
    suspend fun refreshSession(): UserSession?
    suspend fun currentSession(): UserSession?
    suspend fun logout()
}

interface ExamRepository {
    suspend fun fetchExams(): List<Exam>
    suspend fun fetchTemplates(examId: String): List<ExamTemplate>
    suspend fun cachedExams(): List<Exam>
    suspend fun cachedTemplates(examId: String): List<ExamTemplate>
}

interface ScanRepository {
    suspend fun saveScan(outcome: ScanOutcome)
    suspend fun pendingSyncCount(): Int
    suspend fun flaggedScans(): List<ScanReviewItem>
    suspend fun markReviewed(attemptId: String)
    suspend fun queueCount(): Int
    fun enqueueSync()
}
