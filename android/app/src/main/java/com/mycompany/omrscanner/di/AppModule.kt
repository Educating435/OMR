package com.mycompany.omrscanner.di

import android.content.Context
import androidx.room.Room
import androidx.work.WorkManager
import com.jakewharton.retrofit2.converter.kotlinx.serialization.asConverterFactory
import com.mycompany.omrscanner.data.local.OmrDatabase
import com.mycompany.omrscanner.data.remote.OmrApiService
import com.mycompany.omrscanner.data.repository.AuthRepositoryImpl
import com.mycompany.omrscanner.data.repository.ExamRepositoryImpl
import com.mycompany.omrscanner.data.repository.ResultRepositoryImpl
import com.mycompany.omrscanner.data.repository.ScanRepositoryImpl
import com.mycompany.omrscanner.domain.repository.AuthRepository
import com.mycompany.omrscanner.domain.repository.ExamRepository
import com.mycompany.omrscanner.domain.repository.ResultRepository
import com.mycompany.omrscanner.domain.repository.ScanRepository
import dagger.Binds
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import kotlinx.serialization.json.Json
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import javax.inject.Singleton

private const val API_BASE_URL = "http://10.0.2.2:8000/api/v1/"

@Module
@InstallIn(SingletonComponent::class)
object AppModule {
    @Provides
    @Singleton
    fun provideJson(): Json = Json {
        ignoreUnknownKeys = true
        explicitNulls = false
    }

    @Provides
    @Singleton
    fun provideOkHttpClient(): OkHttpClient {
        val logging = HttpLoggingInterceptor().apply {
            level = HttpLoggingInterceptor.Level.BASIC
        }
        return OkHttpClient.Builder()
            .addInterceptor(logging)
            .build()
    }

    @Provides
    @Singleton
    fun provideRetrofit(okHttpClient: OkHttpClient, json: Json): Retrofit =
        Retrofit.Builder()
            .baseUrl(API_BASE_URL)
            .client(okHttpClient)
            .addConverterFactory(json.asConverterFactory("application/json".toMediaType()))
            .build()

    @Provides
    @Singleton
    fun provideOmrApiService(retrofit: Retrofit): OmrApiService =
        retrofit.create(OmrApiService::class.java)

    @Provides
    @Singleton
    fun provideDatabase(@ApplicationContext context: Context): OmrDatabase =
        Room.databaseBuilder(context, OmrDatabase::class.java, "omr_scanner.db").build()

    @Provides
    @Singleton
    fun provideWorkManager(@ApplicationContext context: Context): WorkManager = WorkManager.getInstance(context)
}

@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {
    @Binds
    abstract fun bindAuthRepository(impl: AuthRepositoryImpl): AuthRepository

    @Binds
    abstract fun bindExamRepository(impl: ExamRepositoryImpl): ExamRepository

    @Binds
    abstract fun bindResultRepository(impl: ResultRepositoryImpl): ResultRepository

    @Binds
    abstract fun bindScanRepository(impl: ScanRepositoryImpl): ScanRepository
}
