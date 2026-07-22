# Troubleshooting Guide

## Allan Variance Studio — Android Application

**Version:** 1.0  
**Last Updated:** 2026-07-22  
**Platform:** Android (API 24+, Android 7.0+)

---

## Quick Reference Table

| Symptom | Likely Cause | Quick Fix | Section |
|---------|-----------|-----------|---------|
| App crashes on launch | Insufficient RAM / OS incompatibility | Close background apps, check Android version | [1.1](#11-app-crashes-on-launch) |
| No sensor data recorded | Permissions denied | Re-enable IMU permissions in Settings | [2.1](#21-no-sensor-data-recorded) |
| Recording stops unexpectedly | Battery optimization killing app | Disable battery optimization for Allan Variance Studio | [3.1](#31-recording-stops-unexpectedly) |
| APK build fails in CI | Missing `settings.gradle` or `src/main/` | Add required Gradle and source files | [8.1](#81-apk-build-fails-in-ci) |
| Artifact upload fails | Wrong path in workflow / no APK produced | Fix `path:` in `actions/upload-artifact` | [8.4](#84-artifact-upload-fails-no-files-found) |
| Signal clipping | Excessive movement / loose mounting | Tighten strap, reduce patient movement | [4.1](#41-signal-clipping) |
| Sampling rate below 500 Hz | Power saving mode / thermal throttling | Disable power saving, cool device | [5.1](#51-sampling-rate-below-500-hz) |
| Upload failure | No internet / server down | Store locally, retry on WiFi | [6.1](#61-upload-failure) |
| Device overheats | Ambient temperature >40°C | Move to AC room, pause recording | [7.1](#71-device-overheats) |
| Gradle build 0 seconds | `gradlew` not executable / missing wrapper | `chmod +x gradlew`, verify wrapper files | [8.2](#82-gradle-build-completes-in-0-seconds) |
| Workflow syntax error | Invalid YAML indentation | Validate with online YAML parser | [8.5](#85-workflow-fails-immediately-syntax-error) |

---

## 1. Application Installation & Launch

### 1.1 App Crashes on Launch

**Symptoms:**
- App opens briefly then closes
- "Allan Variance Studio has stopped" error
- Black screen then return to home screen

**Diagnosis:**

1. Check Android version:
   ```
   Settings → About Phone → Android Version
   ```
   Must be 7.0 (API 24) or higher.

2. Check available RAM:
   ```
   Settings → Device Care → Memory
   ```
   Need ≥2 GB free RAM during operation.

3. Check storage space:
   ```
   Settings → Storage
   ```
   Need ≥500 MB free for a 60-second recording at 500 Hz.

**Solutions:**

| Cause | Fix |
|-------|-----|
| Android < 7.0 | Upgrade OS or use a newer device |
| Insufficient RAM | Close all background apps before launching |
| Corrupted install | Uninstall → Reinstall from APK |
| Incompatible device (no gyroscope) | Check device specs; app requires gyroscope |

**Prevention:**
- Maintain ≥1 GB free storage at all times
- Restart device daily if used for clinical recording

---

### 1.2 App Not Installing

**Symptoms:**
- "App not installed" error
- "Parse error" during install
- Security warning blocks install

**Solutions:**

1. **Enable unknown sources:**
   ```
   Settings → Security → Install unknown apps → Chrome/File Manager → Allow
   ```

2. **Check APK integrity:**
   - Verify file size matches expected (debug APK ~5–15 MB)
   - Re-download if file is 0 bytes or truncated

3. **Conflicting signature:**
   - If previous version installed from different source, uninstall first
   - Debug and release APKs have different signatures

---

## 2. Sensor & Recording Issues

### 2.1 No Sensor Data Recorded

**Symptoms:**
- Recording shows 0 samples
- Graph is flat line
- "No sensor data" warning

**Diagnosis Steps:**

1. Check permissions:
   ```
   Settings → Apps → Allan Variance Studio → Permissions
   ```
   Required permissions:
   - **Body sensors** (accelerometer, gyroscope) — MUST be "Allow"
   - **Storage** — MUST be "Allow"
   - **Microphone** — NOT required (deny is fine)

2. Verify sensors exist:
   ```
   Download "Sensor Test" app from Play Store
   Check if accelerometer and gyroscope respond
   ```

3. Check if sensors are disabled:
   ```
   Settings → Accessibility → Some Samsung devices have "Motion" toggles
   ```

**Solutions:**

| Cause | Fix |
|-------|-----|
| Permissions denied | Re-enable all sensor and storage permissions |
| Sensors physically broken | Test with Sensor Test app; use different device |
| Sensors disabled by OS | Check manufacturer-specific motion settings |
| App cache corrupted | Settings → Apps → Allan Variance Studio → Storage → Clear Cache |

**Code-level check (for developers):**
```kotlin
val sensorManager = getSystemService(Context.SENSOR_SERVICE) as SensorManager
val accelerometer = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER)
val gyroscope = sensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE)

if (accelerometer == null || gyroscope == null) {
    Log.e("SENSOR", "Required sensors not available on this device")
}
```

---

### 2.2 Recording Shows Flat Line (No Variation)

**Symptoms:**
- Graph is horizontal line at constant value
- Allan deviation plot shows only quantization noise floor

**Causes:**
1. **Device is completely still** — Expected for static calibration; not an error
2. **Sensor stuck** — Hardware fault; values don't change when device moved
3. **Scaling issue** — Values are being recorded but display range is wrong

**Fix:**
- Gently shake device during test recording
- If values still don't change → sensor hardware fault → use different device

---

### 2.3 Dropped Samples / Gaps in Recording

**Symptoms:**
- Timestamp jumps in exported CSV
- "Dropped samples" warning in app
- Allan deviation plot shows discontinuities

**Causes & Fixes:**

| Cause | Fix |
|-------|-----|
| CPU overloaded | Close all background apps; disable animations |
| Garbage collection pause | Reduce sampling rate to 200 Hz temporarily |
| Thermal throttling | Cool device; remove case; move to AC room |
| Storage write bottleneck | Ensure ≥1 GB free internal storage |
| Low battery (<20%) | Charge device before recording |

**Optimal recording conditions:**
- Battery ≥50%
- Free RAM ≥1.5 GB
- Free storage ≥2 GB
- No other apps running
- Airplane mode ON (except if real-time sync needed)

---

## 3. Battery & Power Issues

### 3.1 Recording Stops Unexpectedly

**Symptoms:**
- Recording ends before set duration
- App disappears from screen
- Partial file saved

**Diagnosis:**

1. Check battery optimization:
   ```
   Settings → Battery → Battery Optimization → Allan Variance Studio
   ```
   If set to "Optimized", Android may kill the app.

2. Check Doze mode:
   ```
   Settings → Battery → Background usage limits
   ```

3. Check if screen locked during recording:
   Some OEMs (Xiaomi, OPPO) aggressively kill apps on screen lock.

**Solutions:**

```
Settings → Apps → Allan Variance Studio → Battery → Unrestricted
Settings → Battery → Battery Optimization → Allan Variance Studio → Don't optimize
```

**OEM-specific:**

| Manufacturer | Additional Setting |
|-------------|------------------|
| Samsung | Settings → Battery → Background usage limits → Deep sleeping apps → Remove Allan Variance Studio |
| Xiaomi | Security → Battery → App battery saver → Allan Variance Studio → No restrictions |
| OPPO/Realme | Settings → Battery → App battery management → Allan Variance Studio → Allow background activity |
| Vivo | Settings → Battery → Background power consumption → Allan Variance Studio → Allow |

---

### 3.2 Excessive Battery Drain During Recording

**Expected:** ~15–20% per hour at 500 Hz with screen on

**If draining >30% per hour:**

1. Reduce screen brightness to minimum
2. Enable "Recording mode" in app (disables real-time graph rendering)
3. Lower sampling rate to 200 Hz if 500 Hz not required
4. Disable GPS/location services
5. Use airplane mode with WiFi only (if sync not needed)

---

## 4. Signal Quality Issues

### 4.1 Signal Clipping

**Symptoms:**
- Waveform hits maximum/minimum and flattens
- "Clipping detected" warning
- Allan deviation shows abnormal plateau at high τ

**Causes:**
- Acceleration exceeds sensor range (±2g/±4g/±8g/±16g)
- Gyroscope exceeds range (±250/±500/±1000/±2000 °/s)
- Loose mounting causing impact spikes

**Fixes:**

1. **Tighten mounting strap:** Device should not shift during movement
2. **Reduce patient movement:** Ask patient to move more gently
3. **Increase sensor range:** In app settings, change accelerometer range to ±8g or ±16g
4. **Check for hardware resonance:** Strap bouncing can create high-frequency artifacts → use foam padding

**Developer check:**
```kotlin
// Log max values during recording to detect clipping
val maxAccel = samples.maxOf { abs(it.accelX) }
if (maxAccel > ACCEL_RANGE * 0.95) {
    Log.w("CLIP", "Accelerometer clipping detected: $maxAccel")
}
```

---

### 4.2 Excessive Noise / Poor Signal-to-Noise Ratio

**Symptoms:**
- Signal appears fuzzy with high-frequency variation
- Allan deviation shows high noise floor
- Tremor peak not visible in PSD

**Causes & Fixes:**

| Cause | Fix |
|-------|-----|
| Loose mounting | Tighten strap; add non-slip pad |
| 50/60 Hz electrical interference | Move away from power lines, transformers |
| Phone vibration from notifications | Enable Do Not Disturb during recording |
| Case resonance | Remove phone case during recording |
| Fan/AC vibration | Turn off fan; move away from AC unit |
| Patient talking/coughing | Ask patient to remain silent |

**Environmental noise checklist:**
- [ ] Device firmly mounted (no wobble)
- [ ] No phone case (or rigid case only)
- [ ] Do Not Disturb enabled
- [ ] Airplane mode (if no sync needed)
- [ ] No fans/AC directly on device
- [ ] Quiet room (no construction, traffic)
- [ ] Stable table/floor (no foot traffic vibration)

---

### 4.3 Motion Artifacts

**Symptoms:**
- Sudden spikes in data
- Allan deviation plot shows unexpected peaks
- Tremor frequency estimate jumps erratically

**Causes:**
- Patient adjusting position
- Device bumped by examiner
- Sudden patient movement (sneeze, startle)

**Fix:**
- Use artifact detection algorithm (enabled by default)
- Manually mark artifact regions in post-processing
- Repeat trial if >5% of recording contains artifacts

---

## 5. Performance & Sampling Issues

### 5.1 Sampling Rate Below 500 Hz

**Symptoms:**
- App shows "Sampling rate: 480 Hz" or lower
- Requested 500 Hz but actual rate is inconsistent
- Timestamps show irregular intervals

**Causes:**

1. **Power saving mode:**
   ```
   Settings → Battery → Power Saving → OFF
   ```

2. **Thermal throttling:**
   - Device CPU reduced due to heat
   - Check battery temperature: `*#*#4636#*#*` → Battery Information
   - If >45°C, cool device before recording

3. **OEM-specific sensor batching:**
   - Some manufacturers batch sensor events to save power
   - Disable in developer options:
     ```
     Settings → Developer options → Sensor refresh rate → Maximum
     ```

4. **High CPU load:**
   - Other apps using CPU
   - System update running in background

**Fix priority order:**
1. Disable all power saving modes
2. Close all background apps
3. Remove phone case
4. Cool device to <40°C
5. Restart device
6. If still failing, device hardware may not support true 500 Hz → use 200 Hz

---

### 5.2 Inconsistent Sampling Rate (Jitter)

**Symptoms:**
- Timestamps not evenly spaced
- Allan deviation shows bias at short τ

**Fix:**
- Use `SENSOR_DELAY_FASTEST` with hardware timestamp interpolation
- In app settings, enable "Timestamp correction"
- If jitter >5 ms RMS, device hardware is inadequate for IEEE 1293-2018 compliance

---

## 6. Data Upload & Sync Issues

### 6.1 Upload Failure

**Symptoms:**
- "Upload failed" error
- Records stuck in "Pending upload" queue
- Cloud sync icon shows red X

**Diagnosis:**

1. Check connectivity:
   ```
   Open browser, visit google.com
   ```

2. Check if server is reachable:
   ```
   App → Settings → Test Connection
   ```

3. Check file size:
   - 60-second recording at 500 Hz ≈ 50–80 MB (binary)
   - Some mobile networks block uploads >50 MB

**Solutions:**

| Cause | Fix |
|-------|-----|
| No internet | Store locally; upload when WiFi available |
| Mobile data limit | Switch to WiFi or enable "Upload on WiFi only" |
| Server down | Retry later; data is safe in local storage |
| File too large | Enable compression in app settings |
| SSL certificate error | Check device date/time is correct |
| Firewall blocking | Use VPN or different network |

**Manual export (if upload consistently fails):**
```
App → Recordings → Select recording → Export → Share via WhatsApp/Email/Bluetooth
```

---

### 6.2 Data Loss After Upload

**Symptoms:**
- Recording shows "Uploaded" but not visible on server
- Partial data on server

**Fix:**
- Don't delete local recording until verified on server
- App keeps local copy for 7 days by default
- Check server dashboard for record

---

## 7. Environmental & Physical Issues

### 7.1 Device Overheats

**Symptoms:**
- Device feels hot to touch
- "Device too hot" warning from Android
- Recording automatically paused
- Performance degraded (sampling rate drops)

**Causes:**
- Ambient temperature >40°C (common in Bangladesh, India, Middle East)
- Direct sunlight on device
- Continuous recording >30 minutes
- Fast charging while recording
- Phone case trapping heat

**Immediate Fix:**
1. Pause recording
2. Move device to shaded, air-conditioned area
3. Remove phone case
4. Place device on cool metal surface (heat sink)
5. Wait 5–10 minutes until cool to touch
6. Resume recording

**Prevention:**
- Schedule recordings during cooler hours (morning/evening)
- Use external cooling fan if available
- Do not charge while recording
- Remove case before recording
- Limit continuous recording to 60-second blocks with cooling breaks

---

### 7.2 Humidity Affects Mounting

**Symptoms:**
- Strap becomes loose during recording
- Device slips on sweaty skin
- Fungal irritation at mounting site

**Fix:**
- Use moisture-wicking strap liner (provided in clinical kit)
- Wipe skin dry before mounting
- For humid climates (>80% RH), use medical-grade micropore tape as backup
- Inspect skin before and after recording
- If fungal infection present, do not mount on that limb

---

### 7.3 Device Slips During Recording

**Symptoms:**
- Signal shows sudden orientation change
- Patient reports device moving
- Post-recording photo shows shifted position

**Fix:**
1. Tighten strap (should be snug but not painful)
2. Use non-slip silicone pad between device and skin
3. For hairy arms, use compression sleeve under strap
4. Check strap size — smaller sizes available for Bangladeshi wrist circumferences (14–18 cm)

---

## 8. CI/CD & Build Issues

### 8.1 APK Build Fails in CI

**Symptoms:**
- GitHub Actions workflow fails at `./gradlew assembleDebug`
- Error: "Could not open init generic class cache"
- Error: "Settings file not found"

**Common Causes & Fixes:**

| Error | Cause | Fix |
|-------|-------|-----|
| `settings.gradle not found` | Missing `android/settings.gradle` | Create `settings.gradle` in `android/` directory |
| `build.gradle not found` | Missing root `android/build.gradle` | Create root-level `build.gradle` |
| `Plugin not found` | Wrong plugin version for Gradle version | Match AGP version to Gradle wrapper version |
| `Could not find com.android.tools.build:gradle` | Missing `google()` repository | Add `google()` to `pluginManagement` block |
| `No toolchains found` | Wrong JDK version in CI | Use `actions/setup-java@v4` with Java 17 |

**Required files checklist:**
```
android/
├── settings.gradle          ← MUST exist
├── build.gradle             ← MUST exist (root level)
├── gradle.properties
├── local.properties
├── gradle/
│   └── wrapper/
│       ├── gradle-wrapper.jar
│       ├── gradle-wrapper.properties
│       └── gradlew
└── app/
    ├── build.gradle         ← MUST exist (module level)
    └── src/
        ├── main/            ← MUST exist
        │   ├── AndroidManifest.xml
        │   ├── java/com/allanvariancestudio/MainActivity.kt
        │   └── res/
        │       ├── layout/activity_main.xml
        │       └── values/strings.xml
        └── androidTest/     ← Your existing tests
```

---

### 8.2 Gradle Build Completes in 0 Seconds

**Symptoms:**
- "Build Debug APK" step shows 0s duration
- No APK produced
- No error visible in logs

**Diagnosis:**

1. Check if `gradlew` is actually executable:
   ```yaml
   - name: Verify gradlew
     run: |
       ls -la android/gradlew
       file android/gradlew
   ```

2. Check if `settings.gradle` exists:
   ```yaml
   - name: Verify settings.gradle
     run: cat android/settings.gradle || echo "MISSING"
   ```

3. Run Gradle with verbose output:
   ```yaml
   - name: Build with verbose output
     run: cd android && ./gradlew assembleDebug --stacktrace --info --console=plain 2>&1
   ```

**Most Common Cause:** `settings.gradle` is missing. Without it, Gradle exits immediately.

**Fix:** Create `android/settings.gradle`:
```gradle
pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = "AllanVarianceStudio"
include ':app'
```

---

### 8.3 Gradle Wrapper Issues

**Symptoms:**
- `gradlew: command not found`
- `gradlew: Permission denied`
- `Could not find gradle-wrapper.jar`

**Fixes:**

```bash
# Make gradlew executable
chmod +x android/gradlew

# Verify wrapper exists
ls -la android/gradle/wrapper/
# Should show: gradle-wrapper.jar, gradle-wrapper.properties, gradlew

# If wrapper is missing, regenerate:
cd android
gradle wrapper --gradle-version 8.4

# Or download official wrapper:
# https://raw.githubusercontent.com/gradle/gradle/v8.4.0/gradlew
```

**In GitHub Actions:**
```yaml
- name: Grant execute permission for gradlew
  run: chmod +x android/gradlew

- name: Verify wrapper
  run: |
    ls -la android/gradlew
    ls -la android/gradle/wrapper/
```

---

### 8.4 Artifact Upload Fails: "No files found"

**Symptoms:**
- `actions/upload-artifact` shows warning: "No files were found with the provided path"
- Artifacts section shows "—" or 0 artifacts

**Diagnosis:**

1. Check if APK was actually built:
   ```yaml
   - name: Find APK files
     run: find android -name "*.apk" -type f 2>/dev/null || echo "NO APK FOUND"
   ```

2. Check build outputs directory:
   ```yaml
   - name: List build outputs
     run: ls -R android/app/build/outputs/ 2>/dev/null || echo "No outputs directory"
   ```

**Common Path Issues:**

| Working Directory | Correct Upload Path | Wrong Path |
|-------------------|---------------------|------------|
| Repo root (default) | `android/app/build/outputs/apk/debug/*.apk` | `app/build/outputs/...` |
| `./android` (set via `defaults`) | `app/build/outputs/apk/debug/*.apk` | `android/app/build/...` |

**Note:** `actions/upload-artifact` paths are relative to **repo root**, not `working-directory`.

**Correct configuration:**
```yaml
jobs:
  build:
    defaults:
      run:
        working-directory: ./android   # affects 'run:' steps only
    steps:
      - uses: actions/checkout@v4

      - name: Build APK
        run: ./gradlew assembleDebug    # runs in ./android

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: debug-apk
          path: android/app/build/outputs/apk/debug/*.apk  # relative to repo root
```

---

### 8.5 Workflow Fails Immediately (Syntax Error)

**Symptoms:**
- Workflow shows red X immediately
- "This workflow graph cannot be shown"
- No jobs run at all

**Fix:**

1. Validate YAML syntax:
   - Use online validator: [yamlchecker.com](https://yamlchecker.com) or [yamllint.com](https://yamllint.com)
   - Or use GitHub's built-in editor (shows red underline for errors)

2. Common YAML errors:
   - **Tabs instead of spaces:** YAML requires spaces only
   - **Missing colon after `with:`** — must be `with:` not `with`
   - **Unclosed quotes:** `path: "android/app/...` (missing closing quote)
   - **Invalid folded scalar:** The `>-` syntax for multi-line strings must be followed by blank line

3. Test with minimal workflow first:
   ```yaml
   name: Test
   on: push
   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - run: echo "Hello"
   ```

---

### 8.6 Node.js 20 Deprecation Warning

**Symptoms:**
- Warning: "Node.js 20 is deprecated... being forced to run on Node.js 24"
- This is a **warning**, not an error
- Does not affect build functionality

**Fix (optional, for cleanliness):**

GitHub is automatically migrating to Node 24. No action needed. If you want to suppress:

```yaml
env:
  ACTIONS_ALLOW_USE_UNSECURE_NODE_VERSION: true  # Not recommended
```

Or wait for `actions/checkout@v5`, `actions/setup-java@v5`, etc. (not yet released as of 2026).

---

## 9. Data Export & Analysis Issues

### 9.1 Cannot Open Exported CSV

**Symptoms:**
- Excel shows garbled text
- Numbers appear as dates
- Decimal separator issues

**Fix:**
- Open in text editor first to verify format
- Use LibreOffice Calc with correct delimiter (comma)
- For Excel: Data → From Text/CSV → select file → set delimiter to comma, encoding to UTF-8

---

### 9.2 Allan Deviation Plot Looks Wrong

**Symptoms:**
- Plot shows negative values (impossible)
- Slope is positive (should be negative for white noise)
- Discontinuities or gaps

**Causes:**
- Insufficient data length (need ≥100× longest τ)
- Clipping artifacts
- Incorrect τ averaging (must be power of 2)

**Fix:**
- Ensure recording duration ≥10× intended maximum τ
- Remove clipped sections before analysis
- Use overlapping Allan variance (default in app)

---

## 10. Getting Help

### 10.1 Before Asking for Help

Please gather:
1. Device model and Android version
2. App version (Settings → About)
3. Exact error message (screenshot or copy-paste)
4. Steps to reproduce
5. What you've already tried

### 10.2 Support Channels

| Issue Type | Contact |
|-----------|---------|
| App bugs / crashes | GitHub Issues: `github.com/ksaad20/AllanVarianceStudio/issues` |
| Build / CI issues | GitHub Discussions or Stack Overflow with `allan-variance-studio` tag |
| Clinical protocol questions | Study coordinator (see clinical_protocol.md) |
| Feature requests | GitHub Discussions |

### 10.3 Debug Information Export

App can export full debug log:
```
Settings → About → Export Debug Log
```
This includes:
- Device specs
- Sensor capabilities
- Recent crash logs
- Recording metadata

Attach this when reporting issues.

---

## 11. Emergency Procedures

### 11.1 Patient Distress During Recording

If patient shows signs of distress (pain, anxiety, dizziness):
1. Stop recording immediately
2. Remove device
3. Assess patient
4. If medical emergency, follow site emergency protocol
5. Document incident in case report form
6. Do not resume without physician clearance

### 11.2 Device Damaged During Clinical Use

1. Secure device (prevent data loss)
2. Switch to backup device
3. Document damage
4. Report to study coordinator
5. If patient injury occurred, follow SAE reporting (see clinical protocol)

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 0.1 | 2026-07-15 | Initial draft |
| 0.2 | 2026-07-18 | Added CI/CD section |
| 0.3 | 2026-07-20 | Added environmental issues (heat, humidity) |
| 1.0 | 2026-07-22 | Complete troubleshooting guide with quick reference table |
