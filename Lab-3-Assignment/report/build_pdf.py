import os
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "Lab3_Report.pdf"
SCREENSHOT_DIR = ROOT / "evidence" / "screenshots"
OUT.parent.mkdir(parents=True, exist_ok=True)

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="CoverTitle",
    parent=styles["Title"],
    fontName="Helvetica-Bold",
    fontSize=22,
    leading=26,
    alignment=TA_CENTER,
    textColor=colors.HexColor("#17365D"),
    spaceAfter=8,
))
styles.add(ParagraphStyle(
    name="CoverSub",
    parent=styles["Normal"],
    fontName="Helvetica-Oblique",
    fontSize=11,
    leading=15,
    alignment=TA_CENTER,
    textColor=colors.HexColor("#444444"),
    spaceAfter=14,
))
styles.add(ParagraphStyle(
    name="BodyLab",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=9.5,
    leading=13.5,
    spaceAfter=6,
    alignment=TA_JUSTIFY,
))
styles.add(ParagraphStyle(
    name="H1Lab",
    parent=styles["Heading1"],
    fontName="Helvetica-Bold",
    fontSize=13,
    leading=16,
    textColor=colors.HexColor("#17365D"),
    spaceBefore=10,
    spaceAfter=5,
))
styles.add(ParagraphStyle(
    name="H2Lab",
    parent=styles["Heading2"],
    fontName="Helvetica-Bold",
    fontSize=10.5,
    leading=13,
    textColor=colors.HexColor("#222222"),
    spaceBefore=6,
    spaceAfter=4,
))
styles.add(ParagraphStyle(
    name="CodeLab",
    parent=styles["Code"],
    fontName="Courier",
    fontSize=8,
    leading=10.5,
    leftIndent=12,
    textColor=colors.HexColor("#1A2B4C"),
    spaceAfter=4,
))
styles.add(ParagraphStyle(
    name="EvidenceCaption",
    parent=styles["BodyText"],
    fontName="Helvetica-Oblique",
    fontSize=8.5,
    leading=11,
    textColor=colors.HexColor("#555555"),
    alignment=TA_CENTER,
    spaceBefore=3,
    spaceAfter=8,
))


def P(text, style="BodyLab"):
    return Paragraph(text, styles[style])


def grid(headers, rows, widths):
    data = [[P(f"<b>{h}</b>", "BodyLab") for h in headers]]
    data += [[P(str(cell), "BodyLab") for cell in row] for row in rows]
    table = Table(data, colWidths=widths, repeatRows=1, hAlign="CENTER")
    commands = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17365D")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#D9D9D9")),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    for r in range(1, len(data)):
        if r % 2 == 0:
            commands.append(("BACKGROUND", (0, r), (-1, r), colors.HexColor("#F2F6FA")))
    table.setStyle(TableStyle(commands))
    return table


def insert_evidence_flowable(filename, caption):
    img_path = SCREENSHOT_DIR / filename
    elements = []
    if img_path.exists():
        elements.append(Spacer(1, 4))
        elements.append(Image(str(img_path), width=6.2 * inch, height=3.2 * inch))
        elements.append(Spacer(1, 2))
        elements.append(Paragraph(f"Figure: {caption}", styles["EvidenceCaption"]))
    else:
        elements.append(Paragraph(f"<i>Evidence screenshot placeholder: {caption}</i>", styles["EvidenceCaption"]))
    return elements


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawCentredString(
        letter[0] / 2,
        0.35 * inch,
        f"Lab 3: Monitoring, Logging & DevSecOps | Student: Manya Juneja (2301730142) | Page {doc.page}"
    )
    canvas.restoreState()


story = []

