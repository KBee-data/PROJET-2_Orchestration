# ==============================================================================
# Stage 1: Builder (Compiles wheels and builds the production virtualenv)
# ==============================================================================
FROM python:3.11-slim AS builder

# Install build dependencies and PostgreSQL development headers
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy uv binary directly from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy dependency specifications first for Docker layer caching
COPY pyproject.toml uv.lock ./

# Install only production dependencies into an isolated virtual environment
RUN uv sync --frozen --no-dev --no-install-project

# ==============================================================================
# Stage 2: Runtime (Minimal, secure production image without compilers)
# ==============================================================================
FROM python:3.11-slim AS runner

# Install only runtime shared libraries (libpq5 for PostgreSQL, curl for healthchecks)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy pre-built virtual environment from builder stage
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy application source code
COPY . .

EXPOSE 8000

# Launch FastAPI via Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]