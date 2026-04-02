package com.mycompany.omrscanner.app.navigation

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.mycompany.omrscanner.auth.AuthScreen
import com.mycompany.omrscanner.exam.ExamScreen
import com.mycompany.omrscanner.history.HistoryScreen
import com.mycompany.omrscanner.result.ResultScreen
import com.mycompany.omrscanner.scanner.ScannerScreen
import com.mycompany.omrscanner.settings.SettingsScreen

@Composable
fun AppNavigation(
    hasCameraPermission: Boolean,
    requestCameraPermission: () -> Unit,
) {
    val tabs = listOf("Auth", "Exams", "Scan", "Results", "History", "Settings")
    var selectedIndex by remember { mutableIntStateOf(0) }

    Scaffold(
        bottomBar = {
            NavigationBar {
                tabs.forEachIndexed { index, label ->
                    NavigationBarItem(
                        selected = selectedIndex == index,
                        onClick = { selectedIndex = index },
                        icon = { Text(label.take(1)) },
                        label = { Text(label) },
                    )
                }
            }
        },
    ) { padding ->
        when (selectedIndex) {
            0 -> AuthScreen(modifier = Modifier.padding(padding))
            1 -> ExamScreen(modifier = Modifier.padding(padding))
            2 ->
                if (hasCameraPermission) {
                    ScannerScreen(modifier = Modifier.padding(padding))
                } else {
                    CameraPermissionScreen(modifier = Modifier.padding(padding), onRequestPermission = requestCameraPermission)
                }

            3 -> ResultScreen(modifier = Modifier.padding(padding))
            4 -> HistoryScreen(modifier = Modifier.padding(padding))
            else -> SettingsScreen(modifier = Modifier.padding(padding))
        }
    }
}

@Composable
private fun CameraPermissionScreen(
    modifier: Modifier = Modifier,
    onRequestPermission: () -> Unit,
) {
    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center,
    ) {
        Text("Camera access is required to capture controlled OMR sheets.", style = MaterialTheme.typography.titleMedium)
        Text(
            "The Android app reads bubbles on-device and syncs results later through FastAPI.",
            modifier = Modifier.padding(top = 12.dp, bottom = 20.dp),
            style = MaterialTheme.typography.bodyMedium,
        )
        Button(onClick = onRequestPermission) {
            Text("Grant camera access")
        }
    }
}
