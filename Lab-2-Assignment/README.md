# DevOps Lab 2: Containerization & Kubernetes Orchestration

**Student Name:** Manya Juneja  
**Roll Number:** 2301730142  
**GitHub Profile:** [@manyajuneja3](https://github.com/manyajuneja3)  
**Repository:** [https://github.com/manyajuneja3/DevOps-Assignment.git](https://github.com/manyajuneja3/DevOps-Assignment.git)  
**Email Address:** manyajuneja03@gmail.com  
**Course:** DevOps Engineering Laboratory  
**Assessment:** Lab 2 Assessment (50 Marks Total)  
**Environment:** Docker Engine 29.x, Docker Compose v5.x, Kubernetes (Minikube) v1.36 / v1.30, kubectl, Python 3.11/3.13  

---

## 📁 Repository Structure & Deliverables

```
d:\Devops Lab 2\
├── submissions/                           <-- 🎯 UPLOAD-READY PDF FILES (One per question)
│   ├── Question_1_Kubernetes_Deployment_and_Service.pdf
│   ├── Question_2_Kubernetes_Rolling_Update_Rollback_Scaling.pdf
│   ├── Question_3_Containerization_and_Orchestration_Report.pdf
│   ├── Question_4_Containerize_Application_Docker.pdf
│   ├── Question_5_Manage_Docker_Containers_and_Compose.pdf
│   ├── Question_6_Docker_Storage_Volumes_BindMounts.pdf
│   ├── Question_7_Docker_Network_Container_Communication.pdf
│   ├── Question_8_Continuous_Deployment_Kubernetes_CICD.pdf
│   └── Question_9_Master_Tools_Manifests_Record_Book.pdf
│
├── zip_submissions/                       <-- 📦 UPLOAD-READY ZIP PACKAGES (Alternative upload)
│   ├── Q1_Kubernetes_Deployment.zip
│   ├── Q2_Kubernetes_Strategies_Scaling.zip
│   ├── Q3_Orchestration_Report.zip
│   ├── Q4_Docker_Containerization.zip
│   ├── Q5_Docker_Management_Compose.zip
│   ├── Q6_Docker_Storage.zip
│   ├── Q7_Docker_Network.zip
│   ├── Q8_Continuous_Deployment.zip
│   ├── Q9_All_Tools_Documentation.zip
│   └── Complete_DevOps_Lab2_Package.zip  <-- Entire workspace archive
│
├── src/                                  <-- 💻 Source Code, Dockerfiles & Manifests
│   ├── app/                              <-- Microservice source & Dockerfiles
│   │   ├── app.py                        <-- Flask REST API with candidate metadata & health endpoints
│   │   ├── requirements.txt              <-- Pinned dependencies (Flask, Redis, Gunicorn)
│   │   ├── Dockerfile                    <-- Multi-stage production build (Non-root UID 10001)
│   │   └── Dockerfile.simple             <-- Single-stage build for layer analysis
│   ├── compose/
│   │   └── docker-compose.yml            <-- Multi-container setup (Web App + Redis Cache)
│   ├── k8s/                              <-- Kubernetes YAML manifests
│   │   ├── deployment.yaml               <-- 3 replicas, RollingUpdate strategy, health probes
│   │   ├── service.yaml                  <-- NodePort service (Port 80 -> NodePort 30080)
│   │   ├── configmap.yaml                <-- Application configuration
│   │   ├── deployment-v2.yaml            <-- Version 2.0 image for rolling update
│   │   ├── deployment-broken.yaml        <-- Simulated faulty image for rollback
│   │   └── kustomization.yaml            <-- Kustomize configuration for GitOps CD
│   ├── cicd/
│   │   └── .github/workflows/deploy.yml  <-- Production GitHub Actions CI/CD Pipeline
│   └── scripts/
│       ├── run_storage_demo.sh           <-- Automated storage demonstration script
│       └── run_network_demo.sh           <-- Automated network demonstration script
│
└── docs/                                 <-- 📄 Detailed Markdown Technical Documentation
```

---

## 📋 Quick Submission Mapping Guide

| Question # | Topic | Marks | PDF Submission File | ZIP Submission File |
| :---: | :--- | :---: | :--- | :--- |
| **1** | Deploy App to Kubernetes (Minikube) & Verify Pods | 5 | `submissions/Question_1_Kubernetes_Deployment_and_Service.pdf` | `zip_submissions/Q1_Kubernetes_Deployment.zip` |
| **2** | Kubernetes Strategies (Rolling Update, Rollback, Scaling) | 5 | `submissions/Question_2_Kubernetes_Rolling_Update_Rollback_Scaling.pdf` | `zip_submissions/Q2_Kubernetes_Strategies_Scaling.zip` |
| **3** | Containerization & Orchestration Report | 10 | `submissions/Question_3_Containerization_and_Orchestration_Report.pdf` | `zip_submissions/Q3_Orchestration_Report.zip` |
| **4** | Containerize Sample App using Docker & Layer Analysis | 5 | `submissions/Question_4_Containerize_Application_Docker.pdf` | `zip_submissions/Q4_Docker_Containerization.zip` |
| **5** | Manage Docker Containers/Images & Docker Compose | 5 | `submissions/Question_5_Manage_Docker_Containers_and_Compose.pdf` | `zip_submissions/Q5_Docker_Management_Compose.zip` |
| **6** | Docker Storage (Loss of Ephemeral Layer, Volumes, Binds) | 5 | `submissions/Question_6_Docker_Storage_Volumes_BindMounts.pdf` | `zip_submissions/Q6_Docker_Storage.zip` |
| **7** | Docker Network (Custom Network, IP vs Name Resolution) | 5 | `submissions/Question_7_Docker_Network_Container_Communication.pdf` | `zip_submissions/Q7_Docker_Network.zip` |
| **8** | Continuous Deployment via Kubernetes & CI/CD Pipeline | 5 | `submissions/Question_8_Continuous_Deployment_Kubernetes_CICD.pdf` | `zip_submissions/Q8_Continuous_Deployment.zip` |
| **9** | Master Record of all Manifests, Commands & Logs | 5 | `submissions/Question_9_Master_Tools_Manifests_Record_Book.pdf` | `zip_submissions/Q9_All_Tools_Documentation.zip` |
| **Total**| **All 9 Lab Experiments** | **50** | **9 Standardized Documents** | **9 Standalone ZIP Packages** |
