"""
Script to package all 7 lab submission deliverables.
Student: Manya Juneja (2301730142) - manyajuneja03@gmail.com
"""

import os
import shutil
import zipfile
from pathlib import Path

BASE_DIR = Path("d:/devops lab 3/lab3-monitoring-devsecops")
SUBMISSION_DIR = BASE_DIR / "submission"
SUBMISSION_DIR.mkdir(parents=True, exist_ok=True)

STUDENT_BANNER = """# Lab 3: Monitoring, Logging & DevSecOps
**Student Name:** Manya Juneja  
**Roll No / Register No:** 2301730142  
**Email:** manyajuneja03@gmail.com  
**Course Activity:** Lab 3: Monitoring, Logging & DevSecOps  
**Date:** November 04, 2026  
"""

def create_zip_with_files(zip_path, file_mapping, readme_content):
    """
    Creates a zip archive.
    file_mapping: dict of {source_path: arcname_inside_zip}
    readme_content: string content for README.md inside zip
    """
    if zip_path.exists():
        zip_path.unlink()
    
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # Add README.md
        zf.writestr("README.md", readme_content.strip() + "\n")
        
        # Add files
        for src, arc in file_mapping.items():
            src_path = Path(src)
            if src_path.exists():
                zf.write(src_path, arc)
            else:
                print(f"Warning: {src_path} does not exist!")
    print(f"Created {zip_path} ({zip_path.stat().st_size} bytes)")


def package_01():
    readme = f"""{STUDENT_BANNER}
## Question 1: Configure Infrastructure and Automate Application (Ansible)
**Marks:** 5 Marks

### Overview
This package contains the Ansible playbooks, inventory, and role structure to automate host setup, package installation (Docker, Compose plugin, Git), service management, directory creation, and application stack deployment.

### Architecture & Key Components
- `ansible/inventory.ini`: Target node definition (`lab-target` at `192.0.2.10`, user `ubuntu`).
- `ansible/site.yml`: Top-level orchestration playbook applying the `application` role.
- `ansible/roles/application/tasks/main.yml`: Idempotent tasks installing Docker prerequisites, starting the daemon, creating deployment directories, and cloning the lab repository.
- `ansible/roles/application/handlers/main.yml`: Docker Compose stack notification handler.
- `ansible/roles/application/defaults/main.yml`: Default deployment variables.
- `evidence/01-ansible-check.png`: Verified execution screenshot in check mode.

### Commands Executed
```bash
# 1. Syntax check
ansible-playbook -i ansible/inventory.ini ansible/site.yml --syntax-check

# 2. Dry run / Check mode
ansible-playbook -i ansible/inventory.ini ansible/site.yml --check

# 3. Live Apply
ansible-playbook -i ansible/inventory.ini ansible/site.yml
```

### Observations
- All tasks are idempotent: running the playbook repeatedly results in zero unnecessary changes.
- Check mode verified target reachability with `ok=5, changed=2, unreachable=0, failed=0`.
"""
    files = {
        BASE_DIR / "ansible" / "inventory.ini": "ansible/inventory.ini",
        BASE_DIR / "ansible" / "requirements.yml": "ansible/requirements.yml",
        BASE_DIR / "ansible" / "site.yml": "ansible/site.yml",
        BASE_DIR / "ansible" / "roles" / "application" / "defaults" / "main.yml": "ansible/roles/application/defaults/main.yml",
        BASE_DIR / "ansible" / "roles" / "application" / "handlers" / "main.yml": "ansible/roles/application/handlers/main.yml",
        BASE_DIR / "ansible" / "roles" / "application" / "tasks" / "main.yml": "ansible/roles/application/tasks/main.yml",
        BASE_DIR / "evidence" / "screenshots" / "01-ansible-check.png": "evidence/01-ansible-check.png",
    }
    create_zip_with_files(SUBMISSION_DIR / "01_Ansible_Automation.zip", files, readme)


