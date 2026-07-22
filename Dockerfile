Dockerfile
# =============================================================================
# AllanVarianceStudio — Production-Ready Multi-Stage Dockerfile
# =============================================================================
# Multi-stage build for optimized image size and security.
# Supports: Python backend (Allan variance analysis) + Android build environment
# =============================================================================

# ---------------------------------------------------------------------------
# STAGE 1: Base Python Environment
# ---------------------------------------------------------------------------
FROM python:3.11-slim-bookworm AS python-base

# Security: Run as non-root user
ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1     PIP_NO_CACHE_DIR=1     PIP_DISABLE_PIP_VERSION_CHECK=1     PIP_DEFAULT_TIMEOUT=100     POETRY_NO_INTERACTION=1     POETRY_VIRTUALENVS_IN_PROJECT=1     POETRY_CACHE_DIR=/tmp/poetry_cache

# Install system dependencies required for scientific Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
    libffi-dev \
    libssl-dev \
    git \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Create non-root user for security
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

WORKDIR /app

# ---------------------------------------------------------------------------
# STAGE 2: Python Dependencies
# ---------------------------------------------------------------------------
FROM python-base AS python-deps

# Copy dependency files first for layer caching
COPY --chown=appuser:appgroup requirements.txt* pyproject.toml* poetry.lock* ./

# Install dependencies based on available files
# Priority: requirements.txt > pyproject.toml
RUN if [ -f requirements.txt ]; then \
        pip install --no-cache-dir -r requirements.txt; \
    elif [ -f pyproject.toml ]; then \
        pip install --no-cache-dir poetry && \
        poetry install --no-dev --no-ansi; \
    else \
        echo "WARNING: No dependency file found. Install manually."; \
    fi

# ---------------------------------------------------------------------------
# STAGE 3: Android Build Environment (Optional)
# ---------------------------------------------------------------------------
FROM python-base AS android-builder

# Install OpenJDK for Android builds
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jdk \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Set Java environment
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Install Android SDK
ENV ANDROID_SDK_ROOT=/opt/android-sdk
ENV ANDROID_HOME=/opt/android-sdk
ENV PATH="${ANDROID_SDK_ROOT}/cmdline-tools/latest/bin:${ANDROID_SDK_ROOT}/platform-tools:${PATH}"

RUN mkdir -p ${ANDROID_SDK_ROOT}/cmdline-tools && \
    cd ${ANDROID_SDK_ROOT}/cmdline-tools && \
    wget -q https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip && \
    unzip -q commandlinetools-linux-11076708_latest.zip && \
    mv cmdline-tools latest && \
    rm commandlinetools-linux-11076708_latest.zip

# Accept licenses and install essential SDK components
RUN yes | sdkmanager --licenses && \
    sdkmanager "platform-tools" "platforms;android-34" "build-tools;34.0.0"

# ---------------------------------------------------------------------------
# STAGE 4: Final Application Image
# ---------------------------------------------------------------------------
FROM python-base AS final

# Copy installed Python packages from deps stage
COPY --from=python-deps /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=python-deps /usr/local/bin /usr/local/bin

# Copy Android SDK if needed (uncomment for Android support)
# COPY --from=android-builder ${ANDROID_SDK_ROOT} ${ANDROID_SDK_ROOT}
# ENV ANDROID_SDK_ROOT=/opt/android-sdk
# ENV ANDROID_HOME=/opt/android-sdk
# ENV PATH="${ANDROID_SDK_ROOT}/cmdline-tools/latest/bin:${ANDROID_SDK_ROOT}/platform-tools:${PATH}"

# Switch to non-root user
USER appuser

# Set working directory
WORKDIR /app

# Copy application code
COPY --chown=appuser:appgroup . .

# Health check for container orchestration
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import allan_variance; print('OK')" || exit 1

# Expose port if running a web service (adjust as needed)
# EXPOSE 8000

# Default command — adjust based on your app's entry point
CMD ["python", "-m", "allan_variance"]
