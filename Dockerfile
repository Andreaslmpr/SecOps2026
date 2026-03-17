# Use an older base image so Docker Scout has vulnerabilities to find
FROM python:3.9-slim-bullseye

LABEL org.opencontainers.image.source="https://github.com/Andreaslmpr/SecOps2026"
LABEL org.opencontainers.image.description="Security Scanning Tool - vulnerabilities detection"

WORKDIR /app

# Install some system utilities that will pull in packages with known CVEs
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    net-tools \
    procps \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN  pip install --no-cache-dir -r requirements.txt
COPY sec.py .

ENTRYPOINT ["python", ""sec.py""]
