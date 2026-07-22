# Clinical Study Protocol

## Allan Variance Studio — Parkinsonian Tremor Detection Validation

**Protocol Version:** 1.0  
**Date:** 2026-07-22  
**Device Platform:** Android (Consumer Smartphone IMU)  
**Compliance:** IEEE Std 1293-2018 (Inertial Sensor Characterization)

---

## 1. Study Overview

### 1.1 Purpose
This protocol defines the standardized procedure for collecting inertial sensor data from Parkinson's disease (PD) patients and healthy controls using the Allan Variance Studio Android application. The goal is to validate the platform's tremor detection pipeline against clinical gold standards.

### 1.2 Background
Consumer smartphone IMUs (Inertial Measurement Units) are increasingly used for biological motion analysis in neurology. Factory calibration assumes ideal conditions and typically underestimates angle random walk and bias instability by 2–3×. This platform provides rigorous IEEE Std 1293-2018 compliant Allan variance characterization to enable clinically meaningful tremor quantification.

### 1.3 Study Design
- **Type:** Prospective, observational, case-control validation study
- **Duration:** 6 months
- **Sites:** Multiple neurology clinics
- **Ethics:** IRB approval required at each site

---

## 2. Objectives

### 2.1 Primary Objective
Validate that smartphone-derived tremor metrics (frequency, amplitude, RMS acceleration) correlate with clinical tremor rating scales (MDS-UPDRS Part III, Fahn-Tolosa-Marin Tremor Rating Scale).

### 2.2 Secondary Objectives
- Assess inter-rater reliability of automated tremor detection vs. neurologist assessment
- Determine optimal sensor sampling configuration for clinical use
- Validate noise model parameters (Q, N, B, K, R) against laboratory-grade IMU reference
- Evaluate patient compliance and usability of the recording protocol

---

## 3. Study Population

### 3.1 Inclusion Criteria

**Parkinson's Disease Group:**
- Confirmed PD diagnosis per UK Parkinson's Disease Society Brain Bank criteria
- Hoehn & Yahr stage I–IV
- Presence of rest tremor on clinical examination
- Age 18–85 years
- Able to provide informed consent

**Healthy Control Group:**
- No known neurological disorder
- Age- and sex-matched to PD group (±5 years)
- Able to provide informed consent

### 3.2 Exclusion Criteria
- Severe dyskinesia interfering with tremor assessment
- Deep brain stimulation (DBS) or other implanted neurostimulation device
- Active psychosis or dementia precluding informed consent
- Upper extremity amputation or severe arthritis affecting hand posture
- Current participation in another interventional tremor study

### 3.3 Sample Size
- **Target enrollment:** 120 participants (60 PD, 60 healthy controls)
- **Power calculation:** Based on detecting ≥0.5 correlation between automated tremor amplitude and MDS-UPDRS item 3.17 (rest tremor) with 90% power at α=0.05

---

## 4. Device & Sensor Configuration

### 4.1 Hardware Requirements
- **Primary device:** Android smartphone with API level 24+ (Android 7.0+)
- **Minimum IMU specifications:**
  - Accelerometer: tri-axial, ≥200 Hz sampling
  - Gyroscope: tri-axial, ≥200 Hz sampling
  - Magnetometer: tri-axial (optional, for orientation correction)
- **Recommended devices:** Samsung Galaxy S21+, Google Pixel 7, or equivalent with verified IMU performance

### 4.2 Allan Variance Studio Configuration

| Parameter | Clinical Recording Mode | Validation Mode |
|-----------|------------------------|-----------------|
| Sampling Rate | 500 Hz (hardware-limited max) | 500 Hz |
| Recording Duration | 60 seconds per trial | 300 seconds per trial |
| Sensor Fusion | Raw sensor output (no fusion) | Raw sensor output |
| Axis Selection | All 6 axes (3 accel + 3 gyro) | All 6 axes |
| Storage Format | Binary + CSV export | Binary + CSV + MATLAB |
| Real-time Display | Tremor amplitude + frequency | Full Allan deviation plot |

### 4.3 Pre-Study Device Characterization
Before clinical deployment, each device must undergo:
1. **Static Allan variance test:** 6-hour static recording to compute noise parameters (Q, N, B, K, R)
2. **Dynamic validation:** Comparison with laboratory-grade IMU (e.g., XSens MTi-30) during known sinusoidal motion
3. **Temperature drift assessment:** Characterization across 15°C–40°C operating range
4. **Pass criteria:**
   - Angle random walk (N) within ±20% of manufacturer spec
   - Bias instability (B) within ±30% of manufacturer spec
   - Correlation with reference IMU ≥0.95 for tremor-frequency motion (3–8 Hz)

---

## 5. Clinical Procedures

### 5.1 Pre-Recording Setup
1. **Device preparation:**
   - Charge battery to ≥80%
   - Close all background applications
   - Enable airplane mode (WiFi/Bluetooth may remain on for data sync)
   - Disable auto-rotate and screen timeout

