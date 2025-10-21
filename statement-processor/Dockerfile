FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy requirements from parent directory if they don't exist locally
COPY ../requirements.txt ./requirements.txt 2>/dev/null || COPY requirements.txt ./requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# This service is meant to be run manually or on-demand
CMD ["python", "app.py"]
