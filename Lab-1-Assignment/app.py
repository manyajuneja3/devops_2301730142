from flask import Flask, jsonify, render_template_string
import os
import datetime

app = Flask(__name__)
VERSION = os.getenv("APP_VERSION", "1.0.0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "Production")
START_TIME = datetime.datetime.now(datetime.timezone.utc)

HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DevOps Lab 1 - CI/CD Web Application</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif; }
        body { background: #0f172a; color: #f8fafc; min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; }
        .card { background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 32px; max-width: 650px; width: 100%; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4); }
        .badge { display: inline-block; background: #0284c7; color: white; padding: 4px 12px; border-radius: 9999px; font-size: 12px; font-weight: 600; text-transform: uppercase; margin-bottom: 16px; }
        .badge.healthy { background: #10b981; }
        h1 { font-size: 26px; margin-bottom: 8px; color: #38bdf8; }
        p.subtitle { color: #94a3b8; font-size: 15px; margin-bottom: 24px; line-height: 1.5; }
        .metrics-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; margin-bottom: 24px; }
        .metric-box { background: #0f172a; padding: 16px; border-radius: 8px; border: 1px solid #334155; }
        .metric-title { font-size: 12px; color: #64748b; text-transform: uppercase; font-weight: 600; margin-bottom: 4px; }
        .metric-value { font-size: 18px; font-weight: 700; color: #f1f5f9; }
        .status-badge { color: #34d399; font-weight: 600; }
        .footer { border-top: 1px solid #334155; padding-top: 16px; display: flex; justify-content: space-between; font-size: 13px; color: #64748b; }
        .nav-links a { color: #38bdf8; text-decoration: none; margin-right: 12px; font-size: 13px; }
        .nav-links a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="card">
        <span class="badge healthy">● System Online</span>
        <h1>DevOps Foundations CI/CD App</h1>
        <p class="subtitle">Automated Continuous Integration and Continuous Deployment pipeline powered by Git, GitHub, and Jenkins on Ubuntu Linux.</p>
        
        <div class="metrics-grid">
            <div class="metric-box">
                <div class="metric-title">Application Version</div>
                <div class="metric-value">{{ version }}</div>
            </div>
            <div class="metric-box">
                <div class="metric-title">Deployment Environment</div>
                <div class="metric-value">{{ environment }}</div>
            </div>
            <div class="metric-box">
                <div class="metric-title">CI/CD Engine</div>
                <div class="metric-value">Jenkins 2.450+ LTS</div>
            </div>
            <div class="metric-box">
                <div class="metric-title">Health Status</div>
                <div class="metric-value status-badge">100% Operational</div>
            </div>
        </div>

        <div class="nav-links" style="margin-bottom: 20px;">
            <a href="/health" target="_blank">View Health JSON API &rarr;</a>
            <a href="/api/info" target="_blank">View Build Info API &rarr;</a>
        </div>

        <div class="footer">
            <span>DevOps Lab 1 Assessment</span>
            <span>Automated Build: #Passed</span>
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HOME_TEMPLATE, version=VERSION, environment=ENVIRONMENT)

@app.route("/health")
def health():
    uptime_seconds = (datetime.datetime.now(datetime.timezone.utc) - START_TIME).total_seconds()
    return jsonify({
        "status": "UP",
        "healthy": True,
        "uptime_seconds": round(uptime_seconds, 2),
        "version": VERSION,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }), 200

@app.route("/metrics")
def metrics():
    return jsonify({
        "cpu_usage_simulated": "12.4%",
        "memory_usage_mb": 45.2,
        "active_threads": 4,
        "request_count": 142
    }), 200

@app.route("/api/info")
def info():
    return jsonify({
        "project": "DevOps Foundations & Continuous Integration",
        "lab": "Lab 1",
        "framework": "Flask / Python 3",
        "ci_cd_tool": "Jenkins Declarative Pipeline",
        "vcs": "Git & GitHub",
        "version": VERSION,
        "environment": ENVIRONMENT
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
