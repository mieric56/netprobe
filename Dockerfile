FROM python:3.12-slim

# Install network tools: ping, mtr, traceroute
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        iputils-ping \
        mtr-tiny \
        traceroute \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Create data dir
RUN mkdir -p /data

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/targets')" || exit 1

# Run
CMD ["python", "main.py"]
