FROM python:3.12-bullseye

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y dos2unix

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Make start script executable
RUN chmod +x start \
    && dos2unix start

# Environment variables with defaults
ENV APP_NAME=${APP_NAME} \
    SH_HOST=${SH_HOST} \
    SH_PORT=${SH_PORT} \
    SH_WORKER=${SH_WORKER} \
    FASTAPI_CONFIG=${FASTAPI_CONFIG}

# Expose the port specified in docker-compose
EXPOSE ${SH_PORT}
EXPOSE ${POSTGRES_HOST_PORT}

# Use start script as entrypoint (matches docker-compose entrypoint)
ENTRYPOINT ["./start"]
