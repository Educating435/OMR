package com.mycompany.omrscanner.camera

import android.content.Context
import dagger.hilt.android.qualifiers.ApplicationContext
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class CameraCaptureCoordinator @Inject constructor(
    @ApplicationContext private val context: Context,
) {
    fun latestCapturedImagePath(): String {
        return "${context.filesDir.absolutePath}/scans/latest-scan.jpg"
    }
}
