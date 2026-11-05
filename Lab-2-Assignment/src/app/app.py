"""
DevOps Lab 2 - Sample Microservice Application
Candidate: Manya Juneja
Roll Number: 2301730142
Email: manyajuneja03@gmail.com
"""

import os
import socket
import logging
from flask import Flask, jsonify, request

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Candidate & Environment metadata
STUDENT_NAME = "Manya Juneja"
STUDENT_ROLL = "2301730142"
STUDENT_EMAIL = "manyajuneja03@gmail.com"
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
APP_ENV = os.getenv("APP_ENV", "production")
HOSTNAME = socket.gethostname()
REDIS_HOST = os.getenv("REDIS_HOST", None)
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Optional Redis connection for multi-container compose demo
redis_client = None
if REDIS_HOST:
    try:
        import redis
        redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, socket_timeout=2)
        redis_client.ping()
        logging.info(f"Connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
    except Exception as e:
        logging.warning(f"Could not connect to Redis: {e}")
        redis_client = None

@app.route("/", methods=["GET"])
def index():
    visit_count = 1
    if redis_client:
        try:
            visit_count = redis_client.incr("page_views")
        except Exception:
            visit_count = "Redis unavailable"

    return jsonify({
        "student_name": STUDENT_NAME,
        "roll_number": STUDENT_ROLL,
        "email": STUDENT_EMAIL,
        "status": "success",
        "message": "Welcome to Cloud-Native Kubernetes & Docker Microservice",
        "version": APP_VERSION,
        "environment": APP_ENV,
        "pod_hostname": HOSTNAME,
        "visitor_count": visit_count
    }), 200

@app.route("/healthz", methods=["GET"])
def health():
    return jsonify({
        "student_name": STUDENT_NAME,
        "roll_number": STUDENT_ROLL,
        "status": "healthy",
        "version": APP_VERSION,
        "hostname": HOSTNAME
    }), 200

@app.route("/ready", methods=["GET"])
def ready():
    return jsonify({
        "status": "ready",
        "service": "active",
        "candidate": STUDENT_NAME
    }), 200

@app.route("/api/info", methods=["GET"])
def info():
    return jsonify({
        "app_name": "devops-lab-app",
        "student_name": STUDENT_NAME,
        "roll_number": STUDENT_ROLL,
        "email": STUDENT_EMAIL,
        "version": APP_VERSION,
        "hostname": HOSTNAME,
        "headers": dict(request.headers)
    }), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
