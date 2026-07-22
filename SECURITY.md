# Security Policy for AllanVarianceStudio

## Supported Versions

The following versions of AllanVarianceStudio are currently supported with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in AllanVarianceStudio, please report it responsibly.

**Please do NOT open a public issue** for security vulnerabilities.

Instead, send an email to: **[your-security-email@example.com]**

Include the following details:
- A clear description of the vulnerability
- Steps to reproduce the issue
- The affected version(s)
- Any potential impact assessment
- Suggested fix (if available)

### Response Timeline

| Action | Timeline |
|--------|----------|
| Initial acknowledgment | Within 48 hours |
| Vulnerability assessment | Within 7 days |
| Patch release (if confirmed) | Within 30 days |
| Public disclosure (after fix) | Coordinated with reporter |

## Security Considerations for Allan Variance Analysis

Given that AllanVarianceStudio processes sensitive sensor data (IMU readings, time-series signals), the following security measures are in place:

### Data Handling
- **No telemetry or external data transmission** — all processing is done locally
- Input data files (`.bag`, `.csv`, `.feather`, `.mat`) are read-only during analysis
- Temporary files generated during computation are cleaned up after session completion

### Dependency Security
- All dependencies are pinned to specific versions in `requirements.txt`
- Regular automated scans for known vulnerabilities in dependencies
- No execution of arbitrary code from input data files

### Input Validation
- Strict validation of file formats and data structures
- Bounds checking on array dimensions and sampling rates
- Rejection of malformed or excessively large inputs

## Known Security Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Malicious input data files | Medium | Input validation, sandboxed parsing |
| Dependency vulnerabilities | Low | Automated scanning, pinned versions |
| Resource exhaustion (DoS) | Low | Input size limits, timeout controls |

## Best Practices for Users

1. **Only process data from trusted sources** — maliciously crafted sensor data files could exploit parser vulnerabilities
2. **Keep dependencies updated** — run `pip install --upgrade -r requirements.txt` regularly
3. **Use virtual environments** — isolate AllanVarianceStudio from other Python projects
4. **Review output files** — verify that generated plots and YAML configs contain expected data

## Security-Related Configuration

```yaml
# Example secure configuration
max_input_file_size_mb: 500
max_samples_per_axis: 10000000
enable_telemetry: false
allow_arbitrary_code_execution: false
```

## Acknowledgments

We thank the following individuals for responsibly disclosing security issues:

- *(List will be updated as reports are received)*
