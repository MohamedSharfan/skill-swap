# Use a lightweight official Python image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies for SQLite + clean up
RUN apt-get update && apt-get install -y gcc libsqlite3-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy your application files into container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create a directory for Flask session storage
RUN mkdir -p /tmp/flask_session

# Set environment variable for Flask session
ENV SESSION_FILE_DIR=/tmp/flask_session

# Set environment variables (optional)
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Expose port 8080 for Cloud Run / Docker
EXPOSE 8080

# Run the Flask app using gunicorn (production server)
CMD ["gunicorn", "-b", ":8080", "app:app"]
