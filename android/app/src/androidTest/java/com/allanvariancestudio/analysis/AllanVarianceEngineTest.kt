package com.allanvariancestudio.data

import org.junit.Test
import org.junit.Assert.*

class SensorRecordTest {

    @Test
    fun testCreation() {
        val record = SensorRecord(
            timestamp = 1000000000L,
            sensorType = 16, // TYPE_GYROSCOPE_UNCALIBRATED
            values = floatArrayOf(0.1f, 0.2f, 0.3f),
            accuracy = 3
        )

        assertEquals(1000000000L, record.timestamp)
        assertEquals(16, record.sensorType)
        assertEquals(3, record.values.size)
        assertEquals(3, record.accuracy)
        assertEquals(0.0f, record.temperature, 0.001f)
    }

    @Test
    fun testCsvRow() {
        val record = SensorRecord(
            timestamp = 1000000000L,
            sensorType = 16,
            values = floatArrayOf(0.1f, 0.2f, 0.3f),
            accuracy = 3,
            temperature = 35.5f
        )

        val csv = record.toCsvRow()
        assertTrue(csv.contains("1000000000"))
        assertTrue(csv.contains("16"))
        assertTrue(csv.contains("0.1"))
        assertTrue(csv.contains("35.5"))
    }

    @Test
    fun testCsvHeader() {
        val header = SensorRecord.csvHeader(3)
        assertTrue(header.contains("timestamp"))
        assertTrue(header.contains("sensorType"))
        assertTrue(header.contains("v1"))
        assertTrue(header.contains("v3"))
        assertTrue(header.contains("accuracy"))
        assertTrue(header.contains("temperature"))
    }

    @Test
    fun testEquals() {
        val record1 = SensorRecord(
            timestamp = 1000000000L,
            sensorType = 16,
            values = floatArrayOf(0.1f, 0.2f, 0.3f),
            accuracy = 3
        )

        val record2 = SensorRecord(
            timestamp = 1000000000L,
            sensorType = 16,
            values = floatArrayOf(0.1f, 0.2f, 0.3f),
            accuracy = 3
        )

        assertEquals(record1, record2)
        assertEquals(record1.hashCode(), record2.hashCode())
    }

    @Test
    fun testNotEquals() {
        val record1 = SensorRecord(
            timestamp = 1000000000L,
            sensorType = 16,
            values = floatArrayOf(0.1f, 0.2f, 0.3f),
            accuracy = 3
        )

        val record2 = SensorRecord(
            timestamp = 2000000000L,
            sensorType = 16,
            values = floatArrayOf(0.1f, 0.2f, 0.3f),
            accuracy = 3
        )

        assertNotEquals(record1, record2)
    }

    @Test
    fun testTemperatureDefault() {
        val record = SensorRecord(
            timestamp = 1000000000L,
            sensorType = 16,
            values = floatArrayOf(0.1f),
            accuracy = 3
        )

        assertEquals(0.0f, record.temperature, 0.001f)
    }
}
