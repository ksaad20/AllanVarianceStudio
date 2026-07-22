# =============================================================================
# AllanVarianceStudio
# Production Multi-stage Dockerfile
# =============================================================================

############################
# Stage 1 - Base
############################
FROM python:3.14-slim-bookworm AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        g++ \
        gfortran \
        git \
        curl \
        ca-certificates \
        libopenblas-dev \
        liblapack-dev \
        libffi-dev \
        libssl-dev && \
    rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:${PATH}"

############################
# Stage 2 - Dependencies
############################
FROM base AS deps

WORKDIR /app

# Copy ONLY the dependency file from the python directory
COPY python/requirements.txt ./requirements.txt

RUN python -m pip install --upgrade pip

RUN python -m pip install -r requirements.txt

############################
# Stage 3 - Final
############################
FROM base AS final

# Copy the virtual environment with installed packages
COPY --from=deps /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:${PATH}"

# Create a non-root user
RUN groupadd --system appgroup && \
    useradd --system --gid appgroup --create-home appuser

WORKDIR /app

# Copy the entire repository
COPY . .

# Set ownership
RUN chown -R appuser:appgroup /app

USER appuser

# Basic health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python --version || exit 1

# Default command
CMD ["python"]