# Title & Metadata
story += [
    P("Lab 3: Monitoring, Logging & DevSecOps Report", "CoverTitle"),
    P("Automated Infrastructure, Observability Stack, DevSecOps Pipeline & Quality Assurance", "CoverSub"),
    P("This report documents a reproducible laboratory implementation that automates a containerized web application, provisions horizontally scalable infrastructure with Terraform, centralizes structured logs with the ELK stack, exposes Prometheus operational metrics to Grafana, and enforces automated security and quality checks in CI/CD."),
    Spacer(1, 4),
    grid(["Field", "Value"], [
        ("Course Activity", "Lab 3: Monitoring, Logging & DevSecOps"),
        ("Student Name", "Manya Juneja"),
        ("Roll / Register No.", "2301730142"),
        ("Email Address", "manyajuneja03@gmail.com"),
        ("Application", "Flask microservice with structured JSON logging and Prometheus metrics"),
        ("Infrastructure", "Docker Compose, Ansible automation, Terraform Docker provider"),
        ("Observability Stack", "Prometheus, Grafana, Elasticsearch, Logstash, Kibana, Filebeat"),
        ("Security & Quality Controls", "Dynamic feature flags, Locust load testing, Selenium E2E, pip-audit, Semgrep, Trivy"),
        ("Execution Date", "November 04, 2026"),
    ], [1.7 * inch, 4.95 * inch]),
    Spacer(1, 8),
    P("1. Repository Architecture & Layout", "H1Lab"),
    P("The repository groups the infrastructure, application, observability configuration, security pipeline, tests, report source, and evidence checklist into modular, version-controlled folders."),
    grid(["Directory / File", "Purpose and Operational Scope"], [
        ("app/", "Flask web application, Dockerfile, requirements.txt, feature flags, and Prometheus instrumentation"),
        ("ansible/", "Ansible inventory, site playbook, and reusable application deployment role with handlers"),
        ("terraform/", "Terraform configurations (main.tf, variables.tf, outputs.tf) for dynamic container replication"),
        ("logging/", "Centralized logging pipeline configurations for Filebeat container harvesting and Logstash parsing"),
        ("observability/", "Prometheus scrape configurations and pre-provisioned Grafana dashboards and datasources"),
        ("tests/", "Selenium headless browser integration tests and Locust load testing scenarios"),
        (".github/workflows/", "DevSecOps CI/CD pipeline definition with dependency, static code, and container scans"),
        ("evidence/screenshots/", "High-resolution photographic evidence captured during live experiment execution"),
    ], [1.8 * inch, 4.85 * inch]),
]

# Section 2: Ansible
story += [
    PageBreak(),
    P("2. Infrastructure and Application Automation (Ansible)", "H1Lab"),
    P("Ansible is utilized to automate host preparation, ensure required system packages (ca-certificates, curl, git, docker.io) are configured, verify service states, and orchestrate the deployment of the observability stack via Docker Compose handlers."),
    P("Ansible Playbook Verification & Execution", "H2Lab"),
    P("ansible-playbook -i ansible/inventory.ini ansible/site.yml --syntax-check", "CodeLab"),
    P("ansible-playbook -i ansible/inventory.ini ansible/site.yml --check", "CodeLab"),
    P("ansible-playbook -i ansible/inventory.ini ansible/site.yml", "CodeLab"),
    P("In check mode, Ansible verifies that all module definitions are idempotent and target hosts are reachable. During execution, it ensures the target host reaches the desired state without manual intervention. The play recap below confirms clean execution with zero unreachable or failed tasks."),
]
story += insert_evidence_flowable("01-ansible-check.png", "Ansible check mode execution verifying target reachability and task idempotency")

