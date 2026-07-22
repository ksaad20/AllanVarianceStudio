# Smartphone Inertial Sensor Calibration Guide

> **Project:** Open-Source IEEE Std 1293-2018 Compliant Allan Variance Characterization Platform
>
> **Application:** Consumer Smartphone Inertial Sensors for Parkinsonian Tremor Research
>
> **Version:** 1.0

---

# Purpose

This guide describes the recommended calibration procedures before collecting inertial sensor data for:

- Allan variance characterization
- Sensor noise analysis
- Tremor assessment
- Parkinsonian motion analysis
- Research-grade reproducibility

Calibration minimizes deterministic sensor errors before stochastic noise characterization.

---

# Calibration Philosophy

Calibration removes systematic errors.

Allan variance characterizes stochastic errors.

These procedures are complementary.

---

# Sensors Covered

- Accelerometer
- Gyroscope
- Magnetometer (optional)
- Gravity Sensor
- Linear Acceleration
- Rotation Vector

Primary analysis uses:

- Accelerometer
- Gyroscope

---

# Environmental Requirements

## Stable Surface

The smartphone should rest on:

- Granite table
- Optical breadboard
- Thick wooden desk
- Concrete surface

Avoid:

- Soft beds
- Foam
- Cushions
- Human hand
- Vibrating desks

---

## Temperature

Recommended:

20–25 °C

Avoid:

- Direct sunlight
- Charging during acquisition
- High CPU load
- Hot environments

Temperature affects MEMS bias stability.

---

## Device Preparation

Before calibration:

✓ Disable battery saver

✓ Enable Airplane Mode (recommended)

✓ Disable automatic updates

✓ Disable screen rotation

✓ Close background applications

✓ Disable vibration

✓ Disable notifications

✓ Restart device if needed

---

# Accelerometer Calibration

## Six-Position Static Calibration

The device should be placed motionless in six orientations.

1. Screen Up

2. Screen Down

3. Left Side Down

4. Right Side Down

5. Top Edge Down

6. Bottom Edge Down

Each position:

Minimum:

60 seconds

Recommended:

120 seconds

Research-grade:

300 seconds

---

## Expected Reading

One axis should measure approximately:

±9.81 m/s²

Remaining axes:

Approximately zero.

---

## Calibration Outputs

Estimate:

- Bias
- Scale factor
- Axis offset
- Cross-axis sensitivity (optional)

---

# Gyroscope Calibration

Place device completely motionless.

Recommended duration:

300–1800 seconds

Do not touch the device.

Estimate:

- Zero-rate bias
- Bias drift
- Noise floor

This dataset is also suitable for Allan variance.

---

# Magnetometer Calibration (Optional)

Perform figure-eight motion.

Repeat:

20–30 seconds

Estimate:

- Hard iron distortion
- Soft iron distortion

Not required for tremor analysis.

---

# Sampling Rate Verification

The application automatically verifies:

- Mean sampling frequency
- Timestamp consistency
- Missing samples
- Jitter
- Effective sampling rate

Recommended:

100–400 Hz

Actual sampling frequency should always be reported.

---

# Allan Variance Dataset

For IEEE-style noise characterization:

Recommended duration:

30–60 minutes

Minimum:

10 minutes

Preferred:

2 hours

Device must remain completely motionless.

---

# Motion Artifact Check

Before acquisition:

Verify:

- No touching
- No table vibration
- No nearby machinery
- No footsteps
- No cable movement

Any disturbance should invalidate that recording segment.

---

# Sensor Saturation Check

Verify:

Accelerometer

No clipping.

Gyroscope

No clipping.

All saturated recordings should be discarded.

---

# Data Quality Metrics

The application automatically reports:

- Sampling frequency
- Sample count
- Missing packets
- Timestamp jitter
- Mean acceleration
- Mean angular velocity
- Standard deviation
- Allan deviation
- Bias instability
- Angle random walk
- Rate random walk

---

# Parkinsonian Tremor Acquisition

## Patient Position

Recommended:

Seated comfortably.

Feet supported.

Back supported.

Hands relaxed.

---

## Rest Tremor

Patient rests hands comfortably.

Duration:

30–60 seconds

---

## Postural Tremor

Patient extends arms horizontally.

Duration:

30–60 seconds

---

## Kinetic Tremor

Patient performs standardized movement.

Examples:

- Finger-to-nose
- Wrist rotation
- Drinking task

---

## Walking Assessment

Phone location should remain consistent.

Examples:

- Trouser pocket
- Waist clip
- Chest harness

Placement must be recorded.

---

# Phone Placement

Record:

- Device model
- Manufacturer
- Android version
- Sensor vendor
- Sensor name
- Sampling frequency
- Placement location
- Orientation

---

# Metadata

Every recording should include:

- Anonymous participant ID
- Recording date
- Sensor type
- Device model
- Firmware version
- Battery level
- Temperature (if available)
- Sampling frequency
- Recording duration

---

# Recommended Dataset Structure

```
participant_001/

    calibration/

        accelerometer/

        gyroscope/

    tremor/

        rest/

        postural/

        kinetic/

    metadata.json
```

---

# Quality Control Checklist

Before recording:

✓ Device restarted

✓ Battery >50%

✓ Stable temperature

✓ Stable surface

✓ Correct sampling frequency

✓ Calibration completed

✓ Sensor availability verified

✓ Storage available

✓ Airplane Mode enabled

✓ Background applications closed

---

# Research Reporting Recommendations

Publications should report:

- Smartphone model
- Operating system
- Sensor manufacturer
- Sampling frequency
- Calibration protocol
- Recording duration
- Allan variance averaging times
- Noise parameters
- Environmental conditions
- Participant posture
- Phone placement

These details improve reproducibility across studies.

---

# Limitations

Consumer smartphones are not laboratory-grade inertial instruments.

Measurements may vary across:

- Manufacturers
- Sensor vendors
- Firmware versions
- Operating systems
- Sampling implementations

Cross-device validation is recommended before combining data from multiple smartphone models.

---

# Ethical Considerations

For human participant studies:

- Obtain ethics committee/IRB approval where required.
- Obtain informed consent from all participants.
- Store only de-identified data.
- Follow applicable privacy regulations (e.g., GDPR, HIPAA, or local requirements).
- Clearly document data retention and sharing policies.

---

# References

- IEEE Std 1293-2018
- IEEE Standard Specification Format Guide and Test Procedure for Linear, Single-Axis, Nongyroscopic Accelerometers
- NIST Technical Notes on Allan Variance
- IEEE Standards on Inertial Sensor Characterization
