FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv pip install --system --no-cache -r pyproject.toml
COPY . .
CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0", "--server.port=8501"]