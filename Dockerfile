# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies (for Pillow and other packages)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Run migrations
RUN python manage.py migrate

# Collect static files (for production)
RUN python manage.py collectstatic --noinput

# Run the development server
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]