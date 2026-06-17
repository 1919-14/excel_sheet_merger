# ── HF Spaces requires the base image to be from Docker Hub ─────────────────
FROM python:3.11-slim

# HF Spaces runs as user 1000 — set up home dir properly
RUN useradd -m -u 1000 appuser

WORKDIR /app

# ── System deps (xlrd needs no extra libs; openpyxl/lxml might) ─────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# ── Python deps ──────────────────────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── App source ───────────────────────────────────────────────────────────────
COPY . .

# ── Streamlit config for HF Spaces ──────────────────────────────────────────
# HF exposes port 7860; Streamlit must bind to 0.0.0.0
RUN mkdir -p /app/.streamlit
RUN echo '\
[server]\n\
port = 7860\n\
address = "0.0.0.0"\n\
headless = true\n\
enableCORS = false\n\
enableXsrfProtection = false\n\
\n\
[browser]\n\
gatherUsageStats = false\n\
' > /app/.streamlit/config.toml

# ── Permissions ──────────────────────────────────────────────────────────────
RUN chown -R appuser:appuser /app
USER appuser

# ── HF Spaces metadata (must be in Dockerfile for Spaces to detect the port) ─
EXPOSE 7860

# ── Entrypoint ───────────────────────────────────────────────────────────────
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]
