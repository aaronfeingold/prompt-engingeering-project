# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install curl and other utilities for debugging
RUN apt-get update && apt-get install -y curl

# Copy the requirements file into the container
COPY pyproject.toml poetry.lock ./

# Install Poetry and configure it
RUN pip install poetry && \
    poetry config virtualenvs.create false

# Install the dependencies
RUN poetry install --no-root

# Copy the rest of the application code into the container
COPY . .

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Expose the port the app runs on
EXPOSE 5000

# Run the application directly using Python
CMD ["python", "run.py"]
