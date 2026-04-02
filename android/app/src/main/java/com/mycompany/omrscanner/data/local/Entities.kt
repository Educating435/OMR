package com.mycompany.omrscanner.data.local

import androidx.room.Dao
import androidx.room.Database
import androidx.room.Entity
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.PrimaryKey
import androidx.room.Query
import androidx.room.RoomDatabase

@Entity(tableName = "cached_exams")
data class CachedExamEntity(
    @PrimaryKey val id: String,
    val title: String,
    val subject: String,
    val totalQuestions: Int,
)

@Entity(tableName = "cached_templates")
data class CachedTemplateEntity(
    @PrimaryKey val id: String,
    val examId: String,
    val revision: Int,
    val totalQuestions: Int,
    val optionsCount: Int,
    val qrPayloadJson: String,
    val layoutJson: String,
    val answerKeyJson: String,
    val positiveMarks: Int,
    val negativeMarks: Int,
)

@Entity(tableName = "scan_attempts")
data class ScanAttemptEntity(
    @PrimaryKey val localAttemptUuid: String,
    val remoteAttemptId: String? = null,
    val examId: String,
    val templateId: String,
    val studentIdentifier: String,
    val setCode: String? = null,
    val score: Float,
    val maxScore: Float,
    val confidence: Float,
    val responsesJson: String,
    val gradingSummaryJson: String,
    val parsedOutputJson: String,
    val needsReview: Boolean,
    val reviewStatus: String,
    val imagePath: String? = null,
    val synced: Boolean = false,
)

@Entity(tableName = "sync_queue")
data class SyncQueueEntity(
    @PrimaryKey val id: String,
    val entityType: String,
    val entityId: String,
    val action: String,
    val status: String = "pending",
    val retryCount: Int = 0,
    val lastError: String? = null,
)

@Dao
interface CacheDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertExams(items: List<CachedExamEntity>)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertTemplates(items: List<CachedTemplateEntity>)

    @Query("SELECT * FROM cached_exams ORDER BY title ASC")
    suspend fun cachedExams(): List<CachedExamEntity>

    @Query("SELECT * FROM cached_templates WHERE examId = :examId ORDER BY revision DESC")
    suspend fun cachedTemplates(examId: String): List<CachedTemplateEntity>
}

@Dao
interface ScanAttemptDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsert(entity: ScanAttemptEntity)

    @Query("SELECT * FROM scan_attempts WHERE synced = 0")
    suspend fun pending(): List<ScanAttemptEntity>

    @Query("SELECT COUNT(*) FROM scan_attempts WHERE synced = 0")
    suspend fun pendingCount(): Int

    @Query("SELECT * FROM scan_attempts WHERE needsReview = 1 ORDER BY rowid DESC")
    suspend fun flagged(): List<ScanAttemptEntity>

    @Query("UPDATE scan_attempts SET synced = 1 WHERE localAttemptUuid = :localAttemptUuid")
    suspend fun markSynced(localAttemptUuid: String)

    @Query("UPDATE scan_attempts SET needsReview = 0, reviewStatus = 'reviewed' WHERE localAttemptUuid = :attemptId OR remoteAttemptId = :attemptId")
    suspend fun markReviewed(attemptId: String)
}

@Dao
interface SyncQueueDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsert(item: SyncQueueEntity)

    @Query("SELECT * FROM sync_queue WHERE status IN ('pending','failed') ORDER BY retryCount ASC")
    suspend fun pending(): List<SyncQueueEntity>

    @Query("SELECT COUNT(*) FROM sync_queue WHERE status IN ('pending','failed')")
    suspend fun count(): Int

    @Query("UPDATE sync_queue SET status = 'done', lastError = NULL WHERE id = :id")
    suspend fun markDone(id: String)

    @Query("UPDATE sync_queue SET status = 'failed', retryCount = retryCount + 1, lastError = :error WHERE id = :id")
    suspend fun markFailed(id: String, error: String)
}

@Database(
    entities = [CachedExamEntity::class, CachedTemplateEntity::class, ScanAttemptEntity::class, SyncQueueEntity::class],
    version = 2,
    exportSchema = false,
)
abstract class OMRDatabase : RoomDatabase() {
    abstract fun scanAttemptDao(): ScanAttemptDao
    abstract fun cacheDao(): CacheDao
    abstract fun syncQueueDao(): SyncQueueDao
}
