# Use official Python 3.13 slim image
FROM python:3.13-slim

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory inside the container
WORKDIR /app

# Install system dependencies required for Pillow and PostgreSQL
RUN apt-get update && apt-get install -y \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Note: We do NOT run migrations or collectstatic here. 
# We do that in docker-compose.yml when the container actually starts.