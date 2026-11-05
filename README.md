# DevOps Assignment

**Student Name:** Manya Juneja  
**Roll Number:** 2301730142  
**Email:** manyajuneja03@gmail.com  
**GitHub:** [@manyajuneja3](https://github.com/manyajuneja3)

This repository contains all three DevOps laboratory assignments. Each lab lives in its own folder with its source code, configuration, and submission-ready reports.

---

## Labs at a glance

| Lab | Topic | Key tools | Folder |
| :---: | :--- | :--- | :--- |
| **1** | DevOps Foundations & Continuous Integration | Git, GitHub, Jenkins, Docker, Python/Flask, pytest | [`Lab-1-Assignment/`](Lab-1-Assignment/) |
| **2** | Containerization & Kubernetes Orchestration | Docker, Docker Compose, Kubernetes (Minikube), kubectl, Kustomize, GitHub Actions | [`Lab-2-Assignment/`](Lab-2-Assignment/) |
| **3** | Monitoring, Logging & DevSecOps | Ansible, Terraform, Prometheus, Grafana, ELK (Elasticsearch, Logstash, Kibana, Filebeat), Trivy, Semgrep, pip-audit, Selenium, Locust | [`Lab-3-Assignment/`](Lab-3-Assignment/) |

---

## Lab 1: DevOps Foundations & Continuous Integration

A Flask web application with a full Jenkins CI/CD pipeline: checkout, build, test, package, deploy, and health check.

- `app.py`, `test_app.py`: application and unit tests
- `Dockerfile`, `deploy.sh`: container build and automated deployment
- `Jenkinsfile`: declarative pipeline definition
- `submissions/`: written reports for Q1–Q7 and a comprehensive submission report

See [Lab-1-Assignment/README.md](Lab-1-Assignment/README.md) for the architecture and run instructions.

## Lab 2: Containerization & Kubernetes Orchestration

Nine experiments covering Docker images, Compose, storage, networking, Kubernetes deployments, rolling updates, rollbacks, scaling, and continuous deployment.

- `src/app/`: Flask microservice and Dockerfiles
- `src/compose/`, `src/k8s/`: Docker Compose and Kubernetes manifests
- `src/cicd/`: GitHub Actions deployment workflow
- `submissions/`: one PDF report per question (Q1–Q9)
- `zip_submissions/`: one ZIP package per question, plus a complete package

See [Lab-2-Assignment/README.md](Lab-2-Assignment/README.md) for the question-to-file mapping.

## Lab 3: Monitoring, Logging & DevSecOps

A local observability and security stack around a Flask application with a feature flag.

- `ansible/`, `terraform/`: infrastructure automation and provisioning
- `logging/`, `observability/`: ELK pipeline, Prometheus, and Grafana configuration
- `.github/workflows/devsecops.yml`: security scanning pipeline
- `tests/`: Selenium end-to-end and Locust load tests
- `evidence/screenshots/`: execution evidence
- `submission/`: PDF, DOCX, and ZIP deliverables for tasks 1–7

See [Lab-3-Assignment/README.md](Lab-3-Assignment/README.md) for the quick start and evidence commands.

---

## Repository structure

```
DevOps-Assignment/
├── Lab-1-Assignment/   # DevOps Foundations & CI (Jenkins)
├── Lab-2-Assignment/   # Docker & Kubernetes
├── Lab-3-Assignment/   # Monitoring, Logging & DevSecOps
└── README.md
```

> **Note:** The GitHub Actions workflows are stored inside each lab folder as assignment material. They do not run automatically from these locations.
