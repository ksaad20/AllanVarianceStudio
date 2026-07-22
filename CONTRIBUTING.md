# Contributing to Allan Variance Studio

Thank you for your interest in contributing to Allan Variance Studio! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Coding Standards](#coding-standards)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)
- [Clinical & Research Contributions](#clinical--research-contributions)
- [Release Process](#release-process)
- [Community](#community)

---

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

### Prerequisites

Before contributing, ensure you have:

- A GitHub account
- Git installed on your local machine
- For Android development: Android Studio Hedgehog (2023.1.1) or later, JDK 17
- For Python development: Python 3.9+, pip, virtualenv
- For clinical contributions: IRB/IEC approval from your institution (if handling patient data)

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/AllanVarianceStudio.git
   cd AllanVarianceStudio
   ```
3. Add the upstream remote:
   ```bash
   git remote add upstream https://github.com/ksaad20/AllanVarianceStudio.git
   ```

## How Can I Contribute?

### Types of Contributions

We welcome contributions in the following areas:

| Area | Skills Needed | Examples |
|------|-------------|----------|
| **Android Development** | Kotlin, Android SDK, Jetpack Compose | UI improvements, sensor optimization, offline mode |
| **Python Analysis** | NumPy, SciPy, scikit-learn, signal processing | New noise models, tremor classifiers, visualization |
| **Clinical Research** | Neurology, movement disorders, biostatistics | Validation studies, protocol design, data collection |
| **Documentation** | Technical writing, Markdown, medical writing | Protocols, user guides, API documentation |
| **DevOps/CI** | GitHub Actions, Docker, cloud platforms | CI optimization, deployment pipelines, testing |
| **Translation** | Native language proficiency | UI localization, clinical materials translation |
| **Hardware Testing** | IMU characterization, sensor calibration | Device validation, noise profiling, temperature testing |

### Good First Issues

Look for issues labeled:
- `good first issue` — Suitable for newcomers
- `help wanted` — Maintainer-requested assistance
- `documentation` — Writing and translation tasks
- `bug` — Verified bugs ready for fixing

## Development Setup

### Android Development

```bash
# 1. Open android/ directory in Android Studio
cd android

# 2. Sync project with Gradle files
# Click "Sync Now" in Android Studio when prompted

# 3. Run tests
./gradlew testDebugUnitTest

# 4. Build debug APK
./gradlew assembleDebug

# 5. Install on connected device
./gradlew installDebug
```

**Required files checklist:**
- [ ] `android/settings.gradle` exists
- [ ] `android/build.gradle` (root) exists
- [ ] `android/app/build.gradle` exists
- [ ] `android/app/src/main/AndroidManifest.xml` exists
- [ ] `android/gradlew` is executable (`chmod +x gradlew`)

### Python Development

```bash
# 1. Navigate to python directory
cd python

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scriptsctivate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run tests
pytest tests/ -v --cov=src

# 5. Run linting
black src/ tests/
flake8 src/ tests/
mypy src/
```

### Pre-commit Hooks (Recommended)

```bash
pip install pre-commit
pre-commit install
```

This runs formatting and linting automatically before each commit.

## Project Structure

```
AllanVarianceStudio/
├── android/                    # Android application
│   ├── app/
│   │   ├── src/
│   │   │   ├── main/           # Application source
│   │   │   │   ├── java/     # Kotlin/Java source files
│   │   │   │   └── res/      # Layouts, strings, themes
│   │   │   └── androidTest/  # Instrumented tests
│   │   └── build.gradle        # Module-level build config
│   ├── build.gradle            # Project-level build config
│   ├── settings.gradle         # Module inclusion
│   └── gradle/
│       └── wrapper/            # Gradle wrapper files
│
├── python/                     # Analysis pipeline
│   ├── src/
│   │   ├── allan_variance.py   # Core AV computation
│   │   ├── noise_model.py      # Parameter fitting (Q, N, B, K, R)
│   │   ├── tremor_simulator.py # Biological signal validation
│   │   └── plot_publication.py # Figure generation
│   ├── tests/                  # Unit tests
│   ├── requirements.txt        # Python dependencies
│   └── notebooks/              # Jupyter analysis notebooks
│
├── docs/                       # Documentation
│   ├── clinical_protocol.md
│   ├── troubleshooting.md
│   └── api_reference.md
│
├── .github/
│   └── workflows/              # CI/CD pipelines
│       ├── android.yml         # Android CI
│       └── python.yml          # Python CI
│
├── README.md
├── LICENSE
└── CODE_OF_CONDUCT.md
```

## Coding Standards

### Kotlin (Android)

- Follow [Kotlin Coding Conventions](https://kotlinlang.org/docs/coding-conventions.html)
- Use meaningful variable names (e.g., `samplingRateHz` not `sr`)
- Document public APIs with KDoc:
  ```kotlin
  /**
   * Computes Allan deviation for given time series data.
   *
   * @param data Input sensor data array (rad/s or m/s²)
   * @param sampleRate Sampling frequency in Hz
   * @param tauMax Maximum averaging time in seconds
   * @return Pair of (tau values, Allan deviation values)
   */
  fun computeAllanDeviation(
      data: DoubleArray,
      sampleRate: Double,
      tauMax: Double
  ): Pair<DoubleArray, DoubleArray>
  ```
- Maximum line length: 120 characters
- Use `val` over `var` where possible
- Prefer immutable data structures

### Python

- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints for function signatures:
  ```python
  from typing import Tuple, Optional
  import numpy as np

  def compute_allan_deviation(
      data: np.ndarray,
      sample_rate: float,
      tau_max: Optional[float] = None
  ) -> Tuple[np.ndarray, np.ndarray]:
      ...
  ```
- Docstrings in Google style:
  ```python
  def fit_noise_model(
      tau: np.ndarray,
      allan_dev: np.ndarray
  ) -> dict:
      """Fit five-parameter noise model to Allan deviation data.

      Args:
          tau: Averaging time values in seconds.
          allan_dev: Allan deviation values.

      Returns:
          Dictionary with keys 'Q', 'N', 'B', 'K', 'R' for noise
          parameters, and 'integration_limit' for optimal averaging time.

      Raises:
          ValueError: If input arrays have incompatible shapes.
      """
  ```
- Maximum line length: 88 characters (Black formatter default)
- Import order: stdlib → third-party → local

### Clinical Data Handling

- **Never commit patient data** to the repository
- Use synthetic data or publicly available datasets for examples
- De-identify all data before sharing (remove names, dates, MRN)
- Store PHI separately from code, with access controls
- Follow your institution's IRB/IEC guidelines

## Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types

| Type | Use For |
|------|---------|
| `feat` | New features |
| `fix` | Bug fixes |
| `docs` | Documentation only |
| `style` | Code style changes (formatting, semicolons) |
| `refactor` | Code restructuring without behavior change |
| `perf` | Performance improvements |
| `test` | Adding or correcting tests |
| `chore` | Build process, dependencies, tooling |
| `ci` | CI/CD configuration |
| `clinical` | Clinical protocol, study design, regulatory |

### Scopes

Common scopes: `android`, `python`, `analysis`, `ui`, `ci`, `docs`, `protocol`

### Examples

```
feat(android): add offline recording mode for low-connectivity clinics

Implements local SQLite storage with automatic sync when WiFi
becomes available. Includes retry logic with exponential backoff.

Closes #42
```

```
fix(python): correct integration limit calculation for tau > 100s

Previous implementation used linear extrapolation beyond data range,
leading to negative integration limits. Now returns NaN with
warning when tau exceeds maximum available averaging time.

Fixes #156
```

```
clinical(protocol): add Bangladesh-specific informed consent template

Includes Bangla translation, cultural adaptations for religious
practices, and 200 BDT transport compensation clause per local
IRB requirements.

Refs #203
```

## Pull Request Process

### Before Submitting

1. **Sync with upstream:**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run all tests locally:**
   ```bash
   # Android
   cd android && ./gradlew testDebugUnitTest lintDebug

   # Python
   cd python && pytest tests/ -v
   ```

3. **Update documentation** if your change affects user-facing behavior

4. **Add tests** for new functionality

5. **Update CHANGELOG.md** if one exists

### PR Template

When opening a PR, please include:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update
- [ ] Clinical protocol change

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing performed (describe)

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No patient data committed
- [ ] IRB approval documented (if clinical)

## Related Issues
Fixes #(issue number)
```

### Review Process

1. All PRs require at least **one review** from a maintainer
2. Clinical/protocol changes require **two reviews** including at least one with clinical expertise
3. CI checks must pass before merge
4. The author should respond to all review comments within 7 days
5. Squash commits before merge if requested by reviewer

## Reporting Bugs

### Before Reporting

- Search existing issues to avoid duplicates
- Check [troubleshooting guide](docs/troubleshooting.md)
- Verify the bug exists on the latest `main` branch

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots / Logs**
If applicable, add screenshots or log output.

**Environment:**
 - Device: [e.g. Samsung Galaxy A54]
 - OS: [e.g. Android 13]
 - App Version: [e.g. 1.0.2]
 - Python Version: [e.g. 3.11]

**Additional context**
Any other relevant information.
```

### Security Vulnerabilities

**Do not open public issues for security bugs.**

Email **security@allanvariancestudio.org** with:
- Description of vulnerability
- Steps to reproduce
- Potential impact (especially if patient data exposure possible)
- Suggested fix (if known)

We will respond within 48 hours and coordinate responsible disclosure.

## Suggesting Enhancements

### Enhancement Request Template

```markdown
**Is your feature request related to a problem?**
A clear description of what the problem is.

**Describe the solution you'd like**
What you want to happen.

**Describe alternatives you've considered**
Other approaches you've thought about.

**Clinical Context**
If applicable, describe the clinical need (e.g., "Neurologists in rural
Bangladesh need offline mode due to unreliable connectivity").

**Additional context**
Mockups, references to papers, or similar implementations.
```

## Clinical & Research Contributions

### Contributing Clinical Data

If you have access to clinical tremor data and wish to contribute:

1. **Verify IRB/IEC approval** at your institution
2. **De-identify all data** (remove names, dates, MRN, facial features from videos)
3. **Document data provenance:**
   - Collection site and date range
   - Device model and calibration status
   - Clinical protocol version used
   - Patient demographics (age range, sex distribution, disease stage)
4. **Submit via secure channel** — do not use GitHub for PHI
5. **Include data dictionary** describing all variables

### Contributing Protocols

For clinical protocol contributions:
- Follow [ICH-GCP](https://ichgcp.net/) guidelines
- Include regulatory requirements for target jurisdiction
- Provide translations if non-English
- Cite relevant literature

### Publication Authorship

Contributors who make substantial intellectual contributions to validation studies may be eligible for co-authorship on resulting publications. Discuss with the PI before beginning work.

## Release Process

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):

```
MAJOR.MINOR.PATCH

MAJOR — Breaking API changes, incompatible clinical protocol updates
MINOR — New features, backward compatible
PATCH — Bug fixes, documentation updates
```

### Release Checklist

- [ ] All tests passing
- [ ] CHANGELOG.md updated
- [ ] Version bumped in `build.gradle` and `__version__.py`
- [ ] Git tag created: `git tag -a v1.2.0 -m "Release version 1.2.0"`
- [ ] GitHub Release drafted with release notes
- [ ] APK/AAB uploaded to GitHub Releases (if Android release)
- [ ] PyPI package published (if Python release)
- [ ] Docker image built and pushed (if applicable)

## Community

### Communication Channels

| Channel | Purpose | Link |
|---------|---------|------|
| GitHub Issues | Bug reports, feature requests | [Issues](https://github.com/ksaad20/AllanVarianceStudio/issues) |
| GitHub Discussions | Q&A, general discussion | [Discussions](https://github.com/ksaad20/AllanVarianceStudio/discussions) |
| Slack (invite-only) | Core team coordination | Request invite via email |
| Email | Private inquiries | kazi.saad.asif@example.com |

### Office Hours

Virtual office hours are held monthly for contributors:
- **Time:** First Saturday of each month, 14:00 UTC
- **Platform:** Google Meet (link posted in Discussions)
- **Agenda:** Open forum for questions, demos, and roadmap discussion

### Recognition

Contributors will be:
- Listed in `CONTRIBUTORS.md`
- Mentioned in release notes for significant contributions
- Invited to present at annual project meeting (virtual)
- Eligible for co-authorship on publications (clinical contributions)

---

## Questions?

If you have questions not covered here:

1. Check existing [Discussions](https://github.com/ksaad20/AllanVarianceStudio/discussions)
2. Open a new Discussion with the `question` label
3. For sensitive matters, email the maintainer directly

Thank you for contributing to open-source clinical neuroscience!
