package com.mycompany.omrscanner.di

import android.content.Context
import androidx.room.Room
import androidx.work.WorkManager
import com.jakewharton.retrofit2.converter.kotlinx.serialization.asConverterFactory
import com.mycompany.omrscanner.core.network.AuthTokenInterceptor
import com.mycompany.omrscanner.core.network.NetworkConfig
import com.mycompany.omrscanner.core.network.TokenRefreshAuthenticator
import com.mycompany.omrscanner.data.local.CacheDao
import com.mycompany.omrscanner.data.local.OMRDatabase
import com.mycompany.omrscanner.data.local.ScanAttemptDao
import com.mycompany.omrscanner.data.local.SyncQueueDao
import com.mycompany.omrscanner.data.remote.OMRApiService
import com.mycompany.omrscanner.data.repository.AuthRepositoryImpl
import com.mycompany.omrscanner.data.repository.ExamRepositoryImpl
import com.mycompany.omrscanner.data.repository.ScanRepositoryImpl
import com.mycompany.omrscanner.domain.repository.AuthRepository
import com.mycompany.omrscanner.domain.repository.ExamRepository
import com.mycompany.omrscanner.domain.repository.ScanRepository
import com.mycompany.omrscanner.omr.pipeline.DefaultOMRProcessor
import com.mycompany.omrscanner.omr.pipeline.OMRProcessor
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
    fun provideOkHttpClient(
        authTokenInterceptor: AuthTokenInterceptor,
        tokenRefreshAuthenticator: TokenRefreshAuthenticator,
    ): OkHttpClient {
        val logging = HttpLoggingInterceptor().apply {
            level = HttpLoggingInterceptor.Level.BODY
        }
        return OkHttpClient.Builder()
            .addInterceptor(authTokenInterceptor)
            .authenticator(tokenRefreshAuthenticator)
            .addInterceptor(logging)
            .build()
    }

    @Provides
    @Singleton
    fun provideRetrofit(okHttpClient: OkHttpClient, json: Json): Retrofit {
        return Retrofit.Builder()
            .baseUrl(NetworkConfig.BASE_URL)
            .client(okHttpClient)
            .addConverterFactory(json.asConverterFactory("application/json".toMediaType()))
            .build()
    }

    @Provides
    @Singleton
    fun provideApi(retrofit: Retrofit): OMRApiService = retrofit.create(OMRApiService::class.java)

    @Provides
    @Singleton
    fun provideDatabase(@ApplicationContext context: Context): OMRDatabase {
        return Room.databaseBuilder(context, OMRDatabase::class.java, "omr_scanner.db").build()
    }

    @Provides
    fun provideScanAttemptDao(database: OMRDatabase): ScanAttemptDao = database.scanAttemptDao()

    @Provides
    fun provideCacheDao(database: OMRDatabase): CacheDao = database.cacheDao()

    @Provides
    fun provideSyncQueueDao(database: OMRDatabase): SyncQueueDao = database.syncQueueDao()

    @Provides
    @Singleton
    fun provideWorkManager(@ApplicationContext context: Context): WorkManager = WorkManager.getInstance(context)
}

@Module
@InstallIn(SingletonComponent::class)
abstract class BindingModule {
    @Binds
    abstract fun bindAuthRepository(impl: AuthRepositoryImpl): AuthRepository

    @Binds
    abstract fun bindExamRepository(impl: ExamRepositoryImpl): ExamRepository

    @Binds
    abstract fun bindScanRepository(impl: ScanRepositoryImpl): ScanRepository

    @Binds
    abstract fun bindOmrPipeline(impl: DefaultOMRProcessor): OMRProcessor
}
