package com.mycompany.omrscanner.data.remote

import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.PATCH
import retrofit2.http.POST
import retrofit2.http.Path

interface OMRApiService {
    @POST("/api/v1/auth/login")
    suspend fun login(@Body request: LoginRequestDto): TokenResponseDto

    @POST("/api/v1/auth/refresh")
    suspend fun refresh(@Body request: RefreshRequestDto): TokenResponseDto

    @GET("/api/v1/exams")
    suspend fun exams(): PaginatedResponseDto<ExamDto>

    @GET("/api/v1/templates/{examId}")
    suspend fun templates(@Path("examId") examId: String): List<TemplateDto>

    @POST("/api/v1/scans/submit")
    suspend fun submitScan(@Body request: ScanSubmissionRequest)

    @GET("/api/v1/review/flagged")
    suspend fun flaggedScans(): List<ReviewItemDto>

    @PATCH("/api/v1/review/{attemptId}")
    suspend fun markReviewed(
        @Path("attemptId") attemptId: String,
        @Body body: Map<String, @JvmSuppressWildcards Any?>,
    )
}