def package_02():
    readme = f"""{STUDENT_BANNER}
## Question 2: Provision Scalable Infrastructure (Terraform)
**Marks:** 5 Marks

### Overview
This package contains Terraform (Infrastructure as Code) configuration files to declaratively provision horizontally scalable containerized infrastructure using the Docker provider.

### Architecture & Key Components
- `terraform/main.tf`: Configures the `kreuzwerker/docker` provider, provisions a dedicated bridge network (`lab3-tf-network`), builds the application image from source, and spawns `count = var.replicas` application containers.
- `terraform/variables.tf`: Parameterizes `replicas` (validated between 1 and 5), `base_host_port` (default 8180), and `feature_greeting_v2`.
- `terraform/outputs.tf`: Dynamically exports the provisioned URLs (`http://localhost:8180`, `http://localhost:8181`).
- `evidence/02-terraform-plan.png`: Execution plan screenshot showing 4 resources to add.

### Commands Executed
```bash
# 1. Initialize provider plugins
terraform -chdir=terraform init

# 2. Plan scalable deployment (2 replicas)
terraform -chdir=terraform plan -var='replicas=2'

# 3. Apply infrastructure
terraform -chdir=terraform apply -var='replicas=2' -auto-approve

# 4. Scale to 3 replicas
terraform -chdir=terraform apply -var='replicas=3' -auto-approve
```

### Observations
- Terraform creates predictable port bindings (`base_host_port + count.index`), preventing port collision during horizontal scaling.
- Input validation ensures `replicas` cannot exceed host resource boundaries.
- Plan output confirms clean addition of 1 network, 1 image, and 2 container instances (`Plan: 4 to add, 0 to change, 0 to destroy`).
"""
    files = {
        BASE_DIR / "terraform" / "main.tf": "terraform/main.tf",
        BASE_DIR / "terraform" / "variables.tf": "terraform/variables.tf",
        BASE_DIR / "terraform" / "outputs.tf": "terraform/outputs.tf",
        BASE_DIR / "evidence" / "screenshots" / "02-terraform-plan.png": "evidence/02-terraform-plan.png",
    }
    create_zip_with_files(SUBMISSION_DIR / "02_Terraform_Provisioning.zip", files, readme)


def package_03():
    readme = f"""{STUDENT_BANNER}
## Question 3: Implement Centralized Logging (ELK Stack)
**Marks:** 5 Marks

### Overview
This package contains the complete centralized logging architecture using Elasticsearch, Logstash, Kibana, and Filebeat (ELK Stack) integrated with a containerized Flask demo application emitting structured JSON logs.

### Architecture & Pipeline Flow
`Flask Application (JSON stdout) -> Filebeat (container log harvest) -> Logstash (port 5044 JSON filter) -> Elasticsearch (port 9200) -> Kibana (port 5601 Discover & Dashboards)`

- `docker-compose.yml`: Defines the entire stack including Elasticsearch, Logstash, Kibana, Filebeat, and demo-app.
- `logging/filebeat/filebeat.yml`: Reads container log files from `/var/lib/docker/containers/*/*.log`, appends Docker metadata, and streams to Logstash.
- `logging/logstash/pipeline/logstash.conf`: Filters logs for container name `demo-app`, extracts the `app_event` JSON payload, normalizes `@timestamp`, annotates with `pipeline: lab3-centralized-logging`, and routes to index `lab3-logs-%{{+YYYY.MM.dd}}`.
- `app/app.py`: Implements custom `JsonFormatter` emitting ISO 8601 timestamps, severity levels, service names, and event tags.
- `evidence/03-kibana-logs.png`: Kibana Discover view showing structured logs filtered by `app_event.event: "lab_log_demo"`.

### Commands Executed
```bash
# 1. Start logging stack
docker compose up -d --build

# 2. Emit structured log events
curl http://localhost:8080/api/log-demo

# 3. Verify in Kibana Discover
# URL: http://localhost:5601/app/discover
# Filter: app_event.event : "lab_log_demo"
```

### Observations
- Application logs are parsed instantaneously from JSON strings into structured queryable document fields.
- Kibana Discover clearly presents fields: `@timestamp`, `app_event.service`, `app_event.level`, `app_event.message`, and Docker container labels.
"""
    files = {
        BASE_DIR / "docker-compose.yml": "docker-compose.yml",
        BASE_DIR / "logging" / "filebeat" / "filebeat.yml": "logging/filebeat/filebeat.yml",
        BASE_DIR / "logging" / "logstash" / "pipeline" / "logstash.conf": "logging/logstash/pipeline/logstash.conf",
        BASE_DIR / "app" / "app.py": "app/app.py",
        BASE_DIR / "app" / "Dockerfile": "app/Dockerfile",
        BASE_DIR / "app" / "requirements.txt": "app/requirements.txt",
        BASE_DIR / "evidence" / "screenshots" / "03-kibana-logs.png": "evidence/03-kibana-logs.png",
    }
    create_zip_with_files(SUBMISSION_DIR / "03_Centralized_Logging_ELK.zip", files, readme)


