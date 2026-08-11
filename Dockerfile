# Use an official lightweight Python image as the base
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Prevent Python from writing .pyc files and enable real-time output logging
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system-level packages needed for database connections
RUN apt-get update && apt-get install -y libpq-dev gcc

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Open port 8000 for the Django web server
EXPOSE 8000