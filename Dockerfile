FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn whitenoise

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Use platform PORT if provided
ENV PORT=8000
EXPOSE 8000

# Run gunicorn
CMD gunicorn auction_site.wsgi:application --bind 0.0.0.0:${PORT}
