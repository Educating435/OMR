package com.mycompany.omrscanner.data.remote

import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Query

interface OmrApiService {
    @POST("auth/login")
    suspend fun login(@Body payload: LoginRequestDto): LoginResponseDto

    @GET("exams")
    suspend fun listExams(): List<ExamDto>

    @GET("templates")
    suspend fun listTemplates(@Query("exam_id") examId: String): List<TemplateDto>

    @POST("results/sync")
    suspend fun syncResult(@Body payload: SyncResultRequestDto)
}
