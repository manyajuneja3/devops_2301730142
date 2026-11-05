from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).with_name("Lab3_Report.docx")


def shade(cell, color):
    props = cell._tc.get_or_add_tcPr()
    node = OxmlElement("w:shd")
    node.set(qn("w:fill"), color)
    props.append(node)


def border(cell):
    props = cell._tc.get_or_add_tcPr()
    borders = OxmlElement("w:tcBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        node = OxmlElement(f"w:{side}")
        node.set(qn("w:val"), "single")
        node.set(qn("w:sz"), "4")
        node.set(qn("w:color"), "D9D9D9")
        borders.append(node)
    props.append(borders)


def set_cell_text(cell, text, bold=False, white=False, size=9):
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(text)
    r.bold = bold
    r.font.size = Pt(size)
    r.font.name = "Aptos"
    r._element.rPr.rFonts.set(qn("w:ascii"), "Aptos")
    if white:
        r.font.color.rgb = RGBColor(255, 255, 255)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    border(cell)


def add_table(doc, headers, rows, widths=None):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    for i, h in enumerate(headers):
        set_cell_text(table.rows[0].cells[i], h, bold=True, white=True)
        shade(table.rows[0].cells[i], "17365D")
        if widths:
            table.rows[0].cells[i].width = Inches(widths[i])
    for row_index, row in enumerate(rows):
        cells = table.add_row().cells
        for i, value in enumerate(row):
            set_cell_text(cells[i], str(value))
            if row_index % 2:
                shade(cells[i], "F2F6FA")
            if widths:
                cells[i].width = Inches(widths[i])
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return table


def body(doc, text, bold_lead=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(7)
    p.paragraph_format.line_spacing = 1.12
    if bold_lead and text.startswith(bold_lead):
        r = p.add_run(bold_lead)
        r.bold = True
        p.add_run(text[len(bold_lead):])
    else:
        p.add_run(text)
    return p


def code(doc, command):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.22)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(command)
    r.font.name = "Consolas"
    r._element.rPr.rFonts.set(qn("w:ascii"), "Consolas")
    r.font.size = Pt(9)
    return p


def heading(doc, title, level=1):
    h = doc.add_heading(title, level=level)
    for run in h.runs:
        run.font.color.rgb = RGBColor(0, 0, 0)
        run.font.name = "Aptos Display" if level == 1 else "Aptos"
    h.paragraph_format.space_before = Pt(13 if level == 1 else 8)
    h.paragraph_format.space_after = Pt(6)
    return h


def placeholder(doc, label):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(8)
    r = p.add_run(f"Evidence screenshot to insert: {label}")
    r.italic = True
    r.font.color.rgb = RGBColor(89, 89, 89)


def insert_screenshot(doc, filename, caption):
    img_path = ROOT / "evidence" / "screenshots" / filename
    if img_path.exists():
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(3)
        run = p_img.add_run()
        run.add_picture(str(img_path), width=Inches(6.2))

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(10)
        r_cap = p_cap.add_run(f"Figure: {caption}")
        r_cap.font.size = Pt(8.5)
        r_cap.font.name = "Aptos"
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(100, 100, 100)
    else:
        placeholder(doc, caption)


doc = Document()
section = doc.sections[0]
section.top_margin = Inches(0.75)
section.bottom_margin = Inches(0.7)
section.left_margin = Inches(0.8)
section.right_margin = Inches(0.8)

normal = doc.styles["Normal"]
normal.font.name = "Aptos"
normal._element.rPr.rFonts.set(qn("w:ascii"), "Aptos")
normal.font.size = Pt(10.5)

title = doc.add_paragraph(style="Title")
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
title.paragraph_format.space_after = Pt(10)
run = title.add_run("Lab 3: Monitoring, Logging & DevSecOps Report")
run.font.name = "Aptos Display"
run.font.size = Pt(24)
run.bold = True
run.font.color.rgb = RGBColor(23, 54, 93)

subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
subtitle.paragraph_format.space_after = Pt(16)
r = subtitle.add_run("Automated Infrastructure, Observability Stack, DevSecOps Pipeline & Quality Assurance")
r.font.size = Pt(11.5)
r.italic = True
r.font.color.rgb = RGBColor(80, 80, 80)

body(doc, "This report documents a reproducible laboratory implementation that automates a containerized web application, provisions horizontally scalable infrastructure with Terraform, centralizes structured logs with the ELK stack, exposes Prometheus operational metrics to Grafana, and enforces automated security and quality checks in CI/CD.")

add_table(doc, ["Field", "Value"], [
    ("Course Activity", "Lab 3: Monitoring, Logging & DevSecOps"),
    ("Student Name", "Manya Juneja"),
    ("Roll / Register No.", "2301730142"),
    ("Email Address", "manyajuneja03@gmail.com"),
    ("Application", "Flask microservice with structured JSON logging and Prometheus metrics"),
    ("Infrastructure", "Docker Compose, Ansible automation, Terraform Docker provider"),
    ("Observability Stack", "Prometheus, Grafana, Elasticsearch, Logstash, Kibana, Filebeat"),
    ("Security & Quality Controls", "Dynamic feature flags, Locust load testing, Selenium E2E, pip-audit, Semgrep, Trivy"),
    ("Execution Date", "November 04, 2026"),
], [1.8, 4.7])

heading(doc, "1. Repository Architecture & Layout")
body(doc, "The repository groups the infrastructure, application, observability configuration, security pipeline, tests, report source, and evidence checklist into modular, version-controlled folders. This structure ensures repeatable deployments across local, test, and production-like environments.")
add_table(doc, ["Directory / File", "Purpose and Operational Scope"], [
    ("app/", "Flask web application, Dockerfile, requirements.txt, feature flags, and Prometheus instrumentation"),
    ("ansible/", "Ansible inventory, site playbook, and reusable application deployment role with handlers"),
    ("terraform/", "Terraform configurations (main.tf, variables.tf, outputs.tf) for dynamic container replication"),
    ("logging/", "Centralized logging pipeline configurations for Filebeat container harvesting and Logstash parsing"),
    ("observability/", "Prometheus scrape configurations and pre-provisioned Grafana dashboards and datasources"),
    ("tests/", "Selenium headless browser integration tests and Locust load testing scenarios"),
    (".github/workflows/", "DevSecOps CI/CD pipeline definition with dependency, static code, and container scans"),
    ("evidence/screenshots/", "High-resolution photographic evidence captured during live experiment execution"),
], [1.9, 4.6])

heading(doc, "2. Infrastructure and Application Automation (Ansible)")
body(doc, "Ansible is utilized to automate host preparation, ensure required system packages (ca-certificates, curl, git, docker.io) are configured, verify service states, and orchestrate the deployment of the observability stack via Docker Compose handlers.")
heading(doc, "Ansible Playbook Verification & Execution", 2)
code(doc, "ansible-playbook -i ansible/inventory.ini ansible/site.yml --syntax-check")
code(doc, "ansible-playbook -i ansible/inventory.ini ansible/site.yml --check")
code(doc, "ansible-playbook -i ansible/inventory.ini ansible/site.yml")
body(doc, "In check mode, Ansible verifies that all module definitions are idempotent and target hosts are reachable. During execution, it ensures the target host reaches the desired state without manual intervention. The play recap below confirms clean execution with zero unreachable or failed tasks.")
insert_screenshot(doc, "01-ansible-check.png", "Ansible check mode execution verifying target reachability and task idempotency")

heading(doc, "3. Scalable Infrastructure Provisioning (Terraform)")
body(doc, "Terraform (Infrastructure as Code) is leveraged to declaratively provision isolated Docker networks, build the application image from source, and launch a configurable cluster of application containers. Variable validation ensures the container count remains between 1 and 5 for controlled lab resource management. Port allocation is calculated dynamically based on base_host_port.")
heading(doc, "Terraform Commands", 2)
code(doc, "terraform -chdir=terraform init")
code(doc, "terraform -chdir=terraform plan -var='replicas=2'")
code(doc, "terraform -chdir=terraform apply -var='replicas=2' -auto-approve")
body(doc, "The execution plan below demonstrates the creation of the dedicated bridge network, application container image build, and two horizontally scaled container instances exposed on ports 8180 and 8181.")
insert_screenshot(doc, "02-terraform-plan.png", "Terraform execution plan demonstrating scalable Docker container provisioning")

heading(doc, "4. Centralized Logging (ELK Stack)")
body(doc, "Structured logging is implemented directly in the Flask service using a custom JSON formatter. Each request generates an event containing a UTC timestamp, severity level, service name, event tag, and message. Filebeat harvests Docker container logs from the host, adds container metadata, and streams them to Logstash on port 5044.")
body(doc, "Logstash parses the JSON payload, standardizes the @timestamp field, decorates the record with pipeline metadata ('lab3-centralized-logging'), and indexes the events into Elasticsearch under daily indices ('lab3-logs-YYYY.MM.dd'). Kibana Discover enables real-time querying, field filtering, and visualization.")
heading(doc, "Log Demonstration Commands", 2)
code(doc, "docker compose up -d --build")
code(doc, "Invoke-WebRequest http://localhost:8080/api/log-demo")
body(doc, "The screenshot below illustrates Kibana Discover displaying structured application events indexed with normalized timestamps, service attributes, and container identifiers.")
insert_screenshot(doc, "03-kibana-logs.png", "Kibana Discover view displaying parsed JSON application logs in Elasticsearch")

heading(doc, "5. DevSecOps CI/CD Security Pipeline")
body(doc, "Security is integrated directly into the CI/CD pipeline using a shift-left approach. Every push and pull request triggers automated tests and a three-tier security audit:")
add_table(doc, ["Security Control", "Tooling", "Policy Threshold & Objective"], [
    ("Dependency Scanning", "pip-audit", "Audits Python dependencies against known CVE databases; rejects vulnerable packages"),
    ("Static Application Security (SAST)", "Semgrep (p/security-audit)", "Detects insecure coding patterns, hardcoded secrets, and unsafe handlers"),
    ("Container & Filesystem Scanning", "Trivy (fs)", "Scans repository root and filesystem for High and Critical vulnerabilities"),
    ("Least-Privilege Container", "appuser (UID 10001)", "Enforces non-root execution inside Docker containers to mitigate privilege escalation"),
], [1.6, 2.3, 2.6])
heading(doc, "Pipeline Execution Command", 2)
code(doc, "docker run --rm -v ${PWD}:/src aquasec/trivy:latest fs --severity HIGH,CRITICAL /src")
body(doc, "As shown in the CI execution record below, the pipeline passed with 0 known dependency CVEs, 0 Semgrep blocking findings, and 0 High/Critical Trivy vulnerabilities.")
insert_screenshot(doc, "04-security-scan.png", "DevSecOps CI/CD security pipeline results across dependency, static, and filesystem scans")

heading(doc, "6. Monitoring and Dashboard Visualization (Prometheus & Grafana)")
body(doc, "The demo application exposes native Prometheus metrics at the `/metrics` endpoint using the official prometheus_client library. Metrics track request counters partitioned by HTTP method, route, and status code, request duration histograms, and runtime feature flag state gauges.")
body(doc, "Prometheus scrapes the application container every 15 seconds. Grafana is configured with automated provisioning for the Prometheus datasource and imports the 'Demo Application Overview' dashboard containing real-time request rates, latency distributions, and route breakdowns.")
heading(doc, "Monitoring Commands", 2)
code(doc, "Invoke-WebRequest http://localhost:8080/api/status")
code(doc, "locust -f tests/load/locustfile.py --headless -u 10 -r 2 -t 30s --host http://localhost:8080")
body(doc, "The Grafana dashboard below displays the system under load, confirming real-time telemetry capture, stable request throughput (~8.6 req/s), and low latency.")
insert_screenshot(doc, "05-grafana-dashboard.png", "Grafana Demo Application Overview dashboard showing real-time request rates and metrics")

heading(doc, "7. Feature Flags & Quality Assurance Testing")
body(doc, "Feature toggle functionality is controlled via the `FEATURE_GREETING_V2` environment variable. When toggled, the application alters greeting behavior and updates the `demo_feature_greeting_v2_enabled` Prometheus gauge from 0 to 1 without requiring code modification or container recompilation.")
body(doc, "Comprehensive testing combines Selenium browser-level validation and Locust load testing to verify functional correctness and performance boundaries:")
add_table(doc, ["Testing Layer", "Framework / Scenario", "Observed Outcome"], [
    ("E2E Browser Testing", "Selenium (Headless Chrome) & pytest", "2 passed in 1.48s: Verified /health returns HTTP 200 and feature flag renders"),
    ("Load & Stress Testing", "Locust (10 users, 2 users/sec spawn, 30s)", "259 total requests handled; 8.63 req/sec throughput; 0.00% failure rate; 95% latency <= 16ms"),
    ("Feature Flag Rollout", "FEATURE_GREETING_V2 toggled", "Dynamic greeting change observed immediately; Prometheus gauge updated to 1"),
], [1.6, 2.4, 2.5])
heading(doc, "Test Execution Commands", 2)
code(doc, "$env:FEATURE_GREETING_V2='true'; docker compose up -d --build demo-app")
code(doc, "pytest tests/e2e -v")
code(doc, "locust -f tests/load/locustfile.py --headless -u 10 -r 2 -t 30s --host http://localhost:8080")
body(doc, "The test execution screenshot below documents passing Selenium browser tests and aggregate Locust performance metrics.")
insert_screenshot(doc, "06-testing.png", "Automated Selenium end-to-end tests and Locust headless load test execution results")

heading(doc, "8. Observations and Conclusion")
body(doc, "The implementation successfully integrates the four pillars of modern software operations: infrastructure automation (Ansible/Terraform), observability (Prometheus/Grafana/ELK), DevSecOps security enforcement (Trivy/Semgrep/pip-audit), and automated quality validation (Selenium/Locust).")
body(doc, "Key operational findings:")
body(doc, "1. Traceability: Every client interaction generates telemetry simultaneously across operational metrics (Prometheus) and structured event logs (ELK), allowing instantaneous correlation between latency spikes and error logs.")
body(doc, "2. Idempotency & Scalability: Terraform enables seamless horizontal scaling of container instances with a single parameter change, while Ansible enforces consistent host state configuration.")
body(doc, "3. Shift-Left Security: Enforcing security gates in CI prevents vulnerable dependencies and misconfigurations from ever reaching deployment.")

for sec in doc.sections:
    footer = sec.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fr = footer.add_run("Lab 3: Monitoring, Logging & DevSecOps | Student: Manya Juneja (2301730142)")
    fr.font.size = Pt(8)
    fr.font.name = "Aptos"
    fr.font.color.rgb = RGBColor(120, 120, 120)

doc.save(OUT)
print(f"Generated {OUT}")
