# Lab 3: Monitoring, Logging & DevSecOps

**Student Name:** Manya Juneja  
**Roll No:** 2301730142  
**Email:** manyajuneja03@gmail.com  
**Course Activity:** Lab 3: Monitoring, Logging & DevSecOps  
**GitHub Repository:** https://github.com/manyajuneja3/DevOps-Assignment.git  

This repository is a reproducible, local lab implementation. It deploys a small Flask application with a feature flag, Prometheus metrics, Grafana, Elasticsearch, Logstash, Kibana, and Filebeat. Ansible automates host preparation and application deployment; Terraform demonstrates horizontally scaled application containers; CI verifies dependencies and scans the repository.

## Architecture

`Browser -> demo-app -> Prometheus -> Grafana`  
`demo-app JSON stdout -> Filebeat -> Logstash -> Elasticsearch -> Kibana`

The `demo-app` publishes `/health`, `/metrics`, `/api/status`, and `/api/log-demo`. The log-demo endpoint creates structured records that are easy to find in Kibana.

## Prerequisites

- Docker Desktop or Docker Engine with Compose v2
- Python 3.11+ for tests and Locust
- Terraform 1.6+ and the Docker provider for the Terraform exercise
- Ansible 2.14+ for the Ansible exercise

Do all execution only on the authorized laboratory environment. Copy `.env.example` to `.env` before starting.

## Quick start

```powershell
Copy-Item .env.example .env
docker compose up -d --build
Invoke-WebRequest http://localhost:8080/health
Invoke-WebRequest http://localhost:8080/api/log-demo
```

Open Grafana at `http://localhost:3000` (admin / admin) and Kibana at `http://localhost:5601`. The Prometheus target page is `http://localhost:9090/targets`.

## Evidence commands

```powershell
# Infrastructure automation
ansible-galaxy collection install -r ansible/requirements.yml
ansible-playbook -i ansible/inventory.ini ansible/site.yml --check
ansible-playbook -i ansible/inventory.ini ansible/site.yml

# IaC plan/apply (uses Docker provider)
terraform -chdir=terraform init
terraform -chdir=terraform plan -var='replicas=2'
terraform -chdir=terraform apply -var='replicas=2'

# Logging and monitoring activity
Invoke-WebRequest http://localhost:8080/api/log-demo
Invoke-WebRequest http://localhost:8080/api/status

# Tests and security
python -m pip install -r tests/requirements.txt
pytest tests/e2e -q
locust -f tests/load/locustfile.py --headless -u 10 -r 2 -t 30s --host http://localhost:8080
docker run --rm -v ${PWD}:/src aquasec/trivy:latest fs --severity HIGH,CRITICAL /src
```

Use the report in `report/` as the submission narrative. Capture the indicated screenshots while running these commands, then update its evidence placeholders before submission.

## Shutdown

```powershell
docker compose down -v
```