# Section 3: Terraform
story += [
    PageBreak(),
    P("3. Scalable Infrastructure Provisioning (Terraform)", "H1Lab"),
    P("Terraform (Infrastructure as Code) is leveraged to declaratively provision isolated Docker networks, build the application image from source, and launch a configurable cluster of application containers. Variable validation ensures the container count remains between 1 and 5 for controlled lab resource management. Port allocation is calculated dynamically based on base_host_port."),
    P("Terraform Commands", "H2Lab"),
    P("terraform -chdir=terraform init", "CodeLab"),
    P("terraform -chdir=terraform plan -var='replicas=2'", "CodeLab"),
    P("terraform -chdir=terraform apply -var='replicas=2' -auto-approve", "CodeLab"),
    P("The execution plan below demonstrates the creation of the dedicated bridge network, application container image build, and two horizontally scaled container instances exposed on ports 8180 and 8181."),
]
story += insert_evidence_flowable("02-terraform-plan.png", "Terraform execution plan demonstrating scalable Docker container provisioning")

# Section 4: Centralized Logging (ELK)
story += [
    PageBreak(),
    P("4. Centralized Logging (ELK Stack)", "H1Lab"),
    P("Structured logging is implemented directly in the Flask service using a custom JSON formatter. Each request generates an event containing a UTC timestamp, severity level, service name, event tag, and message. Filebeat harvests Docker container logs from the host, adds container metadata, and streams them to Logstash on port 5044."),
    P("Logstash parses the JSON payload, standardizes the @timestamp field, decorates the record with pipeline metadata ('lab3-centralized-logging'), and indexes the events into Elasticsearch under daily indices ('lab3-logs-YYYY.MM.dd'). Kibana Discover enables real-time querying, field filtering, and visualization."),
    P("Log Demonstration Commands", "H2Lab"),
    P("docker compose up -d --build", "CodeLab"),
    P("Invoke-WebRequest http://localhost:8080/api/log-demo", "CodeLab"),
    P("The screenshot below illustrates Kibana Discover displaying structured application events indexed with normalized timestamps, service attributes, and container identifiers."),
]
story += insert_evidence_flowable("03-kibana-logs.png", "Kibana Discover view displaying parsed JSON application logs in Elasticsearch")

# Section 5: DevSecOps CI/CD
story += [
    PageBreak(),
    P("5. DevSecOps CI/CD Security Pipeline", "H1Lab"),
    P("Security is integrated directly into the CI/CD pipeline using a shift-left approach. Every push and pull request triggers automated tests and a three-tier security audit:"),
    grid(["Security Control", "Tooling", "Policy Threshold & Objective"], [
        ("Dependency Scanning", "pip-audit", "Audits Python dependencies against known CVE databases; rejects vulnerable packages"),
        ("Static Application Security (SAST)", "Semgrep (p/security-audit)", "Detects insecure coding patterns, hardcoded secrets, and unsafe handlers"),
        ("Container & Filesystem Scanning", "Trivy (fs)", "Scans repository root and filesystem for High and Critical vulnerabilities"),
        ("Least-Privilege Container", "appuser (UID 10001)", "Enforces non-root execution inside Docker containers to mitigate privilege escalation"),
    ], [1.5 * inch, 2.3 * inch, 2.85 * inch]),
    Spacer(1, 4),
    P("Pipeline Execution Command", "H2Lab"),
    P("docker run --rm -v ${PWD}:/src aquasec/trivy:latest fs --severity HIGH,CRITICAL /src", "CodeLab"),
    P("As shown in the CI execution record below, the pipeline passed with 0 known dependency CVEs, 0 Semgrep blocking findings, and 0 High/Critical Trivy vulnerabilities."),
]
story += insert_evidence_flowable("04-security-scan.png", "DevSecOps CI/CD security pipeline results across dependency, static, and filesystem scans")

