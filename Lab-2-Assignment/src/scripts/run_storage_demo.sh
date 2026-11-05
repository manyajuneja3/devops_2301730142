#!/bin/bash
# ==============================================================================
# Script: run_storage_demo.sh
# Purpose: Demonstrate Docker Ephemeral Layers vs Named Volumes vs Bind Mounts
# ==============================================================================

set -e

echo "=== EXPERIMENT 6.1: Loss of Container-Layer Data after Deletion ==="
echo "[+] Starting ephemeral container..."
docker run -d --name ephemeral-demo-container alpine:latest sleep 3600
docker ps -f name=ephemeral-demo-container

echo "[+] Writing test data to non-persistent container layer (/data/state.txt)..."
docker exec ephemeral-demo-container mkdir -p /data
docker exec ephemeral-demo-container sh -c "echo 'CRITICAL_DATA_TIMESTAMP_$(date +%s)' > /data/state.txt"
echo "[+] Verifying file in active container:"
docker exec ephemeral-demo-container cat /data/state.txt

echo "[+] Stopping and deleting container..."
docker stop ephemeral-demo-container
docker rm ephemeral-demo-container

echo "[+] Launching new container from same image to inspect persistence..."
docker run -d --name ephemeral-verify-container alpine:latest sleep 3600
echo "[+] Attempting to read /data/state.txt in new container:"
if docker exec ephemeral-verify-container test -f /data/state.txt; then
    echo "ERROR: Data persisted unexpectedly!"
else
    echo "OBSERVATION: /data/state.txt NOT FOUND. Container layer data was destroyed on deletion (demonstrating ephemeral storage)."
fi
docker rm -f ephemeral-verify-container

echo ""
echo "=== EXPERIMENT 6.2: Permanent Storage Using Docker Named Volume ==="
echo "[+] Creating Docker named volume: persistent-app-vol..."
docker volume create persistent-app-vol
docker volume ls -f name=persistent-app-vol

echo "[+] Launching Container-A with volume mounted at /storage..."
docker run -d --name vol-producer --mount source=persistent-app-vol,target=/storage alpine:latest sleep 3600
docker exec vol-producer sh -c "echo 'VOLUME_PERSISTED_DATABASE_ENTRY_42' > /storage/records.db"
echo "[+] Wrote data via vol-producer:"
docker exec vol-producer cat /storage/records.db

echo "[+] Destroying Container-A..."
docker rm -f vol-producer

echo "[+] Launching Container-B mounting the SAME named volume..."
docker run -d --name vol-consumer --mount source=persistent-app-vol,target=/storage alpine:latest sleep 3600
echo "[+] Reading data in Container-B:"
docker exec vol-consumer cat /storage/records.db
echo "OBSERVATION: Data persisted across container destruction via Named Volume."
docker rm -f vol-consumer

echo ""
echo "=== EXPERIMENT 6.3: Permanent Storage Using Docker Bind Mount ==="
HOST_DIR="$(pwd)/host_storage_demo"
mkdir -p "$HOST_DIR"
echo "HOST_CONFIG_KEY=SECURE_VALUE_XYZ" > "$HOST_DIR/app.conf"

echo "[+] Launching container with Bind Mount from $HOST_DIR to /config..."
docker run -d --name bind-demo-container -v "$HOST_DIR":/config alpine:latest sleep 3600
echo "[+] Reading host file from inside container:"
docker exec bind-demo-container cat /config/app.conf

echo "[+] Modifying file from inside container..."
docker exec bind-demo-container sh -c "echo 'NEW_ENTRY_FROM_CONTAINER' >> /config/app.conf"

echo "[+] Verifying updated file directly on host file system:"
cat "$HOST_DIR/app.conf"

echo "[+] Removing container..."
docker rm -f bind-demo-container
echo "[+] Host file verification after container deletion:"
cat "$HOST_DIR/app.conf"
echo "OBSERVATION: Host filesystem retains data independently of container lifecycle."

