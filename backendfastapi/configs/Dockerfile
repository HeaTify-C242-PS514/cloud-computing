# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set Google Cloud credentials
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/capstone-test-443716-0f00e066d4e2.json

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
