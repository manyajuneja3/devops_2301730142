#!/bin/bash
# ==============================================================================
# Script: deploy.sh
# Purpose: Automated Deployment Script for DevOps Lab 1 CI/CD Pipeline
# ==============================================================================
set -e

APP_NAME="devops-sample-app"
APP_PORT="5000"
HOST_PORT="5000"
IMAGE_NAME="${APP_NAME}:latest"
DEPLOY_LOG="deployment.log"

echo "=========================================="
echo "Starting Automated Deployment at $(date)"
echo "Target Application: ${APP_NAME}"
echo "=========================================="

# 1. Stop and remove existing container if running
echo "[Step 1/4] Checking for existing deployment..."
if [ "$(docker ps -q -f name=${APP_NAME})" ]; then
    echo "Stopping existing container ${APP_NAME}..."
    docker stop ${APP_NAME}
fi

if [ "$(docker ps -aq -f name=${APP_NAME})" ]; then
    echo "Removing existing container ${APP_NAME}..."
    docker rm ${APP_NAME}
fi

# 2. Build Docker container image
echo "[Step 2/4] Building production container image: ${IMAGE_NAME}..."
docker build -t ${IMAGE_NAME} .

# 3. Spin up new container
echo "[Step 3/4] Launching container on port ${HOST_PORT}..."
docker run -d \
  --name ${APP_NAME} \
  --restart unless-stopped \
  -p ${HOST_PORT}:${APP_PORT} \
  -e APP_VERSION="${BUILD_NUMBER:-1.0.0}" \
  -e ENVIRONMENT="Production" \
  ${IMAGE_NAME}

# 4. Deployment Health Verification
echo "[Step 4/4] Verifying deployment health status..."
sleep 3

MAX_RETRIES=10
RETRY_COUNT=0
HEALTHY=false

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:${HOST_PORT}/health || echo "000")
    if [ "$HTTP_STATUS" -eq 200 ]; then
        echo "Healthcheck passed! HTTP status $HTTP_STATUS received."
        HEALTHY=true
        break
    fi
    echo "Waiting for service to be healthy... Attempt $((RETRY_COUNT+1))/$MAX_RETRIES (Status: $HTTP_STATUS)"
    sleep 2
    RETRY_COUNT=$((RETRY_COUNT+1))
done

if [ "$HEALTHY" = true ]; then
    echo "=========================================="
    echo "DEPLOYMENT SUCCESSFUL!"
    echo "Application is live at: http://localhost:${HOST_PORT}/"
    echo "Health Endpoint: http://localhost:${HOST_PORT}/health"
    echo "=========================================="
    exit 0
else
    echo "Deployment failed! Health check did not return HTTP 200." >&2
    docker logs ${APP_NAME}
    exit 1
fi

