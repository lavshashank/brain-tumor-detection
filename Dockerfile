FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port
EXPOSE 5000

# Run with gunicorn
# Using --preload to load app once and fork workers (saves memory)
# Single worker with sync class to avoid memory issues with TensorFlow
# Extended timeout to handle TensorFlow initialization
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--worker-class", "sync", "--timeout", "300", "--graceful-timeout", "300", "--preload", "app:app"]

