package com.mycompany.omrscanner.exam

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.runtime.Composable

@Composable
fun ExamScreen(modifier: Modifier = Modifier) {
    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        Text("Exam cache", style = MaterialTheme.typography.headlineMedium)
        Text("IMPLEMENTED: exam and template data are intended to be cached in Room for offline use.")
        Text("TODO NEXT: connect this screen to repository-backed state and exam selection.")
    }
}
