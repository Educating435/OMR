package com.mycompany.omrscanner.app.navigation

import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import com.mycompany.omrscanner.feature_scan.ScanScreen
import com.mycompany.omrscanner.feature_scan.ScanUiState

@Composable
fun AppNavigation(
    scanState: ScanUiState,
    onProcessScan: () -> Unit,
    modifier: Modifier = Modifier,
) {
    ScanScreen(
        state = scanState,
        onProcessScan = onProcessScan,
        modifier = modifier,
    )
}

