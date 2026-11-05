"""
Lab 3: Monitoring, Logging & DevSecOps
Student: Manya Juneja
Roll No: 2301730142
Email: manyajuneja03@gmail.com
"""

import json
import logging
import os
import time
from datetime import datetime, timezone

from flask import Flask, Response, jsonify, request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest

app = Flask(__name__)
REQUESTS = Counter("demo_http_requests_total", "HTTP requests", ["method", "path", "status"])
LATENCY = Histogram("demo_http_request_duration_seconds", "Request duration", ["path"])
FEATURE_STATE = Gauge("demo_feature_greeting_v2_enabled", "Greeting feature flag state")


class JsonFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "service": "demo-app",
            "message": record.getMessage(),
            "event": getattr(record, "event", "application"),
        })


handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
app.logger.handlers = [handler]
app.logger.setLevel(logging.INFO)


def feature_enabled():
    return os.getenv("FEATURE_GREETING_V2", "false").lower() == "true"


@app.after_request
def observe(response):
    REQUESTS.labels(request.method, request.path, response.status_code).inc()
    return response


@app.get("/")
def home():
    with LATENCY.labels("/").time():
        enabled = feature_enabled()
        FEATURE_STATE.set(1 if enabled else 0)
        greeting = "Welcome to the v2 observable platform" if enabled else "Welcome to the observable platform"
        app.logger.info("homepage served", extra={"event": "homepage"})
        return jsonify({"message": greeting, "greeting_v2": enabled})


@app.get("/health")
def health():
    return jsonify({"status": "healthy"})


@app.get("/api/status")
def status():
    return jsonify({
        "service": "demo-app",
        "student": "Manya Juneja",
        "roll_no": "2301730142",
        "email": "manyajuneja03@gmail.com",
        "feature_greeting_v2": feature_enabled(),
        "time": datetime.now(timezone.utc).isoformat()
    })


@app.get("/api/log-demo")
def log_demo():
    app.logger.info("demonstration log event created", extra={"event": "lab_log_demo"})
    return jsonify({"result": "structured log emitted"})


@app.get("/metrics")
def metrics():
    FEATURE_STATE.set(1 if feature_enabled() else 0)
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
