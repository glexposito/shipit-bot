# syntax=docker/dockerfile:1

FROM python:3.13-slim AS builder
WORKDIR /app

# Copy uv into this image (so we keep a normal OS with /bin/sh etc.)
COPY --from=docker.io/astral/uv:latest /uv /uvx /bin/

# Copy dependency files first for caching
COPY pyproject.toml uv.lock ./

# Create venv + install exactly what's in uv.lock
RUN uv venv
RUN uv sync --frozen

# ---- Final Stage ----
FROM python:3.13-slim
WORKDIR /app

RUN adduser --disabled-password appuser

COPY --from=builder /app/.venv /app/.venv
COPY . .

ENV PATH="/app/.venv/bin:$PATH"

RUN chown -R appuser:appuser /app
USER appuser

CMD ["python", "app.py"]
