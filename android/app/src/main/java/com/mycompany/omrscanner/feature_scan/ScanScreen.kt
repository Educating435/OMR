package com.mycompany.omrscanner.feature_scan

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.Row
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.mycompany.omrscanner.core.ui.AppSectionHeader
import com.mycompany.omrscanner.core.ui.AppTopBar
import com.mycompany.omrscanner.core.ui.EmptyState
import com.mycompany.omrscanner.core.ui.FilterChipTag
import com.mycompany.omrscanner.core.ui.InfoRow
import com.mycompany.omrscanner.core.ui.PremiumCard
import com.mycompany.omrscanner.core.ui.ResultBreakdownCard
import com.mycompany.omrscanner.core.ui.ReviewFlagChip
import com.mycompany.omrscanner.core.ui.ScanInstructionBanner
import com.mycompany.omrscanner.core.ui.SearchBar
import com.mycompany.omrscanner.core.ui.StatTile
import com.mycompany.omrscanner.core.ui.SyncStateIndicator

@Composable
fun ScanScreen(
    state: ScanUiState,
    onProcessScan: () -> Unit,
    modifier: Modifier = Modifier,
) {
    Column(
        modifier = modifier.fillMaxSize(),
        verticalArrangement = Arrangement.spacedBy(18.dp),
    ) {
        AppTopBar(
            eyebrow = "Scanner Console",
            title = "Controlled OMR Capture",
            subtitle = "Designed for institute staff working under fast classroom conditions.",
        )

        ScanInstructionBanner(
            title = "Before scanning",
            body = "Keep the full A4 sheet visible, avoid glare, and align all four corner markers inside the frame.",
        }

        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            FilterChipTag(label = "50 Questions", selected = true)
            FilterChipTag(label = "A4 Portrait", selected = true)
            FilterChipTag(label = "Offline Ready", selected = true)
        }

        PremiumCard {
            AppSectionHeader("Session Snapshot", "Fast overview for scanner operators")
            StatTile("Pending Sync", state.pendingSyncCount.toString())
            StatTile("Local Queue", state.queueCount.toString(), tone = MaterialTheme.colorScheme.secondary)
            SyncStateIndicator(state.pendingSyncCount)
        }

        PremiumCard {
            AppSectionHeader("Scan Action", "Start a guided scan flow and process on device")
            SearchBar(value = "", placeholder = "Selected exam template")
            InfoRow("Mode", "Controlled-template OMR")
            InfoRow("Storage", "App-private scan storage")
            Button(onClick = onProcessScan, enabled = !state.isProcessing, modifier = Modifier.padding(top = 8.dp)) {
                Text(if (state.isProcessing) "Processing scan..." else "Start Scan")
            }
        }

        ResultBreakdownCard(
            score = state.lastSummary.substringBefore(" | ").ifBlank { "No result yet" },
            flagged = state.warning != null,
            summary = state.lastSummary,
        )

        if (state.warning != null) {
            PremiumCard {
                AppSectionHeader("Attention Needed")
                ReviewFlagChip(flagged = true)
                Text(
                    state.warning,
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.error,
                )
            }
        } else {
            EmptyState(
                title = "No active review flag",
                body = "Clean reads and synced states will appear here for staff confidence during bulk scanning.",
            )
        }
    }
}
