package com.mycompany.omrscanner.core.network

import com.jakewharton.retrofit2.converter.kotlinx.serialization.asConverterFactory
import com.mycompany.omrscanner.data.local.SecureSessionStore
import com.mycompany.omrscanner.data.remote.OMRApiService
import com.mycompany.omrscanner.data.remote.RefreshRequestDto
import kotlinx.serialization.json.Json
import okhttp3.Authenticator
import okhttp3.Interceptor
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.Response
import okhttp3.Route
import retrofit2.Retrofit
import javax.inject.Inject
import javax.inject.Singleton
import kotlinx.coroutines.runBlocking

@Singleton
class AuthTokenInterceptor @Inject constructor(
    private val secureSessionStore: SecureSessionStore,
) : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val token = secureSessionStore.read()?.accessToken
        val request = if (token.isNullOrBlank()) {
            chain.request()
        } else {
            chain.request().newBuilder().header("Authorization", "Bearer $token").build()
        }
        return chain.proceed(request)
    }
}

@Singleton
class TokenRefreshAuthenticator @Inject constructor(
    private val secureSessionStore: SecureSessionStore,
    private val json: Json,
) : Authenticator {
    override fun authenticate(route: Route?, response: Response): Request? {
        if (response.request.url.encodedPath.contains("/auth/refresh")) {
            return null
        }
        val current = secureSessionStore.read() ?: return null
        val refreshApi = Retrofit.Builder()
            .baseUrl(NetworkConfig.BASE_URL)
            .client(OkHttpClient.Builder().build())
            .addConverterFactory(json.asConverterFactory("application/json".toMediaType()))
            .build()
            .create(OMRApiService::class.java)

        val refreshed = runCatching { runBlocking { refreshApi.refresh(RefreshRequestDto(current.refreshToken)) } }.getOrNull()
        return if (refreshed == null) {
            secureSessionStore.clear()
            null
        } else {
            secureSessionStore.save(
                com.mycompany.omrscanner.domain.model.UserSession(
                    accessToken = refreshed.access_token,
                    refreshToken = refreshed.refresh_token,
                    role = com.mycompany.omrscanner.core.model.UserRole.valueOf(refreshed.user_role.uppercase()),
                )
            )
            response.request.newBuilder()
                .header("Authorization", "Bearer ${refreshed.access_token}")
                .build()
        }
    }
}
