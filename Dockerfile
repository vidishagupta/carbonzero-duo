# ==============================================================================
# Ultra-Lightweight, Carbon-Efficient Multi-Stage Container
# Base: python:3.12-slim (<140MB vs standard 1.1GB Python image)
# ==============================================================================

FROM python:3.12-slim AS builder

WORKDIR /app

# Ensure minimal build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt || true

# Production Minimal Stage
FROM python:3.12-slim

WORKDIR /app

# Create unprivileged runner user
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --ingroup appgroup appuser

COPY --from=builder /app /app
COPY . .

# Grant ownership
RUN chown -R appuser:appgroup /app

USER appuser

ENV PORT=8080 \
    PYTHONUNBUFFERED=1 \
    PYTHONDOONTWRITEBYTECODE=1

EXPOSE 8080

# Run lightweight server
CMD ["python", "server.py"]
