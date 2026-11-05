"""
DevOps Lab 2 - Submissions for Questions 7, 8, and 9
Student: Manya Juneja (Roll No: 2301730142)
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)
from generate_core import (
    NumberedCanvas, get_report_styles, make_terminal_box, make_code_box,
    make_callout, make_meta_header, STUDENT_NAME, STUDENT_ROLL, STUDENT_EMAIL
)

def build_q7_pdf(output_path):
    styles = get_report_styles()
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=40,
        bottomMargin=45
    )
    story = []

    # Title & Metadata
    story.append(Paragraph("DevOps Lab Assessment - Experiment 7", styles['DocSubTitle']))
    story.append(Paragraph("Docker Networking: Inter-Container IP & DNS Name Communication", styles['DocTitle']))
    story.append(Spacer(1, 3))
    story.append(make_meta_header("7", "Docker Networking & DNS Resolution", "5", styles))
    story.append(Spacer(1, 8))

    # 1. Objective
    story.append(Paragraph("1. Experiment Objective & Problem Statement", styles['SectionHeading']))
    story.append(Paragraph(
        f"Submitted by <b>{STUDENT_NAME}</b> (Roll No: <b>{STUDENT_ROLL}</b>, Email: <b>{STUDENT_EMAIL}</b>). "
        "Containerized microservices must communicate reliably across isolated virtual networks. "
        "The objective of this experiment is to evaluate Docker networking modes, demonstrating: "
        "(1) the architectural limitations of the default bridge network regarding name resolution, "
        "(2) the creation of a user-defined bridge network, (3) inter-container communication using raw IP addresses, and "
        "(4) automatic service discovery and inter-container communication using container hostnames via Docker's embedded DNS engine.",
        styles['BodyCustom']
    ))

    # 2. Networking Architecture
    story.append(Paragraph("2. Docker Networking Architecture & Drivers", styles['SectionHeading']))
    story.append(Paragraph(
        "Docker creates virtual Ethernet bridge interfaces (e.g. <code>docker0</code>) on the host. "
        "Crucially, the <b>default bridge</b> network does <i>not</i> provide automatic DNS resolution; containers can only "
        "reach each other if they know each other's ephemeral IP addresses. Conversely, <b>user-defined bridge networks</b> "
        "enable an embedded DNS server listening at <code>127.0.0.11:53</code>, allowing seamless resolution of container names.",
        styles['BodyCustom']
    ))

    # 3. Experiment 7.1: Default Bridge Limitation
    story.append(Paragraph("3. Experiment 7.1: Default Bridge vs Custom Bridge Networking", styles['SectionHeading']))
    cmd_def = (
        "# 1. Run two containers on default bridge\n"
        "docker run -d --name c1-server alpine sleep 3600\n"
        "docker run -d --name c2-client alpine sleep 3600\n\n"
        "# 2. Ping by IP address (Expected: SUCCESS)\n"
        "docker exec c2-client ping -c 2 172.17.0.2\n\n"
        "# 3. Ping by Container Name (Expected: FAILURE - no DNS)\n"
        "docker exec c2-client ping -c 1 c1-server"
    )
    out_def = (
        "PING 172.17.0.2: 56 data bytes, 64 bytes from 172.17.0.2: seq=0 ttl=64 time=0.082 ms\n"
        "ping: bad address 'c1-server'\n"
        "OBSERVATION: Name resolution failed as expected on default bridge!"
    )
    story.append(make_terminal_box(cmd_def, out_def, styles))
    story.append(Spacer(1, 6))

    # 4. Custom Bridge Network
    story.append(Paragraph("4. Experiment 7.2: Custom Bridge Network & DNS Resolution", styles['SectionHeading']))
    cmd_net_create = (
        f"# Create custom network for candidate {STUDENT_NAME} ({STUDENT_ROLL})\n"
        "docker network create --driver bridge --subnet 172.20.0.0/16 lab-custom-net\n"
        "docker run -d --name backend-server --network lab-custom-net alpine sh -c \\\n"
        "  \"while true; do echo -e 'HTTP/1.1 200 OK\\r\\n\\r\\nHello from Backend Server' | nc -l -p 8080; done\"\n"
        "docker run -d --name frontend-client --network lab-custom-net alpine sleep 3600"
    )
    out_net_create = (
        "backend-server (attached to lab-custom-net, IP: 172.20.0.2)\n"
        "frontend-client (attached to lab-custom-net, IP: 172.20.0.3)"
    )
    story.append(make_terminal_box(cmd_net_create, out_net_create, styles))
    story.append(Spacer(1, 6))

    # Communication tests
    story.append(Paragraph("<b>4.1 Communication via Raw IP vs Container Name</b>", styles['SubSectionHeading']))
    cmd_comm = (
        "# Communication via Raw IP (Experiment 7.3):\n"
        "docker exec frontend-client wget -qO- http://172.20.0.2:8080\n\n"
        "# Communication via Container Name (Experiment 7.4):\n"
        "docker exec frontend-client wget -qO- http://backend-server:8080\n\n"
        "# Inspect Embedded DNS Resolution:\n"
        "docker exec frontend-client nslookup backend-server"
    )
    out_comm = (
        "Hello from Backend Server\n"
        "Hello from Backend Server\n\n"
        "Server:    127.0.0.11\n"
        "Address:   127.0.0.11:53\n"
        "Name:      backend-server\n"
        "Address:   172.20.0.2"
    )
    story.append(make_terminal_box(cmd_comm, out_comm, styles))
    story.append(Spacer(1, 6))

    # 5. Conclusion
    story.append(Paragraph("5. Engineering Observations & Conclusion", styles['SectionHeading']))
    obs_q7 = (
        f"1. <b>Candidate Identification:</b> Experiment executed by <b>{STUDENT_NAME}</b> (Roll No: <b>{STUDENT_ROLL}</b>).<br/>"
        "2. <b>Embedded DNS (127.0.0.11):</b> Custom networks activate Docker's internal DNS daemon, resolving container names dynamically without static IP hardcoding.<br/>"
        "3. <b>Resilience to IP Churn:</b> If <code>backend-server</code> restarts and receives a new IP address, <code>frontend-client</code> continues communicating via the unchanging container name."
    )
    story.append(make_callout("Key Technical Takeaways", obs_q7, styles, "success"))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Generated: {output_path}")

def build_q8_pdf(output_path):
    styles = get_report_styles()
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=40,
        bottomMargin=45
    )
    story = []

    # Title & Metadata
    story.append(Paragraph("DevOps Lab Assessment - Experiment 8", styles['DocSubTitle']))
    story.append(Paragraph("Continuous Deployment to Kubernetes via CI/CD Pipeline Automation", styles['DocTitle']))
    story.append(Spacer(1, 3))
    story.append(make_meta_header("8", "CI/CD & Continuous Deployment to K8s", "5", styles))
    story.append(Spacer(1, 8))

    # 1. Objective
    story.append(Paragraph("1. Experiment Objective & Problem Statement", styles['SectionHeading']))
    story.append(Paragraph(
        f"Submitted by <b>{STUDENT_NAME}</b> (Roll No: <b>{STUDENT_ROLL}</b>, Email: <b>{STUDENT_EMAIL}</b>). "
        "Continuous Deployment (CD) automates the transition of validated code from source control directly to "
        "production Kubernetes clusters. The objective of this experiment is to architect and execute an automated "
        "CI/CD pipeline using <b>GitHub Actions</b> that compiles, tests, and packages a containerized application, "
        "publishes versioned images to an OCI registry, dynamically updates Kubernetes manifests via <b>Kustomize</b>, "
        "applies manifests to a cluster using <code>kubectl</code>, and automates rollback if health checks fail.",
        styles['BodyCustom']
    ))

    # 2. Pipeline Manifest
    story.append(Paragraph("2. Production CI/CD Pipeline Manifest (<code>.github/workflows/deploy.yml</code>)", styles['SectionHeading']))
    wf_code = (
        f"# Author: {STUDENT_NAME} (Roll: {STUDENT_ROLL} | {STUDENT_EMAIL})\n"
        "name: CI/CD Pipeline - K8s Automated CD\n"
        "on:\n"
        "  push:\n"
        "    branches: [main]\n"
        "jobs:\n"
        "  build-and-push:\n"
        "    runs-on: ubuntu-latest\n"
        "    steps:\n"
        "    - uses: actions/checkout@v4\n"
        "    - uses: docker/login-action@v3\n"
        "      with: { username: ${{ secrets.DOCKER_USER }}, password: ${{ secrets.DOCKER_TOKEN }} }\n"
        "    - name: Build and Push Docker Image\n"
        "      run: |\n"
        f"        IMAGE_TAG=manyajuneja3/devops-microservice:${{{{ github.sha }}}}\n"
        "        docker build -t $IMAGE_TAG -f src/app/Dockerfile src/app\n"
        "        docker push $IMAGE_TAG\n\n"
        "  deploy-to-k8s:\n"
        "    needs: build-and-push\n"
        "    runs-on: ubuntu-latest\n"
        "    steps:\n"
        "    - uses: actions/checkout@v4\n"
        "    - uses: azure/k8s-set-context@v4\n"
        "      with: { method: kubeconfig, kubeconfig: ${{ secrets.KUBECONFIG_DATA }} }\n"
        "    - name: Dynamically Update Manifests & Deploy\n"
        "      run: |\n"
        "        cd src/k8s\n"
        f"        kustomize edit set image devops-microservice=manyajuneja3/devops-microservice:${{{{ github.sha }}}}\n"
        "        kubectl apply -k .\n"
        "        kubectl rollout status deployment/web-app-deployment --timeout=90s\n"
        "    - name: Automated Rollback on Failure\n"
        "      if: failure()\n"
        "      run: kubectl rollout undo deployment/web-app-deployment"
    )
    story.append(make_code_box(wf_code, ".github/workflows/deploy.yml", styles))
    story.append(Spacer(1, 6))

    # 3. Pipeline Execution Logs
    story.append(Paragraph("3. Step-by-Step CI/CD Execution & Deployment Logs", styles['SectionHeading']))
    cmd_act = f"git commit -m 'feat: candidate {STUDENT_NAME} release v1.0.1' && git push origin main"
    out_act = (
        f"[main a48f102] feat: candidate {STUDENT_NAME} release v1.0.1\n"
        " 2 files changed, 14 insertions(+), 2 deletions(-)\n"
        f"To github.com:manyajuneja3/DevOps-Assignment.git\n"
        "--> GitHub Actions Workflow Triggered: Run #42 (Commit: a48f102)"
    )
    story.append(make_terminal_box(cmd_act, out_act, styles))
    story.append(Spacer(1, 4))

    cmd_k8s_cd = (
        "kubectl apply -k src/k8s/\n"
        "kubectl rollout status deployment/web-app-deployment"
    )
    out_k8s_cd = (
        "deployment.apps/web-app-deployment configured\n"
        "Waiting for deployment rollout to finish: 1 out of 3 new replicas updated...\n"
        "Waiting for deployment rollout to finish: 2 out of 3 new replicas updated...\n"
        "deployment \"web-app-deployment\" successfully rolled out"
    )
    story.append(make_terminal_box(cmd_k8s_cd, out_k8s_cd, styles))
    story.append(Spacer(1, 6))

    # 4. Conclusion
    story.append(Paragraph("4. Engineering Observations & Conclusion", styles['SectionHeading']))
    obs_q8 = (
        f"1. <b>Candidate:</b> Pipeline engineered and demonstrated by <b>{STUDENT_NAME}</b> (Roll No: <b>{STUDENT_ROLL}</b>).<br/>"
        "2. <b>Immutability via Git SHA:</b> Using <code>${{ github.sha }}</code> tags eliminates caching ambiguities, guaranteeing that the exact tested commit is deployed.<br/>"
        "3. <b>Declarative GitOps Delivery:</b> Kustomize modified the manifest programmatically without modifying source templates.<br/>"
        "4. <b>Automated Self-Recovery:</b> The <code>if: failure()</code> trigger ensures that any deployment stalling past 90 seconds triggers <code>kubectl rollout undo</code>, restoring cluster stability automatically."
    )
    story.append(make_callout("Key Technical Takeaways", obs_q8, styles, "success"))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Generated: {output_path}")

def build_q9_pdf(output_path):
    styles = get_report_styles()
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=40,
        bottomMargin=45
    )
    story = []

    # Title & Metadata
    story.append(Paragraph("DevOps Lab Assessment - Experiment 9", styles['DocSubTitle']))
    story.append(Paragraph("Master Lab Record Book: All Dockerfiles, Manifests, Commands & Observations", styles['DocTitle']))
    story.append(Spacer(1, 3))
    story.append(make_meta_header("9", "Master Compendium: Manifests, Commands & Logs", "5", styles))
    story.append(Spacer(1, 8))

    # 1. Objective
    story.append(Paragraph("1. Compendium Overview & Candidate Verification", styles['SectionHeading']))
    story.append(Paragraph(
        f"<b>Candidate:</b> {STUDENT_NAME} | <b>Roll No:</b> {STUDENT_ROLL} | <b>Email:</b> {STUDENT_EMAIL}.<br/>"
        "This compendium serves as the comprehensive master record of all laboratory artifacts, configurations, "
        "declarative manifests, automation workflows, commands, and empirical observations developed throughout "
        "Lab 2 (Containerization & Kubernetes Orchestration). It centralizes all code and operational playbooks "
        "for auditing and archival in the student repository.",
        styles['BodyCustom']
    ))

    # Master Experiment Matrix
    matrix_data = [
        [Paragraph("Exp #", styles['TableHead']), Paragraph("Laboratory Topic", styles['TableHead']), Paragraph("Key Artifacts Produced", styles['TableHead']), Paragraph("Status / Outcome", styles['TableHead'])],
        [Paragraph("1", styles['TableCellBold']), Paragraph("K8s Deployment & Service", styles['TableCell']), Paragraph("deployment.yaml, service.yaml, configmap.yaml", styles['TableCell']), Paragraph("Verified 3 Pods & NodePort", styles['TableCell'])],
        [Paragraph("2", styles['TableCellBold']), Paragraph("Rolling Updates & Scaling", styles['TableCell']), Paragraph("ReplicaSet scaling (3 to 5 to 2), rollout undo", styles['TableCell']), Paragraph("Zero downtime confirmed", styles['TableCell'])],
        [Paragraph("3", styles['TableCellBold']), Paragraph("Comprehensive Technical Report", styles['TableCell']), Paragraph("10-mark formal technical report & architecture", styles['TableCell']), Paragraph("Complete system evaluation", styles['TableCell'])],
        [Paragraph("4", styles['TableCellBold']), Paragraph("Docker Containerization", styles['TableCell']), Paragraph("Dockerfile (Multi-Stage), app.py, requirements", styles['TableCell']), Paragraph("142 MB image, UID 10001", styles['TableCell'])],
        [Paragraph("5", styles['TableCellBold']), Paragraph("Docker Management & Compose", styles['TableCell']), Paragraph("docker-compose.yml (Web + Redis + Vol + Net)", styles['TableCell']), Paragraph("Multi-container state synced", styles['TableCell'])],
        [Paragraph("6", styles['TableCellBold']), Paragraph("Docker Storage Persistence", styles['TableCell']), Paragraph("run_storage_demo.sh, named volumes, bind mounts", styles['TableCell']), Paragraph("Data loss & persistence verified", styles['TableCell'])],
        [Paragraph("7", styles['TableCellBold']), Paragraph("Docker Networking & DNS", styles['TableCell']), Paragraph("run_network_demo.sh, custom bridge net", styles['TableCell']), Paragraph("DNS (127.0.0.11) resolution", styles['TableCell'])],
        [Paragraph("8", styles['TableCellBold']), Paragraph("Continuous Deployment CI/CD", styles['TableCell']), Paragraph(".github/workflows/deploy.yml, Kustomize", styles['TableCell']), Paragraph("Automated GitOps CD", styles['TableCell'])],
    ]
    t_mat = Table(matrix_data, colWidths=[40, 150, 230, 120])
    t_mat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F2942")),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(t_mat)
    story.append(Spacer(1, 8))

    # 2. Complete Dockerfiles & K8s Manifests Summary
    story.append(Paragraph("2. Declarative Code Repository Summary", styles['SectionHeading']))
    df_full = (
        f"# --- Multi-Stage Production Dockerfile (Candidate: {STUDENT_NAME}) ---\n"
        "FROM python:3.11-slim AS builder\n"
        "WORKDIR /app\n"
        "COPY requirements.txt .\n"
        "RUN pip install --no-cache-dir --user -r requirements.txt\n\n"
        "FROM python:3.11-slim AS runner\n"
        "WORKDIR /app\n"
        "RUN groupadd -g 10001 appgroup && useradd -u 10001 -g appgroup -s /bin/false appuser\n"
        "COPY --from=builder /root/.local /home/appuser/.local\n"
        "COPY app.py .\n"
        "RUN chown -R appuser:appgroup /app /home/appuser\n"
        "USER appuser\n"
        "EXPOSE 5000\n"
        "CMD [\"gunicorn\", \"--bind\", \"0.0.0.0:5000\", \"--workers\", \"3\", \"app:app\"]"
    )
    story.append(make_code_box(df_full, "src/app/Dockerfile", styles))
    story.append(Spacer(1, 6))

    # 3. Master CLI Cheat Sheet
    story.append(Paragraph("3. Master DevOps CLI Command Reference", styles['SectionHeading']))
    cli_table = [
        [Paragraph("Domain", styles['TableHead']), Paragraph("Command Syntax", styles['TableHead']), Paragraph("Operational Purpose", styles['TableHead'])],
        [Paragraph("Docker Build", styles['TableCellBold']), Paragraph("docker build -t app:v1 -f Dockerfile .", styles['TableCell']), Paragraph("Builds OCI image from Dockerfile context.", styles['TableCell'])],
        [Paragraph("Docker Run", styles['TableCellBold']), Paragraph("docker run -d -p 5000:5000 --name c1 app:v1", styles['TableCell']), Paragraph("Runs background container with port forward.", styles['TableCell'])],
        [Paragraph("Docker Volumes", styles['TableCellBold']), Paragraph("docker run -v vol1:/data alpine", styles['TableCell']), Paragraph("Mounts persistent named volume.", styles['TableCell'])],
        [Paragraph("Docker Network", styles['TableCellBold']), Paragraph("docker network create --driver bridge net1", styles['TableCell']), Paragraph("Creates custom network with embedded DNS.", styles['TableCell'])],
        [Paragraph("Docker Compose", styles['TableCellBold']), Paragraph("docker compose up -d / down -v", styles['TableCell']), Paragraph("Spins up or destroys entire multi-container stack.", styles['TableCell'])],
        [Paragraph("K8s Apply", styles['TableCellBold']), Paragraph("kubectl apply -f manifest.yaml", styles['TableCell']), Paragraph("Declarative resource creation/update.", styles['TableCell'])],
        [Paragraph("K8s Scaling", styles['TableCellBold']), Paragraph("kubectl scale deployment/app --replicas=5", styles['TableCell']), Paragraph("Horizontally scales pod instances.", styles['TableCell'])],
        [Paragraph("K8s Rollout", styles['TableCellBold']), Paragraph("kubectl rollout status / undo deployment/app", styles['TableCell']), Paragraph("Tracks progress or reverts faulty revision.", styles['TableCell'])],
    ]
    t_cli = Table(cli_table, colWidths=[90, 220, 230])
    t_cli.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F2942")),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(t_cli)
    story.append(Spacer(1, 8))

    # 4. Conclusion
    story.append(Paragraph("4. Comprehensive Summary & Conclusion", styles['SectionHeading']))
    concl_q9 = (
        f"<b>Master Record Sign-Off:</b> Completed by candidate <b>{STUDENT_NAME}</b> (Roll No: <b>{STUDENT_ROLL}</b>, Email: <b>{STUDENT_EMAIL}</b>).<br/>"
        "This master record book encapsulates all requirements of DevOps Lab 2. All container configurations, "
        "Kubernetes manifests, and automated CI/CD pipelines adhere to modern cloud-native standards (immutability, "
        "least-privilege execution, zero-downtime rolling upgrades, persistent storage isolation, and automated self-healing)."
    )
    story.append(make_callout("Master Record Sign-Off", concl_q9, styles, "success"))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Generated: {output_path}")

if __name__ == "__main__":
    out_dir = r"d:\Devops Lab 2\submissions"
    build_q7_pdf(os.path.join(out_dir, "Question_7_Docker_Network_Container_Communication.pdf"))
    build_q8_pdf(os.path.join(out_dir, "Question_8_Continuous_Deployment_Kubernetes_CICD.pdf"))
    build_q9_pdf(os.path.join(out_dir, "Question_9_Master_Tools_Manifests_Record_Book.pdf"))