2. **Patient preparation:**
   - Rest 10 minutes in quiet room before recording
   - Remove watches, bracelets, or other wrist-worn devices
   - Record ambient temperature and humidity
   - Document patient's medication status (time since last levodopa dose)

3. **Device mounting:**
   - **Hand tremor:** Secure smartphone to dorsal hand using adjustable Velcro strap (provided)
   - Position: Long axis aligned with middle metacarpal, screen facing dorsum
   - **Alternative (forearm):** If hand mounting contraindicated, secure to volar forearm 5cm proximal to wrist crease
   - Verify secure fit — device should not shift during movement

### 5.2 Recording Protocol

#### Trial 1: Rest Tremor (Primary)
- **Posture:** Patient seated, back supported, feet flat on floor
- **Arm position:** Arms supported on armrests or pillows, elbows flexed ~90°, wrists neutral, fingers relaxed
- **Duration:** 60 seconds
- **Instructions:** "Please relax your hands completely. Try not to move."
- **Environment:** Quiet room, dim lighting, minimize distractions

#### Trial 2: Postural Tremor
- **Posture:** Patient seated, arms outstretched forward at shoulder height, palms down
- **Duration:** 30 seconds
- **Instructions:** "Hold your arms out straight. Try to keep them as still as possible."

#### Trial 3: Action/Kinetic Tremor (Optional)
- **Task:** Finger-to-nose testing, 10 repetitions per hand
- **Duration:** Self-paced (~30–45 seconds)
- **Instructions:** "Touch your nose, then touch my finger. Repeat as smoothly as you can."

#### Trial 4: Reproducibility (PD group only)
- Repeat Trial 1 after 30-minute rest period
- Document any change in medication status between trials

### 5.3 Concurrent Clinical Assessment
During each recording session, a board-certified neurologist (blinded to algorithm output) will:
1. Rate tremor using MDS-UPDRS Part III items:
   - 3.17: Rest tremor amplitude (0–4 per limb)
   - 3.18: Constancy of rest tremor (0–4)
   - 3.15: Postural tremor (0–4)
   - 3.16: Kinetic tremor (0–4)
2. Complete Fahn-Tolosa-Marin Tremor Rating Scale (0–4 per item)
3. Record overall clinical impression of tremor severity (mild/moderate/severe)

### 5.4 Data Quality Checks
- Real-time signal quality indicator (Allan Variance Studio UI)
- Minimum acceptable: ≥95% valid samples, no clipping events
- If quality check fails, repeat trial after 2-minute rest

---

## 6. Data Management

### 6.1 Data Flow
```
Smartphone IMU → Allan Variance Studio App → Local Encrypted Storage
                                          ↓
                                    Secure Cloud Sync (HIPAA-compliant)
                                          ↓
                                    Analysis Pipeline (Python backend)
                                          ↓
                                    De-identified Dataset + Clinical Scores
```

### 6.2 File Naming Convention
```
[STUDY_ID]_[SITE]_[SUBJECT_ID]_[VISIT]_[TRIAL]_[DATE]_[TIME].bin

Example:
AVS_001_MGH_PD042_V1_REST_20260722_143052.bin
```

### 6.3 Metadata Schema
Each recording must include:
- Subject demographics (age, sex, handedness, height, weight)
- Clinical diagnosis and disease duration (PD group)
- Medication status (ON/OFF, time since last dose)
- MDS-UPDRS total and subscores
- Device ID and calibration certificate
- Ambient conditions (temperature, humidity)
- Rater ID and certification level

### 6.4 Privacy & Security
- All data encrypted at rest (AES-256) and in transit (TLS 1.3)
- PHI stored separately from sensor data (linked by random study ID)
- Cloud storage: Google Cloud Platform with BAA (Business Associate Agreement)
- Retention: 7 years post-study completion per FDA guidance

---

## 7. Analysis Plan

### 7.1 Signal Processing Pipeline

**Step 1: Preprocessing**
- Remove DC offset and gravity component from accelerometer
- Apply bandpass filter: 1–25 Hz (tremor + harmonics)
- Detect and interpolate motion artifacts (>3σ from local mean)

**Step 2: Tremor Feature Extraction**
- **Dominant frequency:** Peak power spectral density (PSD) in 3–8 Hz band
- **Tremor amplitude:** RMS acceleration in tremor band (mg)
- **Harmonic ratio:** Power at 2× fundamental / power at fundamental
- **Tremor regularity:** Coefficient of variation of inter-peak intervals

**Step 3: Allan Variance Characterization**
- Compute Allan deviation σ(τ) for τ = 0.01s to 100s
- Fit five-parameter noise model:
  - Q (quantization noise)
  - N (angle random walk)
  - B (bias instability)
  - K (rate random walk)
  - R (rate ramp)
- Extract integration limit (τ where σ(τ) is minimum)

**Step 4: Tremor Detection Classification**
- Input: Tremor features + noise model parameters
- Classifier: Random Forest (validated) or neural network
- Output: Tremor present/absent + confidence score

