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
    val updatedAt: String,
)

@Entity(tableName = "cached_templates")
data class CachedTemplateEntity(
    @PrimaryKey val id: String,
    val examId: String,
    val templateCode: String,
    val bubbleLayoutJson: String,
    val qrPayloadJson: String,
)

@Entity(tableName = "pending_results")
data class PendingResultEntity(
    @PrimaryKey val localAttemptId: String,
    val examId: String,
    val templateId: String,
    val rollNumber: String,
    val setCode: String,
    val score: Double,
    val maxScore: Double,
    val correctCount: Int,
    val wrongCount: Int,
    val unattemptedCount: Int,
    val needsReview: Boolean,
    val capturedAtIso: String,
    val payloadJson: String,
    val syncState: String,
)

@Dao
interface ExamDao {
    @Query("SELECT * FROM cached_exams ORDER BY updatedAt DESC")
    suspend fun getAll(): List<CachedExamEntity>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun replaceAll(rows: List<CachedExamEntity>)
}

@Dao
interface TemplateDao {
    @Query("SELECT * FROM cached_templates WHERE examId = :examId")
    suspend fun getByExamId(examId: String): List<CachedTemplateEntity>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun replaceAll(rows: List<CachedTemplateEntity>)
}

@Dao
interface PendingResultDao {
    @Query("SELECT * FROM pending_results ORDER BY capturedAtIso DESC")
    suspend fun getAll(): List<PendingResultEntity>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsert(row: PendingResultEntity)

    @Query("DELETE FROM pending_results WHERE localAttemptId = :localAttemptId")
    suspend fun delete(localAttemptId: String)
}

@Database(
    entities = [CachedExamEntity::class, CachedTemplateEntity::class, PendingResultEntity::class],
    version = 1,
    exportSchema = false,
)
abstract class OmrDatabase : RoomDatabase() {
    abstract fun examDao(): ExamDao
    abstract fun templateDao(): TemplateDao
    abstract fun pendingResultDao(): PendingResultDao
}
