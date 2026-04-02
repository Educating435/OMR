package com.mycompany.omrscanner.core.util

import kotlinx.serialization.json.Json

inline fun <reified T> Json.encode(value: T): String = encodeToString(value)

inline fun <reified T> Json.decode(value: String): T = decodeFromString(value)