### 7.2 Statistical Analysis

**Primary Endpoint:**
- Pearson correlation between automated tremor amplitude and MDS-UPDRS item 3.17
- Target: r ≥ 0.70 (strong correlation)

**Secondary Analyses:**
- Bland-Altman agreement between automated and clinical tremor frequency
- ROC curve for tremor detection (automated vs. neurologist gold standard)
- Intra-class correlation coefficient (ICC) for test-retest reliability
- Subgroup analysis: ON vs. OFF medication, early vs. advanced PD

**Software:** Python (SciPy, scikit-learn), R (lme4 for mixed-effects models)

---

## 8. Safety & Adverse Events

### 8.1 Risk Assessment
- **Minimal risk:** Device is consumer smartphone, no invasive procedures
- **Potential risks:**
  - Skin irritation from Velcro strap (rare)
  - Mild fatigue from prolonged posture holding
  - Anxiety from tremor observation (mitigated by private recording room)

### 8.2 Adverse Event Reporting
- All AEs logged in study database within 24 hours
- Serious AEs (SAEs) reported to IRB and sponsor within 72 hours
- Independent Data Safety Monitoring Board (DSMB) reviews quarterly

### 8.3 Device Malfunction
- If smartphone fails during recording, use backup device (pre-characterized)
- Document malfunction in case report form
- Report to sponsor if malfunction rate exceeds 5%

---

## 9. Quality Assurance

### 9.1 Rater Training
- All neurologists complete standardized tremor rating training
- Inter-rater reliability: Cohen's κ ≥ 0.80 required before independent scoring
- Quarterly calibration sessions with video-recorded tremor samples

### 9.2 Data Quality Metrics
- **Completeness:** ≥95% of scheduled recordings completed
- **Validity:** ≥90% of recordings pass signal quality check
- **Timeliness:** Data uploaded within 24 hours of collection

### 9.3 Audit Trail
- All data modifications logged with user ID, timestamp, and reason
- Regular automated checks for anomalous data patterns
- Source data verification: 20% random sample checked against original recordings

---

## 10. Regulatory Compliance

### 10.1 FDA Considerations
- This study supports a 510(k) submission for Software as a Medical Device (SaMD)
- Allan Variance Studio classified as Class II device (tremor diagnostic aid)
- Predicate device: Kinesia 360 (Great Lakes NeuroTechnologies)

### 10.2 Data Standards
- Clinical data: CDISC SDTM/ADaM format
- Sensor data: IEEE 1451.4 transducer electronic data sheet (TEDS) compatible
- Code: FDA software validation guidance (General Principles of Software Validation)

### 10.3 Publication Plan
- Primary results submitted to peer-reviewed journal (target: Movement Disorders)
- De-identified dataset deposited in PhysioNet or Zenodo
- Open-source release of analysis pipeline (Apache 2.0 license)

---

## 11. Appendices

### Appendix A: Informed Consent Template
[Available from study coordinator]

### Appendix B: MDS-UPDRS Scoring Guidelines
[Link to MDS official training materials]

### Appendix C: Device Calibration Certificate Template
```
Device ID: [IMEI or serial number]
Calibration Date: [YYYY-MM-DD]
Calibration Technician: [Name, certification]

Noise Parameters (Allan Variance):
- Quantization noise (Q): [value] °/s·√s
- Angle random walk (N): [value] °/√h
- Bias instability (B): [value] °/h
- Rate random walk (K): [value] °/s·√h
- Rate ramp (R): [value] °/s²

Validation Results:
- Static test duration: [hours]
- Correlation with reference IMU: [r value]
- Temperature range tested: [°C]
- Pass/Fail: [status]

Next calibration due: [date]
```

### Appendix D: Troubleshooting Guide

| Problem | Likely Cause | Solution |
|---------|-----------|----------|
| No sensor data | Permissions denied | Re-enable IMU permissions in Android settings |
| Signal clipping | Excessive movement | Reduce patient movement, check mounting |
| Sampling rate <500 Hz | Power saving mode | Disable battery optimization for app |
| Upload failure | Network connectivity | Retry on WiFi; data stored locally until sync |
| App crash | Insufficient memory | Close background apps, restart device |

### Appendix E: Contact Information
- **Principal Investigator:** [Name, MD, institution]
- **Study Coordinator:** [Name, email, phone]
- **Technical Support:** [Email for Allan Variance Studio issues]
- **24-Hour Emergency Line:** [Phone number]

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-07-15 | Kazi Saad Asif | Initial draft |
| 0.2 | 2026-07-18 | [PI Name] | Clinical review, added MDS-UPDRS details |
| 0.3 | 2026-07-20 | [Biostatistician] | Power calculation, analysis plan |
| 1.0 | 2026-07-22 | Kazi Saad Asif | Final protocol for IRB submission |

**Next Review Date:** 2026-10-22  
**Approval Signatures:** [PI] _______________ [Sponsor] _______________ [IRB Chair] _______________