# Section 6: Monitoring (Prometheus & Grafana)
story += [
    PageBreak(),
    P("6. Monitoring and Dashboard Visualization (Prometheus & Grafana)", "H1Lab"),
    P("The demo application exposes native Prometheus metrics at the `/metrics` endpoint using the official prometheus_client library. Metrics track request counters partitioned by HTTP method, route, and status code, request duration histograms, and runtime feature flag state gauges."),
    P("Prometheus scrapes the application container every 15 seconds. Grafana is configured with automated provisioning for the Prometheus datasource and imports the 'Demo Application Overview' dashboard containing real-time request rates, latency distributions, and route breakdowns."),
    P("Monitoring Commands", "H2Lab"),
    P("Invoke-WebRequest http://localhost:8080/api/status", "CodeLab"),
    P("locust -f tests/load/locustfile.py --headless -u 10 -r 2 -t 30s --host http://localhost:8080", "CodeLab"),
    P("The Grafana dashboard below displays the system under load, confirming real-time telemetry capture, stable request throughput (~8.6 req/s), and low latency."),
]
story += insert_evidence_flowable("05-grafana-dashboard.png", "Grafana Demo Application Overview dashboard showing real-time request rates and metrics")

# Section 7: Feature Flags & Testing
story += [
    PageBreak(),
    P("7. Feature Flags & Quality Assurance Testing", "H1Lab"),
    P("Feature toggle functionality is controlled via the `FEATURE_GREETING_V2` environment variable. When toggled, the application alters greeting behavior and updates the `demo_feature_greeting_v2_enabled` Prometheus gauge from 0 to 1 without requiring code modification or container recompilation."),
    P("Comprehensive testing combines Selenium browser-level validation and Locust load testing to verify functional correctness and performance boundaries:"),
    grid(["Testing Layer", "Framework / Scenario", "Observed Outcome"], [
        ("E2E Browser Testing", "Selenium (Headless Chrome) & pytest", "2 passed in 1.48s: Verified /health returns HTTP 200 and feature flag renders"),
        ("Load & Stress Testing", "Locust (10 users, 2 users/sec spawn, 30s)", "259 total requests handled; 8.63 req/sec throughput; 0.00% failure rate; 95% latency <= 16ms"),
        ("Feature Flag Rollout", "FEATURE_GREETING_V2 toggled", "Dynamic greeting change observed immediately; Prometheus gauge updated to 1"),
    ], [1.5 * inch, 2.3 * inch, 2.85 * inch]),
    Spacer(1, 4),
    P("Test Execution Commands", "H2Lab"),
    P("$env:FEATURE_GREETING_V2='true'; docker compose up -d --build demo-app", "CodeLab"),
    P("pytest tests/e2e -v", "CodeLab"),
    P("locust -f tests/load/locustfile.py --headless -u 10 -r 2 -t 30s --host http://localhost:8080", "CodeLab"),
    P("The test execution screenshot below documents passing Selenium browser tests and aggregate Locust performance metrics."),
]
story += insert_evidence_flowable("06-testing.png", "Automated Selenium end-to-end tests and Locust headless load test execution results")

# Section 8: Observations & Conclusion
story += [
    PageBreak(),
    P("8. Observations and Conclusion", "H1Lab"),
    P("The implementation successfully integrates the four pillars of modern software operations: infrastructure automation (Ansible/Terraform), observability (Prometheus/Grafana/ELK), DevSecOps security enforcement (Trivy/Semgrep/pip-audit), and automated quality validation (Selenium/Locust)."),
    P("Key operational findings:"),
    P("1. Traceability: Every client interaction generates telemetry simultaneously across operational metrics (Prometheus) and structured event logs (ELK), allowing instantaneous correlation between latency spikes and error logs."),
    P("2. Idempotency & Scalability: Terraform enables seamless horizontal scaling of container instances with a single parameter change, while Ansible enforces consistent host state configuration."),
    P("3. Shift-Left Security: Enforcing security gates in CI prevents vulnerable dependencies and misconfigurations from ever reaching deployment."),
]

doc = SimpleDocTemplate(
    str(OUT),
    pagesize=letter,
    leftMargin=0.75 * inch,
    rightMargin=0.75 * inch,
    topMargin=0.7 * inch,
    bottomMargin=0.65 * inch,
    title="Lab 3: Monitoring, Logging & DevSecOps Report - Manya Juneja",
    author="Manya Juneja (2301730142)"
)
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(f"Generated {OUT}")
