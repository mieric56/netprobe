FROM python:3.12-slim

# Install network tools: ping, mtr, traceroute
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        iputils-ping \
        mtr-tiny \
        traceroute \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire app into /app
COPY . .

# Safety: if zip created a nested netprobe/ folder, flatten it
RUN if [ -d /app/netprobe ] && [ -f /app/netprobe/main.py ]; then \
      cp -rn /app/netprobe/* /app/ 2>/dev/null; \
      cp -rn /app/netprobe/.* /app/ 2>/dev/null; \
      rm -rf /app/netprobe; \
    fi

# Verify the structure is correct (will fail the build if wrong)
RUN test -f /app/main.py && test -f /app/backend/api.py && echo "Structure OK" || (echo "ERROR: files not in expected location" && ls -laR /app/ && exit 1)

# Create persistent data dir
RUN mkdir -p /data

# Unbuffered output + ensure /app is in Python path
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/targets')" || exit 1

CMD ["python", "/app/main.py"]
