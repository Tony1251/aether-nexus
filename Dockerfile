# Base image
FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

# Set environment
ENV PYTHONUNBUFFERED=1

# Default command: keep running or trigger the pipeline
CMD ["python", "engine/pipeline.py"]
