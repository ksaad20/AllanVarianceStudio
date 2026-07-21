// android/app/src/main/java/com/allanvariancestudio/data/SensorRecord.kt
package com.allanvariancestudio.data

data class SensorRecord(
    val timestamp: Long,           // nanoseconds (event.timestamp)
    val sensorType: Int,           // Sensor.TYPE_*
    val values: FloatArray,        // raw sensor values (x, y, z, etc.)
    val accuracy: Int,           // SENSOR_STATUS_*
    val temperature: Float = 0f   // device temperature if available
) {
    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (javaClass != other?.javaClass) return false
        other as SensorRecord
        return timestamp == other.timestamp &&
               sensorType == other.sensorType &&
               values.contentEquals(other.values) &&
               accuracy == other.accuracy &&
               temperature == other.temperature
    }

    override fun hashCode(): Int {
        var result = timestamp.hashCode()
        result = 31 * result + sensorType
        result = 31 * result + values.contentHashCode()
        result = 31 * result + accuracy
        result = 31 * result + temperature.hashCode()
        return result
    }

    fun toCsvRow(): String {
        return "$timestamp,$sensorType,${values.joinToString(",")},$accuracy,$temperature"
    }

    companion object {
        fun csvHeader(numValues: Int): String {
            val valueHeaders = (1..numValues).joinToString(",") { "v$it" }
            return "timestamp,sensorType,$valueHeaders,accuracy,temperature"
        }
    }
}
