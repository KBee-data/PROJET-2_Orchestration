# ==============================================================================
# Stage 1: Builder (Builds the production virtualenv)
# ==============================================================================
FROM python:3.11-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock README.md* ./
RUN uv sync --frozen --no-dev

# ==============================================================================
# Stage 2: Runtime (Minimal production image)
# ==============================================================================
FROM python:3.11-slim AS runner

WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy Streamlit frontend application
COPY . .

EXPOSE 8501

# Launch Streamlit application
CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0", "--server.port=8501"]