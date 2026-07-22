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

ENV PATH="/opt/venv/bin:$PATH"

############################
# Stage 2 - Dependencies
############################
FROM base AS deps

WORKDIR /app

COPY requirements.txt* pyproject.toml* poetry.lock* ./

RUN pip install --upgrade pip

RUN if [ -f requirements.txt ]; then \
        pip install -r requirements.txt; \
    elif [ -f pyproject.toml ]; then \
        pip install poetry && \
        poetry config virtualenvs.create false && \
        poetry install --only main; \
    else \
        echo "No dependency file found."; \
    fi

############################
# Stage 3 - Final
############################
FROM base AS final

COPY --from=deps /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

RUN groupadd -r appgroup && \
    useradd -r -g appgroup appuser

WORKDIR /app

COPY . .

RUN chown -R appuser:appgroup /app

USER appuser

HEALTHCHECK CMD python --version || exit 1

CMD ["python"]
