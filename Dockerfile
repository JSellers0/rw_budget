# ~/projects/rw_budget/Dockerfile

FROM python:3.13-slim-trixie

WORKDIR /app

# Install uv (fast Python package manager)
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    pkg-config \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*


# Alternative: Install via pip (simpler)
RUN pip install uv

# Verify uv is installed
RUN which uv && uv --version

# Create directories for volumes BEFORE copying code
RUN mkdir -p /app/cache
RUN mkdir -p /app/logs
RUN mkdir -p /app/static
RUN mkdir -p /app/tmp
RUN mkdir -p /app/uploads

# Copy dependency files first (better caching)
COPY pyproject.toml uv.lock ./

# Install Python dependencies using uv
RUN uv pip install --system -r pyproject.toml

# Copy application code
COPY . .

# Create non-root user (UID 1000 matches typical first user)
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose the Flask port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Use run.py as the entry point with gunicorn
CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", \
     "--access-logfile", "/app/logs/access.log", \
     "--error-logfile", "/app/logs/error.log", \
     "--capture-output", \
     "--log-level", "info", \
     "run:app"]