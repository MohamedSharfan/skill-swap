# Use the official Python image
FROM python:3.10-slim

# Set working directory in container
WORKDIR /app

# Copy all files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 (Cloud Run expects this)
EXPOSE 8080

# Run your Flask app using gunicorn
CMD ["gunicorn", "-b", ":8080", "app:app"]
