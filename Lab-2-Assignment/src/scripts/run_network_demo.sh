#!/bin/bash
# ==============================================================================
# Script: run_network_demo.sh
# Purpose: Demonstrate Docker Networking: Default Bridge vs Custom Bridge,
#          IP Communication vs Automatic DNS Container Name Resolution.
# ==============================================================================

set -e

echo "=== PART 1: Default Bridge Network Behavior (No Embedded DNS) ==="
docker run -d --name default-srv alpine sleep 3600
docker run -d --name default-cli alpine sleep 3600

DEFAULT_SRV_IP=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' default-srv)
echo "[+] Default server container IP: $DEFAULT_SRV_IP"

echo "[+] Pinging by IP on default bridge (Expected: Success)..."
docker exec default-cli ping -c 2 "$DEFAULT_SRV_IP"

echo "[+] Pinging by NAME on default bridge (Expected: FAILURE - no DNS on default bridge)..."
docker exec default-cli ping -c 1 default-srv || echo "OBSERVATION: Name resolution failed as expected on default bridge!"

docker rm -f default-srv default-cli

echo ""
echo "=== PART 2: Custom User-Defined Bridge Network ==="
echo "[+] Creating custom bridge network: lab-custom-network..."
docker network create --driver bridge lab-custom-network
docker network inspect lab-custom-network

echo "[+] Starting Web Server Container attached to custom network..."
docker run -d --name backend-server --network lab-custom-network alpine sh -c \
    "while true; do echo -e 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello from Backend Server Container!' | nc -l -p 8080; done"

echo "[+] Starting Client Container attached to custom network..."
docker run -d --name frontend-client --network lab-custom-network alpine sleep 3600

SERVER_IP=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' backend-server)
echo "[+] Backend server IP assigned: $SERVER_IP"

echo "[+] Test 1: Communication via Container IP Address:"
docker exec frontend-client wget -qO- "http://$SERVER_IP:8080"

echo ""
echo "[+] Test 2: Communication via Container Name (Docker Embedded DNS 127.0.0.11):"
docker exec frontend-client wget -qO- "http://backend-server:8080"

echo ""
echo "[+] Test 3: Inspecting DNS resolution via nslookup:"
docker exec frontend-client nslookup backend-server

echo "[+] Cleaning up..."
docker rm -f backend-server frontend-client
docker network rm lab-custom-network
echo "=== Network Demonstration Completed Successfully ==="

