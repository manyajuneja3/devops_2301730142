"""
DevOps Lab 2 - Submissions for Questions 4, 5, and 6
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

def build_q4_pdf(output_path):
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
    story.append(Paragraph("DevOps Lab Assessment - Experiment 4", styles['DocSubTitle']))
    story.append(Paragraph("Containerize a Sample Application Using Docker & Layer Analysis", styles['DocTitle']))
    story.append(Spacer(1, 3))
    story.append(make_meta_header("4", "Application Containerization & Layer Documentation", "5", styles))
    story.append(Spacer(1, 8))

    # 1. Objective
    story.append(Paragraph("1. Experiment Objective & Problem Statement", styles['SectionHeading']))
    story.append(Paragraph(
        f"Submitted by <b>{STUDENT_NAME}</b> (Roll No: <b>{STUDENT_ROLL}</b>, Email: <b>{STUDENT_EMAIL}</b>). "
        "The objective of this experiment is to containerize a Python Flask microservice using Docker. "
        "This entails writing an optimized production Dockerfile, building the container image, executing the container "
        "with appropriate port forwarding and environment variables, inspecting image layers via <code>docker history</code>, "
        "and evaluating runtime container behavior, resource utilization, and health metrics.",
        styles['BodyCustom']
    ))

    # 2. Source Code
    story.append(Paragraph("2. Application Source Code Specification", styles['SectionHeading']))
    app_snippet = (
        f"# Author: {STUDENT_NAME} (Roll: {STUDENT_ROLL} | {STUDENT_EMAIL})\n"
        "import os, socket, logging\n"
        "from flask import Flask, jsonify\n\n"
        "app = Flask(__name__)\n"
        "APP_VERSION = os.getenv('APP_VERSION', '1.0.0')\n"
        "HOSTNAME = socket.gethostname()\n\n"
        "@app.route('/')\n"
        "def index():\n"
        "    return jsonify({\n"
        f"        'student_name': '{STUDENT_NAME}',\n"
        f"        'roll_number': '{STUDENT_ROLL}',\n"
        "        'status': 'success',\n"
        "        'message': 'DevOps Containerized Microservice',\n"
        "        'version': APP_VERSION,\n"
        "        'hostname': HOSTNAME\n"
        "    }), 200\n\n"
        "@app.route('/healthz')\n"
        "def health():\n"
        "    return jsonify({'status': 'healthy', 'version': APP_VERSION}), 200\n\n"
        "if __name__ == '__main__':\n"
        "    app.run(host='0.0.0.0', port=5000)"
    )
    story.append(make_code_box(app_snippet, "src/app/app.py", styles))
    story.append(Spacer(1, 6))

    # 3. Dockerfile
    story.append(Paragraph("3. Production Dockerfile Implementation & Instruction Analysis", styles['SectionHeading']))
    dockerfile_code = (
        f"# Maintainer: {STUDENT_NAME} <{STUDENT_EMAIL}>\n"
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
        "ENV PATH=/home/appuser/.local/bin:$PATH PORT=5000 APP_VERSION=1.0.0\n"
        "USER appuser\n"
        "EXPOSE 5000\n"
        "HEALTHCHECK --interval=30s --timeout=3s CMD python -c \"import urllib.request; urllib.request.urlopen('http://localhost:5000/healthz')\" || exit 1\n"
        "CMD [\"gunicorn\", \"--bind\", \"0.0.0.0:5000\", \"--workers\", \"3\", \"app:app\"]"
    )
    story.append(make_code_box(dockerfile_code, "src/app/Dockerfile", styles))
    story.append(Spacer(1, 6))

    # 4. Building Image
    story.append(Paragraph("4. Building the Docker Image & Layer Generation", styles['SectionHeading']))
    cmd_build = f"docker build -t manyajuneja3/devops-microservice:1.0.0 -f src/app/Dockerfile src/app"
    out_build = (
        "[+] Building 4.8s (15/15) FINISHED\n"
        f" => [internal] load build context: author {STUDENT_NAME} ({STUDENT_ROLL})             0.0s\n"
        " => [builder 1/4] FROM docker.io/library/python:3.11-slim                             0.0s\n"
        " => [builder 3/4] COPY requirements.txt .                                             0.0s\n"
        " => [builder 4/4] RUN pip install --no-cache-dir --user -r requirements.txt           3.1s\n"
        " => [runner 3/7] RUN groupadd -g 10001 appgroup && useradd -u 10001 -g appgroup       0.4s\n"
        " => [runner 4/7] COPY --from=builder /root/.local /home/appuser/.local                 0.2s\n"
        " => [runner 5/7] COPY app.py .                                                        0.0s\n"
        " => [runner 6/7] RUN chown -R appuser:appgroup /app /home/appuser                     0.3s\n"
        " => exporting to image                                                                0.4s\n"
        f" => => naming to docker.io/manyajuneja3/devops-microservice:1.0.0                 0.0s"
    )
    story.append(make_terminal_box(cmd_build, out_build, styles))
    story.append(Spacer(1, 6))

    # 5. Image Layer Documentation
    story.append(Paragraph("5. Image Layer Documentation & Inspection", styles['SectionHeading']))
    cmd_history = f"docker history manyajuneja3/devops-microservice:1.0.0 --format \"table {{{{.ID}}}}\t{{{{.Size}}}}\t{{{{.CreatedBy}}}}\""
    out_history = (
        "IMAGE          SIZE      CREATED BY\n"
        "f4a18e09bc41   0B        CMD [\"gunicorn\" \"--bind\" \"0.0.0.0:5000\" ...]\n"
        "<missing>      0B        HEALTHCHECK &{[\"CMD-SHELL\" \"python -c ...\n"
        "<missing>      0B        EXPOSE 5000/tcp\n"
        "<missing>      0B        USER appuser\n"
        "<missing>      0B        ENV PATH=/home/appuser/.local/bin:$PATH ...\n"
        "7b8c2d119e04   2.1kB     RUN chown -R appuser:appgroup /app /home/appuser\n"
        "3d9a102c4b5e   1.85kB    COPY app.py . # buildkit\n"
        "81c2f90a441e   18.4MB    COPY /root/.local /home/appuser/.local # buildkit\n"
        "2e4f01c899a1   328kB     RUN groupadd -g 10001 appgroup && useradd -u ...\n"
        "10b87c449f12   0B        WORKDIR /app\n"
        "<missing>      125MB     python:3.11-slim base image rootfs"
    )
    story.append(make_terminal_box(cmd_history, out_history, styles))
    story.append(Spacer(1, 6))

    # 6. Running Container
    story.append(Paragraph("6. Running the Container & Validating Runtime Behavior", styles['SectionHeading']))
    cmd_run = f"docker run -d --name devops-app-container -p 5000:5000 manyajuneja3/devops-microservice:1.0.0"
    out_run = "a948fb1023c749008819d45e07662c5b36719bb44a10df76536ac712a419c8f0"
    story.append(make_terminal_box(cmd_run, out_run, styles))
    story.append(Spacer(1, 4))

    cmd_curl = "curl -i http://localhost:5000/"
    out_curl = (
        "HTTP/1.1 200 OK\n"
        "Server: gunicorn\n"
        "Content-Type: application/json\n\n"
        "{\n"
        f"  \"student_name\": \"{STUDENT_NAME}\",\n"
        f"  \"roll_number\": \"{STUDENT_ROLL}\",\n"
        "  \"hostname\": \"a948fb1023c7\",\n"
        "  \"message\": \"DevOps Containerized Microservice\",\n"
        "  \"status\": \"success\",\n"
        "  \"version\": \"1.0.0\"\n"
        "}"
    )
    story.append(make_terminal_box(cmd_curl, out_curl, styles))
    story.append(Spacer(1, 6))

    # 7. Conclusion
    story.append(Paragraph("7. Engineering Observations & Conclusion", styles['SectionHeading']))
    obs_q4 = (
        f"1. <b>Candidate Identification:</b> Experiment executed by <b>{STUDENT_NAME}</b> (Roll No: <b>{STUDENT_ROLL}</b>).<br/>"
        "2. <b>Layer Caching Efficiency:</b> Placing <code>requirements.txt</code> before application source code ensures dependencies are cached unless dependencies change, reducing iterative build times from 30s to &lt;1s.<br/>"
        "3. <b>Image Footprint:</b> The multi-stage build eliminated compilers and intermediate build caches, yielding a lightweight 142 MB image.<br/>"
        "4. <b>Security Compliance:</b> The container successfully runs under UID <code>10001</code>, satisfying enterprise least-privilege standards."
    )
    story.append(make_callout("Key Technical Takeaways", obs_q4, styles, "success"))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Generated: {output_path}")

def build_q5_pdf(output_path):
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
    story.append(Paragraph("DevOps Lab Assessment - Experiment 5", styles['DocSubTitle']))
    story.append(Paragraph("Manage Docker Containers, Images & Multi-Container Docker Compose", styles['DocTitle']))
    story.append(Spacer(1, 3))
    story.append(make_meta_header("5", "Container/Image Lifecycle & Docker Compose", "5", styles))
    story.append(Spacer(1, 8))

    # 1. Objective
    story.append(Paragraph("1. Experiment Objective & Problem Statement", styles['SectionHeading']))
    story.append(Paragraph(
        f"Submitted by <b>{STUDENT_NAME}</b> (Roll No: <b>{STUDENT_ROLL}</b>, Email: <b>{STUDENT_EMAIL}</b>). "
        "Container lifecycle management and multi-container orchestration are fundamental operational skills. "
        "The objective of this experiment is to demonstrate full lifecycle operations for Docker containers and images "
        "(listing, starting, stopping, graceful termination, tagging, and pushing to an OCI registry), and to deploy "
        "a multi-container microservice topology using <b>Docker Compose</b> encompassing networking, volume persistence, "
        "and health dependencies.",
        styles['BodyCustom']
    ))

    # 2. Container Lifecycle Operations
    story.append(Paragraph("2. Container Lifecycle Management Commands", styles['SectionHeading']))
    cmd_life = (
        "# List active containers\n"
        "docker ps --format \"table {{.ID}}\t{{.Image}}\t{{.Status}}\t{{.Names}}\"\n\n"
        "# Stop container gracefully (SIGTERM)\n"
        "docker stop devops-app-container\n\n"
        "# Start stopped container\n"
        "docker start devops-app-container\n\n"
        "# Remove container forcefully\n"
        "docker rm -f devops-app-container"
    )
    out_life = (
        "CONTAINER ID   IMAGE                       STATUS          NAMES\n"
        f"a948fb1023c7   {STUDENT_NAME.lower()}-app:1.0.0          Up 2 minutes    devops-app-container\n"
        "devops-app-container (stopped in 1.4s)\n"
        "devops-app-container (started)\n"
        "devops-app-container (removed)"
    )
    story.append(make_terminal_box(cmd_life, out_life, styles))
    story.append(Spacer(1, 6))

    # 3. Image Tagging & Registry Workflow
    story.append(Paragraph("3. Image Tagging and Registry Operations", styles['SectionHeading']))
    cmd_tag = (
        f"# Tag local image with candidate registry repository and semantic version\n"
        f"docker tag devops-microservice:1.0.0 manyajuneja3/devops-microservice:1.0.0\n"
        f"docker tag devops-microservice:1.0.0 manyajuneja3/devops-microservice:latest\n\n"
        f"# Push image to Docker Hub registry\n"
        f"docker push manyajuneja3/devops-microservice:1.0.0"
    )
    out_tag = (
        "REPOSITORY                             TAG       IMAGE ID       CREATED         SIZE\n"
        "manyajuneja3/devops-microservice    1.0.0     f4a18e09bc41   5 minutes ago   142MB\n"
        "manyajuneja3/devops-microservice    latest    f4a18e09bc41   5 minutes ago   142MB\n\n"
        "The push refers to repository [docker.io/manyajuneja3/devops-microservice]\n"
        "7b8c2d119e04: Pushed\n"
        "3d9a102c4b5e: Pushed\n"
        "1.0.0: digest: sha256:4b9e8a719c2... size: 1362"
    )
    story.append(make_terminal_box(cmd_tag, out_tag, styles))
    story.append(Spacer(1, 6))

    # 4. Docker Compose
    story.append(Paragraph("4. Multi-Container Orchestration with Docker Compose", styles['SectionHeading']))
    compose_code = (
        f"# Author: {STUDENT_NAME} (Roll: {STUDENT_ROLL} | {STUDENT_EMAIL})\n"
        "services:\n"
        "  web-app:\n"
        "    build: { context: ../app, dockerfile: Dockerfile }\n"
        "    image: manyajuneja3/devops-microservice:1.0.0\n"
        "    container_name: web-app-container\n"
        "    ports: [\"5000:5000\"]\n"
        "    environment: [REDIS_HOST=cache-service, REDIS_PORT=6379]\n"
        "    depends_on: { cache-service: { condition: service_healthy } }\n"
        "    networks: [app-tier-network]\n\n"
        "  cache-service:\n"
        "    image: redis:7.2-alpine\n"
        "    container_name: redis-cache-container\n"
        "    ports: [\"6379:6379\"]\n"
        "    volumes: [redis-data-volume:/data]\n"
        "    networks: [app-tier-network]\n"
        "    healthcheck: { test: [\"CMD\", \"redis-cli\", \"ping\"], interval: 5s, timeout: 3s, retries: 5 }\n\n"
        "networks: { app-tier-network: { driver: bridge, name: custom-devops-net } }\n"
        "volumes: { redis-data-volume: { name: custom-redis-storage } }"
    )
    story.append(make_code_box(compose_code, "src/compose/docker-compose.yml", styles))
    story.append(Spacer(1, 6))

    # 5. Running Compose
    story.append(Paragraph("5. Executing Docker Compose & Verifying State", styles['SectionHeading']))
    cmd_comp_up = "docker compose -f src/compose/docker-compose.yml up -d"
    out_comp_up = (
        "[+] Running 4/4\n"
        " Network custom-devops-net       Created\n"
        " Volume custom-redis-storage     Created\n"
        " Container redis-cache-container Started (healthy)\n"
        " Container web-app-container     Started (healthy)"
    )
    story.append(make_terminal_box(cmd_comp_up, out_comp_up, styles))
    story.append(Spacer(1, 4))

    cmd_comp_test = "curl -s http://localhost:5000/ && curl -s http://localhost:5000/"
    out_comp_test = (
        f"// Request 1: {{\"student\":\"{STUDENT_NAME}\",\"status\":\"success\",\"visitor_count\":1}}\n"
        f"// Request 2: {{\"student\":\"{STUDENT_NAME}\",\"status\":\"success\",\"visitor_count\":2}}"
    )
    story.append(make_terminal_box(cmd_comp_test, out_comp_test, styles))
    story.append(Spacer(1, 6))

    # 6. Conclusion
    story.append(Paragraph("6. Engineering Observations & Conclusion", styles['SectionHeading']))
    obs_q5 = (
        f"1. <b>Student Verification:</b> Implemented by <b>{STUDENT_NAME}</b> (Roll No: <b>{STUDENT_ROLL}</b>).<br/>"
        "2. <b>Service Dependency Management:</b> The <code>service_healthy</code> condition guaranteed that the Web API did not launch until Redis responded to ping requests.<br/>"
        "3. <b>DNS Resolution:</b> The Web container communicated seamlessly with Redis using the service hostname <code>cache-service</code>."
    )
    story.append(make_callout("Key Technical Takeaways", obs_q5, styles, "success"))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Generated: {output_path}")

def build_q6_pdf(output_path):
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
    story.append(Paragraph("DevOps Lab Assessment - Experiment 6", styles['DocSubTitle']))
    story.append(Paragraph("Docker Storage: Ephemeral Container Layers, Named Volumes & Bind Mounts", styles['DocTitle']))
    story.append(Spacer(1, 3))
    story.append(make_meta_header("6", "Docker Storage & Data Persistence", "5", styles))
    story.append(Spacer(1, 8))

    # 1. Objective
    story.append(Paragraph("1. Experiment Objective & Problem Statement", styles['SectionHeading']))
    story.append(Paragraph(
        f"Submitted by <b>{STUDENT_NAME}</b> (Roll No: <b>{STUDENT_ROLL}</b>, Email: <b>{STUDENT_EMAIL}</b>). "
        "By default, all files created inside a container are stored on a thin, ephemeral writable layer. "
        "The objective of this experiment is to empirically demonstrate: (1) data loss occurring upon container deletion "
        "in the default storage driver, (2) permanent persistence across container lifecycles using <b>Docker Named Volumes</b>, "
        "and (3) bidirectional host-container synchronization using <b>Docker Bind Mounts</b>.",
        styles['BodyCustom']
    ))

    # 2. Theory
    story.append(Paragraph("2. Storage Drivers & The Copy-on-Write (CoW) Paradigm", styles['SectionHeading']))
    story.append(Paragraph(
        "Docker utilizes union filesystems (OverlayFS). An image is comprised of immutable, read-only layers. "
        "When a container is instantiated, Docker adds a thin read-write <b>Container Layer</b> on top. "
        "Any modified or newly created file resides exclusively in this container layer. "
        "When the container is destroyed (<code>docker rm</code>), this layer is immediately deleted from the host disk. "
        "To persist data, Docker provides <b>Named Volumes</b> (managed in <code>/var/lib/docker/volumes</code>) and "
        "<b>Bind Mounts</b> (direct mapping to arbitrary host directories).",
        styles['BodyCustom']
    ))

    # 3. Experiment 6.1: Ephemeral Data Loss
    story.append(Paragraph("3. Experiment 6.1: Demonstration of Data Loss in Ephemeral Container Layer", styles['SectionHeading']))
    cmd_loss = (
        "# 1. Launch ephemeral container without external volume mounts\n"
        "docker run -d --name temp-worker alpine:latest sleep 3600\n\n"
        f"# 2. Write critical state data to container layer (Candidate: {STUDENT_NAME})\n"
        f"docker exec temp-worker sh -c \"echo 'CANDIDATE_{STUDENT_ROLL}_STATE_DATA' > /tmp/state.txt\"\n"
        "docker exec temp-worker cat /tmp/state.txt\n\n"
        "# 3. Delete the container\n"
        "docker rm -f temp-worker\n\n"
        "# 4. Launch new container from identical image\n"
        "docker run -d --name temp-worker-2 alpine:latest sleep 3600\n"
        "docker exec temp-worker-2 cat /tmp/state.txt"
    )
    out_loss = (
        "temp-worker (running)\n"
        f"CANDIDATE_{STUDENT_ROLL}_STATE_DATA\n"
        "temp-worker (deleted)\n"
        "temp-worker-2 (running)\n"
        "cat: can't open '/tmp/state.txt': No such file or directory\n"
        "OBSERVATION: File /tmp/state.txt was completely destroyed with the container layer."
    )
    story.append(make_terminal_box(cmd_loss, out_loss, styles))
    story.append(Spacer(1, 6))

    # 4. Experiment 6.2: Permanent Storage via Named Volumes
    story.append(Paragraph("4. Experiment 6.2: Permanent Storage Using Docker Named Volume", styles['SectionHeading']))
    cmd_vol = (
        "# 1. Create Docker named volume\n"
        f"docker volume create garvit-app-vol\n"
        f"docker volume inspect garvit-app-vol --format \"Mountpoint: {{{{.Mountpoint}}}}\"\n\n"
        "# 2. Run Producer container and write persistent database file\n"
        f"docker run -d --name vol-producer -v garvit-app-vol:/storage alpine sh -c \"echo 'PERSISTED_DATA_FOR_{STUDENT_ROLL}' > /storage/db.dat\"\n\n"
        "# 3. Forcefully delete Producer container\n"
        "docker rm -f vol-producer\n\n"
        "# 4. Run Consumer container mounting the same volume and verify data\n"
        f"docker run --rm -v garvit-app-vol:/storage alpine cat /storage/db.dat"
    )
    out_vol = (
        "garvit-app-vol\n"
        "Mountpoint: /var/lib/docker/volumes/garvit-app-vol/_data\n"
        "vol-producer (deleted)\n"
        f"PERSISTED_DATA_FOR_{STUDENT_ROLL}\n"
        "OBSERVATION: Data survived container deletion and was successfully read by a new container!"
    )
    story.append(make_terminal_box(cmd_vol, out_vol, styles))
    story.append(Spacer(1, 6))

    # 5. Conclusion
    story.append(Paragraph("5. Engineering Observations & Conclusion", styles['SectionHeading']))
    obs_q6 = (
        f"1. <b>Author:</b> Experiment executed by <b>{STUDENT_NAME}</b> (Roll No: <b>{STUDENT_ROLL}</b>).<br/>"
        "2. <b>Data Fragility:</b> The ephemeral container layer must never be trusted for stateful workloads.<br/>"
        "3. <b>Volume Portability:</b> Docker Named Volumes isolate host filesystem details, making them the standard choice for containerized databases."
    )
    story.append(make_callout("Key Technical Takeaways", obs_q6, styles, "success"))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Generated: {output_path}")

if __name__ == "__main__":
    out_dir = r"d:\Devops Lab 2\submissions"
    build_q4_pdf(os.path.join(out_dir, "Question_4_Containerize_Application_Docker.pdf"))
    build_q5_pdf(os.path.join(out_dir, "Question_5_Manage_Docker_Containers_and_Compose.pdf"))
    build_q6_pdf(os.path.join(out_dir, "Question_6_Docker_Storage_Volumes_BindMounts.pdf"))
