# DevOps Foundations & Continuous Integration Pipeline

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://jenkins.io)
[![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue)](https://python.org)
[![Docker](https://img.shields.io/badge/docker-ready-2496ED)](https://docker.com)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-Jenkins%20Declarative%20Pipeline-red)](https://jenkins.io)

This repository contains the complete implementation for **DevOps Lab 1: DevOps Foundations & Continuous Integration**. It establishes version control, continuous integration, and automated deployment for a web application utilizing Git, GitHub, Docker, and Jenkins on Ubuntu Linux.

---

## 📋 Architecture Overview

The CI/CD pipeline implements a standard end-to-end DevOps automation flow:

```
+-----------------------------------------------------------------------------------+
|                                 DEVELOPER WORKSPACE                               |
|   git commit -> git push origin main / feature branches                          |
+------------------------------------------+----------------------------------------+
                                           |
                                           v
+-----------------------------------------------------------------------------------+
|                                GITHUB REPOSITORY                                  |
|   Webhook triggers Jenkins via HTTP POST (http://<jenkins-host>:8080/github-webhook)|
+------------------------------------------+----------------------------------------+
                                           |
                                           v
+-----------------------------------------------------------------------------------+
|                              JENKINS CI/CD SERVER                                 |
|                                                                                   |
|  [Stage 1: Checkout]     -> Clones repository SHA at commit point                 |
|  [Stage 2: Build]        -> Sets up Python venv, resolves requirements            |
|  [Stage 3: Test]         -> Executes PyTest unit test suite & generates JUnit XML |
|  [Stage 4: Package]      -> Bundles deployable release tarball / Docker image     |
|  [Stage 5: Deploy]       -> Executes deploy.sh, stops stale container, launches   |
|  [Stage 6: Healthcheck]  -> Probes /health endpoint to ensure zero downtime       |
|  [Post-Build Actions]    -> Archives JUnit reports, release artifacts & cleans up|
+------------------------------------------+----------------------------------------+
                                           |
                                           v
+-----------------------------------------------------------------------------------+
|                             DEPLOYMENT ENVIRONMENT                                |
|   Docker Container running on Port 5000 (http://localhost:5000)                   |
|   Endpoints: / (UI), /health (Health JSON API), /api/info (Metadata)              |
+-----------------------------------------------------------------------------------+
```

---

## 🛠 Project Structure

```
.
├── .gitignore              # Ignored files (virtualenvs, caches, logs)
├── app.py                  # Core Flask web application & REST endpoints
├── test_app.py             # Unit test suite for pytest / unittest
├── requirements.txt        # Python dependency manifest
├── Dockerfile              # Multi-stage container definition
├── deploy.sh               # Automated deployment & rollback verification script
├── Jenkinsfile             # Declarative Jenkins CI/CD pipeline definition
└── README.md               # Project documentation & execution guide
```

---

## 🚀 Quick Start & Local Execution

### 1. Run Unit Tests Locally
```bash
python -m unittest test_app.py -v
```

### 2. Run Application Locally
```bash
pip install -r requirements.txt
python app.py
```
Visit: `http://localhost:5000`

### 3. Run Containerized
```bash
docker build -t devops-sample-app:latest .
docker run -d -p 5000:5000 --name devops-sample-app devops-sample-app:latest
curl http://localhost:5000/health
```

---

## 🔧 Jenkins Pipeline Stages

| Stage | Goal | Commands / Actions |
|---|---|---|
| **Checkout** | Pulls latest code from Git | `checkout scm` |
| **Build & Dependencies** | Compiles code, isolates venv | `pip install -r requirements.txt`, `python -m py_compile` |
| **Run Tests** | Runs unit tests & exports JUnit XML | `pytest test_app.py --junitxml=test-results.xml` |
| **Package Artifacts** | Creates release archive | `tar -czf dist/${APP_NAME}-v${BUILD_NUMBER}.tar.gz` |
| **Deploy Application** | Zero-downtime container rollout | `bash deploy.sh` |
| **Health Verification** | Smoke test verification | `curl -f http://localhost:5000/health` |
| **Post-Build Actions** | Cleanup, reporting, notifications | `junit`, `archiveArtifacts`, `cleanWs()` |

---

## 📝 Lab Author
- **Course:** DevOps Foundations & Continuous Integration (Lab 1)
- **Status:** Complete & Fully Verified

