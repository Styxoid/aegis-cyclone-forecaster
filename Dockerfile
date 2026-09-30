# Production Dockerfile for Google Cloud Run (AegisSurge Simulation Core)
FROM python:3.12-slim

WORKDIR /app

# Prevent Python from writing .pyc and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and pre-cached datasets
COPY aegis_core/ aegis_core/
COPY services/ services/
COPY api/ api/
COPY data/ data/

# Ensure datasets are seeded
RUN python data/seed_fani.py

EXPOSE 8080

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]