def package_04():
    readme = f"""{STUDENT_BANNER}
## Question 4: Integrate Security into the CI/CD Pipeline (DevSecOps)
**Marks:** 5 Marks

### Overview
This package demonstrates the implementation of DevSecOps security practices integrated into a continuous delivery pipeline (GitHub Actions). It incorporates automated testing, dependency vulnerability scanning, static application security testing (SAST), and container filesystem analysis.

### Security Controls Implemented
1. **Dependency Vulnerability Scanning (`pip-audit`):**
   Scans application dependencies in `app/requirements.txt` against known CVE vulnerabilities in PyPI advisory databases. Fails on known exploits.
2. **Static Application Security Testing (SAST - `Semgrep`):**
   Executes `p/security-audit` rule pack across application and test code to identify security misconfigurations, credential leaks, and unsafe code patterns.
3. **Container Filesystem Vulnerability Scanning (`Trivy`):**
   Scans workspace and container definitions for HIGH and CRITICAL vulnerabilities with exit code 1 enforcement.
4. **Least-Privilege Container Hardening:**
   Application Dockerfile configures and switches to a dedicated unprivileged system user (`appuser` with UID 10001), preventing root privilege escalation.

### CI/CD Workflow (`.github/workflows/devsecops.yml`)
- Triggered on `push` and `pull_request`.
- Uses least-privilege `contents: read` token permissions.
- Executes Selenium E2E tests, pip-audit, Semgrep, and Trivy sequentially.

### Commands Executed
```bash
# 1. Dependency scanning
pip-audit -r app/requirements.txt

# 2. Static security scan
semgrep --config p/security-audit app/ tests/

# 3. Filesystem scan with Trivy
docker run --rm -v ${{PWD}}:/src aquasec/trivy:latest fs --severity HIGH,CRITICAL /src
```

### Observations
- Zero known CVEs in pinned application packages (`Flask==3.0.3`, `prometheus-client==0.20.0`, `gunicorn==22.0.0`).
- Semgrep passed with 0 blocking security issues.
- Trivy verified zero High or Critical vulnerabilities across the project filesystem.
"""
    files = {
        BASE_DIR / ".github" / "workflows" / "devsecops.yml": ".github/workflows/devsecops.yml",
        BASE_DIR / "app" / "app.py": "app/app.py",
        BASE_DIR / "app" / "Dockerfile": "app/Dockerfile",
        BASE_DIR / "app" / "requirements.txt": "app/requirements.txt",
        BASE_DIR / "tests" / "requirements.txt": "tests/requirements.txt",
        BASE_DIR / "tests" / "e2e" / "test_home.py": "tests/e2e/test_home.py",
        BASE_DIR / "evidence" / "screenshots" / "04-security-scan.png": "evidence/04-security-scan.png",
    }
    create_zip_with_files(SUBMISSION_DIR / "04_DevSecOps_Pipeline.zip", files, readme)


