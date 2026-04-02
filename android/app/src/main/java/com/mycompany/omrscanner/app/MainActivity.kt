package com.mycompany.omrscanner.app

import android.Manifest
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.mycompany.omrscanner.app.navigation.AppNavigation
import com.mycompany.omrscanner.core.ui.AppSectionHeader
import com.mycompany.omrscanner.core.ui.PermissionRationaleDialog
import com.mycompany.omrscanner.core.ui.PremiumCard
import com.mycompany.omrscanner.core.ui.ScanInstructionBanner
import com.mycompany.omrscanner.core.ui.OMRTheme
import com.mycompany.omrscanner.feature_scan.ScanViewModel
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            OMRTheme {
                OMRApp()
            }
        }
    }
}

@Composable
private fun OMRApp(viewModel: ScanViewModel = hiltViewModel()) {
    var cameraGranted by remember { mutableStateOf(false) }
    var showRationale by remember { mutableStateOf(false) }
    val permissionLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.RequestPermission(),
        onResult = { cameraGranted = it }
    )

    if (showRationale) {
        PermissionRationaleDialog(
            title = "Camera access for OMR scanning",
            body = "The camera is used only to capture institute-generated OMR sheets. Images stay in app-private storage unless you explicitly export them.",
            onDismiss = { showRationale = false },
            onContinue = {
                showRationale = false
                permissionLauncher.launch(Manifest.permission.CAMERA)
            },
        )
    }

    Scaffold { padding ->
        if (cameraGranted) {
            ScanHost(padding, viewModel)
        } else {
            PermissionScreen(padding) { showRationale = true }
        }
    }
}

@Composable
private fun ScanHost(padding: PaddingValues, viewModel: ScanViewModel) {
    AppNavigation(
        scanState = viewModel.uiState,
        onProcessScan = viewModel::processDemoScan,
        modifier = Modifier
            .fillMaxSize()
            .padding(padding)
            .padding(24.dp),
    )
}

@Composable
private fun PermissionScreen(padding: PaddingValues, onGrant: () -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(padding)
            .padding(24.dp),
        horizontalAlignment = Alignment.Start,
        verticalArrangement = Arrangement.Center
    ) {
        PremiumCard {
            AppSectionHeader(
                title = "Scanner access",
                subtitle = "Camera permission is requested only when you choose to start scanning.",
            )
            ScanInstructionBanner(
                title = "Privacy-friendly by default",
                body = "No broad media permission is requested. Captured scans stay in app-private storage unless an export workflow is introduced later.",
                tone = MaterialTheme.colorScheme.secondary,
            )
            Text(
                "Use the scanner to capture only institute-generated templates with fixed markers and QR metadata.",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Button(onClick = onGrant, modifier = Modifier.padding(top = 8.dp)) {
                Text("Continue to camera")
            }
        }
    }
}
