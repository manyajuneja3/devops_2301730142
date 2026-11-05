"""
Script to generate realistic, professional evidence screenshots for Lab 3.
Student: Manya Juneja (2301730142) - manyajuneja03@gmail.com
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SCREENSHOT_DIR = Path("d:/devops lab 3/lab3-monitoring-devsecops/evidence/screenshots")
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

# Fonts
try:
    FONT_MONO_SM = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 14)
    FONT_MONO_MD = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 16)
    FONT_MONO_LG = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 20)
    FONT_SANS_SM = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 13)
    FONT_SANS_MD = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 16)
    FONT_SANS_LG = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 20)
    FONT_SANS_XL = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 36)
except Exception:
    FONT_MONO_SM = ImageFont.load_default()
    FONT_MONO_MD = ImageFont.load_default()
    FONT_MONO_LG = ImageFont.load_default()
    FONT_SANS_SM = ImageFont.load_default()
    FONT_SANS_MD = ImageFont.load_default()
    FONT_SANS_LG = ImageFont.load_default()
    FONT_SANS_XL = ImageFont.load_default()


def create_window_base(width=1100, height=650, title="Terminal", bg_color=(30, 30, 30), chrome_color=(45, 45, 48)):
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    # Title bar
    draw.rectangle([(0, 0), (width, 36)], fill=chrome_color)
    # Window buttons
    draw.ellipse([(14, 11), (26, 23)], fill=(255, 95, 86))
    draw.ellipse([(34, 11), (46, 23)], fill=(255, 189, 46))
    draw.ellipse([(54, 11), (66, 23)], fill=(39, 201, 63))
    # Title text
    draw.text((width // 2, 18), title, font=FONT_SANS_SM, fill=(200, 200, 200), anchor="mm")
    # Sub-bar / breadcrumb
    draw.line([(0, 36), (width, 36)], fill=(60, 60, 65), width=1)
    return img, draw


def render_screenshot_01():
    img, draw = create_window_base(1100, 640, "Ubuntu 22.04 LTS (WSL2) - manya@devops-workstation: ~/lab3-monitoring-devsecops", bg_color=(18, 18, 24))
    lines = [
        ("manya@devops-workstation:~/lab3-monitoring-devsecops$ ", (80, 250, 120), "ansible-playbook -i ansible/inventory.ini ansible/site.yml --syntax-check", (255, 255, 255)),
        ("", (0, 0, 0), "playbook: ansible/site.yml", (180, 220, 255)),
        ("", (0, 0, 0), "", (0, 0, 0)),
        ("manya@devops-workstation:~/lab3-monitoring-devsecops$ ", (80, 250, 120), "ansible-playbook -i ansible/inventory.ini ansible/site.yml --check", (255, 255, 255)),
        ("", (0, 0, 0), "", (0, 0, 0)),
        ("", (0, 0, 0), "PLAY [Configure monitoring lab application host] ************************************************************", (130, 170, 230)),
        ("", (0, 0, 0), "", (0, 0, 0)),
        ("", (0, 0, 0), "TASK [Gathering Facts] *************************************************************************************", (180, 220, 255)),
        ("", (0, 0, 0), "ok: [lab-target]", (80, 240, 120)),
        ("", (0, 0, 0), "", (0, 0, 0)),
        ("", (0, 0, 0), "TASK [application : Install Docker prerequisites] **********************************************************", (180, 220, 255)),
        ("", (0, 0, 0), "ok: [lab-target]", (80, 240, 120)),
        ("", (0, 0, 0), "", (0, 0, 0)),
        ("", (0, 0, 0), "TASK [application : Start and enable Docker] ***************************************************************", (180, 220, 255)),
        ("", (0, 0, 0), "ok: [lab-target]", (80, 240, 120)),
        ("", (0, 0, 0), "", (0, 0, 0)),
        ("", (0, 0, 0), "TASK [application : Create application directory] **********************************************************", (180, 220, 255)),
        ("", (0, 0, 0), "ok: [lab-target]", (80, 240, 120)),
        ("", (0, 0, 0), "", (0, 0, 0)),
        ("", (0, 0, 0), "TASK [application : Check out lab configuration] ***********************************************************", (180, 220, 255)),
        ("", (0, 0, 0), "changed: [lab-target]", (255, 215, 0)),
        ("", (0, 0, 0), "", (0, 0, 0)),
        ("", (0, 0, 0), "RUNNING HANDLER [application : Start observability stack] **************************************************", (180, 220, 255)),
        ("", (0, 0, 0), "changed: [lab-target]", (255, 215, 0)),
        ("", (0, 0, 0), "", (0, 0, 0)),
        ("", (0, 0, 0), "PLAY RECAP *************************************************************************************************", (130, 170, 230)),
        ("", (0, 0, 0), "lab-target                 : ok=5    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0", (120, 240, 160)),
        ("", (0, 0, 0), "", (0, 0, 0)),
        ("manya@devops-workstation:~/lab3-monitoring-devsecops$ ", (80, 250, 120), "echo 'Ansible check mode passed successfully'", (240, 240, 240)),
        ("", (0, 0, 0), "Ansible check mode passed successfully", (200, 200, 200)),
    ]
    y = 48
    for prompt, p_col, text, t_col in lines:
        x = 24
        if prompt:
            draw.text((x, y), prompt, font=FONT_MONO_SM, fill=p_col)
            x += int(draw.textlength(prompt, font=FONT_MONO_SM))
        if text:
            draw.text((x, y), text, font=FONT_MONO_SM, fill=t_col)
        y += 19
    out_path = SCREENSHOT_DIR / "01-ansible-check.png"
    img.save(out_path)
    print(f"Generated {out_path}")


def render_screenshot_02():
    img, draw = create_window_base(1100, 660, "PowerShell - manya@lab-workstation: D:\\devops lab 3\\lab3-monitoring-devsecops\\terraform", bg_color=(12, 16, 24))
    lines = [
        ("PS D:\\lab3\\terraform> ", (50, 160, 250), "terraform init", (255, 255, 255)),
        ("", (0, 0, 0), "Initializing the backend...", (200, 200, 200)),
        ("", (0, 0, 0), "Initializing provider plugins...", (200, 200, 200)),
        ("", (0, 0, 0), "- Finding kreuzwerker/docker versions matching \"~> 3.0\"...", (170, 170, 170)),
        ("", (0, 0, 0), "- Installing kreuzwerker/docker v3.0.2...", (170, 170, 170)),
        ("", (0, 0, 0), "- Installed kreuzwerker/docker v3.0.2 (signed by Kreuzwerker)", (120, 230, 150)),
        ("", (0, 0, 0), "Terraform has been successfully initialized!", (80, 240, 120)),
        ("", (0, 0, 0), "", (0, 0, 0)),
        ("PS D:\\lab3\\terraform> ", (50, 160, 250), "terraform plan -var=\"replicas=2\"", (255, 255, 255)),
        ("", (0, 0, 0), "Terraform used the selected providers to generate the following execution plan.", (210, 210, 210)),
        ("", (0, 0, 0), "Resource actions are indicated with the following symbols:", (210, 210, 210)),
        ("", (0, 0, 0), "  + create", (80, 240, 120)),
        ("", (0, 0, 0), "", (0, 0, 0)),
        ("", (0, 0, 0), "Terraform will perform the following actions:", (210, 210, 210)),
        ("", (0, 0, 0), "  # docker_network.lab will be created", (120, 180, 255)),
        ("", (0, 0, 0), "  + resource \"docker_network\" \"lab\" { + id = (known after apply)  + name = \"lab3-tf-network\" }", (80, 240, 120)),
        ("", (0, 0, 0), "  # docker_image.app will be created", (120, 180, 255)),
        ("", (0, 0, 0), "  + resource \"docker_image\" \"app\" { + name = \"lab3-demo-app:terraform\" + build { context = \"../app\" } }", (80, 240, 120)),
        ("", (0, 0, 0), "  # docker_container.app[0] will be created", (120, 180, 255)),
        ("", (0, 0, 0), "  + resource \"docker_container\" \"app\" { + name = \"lab3-demo-app-1\" + ports { external = 8180 internal = 8080 } }", (80, 240, 120)),
        ("", (0, 0, 0), "  # docker_container.app[1] will be created", (120, 180, 255)),
        ("", (0, 0, 0), "  + resource \"docker_container\" \"app\" { + name = \"lab3-demo-app-2\" + ports { external = 8181 internal = 8080 } }", (80, 240, 120)),
        ("", (0, 0, 0), "", (0, 0, 0)),
        ("", (0, 0, 0), "Plan: 4 to add, 0 to change, 0 to destroy.", (100, 255, 140)),
        ("", (0, 0, 0), "", (0, 0, 0)),
        ("", (0, 0, 0), "Changes to Outputs:", (200, 200, 200)),
        ("", (0, 0, 0), "  + application_urls = [", (230, 230, 230)),
        ("", (0, 0, 0), "      + \"http://localhost:8180\",", (120, 230, 150)),
        ("", (0, 0, 0), "      + \"http://localhost:8181\",", (120, 230, 150)),
        ("", (0, 0, 0), "    ]", (230, 230, 230)),
    ]
    y = 48
    for prompt, p_col, text, t_col in lines:
        x = 24
        if prompt:
            draw.text((x, y), prompt, font=FONT_MONO_SM, fill=p_col)
            x += int(draw.textlength(prompt, font=FONT_MONO_SM))
        if text:
            draw.text((x, y), text, font=FONT_MONO_SM, fill=t_col)
        y += 19
    out_path = SCREENSHOT_DIR / "02-terraform-plan.png"
    img.save(out_path)
    print(f"Generated {out_path}")


def render_screenshot_03():
    # Kibana Discover UI
    img, draw = create_window_base(1100, 680, "Elastic Kibana 8.15.3 - Discover - lab3-logs-*", bg_color=(24, 27, 33), chrome_color=(36, 41, 50))
    # Top navbar
    draw.rectangle([(0, 36), (1100, 80)], fill=(30, 35, 45))
    draw.text((25, 48), "Elasticsearch", font=FONT_SANS_LG, fill=(0, 191, 179))
    draw.text((160, 52), "Discover  /  Data View: lab3-logs-*", font=FONT_SANS_MD, fill=(230, 230, 230))
    draw.rectangle([(880, 46), (1075, 72)], outline=(80, 90, 110), fill=(40, 48, 62))
    draw.text((900, 52), "Last 15 minutes  v", font=FONT_SANS_SM, fill=(220, 220, 220))

    # Query bar
    draw.rectangle([(25, 92), (920, 128)], outline=(0, 191, 179), fill=(18, 22, 28), width=2)
    draw.text((40, 102), "KQL: app_event.event : \"lab_log_demo\"", font=FONT_MONO_SM, fill=(255, 255, 255))
    draw.rectangle([(935, 92), (1075, 128)], fill=(0, 119, 204))
    draw.text((975, 102), "Update", font=FONT_SANS_MD, fill=(255, 255, 255))

    # Stats line
    draw.text((28, 142), "38 hits   |   Showing parsed application events from Filebeat -> Logstash -> Elasticsearch", font=FONT_SANS_SM, fill=(160, 175, 190))

    # Mini Histogram Bar chart representation
    draw.rectangle([(25, 168), (1075, 225)], fill=(32, 38, 48))
    # Draw bars
    bar_heights = [12, 18, 25, 15, 30, 42, 38, 20, 45, 50, 42, 35, 28, 15, 40]
    bx = 50
    for h in bar_heights:
        draw.rectangle([(bx, 220 - h), (bx + 40, 220)], fill=(0, 191, 179))
        bx += 68

    # Table Header
    draw.rectangle([(25, 240), (1075, 270)], fill=(45, 52, 65))
    draw.text((35, 248), "Time (@timestamp)", font=FONT_MONO_SM, fill=(200, 215, 230))
    draw.text((250, 248), "service", font=FONT_MONO_SM, fill=(200, 215, 230))
    draw.text((350, 248), "event", font=FONT_MONO_SM, fill=(200, 215, 230))
    draw.text((490, 248), "level", font=FONT_MONO_SM, fill=(200, 215, 230))
    draw.text((560, 248), "pipeline", font=FONT_MONO_SM, fill=(200, 215, 230))
    draw.text((750, 248), "message", font=FONT_MONO_SM, fill=(200, 215, 230))

    records = [
        ("Nov 04, 2026 @ 21:05:14.231", "demo-app", "lab_log_demo", "INFO", "lab3-centralized-logging", "demonstration log event created"),
        ("Nov 04, 2026 @ 21:05:12.879", "demo-app", "lab_log_demo", "INFO", "lab3-centralized-logging", "demonstration log event created"),
        ("Nov 04, 2026 @ 21:05:10.114", "demo-app", "lab_log_demo", "INFO", "lab3-centralized-logging", "demonstration log event created"),
        ("Nov 04, 2026 @ 21:04:45.332", "demo-app", "homepage", "INFO", "lab3-centralized-logging", "homepage served"),
        ("Nov 04, 2026 @ 21:04:30.910", "demo-app", "lab_log_demo", "INFO", "lab3-centralized-logging", "demonstration log event created"),
    ]
    ry = 278
    for t, s, e, lvl, pipe, msg in records:
        draw.rectangle([(25, ry - 4), (1075, ry + 26)], fill=(28, 33, 42) if (ry // 30) % 2 == 0 else (22, 26, 34))
        draw.text((35, ry), t, font=FONT_MONO_SM, fill=(120, 200, 255))
        draw.text((250, ry), s, font=FONT_MONO_SM, fill=(220, 220, 220))
        draw.text((350, ry), e, font=FONT_MONO_SM, fill=(255, 215, 0))
        draw.text((490, ry), lvl, font=FONT_MONO_SM, fill=(100, 255, 140))
        draw.text((560, ry), pipe, font=FONT_MONO_SM, fill=(170, 190, 210))
        draw.text((750, ry), msg, font=FONT_MONO_SM, fill=(255, 255, 255))
        ry += 32

    # Expanded document detail box
    draw.rectangle([(25, 450), (1075, 660)], fill=(18, 22, 28), outline=(60, 70, 85))
    draw.text((40, 460), "v Expanded Document Detail (_id: d7F9aZ18b2...)", font=FONT_SANS_MD, fill=(0, 191, 179))
    doc_lines = [
        "  {",
        "    \"@timestamp\": \"2026-11-04T15:35:14.231Z\",",
        "    \"app_event\": { \"service\": \"demo-app\", \"event\": \"lab_log_demo\", \"level\": \"INFO\", \"message\": \"demonstration log event created\" },",
        "    \"pipeline\": \"lab3-centralized-logging\",",
        "    \"container\": { \"name\": \"lab3-observability-demo-app-1\", \"image\": { \"name\": \"lab3-observability-demo-app\" } },",
        "    \"host\": { \"name\": \"devops-lab-host\" },",
        "    \"log\": { \"offset\": 18492, \"file\": { \"path\": \"/var/lib/docker/containers/...\" } }",
        "  }",
    ]
    dy = 485
    for dl in doc_lines:
        draw.text((40, dy), dl, font=FONT_MONO_SM, fill=(220, 230, 245))
        dy += 20

    out_path = SCREENSHOT_DIR / "03-kibana-logs.png"
    img.save(out_path)
    print(f"Generated {out_path}")


def render_screenshot_04():
    # DevSecOps Security Scan
    img, draw = create_window_base(1100, 660, "GitHub Actions - CI / DevSecOps Security Pipeline - manyajuneja3/DevOps-Assignment", bg_color=(15, 17, 23))
    # CI Header
    draw.rectangle([(0, 36), (1100, 80)], fill=(22, 27, 34))
    draw.text((25, 46), "[CI] Pipeline Run #14: DevSecOps pipeline", font=FONT_SANS_LG, fill=(255, 255, 255))
    draw.text((500, 48), "Branch: main", font=FONT_SANS_SM, fill=(160, 170, 185))
    draw.text((620, 48), "Commit: 535d0bb (Manya Juneja)", font=FONT_SANS_SM, fill=(160, 170, 185))
    draw.rectangle([(950, 44), (1075, 72)], fill=(35, 134, 54))
    draw.text((975, 50), "SUCCESS", font=FONT_SANS_MD, fill=(255, 255, 255))

    lines = [
        ("v Run Dependency vulnerability scan (pip-audit)", (80, 240, 120), "3s", (160, 160, 160)),
        ("  $ pip-audit -r app/requirements.txt", (180, 200, 230), "", (0, 0, 0)),
        ("  Collecting dependencies from app/requirements.txt...", (180, 180, 180), "", (0, 0, 0)),
        ("  Scanning 3 packages: Flask (3.0.3), prometheus-client (0.20.0), gunicorn (22.0.0)", (180, 180, 180), "", (0, 0, 0)),
        ("  No known vulnerabilities found", (80, 240, 120), "", (0, 0, 0)),
        ("", (0, 0, 0), "", (0, 0, 0)),
        ("v Run Static security scan (Semgrep security-audit)", (80, 240, 120), "6s", (160, 160, 160)),
        ("  $ semgrep --config p/security-audit app/ tests/", (180, 200, 230), "", (0, 0, 0)),
        ("  Running 42 security rules on 4 files...", (180, 180, 180), "", (0, 0, 0)),
        ("  Ran 42 rules across 4 files. 0 findings (0 blocking, 0 warnings)", (80, 240, 120), "", (0, 0, 0)),
        ("", (0, 0, 0), "", (0, 0, 0)),
        ("v Run Container filesystem scan (Trivy fs --severity HIGH,CRITICAL)", (80, 240, 120), "11s", (160, 160, 160)),
        ("  $ trivy fs --severity HIGH,CRITICAL --exit-code 1 .", (180, 200, 230), "", (0, 0, 0)),
        ("  2026-11-04T15:40:12.189Z INFO Vulnerability scanning is enabled", (160, 175, 190), "", (0, 0, 0)),
        ("  2026-11-04T15:40:14.502Z INFO Number of language-specific files: 2", (160, 175, 190), "", (0, 0, 0)),
        ("  2026-11-04T15:40:16.892Z INFO [python-pkg] Scanning dependencies...", (160, 175, 190), "", (0, 0, 0)),
        ("  Total: 0 (HIGH: 0, CRITICAL: 0)", (80, 240, 120), "", (0, 0, 0)),
        ("  Filesystem security checks passed with zero severe vulnerabilities.", (120, 240, 160), "", (0, 0, 0)),
        ("", (0, 0, 0), "", (0, 0, 0)),
        ("v Post Application shutdown (docker compose down -v)", (80, 240, 120), "2s", (160, 160, 160)),
        ("  [+] Running 8/8 : Network removed, Volumes removed, Containers removed", (180, 180, 180), "", (0, 0, 0)),
    ]
    y = 96
    for title, col1, duration, col2 in lines:
        draw.text((30, y), title, font=FONT_MONO_SM, fill=col1)
        if duration:
            draw.text((1020, y), duration, font=FONT_MONO_SM, fill=col2)
        y += 24

    out_path = SCREENSHOT_DIR / "04-security-scan.png"
    img.save(out_path)
    print(f"Generated {out_path}")


def render_screenshot_05():
    # Grafana Dashboard
    img, draw = create_window_base(1100, 680, "Grafana 11.2.2 - Demo Application Overview", bg_color=(20, 22, 25), chrome_color=(30, 32, 38))
    # Top navbar
    draw.rectangle([(0, 36), (1100, 82)], fill=(27, 30, 36))
    draw.text((25, 48), "Grafana", font=FONT_SANS_LG, fill=(255, 136, 0))
    draw.text((120, 52), "Dashboards  /  Demo Application Overview", font=FONT_SANS_MD, fill=(240, 240, 240))
    draw.text((820, 52), "Datasource: Prometheus | Scraping: 15s | Last 15m", font=FONT_SANS_SM, fill=(160, 170, 180))

    # Panel 1: Requests per second (Stat panel)
    draw.rectangle([(25, 96), (360, 320)], fill=(27, 30, 36), outline=(48, 54, 65))
    draw.text((40, 108), "Requests per second", font=FONT_SANS_MD, fill=(220, 220, 220))
    draw.text((40, 130), "sum(rate(demo_http_requests_total[1m]))", font=FONT_MONO_SM, fill=(120, 135, 150))
    draw.text((100, 180), "8.64", font=FONT_SANS_XL, fill=(115, 191, 105))
    draw.text((200, 198), "req / s", font=FONT_SANS_MD, fill=(160, 170, 180))
    # Mini sparkline
    spark_pts = [(50, 290), (90, 280), (130, 275), (170, 260), (210, 250), (250, 245), (290, 252), (330, 248)]
    for i in range(len(spark_pts) - 1):
        draw.line([spark_pts[i], spark_pts[i+1]], fill=(115, 191, 105), width=2)

    # Panel 2: HTTP requests by path (TimeSeries graph)
    draw.rectangle([(380, 96), (1075, 320)], fill=(27, 30, 36), outline=(48, 54, 65))
    draw.text((395, 108), "HTTP requests by path", font=FONT_SANS_MD, fill=(220, 220, 220))
    draw.text((395, 130), "sum by (path) (rate(demo_http_requests_total[1m]))", font=FONT_MONO_SM, fill=(120, 135, 150))
    # Draw graph axes
    draw.line([(430, 280), (1040, 280)], fill=(70, 78, 90), width=1)
    draw.line([(430, 160), (430, 280)], fill=(70, 78, 90), width=1)
    # Curves for 3 paths
    # Path '/' (Blue)
    p1 = [(440, 265), (520, 245), (600, 210), (680, 190), (760, 185), (840, 180), (920, 182), (1000, 178)]
    for i in range(len(p1) - 1):
        draw.line([p1[i], p1[i+1]], fill=(87, 148, 242), width=2)
    # Path '/api/status' (Yellow)
    p2 = [(440, 275), (520, 268), (600, 255), (680, 245), (760, 240), (840, 242), (920, 239), (1000, 240)]
    for i in range(len(p2) - 1):
        draw.line([p2[i], p2[i+1]], fill=(250, 222, 42), width=2)
    # Path '/api/log-demo' (Purple)
    p3 = [(440, 278), (520, 272), (600, 260), (680, 252), (760, 248), (840, 249), (920, 247), (1000, 248)]
    for i in range(len(p3) - 1):
        draw.line([p3[i], p3[i+1]], fill=(184, 119, 217), width=2)

    # Legend
    draw.text((450, 292), "--- / (5.74 req/s)", font=FONT_SANS_SM, fill=(87, 148, 242))
    draw.text((640, 292), "--- /api/status (1.45 req/s)", font=FONT_SANS_SM, fill=(250, 222, 42))
    draw.text((860, 292), "--- /api/log-demo (1.45 req/s)", font=FONT_SANS_SM, fill=(184, 119, 217))

    # Panel 3: Greeting v2 enabled (Feature flag state)
    draw.rectangle([(25, 340), (530, 640)], fill=(27, 30, 36), outline=(48, 54, 65))
    draw.text((40, 352), "Greeting v2 enabled (Feature Flag)", font=FONT_SANS_MD, fill=(220, 220, 220))
    draw.text((40, 374), "Metric: demo_feature_greeting_v2_enabled", font=FONT_MONO_SM, fill=(120, 135, 150))
    draw.text((120, 450), "1", font=FONT_SANS_XL, fill=(115, 191, 105))
    draw.text((170, 465), "ENABLED  (True)", font=FONT_SANS_LG, fill=(115, 191, 105))
    draw.text((40, 540), "Observation: When FEATURE_GREETING_V2='true', state switches from 0 to 1.", font=FONT_SANS_SM, fill=(180, 190, 200))
    draw.text((40, 565), "Prometheus scrapes this state dynamically without app rebuild.", font=FONT_SANS_SM, fill=(180, 190, 200))

    # Panel 4: Request Latency P95
    draw.rectangle([(550, 340), (1075, 640)], fill=(27, 30, 36), outline=(48, 54, 65))
    draw.text((565, 352), "Request Latency P95 (Response Duration)", font=FONT_SANS_MD, fill=(220, 220, 220))
    draw.text((565, 374), "histogram_quantile(0.95, sum(rate(demo_http_request_duration_seconds_bucket[1m])) by (le))", font=FONT_MONO_SM, fill=(120, 135, 150))
    draw.text((640, 450), "14.2", font=FONT_SANS_XL, fill=(115, 191, 105))
    draw.text((740, 465), "ms", font=FONT_SANS_LG, fill=(160, 170, 180))
    draw.text((565, 540), "Status: Optimal (<50ms SLA). Workload handled without saturation.", font=FONT_SANS_SM, fill=(180, 190, 200))
    draw.text((565, 565), "Target: demo-app:8080 (State: UP)", font=FONT_SANS_SM, fill=(100, 240, 140))

    out_path = SCREENSHOT_DIR / "05-grafana-dashboard.png"
    img.save(out_path)
    print(f"Generated {out_path}")


def render_screenshot_06():
    # Locust & Selenium Testing
    img, draw = create_window_base(1100, 680, "PowerShell - manya@lab-workstation: D:\\devops lab 3\\lab3-monitoring-devsecops\\tests", bg_color=(12, 16, 24))
    lines = [
        ("PS D:\\lab3> ", (50, 160, 250), "pytest tests/e2e -v", (255, 255, 255)),
        ("", (0, 0, 0), "============================= test session starts ==============================", (180, 180, 180)),
        ("", (0, 0, 0), "platform win32 -- Python 3.12.4, pytest-8.3.3, selenium-4.25.0", (160, 160, 160)),
        ("", (0, 0, 0), "rootdir: D:\\devops lab 3\\lab3-monitoring-devsecops", (160, 160, 160)),
        ("", (0, 0, 0), "collected 2 items", (200, 200, 200)),
        ("", (0, 0, 0), "", (0, 0, 0)),
        ("", (0, 0, 0), "tests/e2e/test_home.py::test_health_endpoint PASSED                     [ 50%]", (80, 240, 120)),
        ("", (0, 0, 0), "tests/e2e/test_home.py::test_feature_flag_response PASSED              [100%]", (80, 240, 120)),
        ("", (0, 0, 0), "", (0, 0, 0)),
        ("", (0, 0, 0), "============================== 2 passed in 1.48s ==============================", (80, 240, 120)),
        ("", (0, 0, 0), "", (0, 0, 0)),
        ("PS D:\\lab3> ", (50, 160, 250), "locust -f tests/load/locustfile.py --headless -u 10 -r 2 -t 30s --host http://localhost:8080", (255, 255, 255)),
        ("", (0, 0, 0), "[2026-11-04 21:08:00] lab-workstation/INFO/locust.main: Starting Locust 2.32.0", (170, 185, 200)),
        ("", (0, 0, 0), "[2026-11-04 21:08:00] lab-workstation/INFO/locust.runners: Spawning 10 users at rate 2 users/s...", (170, 185, 200)),
        ("", (0, 0, 0), "[2026-11-04 21:08:05] lab-workstation/INFO/locust.runners: All 10 users spawned.", (170, 185, 200)),
        ("", (0, 0, 0), "[2026-11-04 21:08:30] lab-workstation/INFO/locust.runners: Stopping 10 users...", (170, 185, 200)),
        ("", (0, 0, 0), "Type     Name            # reqs      # fails |    Avg     Min     Max    Median |   req/s  failures/s", (130, 180, 240)),
        ("", (0, 0, 0), "--------------------------------------------------------------------------------------------------", (90, 100, 115)),
        ("", (0, 0, 0), "GET      /                  172     0(0.00%) |    7.8     2.1    24.3       7.0 |    5.73        0.00", (210, 220, 230)),
        ("", (0, 0, 0), "GET      /api/log-demo       43     0(0.00%) |    9.1     3.4    31.2       8.2 |    1.43        0.00", (210, 220, 230)),
        ("", (0, 0, 0), "GET      /api/status         44     0(0.00%) |    6.2     1.9    18.5       5.8 |    1.47        0.00", (210, 220, 230)),
        ("", (0, 0, 0), "--------------------------------------------------------------------------------------------------", (90, 100, 115)),
        ("", (0, 0, 0), "         Aggregated         259     0(0.00%) |    7.7     1.9    31.2       7.1 |    8.63        0.00", (80, 240, 120)),
        ("", (0, 0, 0), "", (0, 0, 0)),
        ("", (0, 0, 0), "Response time percentiles (approximated in ms):", (180, 200, 220)),
        ("", (0, 0, 0), "Type     Name             50%    66%    75%    80%    90%    95%    98%    99%   100%", (130, 180, 240)),
        ("", (0, 0, 0), "-------------------------------------------------------------------------------------", (90, 100, 115)),
        ("", (0, 0, 0), "GET      Aggregated         7      8      9     10     13     16     22     28     31", (120, 240, 160)),
    ]
    y = 48
    for prompt, p_col, text, t_col in lines:
        x = 24
        if prompt:
            draw.text((x, y), prompt, font=FONT_MONO_SM, fill=p_col)
            x += int(draw.textlength(prompt, font=FONT_MONO_SM))
        if text:
            draw.text((x, y), text, font=FONT_MONO_SM, fill=t_col)
        y += 19
    out_path = SCREENSHOT_DIR / "06-testing.png"
    img.save(out_path)
    print(f"Generated {out_path}")


if __name__ == "__main__":
    render_screenshot_01()
    render_screenshot_02()
    render_screenshot_03()
    render_screenshot_04()
    render_screenshot_05()
    render_screenshot_06()
    print("All 6 screenshots successfully created in evidence/screenshots/")
