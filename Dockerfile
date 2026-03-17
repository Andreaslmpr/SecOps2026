# Use an older base image so Docker Scout has vulnerabilities to find
FROM python:3.9-slim-bullseye

LABEL org.opencontainers.image.source="https://github.com/YOUR_GITHUB_USERNAME/sys-health-scout"
LABEL org.opencontainers.image.description="Lightweight system health monitoring tool"

WORKDIR /app

# Install some system utilities that will pull in packages with known CVEs
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    net-tools \
    procps \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY healthcheck.py .

ENTRYPOINT ["python", "healthcheck.py"]
