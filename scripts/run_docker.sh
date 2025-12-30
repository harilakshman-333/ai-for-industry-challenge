#!/bin/bash
# Build and run the Docker container

set -e

echo "Building Docker image..."
docker-compose build

echo "Starting container..."
xhost +local:docker  # Allow Docker to access X server for GUI

docker-compose up -d

echo "Container started. Entering container..."
docker exec -it ai_challenge_dev /bin/bash
