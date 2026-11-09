# Use an official Python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Build version provided by GitHub Actions
ARG GIT_SHA=unknown
ENV GIT_SHA=${GIT_SHA}

# Copy dependency definitions
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Document the application port
EXPOSE 5000

# Start the Flask application
CMD ["python", "app.py"]