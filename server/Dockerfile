# Dockerfile for Flask app
FROM python:3.12-alpine

# Set the working directory for the Flask app container
WORKDIR /app

# Install build dependencies
RUN apk add --no-cache \
    build-base \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev \
    cargo \
    g++ \
    gfortran \
    openblas-dev

# Copy the requirements.txt and install dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copy the Flask app code into the container
COPY ./ /app

# Expose port 5000 for Flask
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]