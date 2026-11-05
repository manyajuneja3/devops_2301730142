# ==========================================
# DevOps Lab 2 - Production Multi-Stage Dockerfile
# Candidate: Manya Juneja (Roll No: 2301730142 | manyajuneja03@gmail.com)
# ==========================================
FROM python:3.11-slim AS builder

LABEL maintainer="Manya Juneja <manyajuneja03@gmail.com>"
LABEL student.roll="2301730142"

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies to wheels
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ==========================================
# Stage 2: Minimal Distroless / Slim Runtime
# ==========================================
FROM python:3.11-slim AS runner

LABEL maintainer="Manya Juneja <manyajuneja03@gmail.com>"
LABEL student.roll="2301730142"

WORKDIR /app

# Create a non-privileged system user for security hardening
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /bin/false appuser

# Copy installed dependencies from builder stage
COPY --from=builder /root/.local /home/appuser/.local

# Copy application source code
COPY app.py .

# Adjust permissions
RUN chown -R appuser:appgroup /app /home/appuser

# Environment variables
ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=5000 \
    APP_VERSION=1.0.0

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5000

# Container Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/healthz')" || exit 1

# Launch production WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "--access-logfile", "-", "app:app"]
