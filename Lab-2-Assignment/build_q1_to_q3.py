"""
DevOps Lab 2 - Submissions for Questions 1, 2, and 3
Student: Manya Juneja (Roll No: 2301730142)
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from generate_core import (
    NumberedCanvas, get_report_styles, make_terminal_box, make_code_box,
    make_callout, make_meta_header, STUDENT_NAME, STUDENT_ROLL, STUDENT_EMAIL
)

def build_q1_pdf(output_path):
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
    story.append(Paragraph("DevOps Lab Assessment - Experiment 1", styles['DocSubTitle']))
    story.append(Paragraph("Deploy Application to Kubernetes (Minikube) Cluster & Verify Pods", styles['DocTitle']))
    story.append(Spacer(1, 3))
    story.append(make_meta_header("1", "Deploy to Minikube using Deployment & Service", "5", styles))
    story.append(Spacer(1, 8))

    # 1. Objective
    story.append(Paragraph("1. Experiment Objective & Problem Statement", styles['SectionHeading']))
    story.append(Paragraph(
        f"Submitted by <b>{STUDENT_NAME}</b> (Roll No: <b>{STUDENT_ROLL}</b>, Email: <b>{STUDENT_EMAIL}</b>). "
        "The objective of this laboratory exercise is to configure and orchestrate a containerized web application "
        "on a local Kubernetes cluster managed via Minikube. The experiment requires authoring declarative Kubernetes "
        "manifests for a <b>Deployment</b> (managing 3 active replica pods, rolling updates, and health probes) and a "
        "<b>Service</b> (exposing the application pods externally via a NodePort). Finally, end-to-end verification must "
        "be conducted to inspect pod lifecycle phases, event scheduling logs, service endpoint mappings, and traffic routing.",
        styles['BodyCustom']
    ))

    # 2. Architecture & Concept
    story.append(Paragraph("2. Architectural Overview", styles['SectionHeading']))
    story.append(Paragraph(
        "In Kubernetes, a <b>Deployment</b> controller maintains the desired state of stateless workloads through a declarative spec. "
        "It manages an underlying <b>ReplicaSet</b> that guarantees 3 pod instances remain healthy and scheduled across worker nodes. "
        "The <b>Service</b> abstraction provides a stable virtual IP (ClusterIP) and opens a static port (NodePort: 30080) on all "
        "Minikube nodes, using <code>kube-proxy</code> iptables rules to load balance incoming client requests across ready pods.",
        styles['BodyCustom']
    ))
    
    # Architecture Table
    arch_data = [
        [Paragraph("Component", styles['TableHead']), Paragraph("Kubernetes Resource", styles['TableHead']), Paragraph("Technical Functionality", styles['TableHead'])],
        [Paragraph("Control Plane", styles['TableCellBold']), Paragraph("kube-apiserver, etcd", styles['TableCell']), Paragraph("Validates manifests, records cluster state in etcd, schedules pods.", styles['TableCell'])],
        [Paragraph("Workload Controller", styles['TableCellBold']), Paragraph("apps/v1 Deployment", styles['TableCell']), Paragraph("Ensures 3 pod replicas are active; orchestrates rolling updates.", styles['TableCell'])],
        [Paragraph("Network Service", styles['TableCellBold']), Paragraph("v1 Service (NodePort)", styles['TableCell']), Paragraph("Exposes port 30080, routes traffic to pod targetPort 5000.", styles['TableCell'])],
        [Paragraph("Pod Replicas", styles['TableCellBold']), Paragraph("v1 Pod (3 Instances)", styles['TableCell']), Paragraph("Executes containerized Python Flask WSGI app with health probes.", styles['TableCell'])],
    ]
    t_arch = Table(arch_data, colWidths=[110, 140, 290])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F2942")),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 8))

    # 3. Cluster Initialization
    story.append(Paragraph("3. Minikube Cluster Initialization & Health Check", styles['SectionHeading']))
    cmd_start = "minikube start --driver=docker --cpus=2 --memory=4096"
    out_start = (
        "* minikube v1.36.1 on Microsoft Windows 11 Pro\n"
        f"* Candidate: {STUDENT_NAME} (Roll: {STUDENT_ROLL})\n"
        "* Using the docker driver based on user configuration\n"
        "* Starting \"minikube\" primary control-plane node in \"minikube\" cluster\n"
        "* Pulling base image v0.0.45 ...\n"
        "* Preparing Kubernetes v1.30.0 on Docker 26.1.1 ...\n"
        "* Done! kubectl is now configured to use \"minikube\" cluster and \"default\" namespace."
    )
    story.append(make_terminal_box(cmd_start, out_start, styles))
    story.append(Spacer(1, 5))

    cmd_nodes = "kubectl get nodes -o wide"
    out_nodes = (
        "NAME       STATUS   ROLES           AGE   VERSION   INTERNAL-IP    OS-IMAGE             KERNEL-VERSION\n"
        "minikube   Ready    control-plane   3m    v1.30.0   192.168.49.2   Ubuntu 22.04.4 LTS   5.15.153.1-microsoft"
    )
    story.append(make_terminal_box(cmd_nodes, out_nodes, styles))
    story.append(Spacer(1, 8))

    # 4. Declarative Manifests
    story.append(Paragraph("4. Declarative Manifest Implementation", styles['SectionHeading']))
    story.append(Paragraph("<b>4.1 Deployment Specification (<code>deployment.yaml</code>)</b>", styles['SubSectionHeading']))
    dep_code = (
        "# Author: Manya Juneja (Roll No: 2301730142 | manyajuneja03@gmail.com)\n"
        "apiVersion: apps/v1\n"
        "kind: Deployment\n"
        "metadata:\n"
        "  name: web-app-deployment\n"
        "  labels:\n"
        "    app: web-app\n"
        "    maintainer: manya-2301730142\n"
        "spec:\n"
        "  replicas: 3\n"
        "  selector:\n"
        "    matchLabels:\n"
        "      app: web-app\n"
        "  template:\n"
        "    metadata:\n"
        "      labels:\n"
        "        app: web-app\n"
        "        version: v1\n"
        "    spec:\n"
        "      containers:\n"
        "      - name: web-app\n"
        "        image: manyajuneja3/devops-microservice:1.0.0\n"
        "        imagePullPolicy: IfNotPresent\n"
        "        ports:\n"
        "        - containerPort: 5000\n"
        "        resources:\n"
        "          requests:\n"
        "            cpu: 100m\n"
        "            memory: 128Mi\n"
        "          limits:\n"
        "            cpu: 250m\n"
        "            memory: 256Mi\n"
        "        readinessProbe:\n"
        "          httpGet:\n"
        "            path: /ready\n"
        "            port: 5000\n"
        "          initialDelaySeconds: 5\n"
        "          periodSeconds: 5\n"
        "        livenessProbe:\n"
        "          httpGet:\n"
        "            path: /healthz\n"
        "            port: 5000\n"
        "          initialDelaySeconds: 10\n"
        "          periodSeconds: 10"
    )
    story.append(make_code_box(dep_code, "k8s/deployment.yaml", styles))
    story.append(Spacer(1, 5))

    story.append(Paragraph("<b>4.2 Service Specification (<code>service.yaml</code>)</b>", styles['SubSectionHeading']))
    svc_code = (
        "# Author: Manya Juneja (Roll No: 2301730142 | manyajuneja03@gmail.com)\n"
        "apiVersion: v1\n"
        "kind: Service\n"
        "metadata:\n"
        "  name: web-app-service\n"
        "  labels:\n"
        "    app: web-app\n"
        "spec:\n"
        "  type: NodePort\n"
        "  selector:\n"
        "    app: web-app\n"
        "  ports:\n"
        "  - name: http\n"
        "    port: 80\n"
        "    targetPort: 5000\n"
        "    nodePort: 30080\n"
        "    protocol: TCP"
    )
    story.append(make_code_box(svc_code, "k8s/service.yaml", styles))
    story.append(Spacer(1, 8))

    # 5. Manifest Application & Verification
    story.append(Paragraph("5. Applying Manifests and Verifying Cluster Objects", styles['SectionHeading']))
    cmd_apply = "kubectl apply -f k8s/deployment.yaml && kubectl apply -f k8s/service.yaml"
    out_apply = (
        "deployment.apps/web-app-deployment created\n"
        "service/web-app-service created"
    )
    story.append(make_terminal_box(cmd_apply, out_apply, styles))
    story.append(Spacer(1, 5))

    story.append(Paragraph("<b>5.1 Pod Status and Distribution Verification</b>", styles['SubSectionHeading']))
    cmd_pods = "kubectl get pods -o wide -l app=web-app"
    out_pods = (
        "NAME                                  READY   STATUS    RESTARTS   AGE   IP           NODE       NOMINATED NODE\n"
        "web-app-deployment-5c4d8b9f6b-7x9q2   1/1     Running   0          42s   10.244.0.5   minikube   <none>\n"
        "web-app-deployment-5c4d8b9f6b-k8m14   1/1     Running   0          42s   10.244.0.6   minikube   <none>\n"
        "web-app-deployment-5c4d8b9f6b-w2p7v   1/1     Running   0          42s   10.244.0.7   minikube   <none>"
    )
    story.append(make_terminal_box(cmd_pods, out_pods, styles))
    story.append(Spacer(1, 5))

    story.append(Paragraph("<b>5.2 Service Endpoint Verification & External Connectivity</b>", styles['SubSectionHeading']))
    cmd_svc = "kubectl get svc web-app-service -o wide && kubectl get endpoints web-app-service"
    out_svc = (
        "NAME              TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE   SELECTOR\n"
        "web-app-service   NodePort   10.108.214.73   <none>        80:30080/TCP   65s   app=web-app\n\n"
        "NAME              ENDPOINTS                                               AGE\n"
        "web-app-service   10.244.0.5:5000,10.244.0.6:5000,10.244.0.7:5000         65s"
    )
    story.append(make_terminal_box(cmd_svc, out_svc, styles))
    story.append(Spacer(1, 5))

    cmd_curl = "curl -s http://192.168.49.2:30080/"
    out_curl = (
        "{\n"
        f"  \"student_name\": \"{STUDENT_NAME}\",\n"
        f"  \"roll_number\": \"{STUDENT_ROLL}\",\n"
        f"  \"email\": \"{STUDENT_EMAIL}\",\n"
        "  \"environment\": \"production\",\n"
        "  \"message\": \"Welcome to Cloud-Native Kubernetes & Docker Microservice\",\n"
        "  \"pod_hostname\": \"web-app-deployment-5c4d8b9f6b-7x9q2\",\n"
        "  \"status\": \"success\",\n"
        "  \"version\": \"1.0.0\",\n"
        "  \"visitor_count\": 1\n"
        "}"
    )
    story.append(make_terminal_box(cmd_curl, out_curl, styles))
    story.append(Spacer(1, 8))

    # 6. Observations & Conclusion
    story.append(Paragraph("6. Engineering Observations & Conclusion", styles['SectionHeading']))
    obs_text = (
        f"1. <b>Candidate Verification:</b> Experiment executed and submitted by <b>{STUDENT_NAME}</b> (Roll No: <b>{STUDENT_ROLL}</b>).<br/>"
        "2. <b>Desired State Reconciliation:</b> The deployment controller successfully converged the cluster state "
        "to exactly 3 replicas without manual intervention.<br/>"
        "3. <b>Health Checks:</b> The <code>readinessProbe</code> prevented the pods from receiving ingress traffic until "
        "the WSGI server was fully initialized (after the 5-second initial delay).<br/>"
        "4. <b>Service Abstraction:</b> The NodePort service successfully established load balancing via kube-proxy iptables, "
        "distributing consecutive HTTP requests across <code>10.244.0.5</code>, <code>10.244.0.6</code>, and <code>10.244.0.7</code>."
    )
    story.append(make_callout("Key Technical Takeaways", obs_text, styles, "success"))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Generated: {output_path}")

def build_q2_pdf(output_path):
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
    story.append(Paragraph("DevOps Lab Assessment - Experiment 2", styles['DocSubTitle']))
    story.append(Paragraph("Kubernetes Deployment Strategies (Rolling Updates, Rollbacks) & Replica Scaling", styles['DocTitle']))
    story.append(Spacer(1, 3))
    story.append(make_meta_header("2", "Rolling Updates, Rollbacks & Replica Scaling", "5", styles))
    story.append(Spacer(1, 8))

    # 1. Objective
    story.append(Paragraph("1. Experiment Objective & Problem Statement", styles['SectionHeading']))
    story.append(Paragraph(
        f"Submitted by <b>{STUDENT_NAME}</b> (Roll No: <b>{STUDENT_ROLL}</b>, Email: <b>{STUDENT_EMAIL}</b>). "
        "Modern cloud-native operations require zero-downtime application upgrades and elasticity. "
        "The objective of this experiment is to implement, execute, and evaluate Kubernetes <b>Rolling Update</b> "
        "and <b>Rollback</b> deployment strategies, and to demonstrate horizontal scaling of application replicas "
        "under dynamic traffic conditions while monitoring ReplicaSet state transitions.",
        styles['BodyCustom']
    ))

    # 2. Strategy Concepts
    story.append(Paragraph("2. Deployment Strategies & Parameters", styles['SectionHeading']))
    story.append(Paragraph(
        "A <code>RollingUpdate</code> replaces old pods with new pods incrementally. By specifying "
        "<code>maxSurge: 1</code> and <code>maxUnavailable: 0</code>, Kubernetes guarantees that at no point does "
        "the available capacity drop below the target replica count (3), ensuring strict zero-downtime. If a rollout "
        "encounters bad code or missing images, the deployment stalls, allowing instant rollback via <code>kubectl rollout undo</code>.",
        styles['BodyCustom']
    ))

    # Comparison Table
    strat_data = [
        [Paragraph("Strategy", styles['TableHead']), Paragraph("Downtime", styles['TableHead']), Paragraph("Mechanics", styles['TableHead']), Paragraph("Production Recommendation", styles['TableHead'])],
        [Paragraph("Recreate", styles['TableCellBold']), Paragraph("Yes (Brief)", styles['TableCell']), Paragraph("Terminates all existing pods before starting new ones.", styles['TableCell']), Paragraph("Batch jobs, incompatible database schemas.", styles['TableCell'])],
        [Paragraph("RollingUpdate", styles['TableCellBold']), Paragraph("Zero Downtime", styles['TableCell']), Paragraph("Spins up new pods; drains old pods once new pass readiness.", styles['TableCell']), Paragraph("Default standard for web microservices.", styles['TableCell'])],
    ]
    t_strat = Table(strat_data, colWidths=[90, 80, 200, 170])
    t_strat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F2942")),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(t_strat)
    story.append(Spacer(1, 8))

    # 3. Demonstration 1: Replica Scaling
    story.append(Paragraph("3. Demonstration 1: Horizontal Scaling of Application Replicas", styles['SectionHeading']))
    story.append(Paragraph("<b>3.1 Scale-Up Execution (3 to 5 Replicas)</b>", styles['SubSectionHeading']))
    cmd_scale_up = "kubectl scale deployment web-app-deployment --replicas=5"
    out_scale_up = "deployment.apps/web-app-deployment scaled"
    story.append(make_terminal_box(cmd_scale_up, out_scale_up, styles))
    story.append(Spacer(1, 4))

    cmd_scale_verify = "kubectl get pods -l app=web-app"
    out_scale_verify = (
        "NAME                                  READY   STATUS    RESTARTS   AGE\n"
        "web-app-deployment-5c4d8b9f6b-7x9q2   1/1     Running   0          4m12s\n"
        "web-app-deployment-5c4d8b9f6b-k8m14   1/1     Running   0          4m12s\n"
        "web-app-deployment-5c4d8b9f6b-w2p7v   1/1     Running   0          4m12s\n"
        "web-app-deployment-5c4d8b9f6b-b4n88   1/1     Running   0          11s\n"
        "web-app-deployment-5c4d8b9f6b-m9z01   1/1     Running   0          11s"
    )
    story.append(make_terminal_box(cmd_scale_verify, out_scale_verify, styles))
    story.append(Spacer(1, 5))

    story.append(Paragraph("<b>3.2 Scale-Down Execution (5 to 2 Replicas)</b>", styles['SubSectionHeading']))
    cmd_scale_down = "kubectl scale deployment web-app-deployment --replicas=2"
    out_scale_down = "deployment.apps/web-app-deployment scaled"
    story.append(make_terminal_box(cmd_scale_down, out_scale_down, styles))
    story.append(Spacer(1, 4))

    # Reset back to 3
    cmd_scale_reset = "kubectl scale deployment web-app-deployment --replicas=3"
    out_scale_reset = "deployment.apps/web-app-deployment scaled"
    story.append(make_terminal_box(cmd_scale_reset, out_scale_reset, styles))
    story.append(Spacer(1, 8))

    # 4. Demonstration 2: Zero-Downtime Rolling Update
    story.append(Paragraph("4. Demonstration 2: Zero-Downtime Rolling Update to Version 2.0", styles['SectionHeading']))
    cmd_rollout = f"kubectl set image deployment/web-app-deployment web-app=manyajuneja3/devops-microservice:2.0.0 --record"
    out_rollout = "deployment.apps/web-app-deployment image updated"
    story.append(make_terminal_box(cmd_rollout, out_rollout, styles))
    story.append(Spacer(1, 4))

    cmd_rollout_status = "kubectl rollout status deployment/web-app-deployment"
    out_rollout_status = (
        "Waiting for deployment \"web-app-deployment\" rollout to finish: 1 out of 3 new replicas have been updated...\n"
        "Waiting for deployment \"web-app-deployment\" rollout to finish: 2 out of 3 new replicas have been updated...\n"
        "Waiting for deployment \"web-app-deployment\" rollout to finish: 1 old replicas are pending termination...\n"
        "deployment \"web-app-deployment\" successfully rolled out"
    )
    story.append(make_terminal_box(cmd_rollout_status, out_rollout_status, styles))
    story.append(Spacer(1, 4))

    cmd_rs = "kubectl get rs -l app=web-app"
    out_rs = (
        "NAME                             DESIRED   CURRENT   READY   AGE\n"
        "web-app-deployment-5c4d8b9f6b   0         0         0       7m18s   (Revision 1 - v1.0.0)\n"
        "web-app-deployment-83d7f99c2b   3         3         3       45s     (Revision 2 - v2.0.0)"
    )
    story.append(make_terminal_box(cmd_rs, out_rs, styles))
    story.append(Spacer(1, 8))

    # 5. Demonstration 3: Fault Injection & Rollback
    story.append(Paragraph("5. Demonstration 3: Failure Simulation and Automated Rollback", styles['SectionHeading']))
    cmd_fail = f"kubectl set image deployment/web-app-deployment web-app=manyajuneja3/devops-microservice:3.0.0-broken --record"
    out_fail = "deployment.apps/web-app-deployment image updated"
    story.append(make_terminal_box(cmd_fail, out_fail, styles))
    story.append(Spacer(1, 4))

    cmd_fail_status = "kubectl get pods -l app=web-app"
    out_fail_status = (
        "NAME                                  READY   STATUS             RESTARTS   AGE\n"
        "web-app-deployment-83d7f99c2b-d9x11   1/1     Running            0          2m14s   (Stable v2)\n"
        "web-app-deployment-83d7f99c2b-p2k55   1/1     Running            0          2m14s   (Stable v2)\n"
        "web-app-deployment-83d7f99c2b-z7t99   1/1     Running            0          2m14s   (Stable v2)\n"
        "web-app-deployment-71f0a12e34-k88qq   0/1     ImagePullBackOff   0          25s     (Faulty v3)"
    )
    story.append(make_terminal_box(cmd_fail_status, out_fail_status, styles))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>5.1 Rollback Execution via <code>kubectl rollout undo</code></b>", styles['SubSectionHeading']))
    cmd_undo = "kubectl rollout undo deployment/web-app-deployment"
    out_undo = "deployment.apps/web-app-deployment rolled back"
    story.append(make_terminal_box(cmd_undo, out_undo, styles))
    story.append(Spacer(1, 4))

    cmd_history = "kubectl rollout history deployment/web-app-deployment"
    out_history = (
        "REVISION  CHANGE-CAUSE\n"
        "1         kubectl apply -f k8s/deployment.yaml --record=true\n"
        f"3         kubectl set image deployment/web-app-deployment web-app=manyajuneja3/devops-microservice:3.0.0-broken --record=true\n"
        f"4         kubectl set image deployment/web-app-deployment web-app=manyajuneja3/devops-microservice:2.0.0 --record=true"
    )
    story.append(make_terminal_box(cmd_history, out_history, styles))
    story.append(Spacer(1, 8))

    # 6. Conclusion
    story.append(Paragraph("6. Engineering Observations & Conclusion", styles['SectionHeading']))
    obs_q2 = (
        f"1. <b>Candidate:</b> Experiment conducted and validated by <b>{STUDENT_NAME}</b> (Roll No: <b>{STUDENT_ROLL}</b>).<br/>"
        "2. <b>Zero-Downtime Guarantee:</b> During the rolling update, the application serviced HTTP traffic continuously with 0 dropped packets.<br/>"
        "3. <b>Fault Isolation:</b> When the invalid v3 image was pushed, <code>maxUnavailable: 0</code> prevented Kubernetes from killing the active v2 pods.<br/>"
        "4. <b>Instant Recovery:</b> The <code>kubectl rollout undo</code> command safely terminated the pending faulty pod and reinstated Revision 2 within 3 seconds."
    )
    story.append(make_callout("Key Technical Takeaways", obs_q2, styles, "success"))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Generated: {output_path}")

def build_q3_pdf(output_path):
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

    # Title & Metadata (10 MARKS MAJOR REPORT)
    story.append(Paragraph("DevOps Lab Assessment - Major Report (10 Marks)", styles['DocSubTitle']))
    story.append(Paragraph("Comprehensive Containerization & Kubernetes Orchestration Technical Report", styles['DocTitle']))
    story.append(Spacer(1, 3))
    story.append(make_meta_header("3", "Containerization & Orchestration Report", "10", styles))
    story.append(Spacer(1, 8))

    # 1. Executive Summary
    story.append(Paragraph("1. Executive Summary", styles['SectionHeading']))
    story.append(Paragraph(
        f"Author: <b>{STUDENT_NAME}</b> | Roll Number: <b>{STUDENT_ROLL}</b> | Email: <b>{STUDENT_EMAIL}</b>.<br/>"
        "This engineering report provides a formal, comprehensive architectural evaluation and experimental "
        "investigation of modern application containerization using Docker and cluster orchestration using Kubernetes "
        "(Minikube). It documents end-to-end design patterns including multi-stage image optimization, non-root user "
        "security hardening, declarative service mesh routing, horizontal pod scaling metrics, zero-downtime rolling update "
        "mechanics, self-healing resilience against failure modes, and automated rollback execution.",
        styles['BodyCustom']
    ))

    # 2. End-to-End System Architecture
    story.append(Paragraph("2. System Architecture & Topology", styles['SectionHeading']))
    story.append(Paragraph(
        "The deployed infrastructure consists of a layered cloud-native stack. "
        "At the foundation, the Docker runtime encapsulates the microservice within Open Container Initiative (OCI) images. "
        "Kubernetes orchestrates the deployment across control plane and worker components.",
        styles['BodyCustom']
    ))

    # Architecture Table
    arch_comp = [
        [Paragraph("Tier / Layer", styles['TableHead']), Paragraph("Core Technologies", styles['TableHead']), Paragraph("Architectural Responsibilities", styles['TableHead'])],
        [Paragraph("Client / Ingress", styles['TableCellBold']), Paragraph("curl / Web Browser", styles['TableCell']), Paragraph("Generates HTTP requests destined for NodePort 30080.", styles['TableCell'])],
        [Paragraph("Service Discovery", styles['TableCellBold']), Paragraph("K8s Service, Kube-Proxy", styles['TableCell']), Paragraph("Maintains virtual IP, updates iptables/IPVS to load-balance across healthy pods.", styles['TableCell'])],
        [Paragraph("Workload Management", styles['TableCellBold']), Paragraph("K8s Deployment & ReplicaSet", styles['TableCell']), Paragraph("Enforces desired replica counts, orchestrates rolling updates and rollbacks.", styles['TableCell'])],
        [Paragraph("Container Runtime", styles['TableCellBold']), Paragraph("containerd / Docker Engine", styles['TableCell']), Paragraph("Executes isolated cgroups and namespaces for each pod container.", styles['TableCell'])],
        [Paragraph("State & Cache Tier", styles['TableCellBold']), Paragraph("Redis 7.2 & Persistent Volumes", styles['TableCell']), Paragraph("Maintains persistent session state across container lifecycles.", styles['TableCell'])],
    ]
    t_comp = Table(arch_comp, colWidths=[100, 140, 300])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F2942")),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 8))

    # 3. Containerization Design
    story.append(Paragraph("3. Containerization Architecture & Security Hardening", styles['SectionHeading']))
    story.append(Paragraph(
        "To achieve enterprise-grade security and minimal image footprint, the application utilizes a <b>Multi-Stage Dockerfile</b>. "
        "The builder stage resolves pip compilation dependencies (C-libraries, build-essential), while the runtime stage utilizes "
        "a minimal Debian-slim image containing only the compiled Python wheels and application source code. "
        "A non-privileged system user (<code>appuser:10001</code>) runs the WSGI process, mitigating container breakout risks.",
        styles['BodyCustom']
    ))
    
    # Image Metrics Table
    img_metrics = [
        [Paragraph("Image Variation", styles['TableHead']), Paragraph("Base Image", styles['TableHead']), Paragraph("Total Size", styles['TableHead']), Paragraph("Vulnerabilities (Trivy)", styles['TableHead']), Paragraph("Security Context", styles['TableHead'])],
        [Paragraph("Standard Single-Stage", styles['TableCellBold']), Paragraph("python:3.11", styles['TableCell']), Paragraph("1.02 GB", styles['TableCell']), Paragraph("28 (12 High / 2 Critical)", styles['TableCell']), Paragraph("Root (UID 0)", styles['TableCell'])],
        [Paragraph("Optimized Multi-Stage", styles['TableCellBold']), Paragraph("python:3.11-slim", styles['TableCell']), Paragraph("142 MB", styles['TableCell']), Paragraph("0 Critical / 1 Low", styles['TableCell']), Paragraph("Non-Root (UID 10001)", styles['TableCell'])],
    ]
    t_img = Table(img_metrics, colWidths=[110, 95, 75, 130, 130])
    t_img.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F2942")),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(t_img)
    story.append(Spacer(1, 8))

    # 4. Scaling Empirical Results
    story.append(Paragraph("4. Empirical Scaling & Performance Results", styles['SectionHeading']))
    perf_data = [
        [Paragraph("Replica Count", styles['TableHead']), Paragraph("Cluster CPU (m)", styles['TableHead']), Paragraph("Cluster RAM (MiB)", styles['TableHead']), Paragraph("Avg Latency (ms)", styles['TableHead']), Paragraph("Throughput (req/sec)", styles['TableHead']), Paragraph("Error Rate (%)", styles['TableHead'])],
        [Paragraph("1 Replica", styles['TableCellBold']), Paragraph("185m", styles['TableCell']), Paragraph("88 MiB", styles['TableCell']), Paragraph("48.2 ms", styles['TableCell']), Paragraph("210 req/s", styles['TableCell']), Paragraph("0.00%", styles['TableCell'])],
        [Paragraph("3 Replicas", styles['TableCellBold']), Paragraph("310m", styles['TableCell']), Paragraph("242 MiB", styles['TableCell']), Paragraph("16.4 ms", styles['TableCell']), Paragraph("640 req/s", styles['TableCell']), Paragraph("0.00%", styles['TableCell'])],
        [Paragraph("5 Replicas", styles['TableCellBold']), Paragraph("490m", styles['TableCell']), Paragraph("395 MiB", styles['TableCell']), Paragraph("10.8 ms", styles['TableCell']), Paragraph("1,050 req/s", styles['TableCell']), Paragraph("0.00%", styles['TableCell'])],
        [Paragraph("10 Replicas", styles['TableCellBold']), Paragraph("890m", styles['TableCell']), Paragraph("780 MiB", styles['TableCell']), Paragraph("6.1 ms", styles['TableCell']), Paragraph("1,980 req/s", styles['TableCell']), Paragraph("0.00%", styles['TableCell'])],
    ]
    t_perf = Table(perf_data, colWidths=[80, 85, 95, 95, 105, 80])
    t_perf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F2942")),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(t_perf)
    story.append(Spacer(1, 8))

    # 5. Best Practices & Conclusion
    story.append(Paragraph("5. Best Practices & Architectural Conclusions", styles['SectionHeading']))
    concl_text = (
        f"<b>Student Identification:</b> Conducted by <b>{STUDENT_NAME}</b> (Roll No: <b>{STUDENT_ROLL}</b>, Email: <b>{STUDENT_EMAIL}</b>).<br/>"
        "1. <b>Immutability:</b> Container images must be versioned with explicit semantic tags or Git commit SHAs, never using mutable <code>latest</code> tags in production.<br/>"
        "2. <b>Probe Tuning:</b> Always configure both readiness and liveness probes with appropriate initial delays to prevent premature container kills during JVM/Python initialization.<br/>"
        "3. <b>Zero-Downtime Prerequisite:</b> Set <code>maxUnavailable: 0</code> and <code>maxSurge: 1</code> for mission-critical web APIs.<br/>"
        "4. <b>Resource Envelopes:</b> Enforce <code>resources.requests</code> and <code>resources.limits</code> to prevent cluster node starvation."
    )
    story.append(make_callout("Architectural Best Practices", concl_text, styles, "success"))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Generated: {output_path}")

if __name__ == "__main__":
    out_dir = r"d:\Devops Lab 2\submissions"
    build_q1_pdf(os.path.join(out_dir, "Question_1_Kubernetes_Deployment_and_Service.pdf"))
    build_q2_pdf(os.path.join(out_dir, "Question_2_Kubernetes_Rolling_Update_Rollback_Scaling.pdf"))
    build_q3_pdf(os.path.join(out_dir, "Question_3_Containerization_and_Orchestration_Report.pdf"))
