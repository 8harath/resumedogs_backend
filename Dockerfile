# filepath: /media/kitn/CodeStuff/cv_bandar/Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables to prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1

# Install system dependencies required for pdflatex and potentially other libraries
# Using texlive-full is large (~3GB+), consider texlive-latex-base and specific packages if size is critical
RUN apt-get update && apt-get install -y --no-install-recommends \
    texlive-latex-base \
    texlive-fonts-recommended \
    texlive-latex-extra \
    # Add any other system dependencies your Python packages might need
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# Use --no-cache-dir to reduce image size
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
# Ensure .dockerignore excludes .venv, .env, __pycache__, etc. if needed
COPY . .

# Make port 8080 available to the world outside this container (or the port you configure via $PORT)
# The actual port mapping happens during `docker run`
EXPOSE 8080

# Define environment variable for the port (optional, uvicorn default is 8000)
ENV PORT=8080
ENV HOST=0.0.0.0 
# Listen on all interfaces within the container

# Run uvicorn when the container launches
# Use 0.0.0.0 as host to be accessible from outside the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "4"]