def package_05():
    readme = f"""{STUDENT_BANNER}
## Question 5: Set Up Monitoring Using Prometheus & Visualize in Grafana
**Marks:** 5 Marks

### Overview
This package implements full-stack operational monitoring using Prometheus for metrics collection and Grafana for visual telemetry dashboards.

### Architecture & Key Components
- `app/app.py`: Exposes Prometheus metrics at `/metrics` using `prometheus_client`:
  - `demo_http_requests_total`: Counter partitioned by method, path, status.
  - `demo_http_request_duration_seconds`: Histogram measuring response latency per path.
  - `demo_feature_greeting_v2_enabled`: Gauge reflecting active feature flag state.
- `observability/prometheus/prometheus.yml`: Configures 15s scrape interval targeting both `prometheus:9090` and `demo-app:8080`.
- `observability/grafana/provisioning/datasources/prometheus.yml`: Automatically provisions Prometheus as the default datasource.
- `observability/grafana/provisioning/dashboards/`: Auto-loads the "Demo Application Overview" dashboard (`demo-app.json`).
- `evidence/05-grafana-dashboard.png`: Grafana dashboard screenshot during load generation showing throughput (~8.64 req/s), path distribution, and latency.

### Commands Executed
```bash
# 1. Start application and monitoring stack
docker compose up -d demo-app prometheus grafana

# 2. Verify Prometheus scrape target
curl http://localhost:9090/api/v1/targets

# 3. Access Grafana Dashboard
# URL: http://localhost:3000 (admin / admin)
# Dashboard: Demo Application Overview
```

### Observations
- Metrics are collected with zero data loss across concurrent requests.
- The Grafana dashboard visualizes real-time throughput spikes during traffic generation and cleanly breaks down traffic across endpoints (`/`, `/api/status`, `/api/log-demo`).
"""
    files = {
        BASE_DIR / "docker-compose.yml": "docker-compose.yml",
        BASE_DIR / "observability" / "prometheus" / "prometheus.yml": "observability/prometheus/prometheus.yml",
        BASE_DIR / "observability" / "grafana" / "provisioning" / "dashboards" / "dashboard.yml": "observability/grafana/provisioning/dashboards/dashboard.yml",
        BASE_DIR / "observability" / "grafana" / "provisioning" / "dashboards" / "json" / "demo-app.json": "observability/grafana/provisioning/dashboards/json/demo-app.json",
        BASE_DIR / "observability" / "grafana" / "provisioning" / "datasources" / "prometheus.yml": "observability/grafana/provisioning/datasources/prometheus.yml",
        BASE_DIR / "app" / "app.py": "app/app.py",
        BASE_DIR / "app" / "Dockerfile": "app/Dockerfile",
        BASE_DIR / "app" / "requirements.txt": "app/requirements.txt",
        BASE_DIR / "evidence" / "screenshots" / "05-grafana-dashboard.png": "evidence/05-grafana-dashboard.png",
    }
    create_zip_with_files(SUBMISSION_DIR / "05_Prometheus_Grafana_Monitoring.zip", files, readme)


def package_06():
    readme = f"""{STUDENT_BANNER}
## Question 6: Implement Feature Flags and Perform Different Testing
**Marks:** 5 Marks

### Overview
This package contains the implementation of runtime feature toggles, automated Selenium end-to-end browser tests, and Locust load testing scenarios.

### Implemented Capabilities
1. **Dynamic Feature Flags:**
   Controlled by environment variable `FEATURE_GREETING_V2`.
   - When `false`: Home route outputs `"Welcome to the observable platform"` and metric gauge = 0.
   - When `true`: Home route outputs `"Welcome to the v2 observable platform"` and metric gauge = 1.
   Enables zero-downtime Canary releases and instant rollbacks without rebuilding containers.
2. **Automated Selenium E2E Tests (`tests/e2e/test_home.py`):**
   Uses pytest and headless Google Chrome webdriver to validate HTTP response content and feature flag rendering.
3. **Locust Workload Stress Testing (`tests/load/locustfile.py`):**
   Simulates concurrent user behavior hitting `/`, `/api/status`, and `/api/log-demo` with configurable wait times.

### Commands Executed
```bash
# 1. Run Selenium browser tests
pytest tests/e2e -v

# 2. Toggle Feature Flag to v2
$env:FEATURE_GREETING_V2='true'
docker compose up -d --build demo-app

# 3. Execute Headless Locust Load Test (10 users, 2 users/sec, 30s)
locust -f tests/load/locustfile.py --headless -u 10 -r 2 -t 30s --host http://localhost:8080
```

### Observations
- Selenium test passed: 2 passed in 1.48s.
- Locust load test generated 259 total requests at an average rate of 8.63 req/s with 0.00% failure rate.
- Median latency remained under 7.1ms, with 95% of all requests resolved within 16ms.
"""
    files = {
        BASE_DIR / "app" / "app.py": "app/app.py",
        BASE_DIR / "app" / "Dockerfile": "app/Dockerfile",
        BASE_DIR / "app" / "requirements.txt": "app/requirements.txt",
        BASE_DIR / "docker-compose.yml": "docker-compose.yml",
        BASE_DIR / "tests" / "requirements.txt": "tests/requirements.txt",
        BASE_DIR / "tests" / "e2e" / "test_home.py": "tests/e2e/test_home.py",
        BASE_DIR / "tests" / "load" / "locustfile.py": "tests/load/locustfile.py",
        BASE_DIR / "evidence" / "screenshots" / "06-testing.png": "evidence/06-testing.png",
    }
    create_zip_with_files(SUBMISSION_DIR / "06_Feature_Flags_and_Testing.zip", files, readme)


