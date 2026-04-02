package com.mycompany.omrscanner.core.ui

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.ColorScheme
import androidx.compose.material3.Typography
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp

private val Indigo = Color(0xFF2447B8)
private val IndigoDark = Color(0xFF17337F)
private val Teal = Color(0xFF0E8C83)
private val Surface = Color(0xFFF7F8FB)
private val SurfaceAlt = Color(0xFFEEF2F8)
private val Ink = Color(0xFF162033)
private val Error = Color(0xFFC83C4A)
private val Warning = Color(0xFFC9871A)

private val LightColors: ColorScheme = lightColorScheme(
    primary = Indigo,
    onPrimary = Color.White,
    primaryContainer = Color(0xFFDDE5FF),
    onPrimaryContainer = IndigoDark,
    secondary = Teal,
    onSecondary = Color.White,
    secondaryContainer = Color(0xFFD7F4EF),
    onSecondaryContainer = Color(0xFF0A4C47),
    error = Error,
    onError = Color.White,
    errorContainer = Color(0xFFFDE0E3),
    onErrorContainer = Color(0xFF5B1018),
    background = Surface,
    onBackground = Ink,
    surface = Color.White,
    onSurface = Ink,
    surfaceVariant = SurfaceAlt,
    onSurfaceVariant = Color(0xFF586174),
    outline = Color(0xFFCAD1DF),
)

private val DarkColors: ColorScheme = darkColorScheme(
    primary = Color(0xFFB8C7FF),
    secondary = Color(0xFF8CE0D8),
    background = Color(0xFF11151D),
    surface = Color(0xFF171C25),
    onSurface = Color(0xFFF3F6FB),
)

private val AppTypography = Typography(
    headlineLarge = TextStyle(fontFamily = FontFamily.SansSerif, fontWeight = FontWeight.Bold, fontSize = 30.sp, lineHeight = 36.sp),
    headlineMedium = TextStyle(fontFamily = FontFamily.SansSerif, fontWeight = FontWeight.Bold, fontSize = 24.sp, lineHeight = 30.sp),
    titleLarge = TextStyle(fontFamily = FontFamily.SansSerif, fontWeight = FontWeight.SemiBold, fontSize = 20.sp, lineHeight = 26.sp),
    titleMedium = TextStyle(fontFamily = FontFamily.SansSerif, fontWeight = FontWeight.SemiBold, fontSize = 16.sp, lineHeight = 22.sp),
    bodyLarge = TextStyle(fontFamily = FontFamily.SansSerif, fontWeight = FontWeight.Normal, fontSize = 16.sp, lineHeight = 24.sp),
    bodyMedium = TextStyle(fontFamily = FontFamily.SansSerif, fontWeight = FontWeight.Normal, fontSize = 14.sp, lineHeight = 20.sp),
    labelLarge = TextStyle(fontFamily = FontFamily.SansSerif, fontWeight = FontWeight.Medium, fontSize = 14.sp, lineHeight = 20.sp),
)

@Composable
fun OMRTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = if (isSystemInDarkTheme()) DarkColors else LightColors,
        typography = AppTypography,
        content = content,
    )
}
