package com.mycompany.omrscanner.data.local

import android.content.Context
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey
import com.mycompany.omrscanner.core.model.UserRole
import com.mycompany.omrscanner.domain.model.UserSession
import dagger.hilt.android.qualifiers.ApplicationContext
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class SecureSessionStore @Inject constructor(
    @ApplicationContext context: Context,
) {
    private val masterKey = MasterKey.Builder(context).setKeyScheme(MasterKey.KeyScheme.AES256_GCM).build()
    private val prefs = EncryptedSharedPreferences.create(
        context,
        "secure_session",
        masterKey,
        EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
        EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM,
    )

    fun save(session: UserSession) {
        prefs.edit()
            .putString("access_token", session.accessToken)
            .putString("refresh_token", session.refreshToken)
            .putString("role", session.role.name)
            .apply()
    }

    fun read(): UserSession? {
        val accessToken = prefs.getString("access_token", null) ?: return null
        val refreshToken = prefs.getString("refresh_token", null) ?: return null
        val role = prefs.getString("role", UserRole.VIEWER.name) ?: UserRole.VIEWER.name
        return UserSession(accessToken = accessToken, refreshToken = refreshToken, role = UserRole.valueOf(role))
    }

    fun clear() {
        prefs.edit().clear().apply()
    }
}