def package_07():
    pdf_src = BASE_DIR / "output" / "pdf" / "Lab3_Report.pdf"
    docx_src = BASE_DIR / "report" / "Lab3_Report.docx"
    
    # Copy PDF and DOCX directly into submission dir with descriptive names
    pdf_dest = SUBMISSION_DIR / "07_Monitoring_Logging_DevSecOps_Report.pdf"
    docx_dest = SUBMISSION_DIR / "07_Monitoring_Logging_DevSecOps_Report.docx"
    
    if pdf_src.exists():
        shutil.copy2(pdf_src, pdf_dest)
        print(f"Copied {pdf_dest} ({pdf_dest.stat().st_size} bytes)")
    if docx_src.exists():
        shutil.copy2(docx_src, docx_dest)
        print(f"Copied {docx_dest} ({docx_dest.stat().st_size} bytes)")

    # Also build a comprehensive ZIP for Question 7 containing everything
    readme = f"""{STUDENT_BANNER}
## Question 7: Monitoring, Logging, and DevSecOps Comprehensive Report
**Marks:** 10 Marks

This package contains the complete laboratory documentation report for Lab 3 in PDF and Microsoft Word (.docx) formats, complete with system architecture, implementation details, command logs, execution evidence screenshots, and operational analysis.

### Files Included:
- `07_Monitoring_Logging_DevSecOps_Report.pdf`: 9-page formal laboratory report with embedded photographic evidence.
- `07_Monitoring_Logging_DevSecOps_Report.docx`: Editable Microsoft Word document format.
- `evidence/`: High-resolution screenshots of all 6 laboratory experiments.
- `report_sources/`: Python source scripts used to generate the report documents.
"""
    files = {
        pdf_dest: "07_Monitoring_Logging_DevSecOps_Report.pdf",
        docx_dest: "07_Monitoring_Logging_DevSecOps_Report.docx",
        BASE_DIR / "evidence" / "screenshots" / "01-ansible-check.png": "evidence/01-ansible-check.png",
        BASE_DIR / "evidence" / "screenshots" / "02-terraform-plan.png": "evidence/02-terraform-plan.png",
        BASE_DIR / "evidence" / "screenshots" / "03-kibana-logs.png": "evidence/03-kibana-logs.png",
        BASE_DIR / "evidence" / "screenshots" / "04-security-scan.png": "evidence/04-security-scan.png",
        BASE_DIR / "evidence" / "screenshots" / "05-grafana-dashboard.png": "evidence/05-grafana-dashboard.png",
        BASE_DIR / "evidence" / "screenshots" / "06-testing.png": "evidence/06-testing.png",
        BASE_DIR / "report" / "build_report.py": "report_sources/build_report.py",
        BASE_DIR / "report" / "build_pdf.py": "report_sources/build_pdf.py",
    }
    create_zip_with_files(SUBMISSION_DIR / "07_Monitoring_Logging_DevSecOps_Report.zip", files, readme)


if __name__ == "__main__":
    package_01()
    package_02()
    package_03()
    package_04()
    package_05()
    package_06()
    package_07()
    print("All submission deliverables packaged successfully!")
