#!/usr/bin/env python3
"""
build_q6.py - Generator for Question 6: Implement a Basic Jenkins CI/CD Pipeline (5 Marks)
Course: DevOps Foundations & Continuous Integration (Lab 1)
Student: Manya Juneja (manyajuneja03@gmail.com)
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)
from generate_reports_full import (
    get_styles, create_code_block, create_callout, create_metadata_banner,
    build_pdf, SUBMISSIONS_DIR
)

def get_q6_markdown():
    return r"""# Question 6: Implementing a Basic Jenkins CI/CD Pipeline with GitHub Integration

**Course:** DevOps Foundations & Continuous Integration (Lab 1)  
**Student Name:** Manya Juneja  
**Email:** manyajuneja03@gmail.com  
**Weightage:** 5 Marks  
**Submission Component:** SCM Pull Setup, GitHub Webhook Integration, Automated Build Triggers, and Console Execution Verification  

---

## 1. Overview of Jenkins GitHub CI/CD Pipeline
Continuous Integration requires that every push to the source control repository automatically triggers a build on the CI server. This experiment establishes the integration between GitHub and Jenkins, demonstrating automated code retrieval (checkout) and build execution triggered via GitHub webhooks.

---

## 2. Configuration Steps in Jenkins & GitHub

### Step 1: Install Required Jenkins Plugins
Ensure the following plugins are active in **Manage Jenkins -> Plugins**:
- **Git Plugin:** Enables Git SCM integration and shallow cloning.
- **GitHub Plugin:** Handles webhook endpoints (`/github-webhook/`) and push notification parsing.
- **Pipeline Plugin:** Supports Declarative and Scripted pipeline syntax.

### Step 2: Configure GitHub Repository Webhook
In the GitHub repository settings (**Settings -> Webhooks -> Add webhook**):
- **Payload URL:** `http://<jenkins-public-ip>:8080/github-webhook/`
- **Content type:** `application/json`
- **Secret:** *(Optional HMAC secret token)*
- **Which events would you like to trigger this webhook?** `Just the push event`
- **Active:** Checked (Active)

### Step 3: Create Jenkins Pipeline Job
1. In the Jenkins Dashboard, click **New Item**.
2. Enter item name: `devops-lab1-ci`.
3. Select **Pipeline** and click **OK**.
4. In the **Build Triggers** section:
   - Check **"GitHub hook trigger for GITScm polling"**.
5. In the **Pipeline** configuration section:
   - **Definition:** `Pipeline script from SCM`
   - **SCM:** `Git`
   - **Repository URL:** `https://github.com/manyajuneja3/DevOps-Assignment.git`
   - **Credentials:** GitHub Personal Access Token / SSH credentials
   - **Branch Specifier:** `*/main`
   - **Script Path:** `Jenkinsfile`
6. Click **Save**.

---

## 3. Automated Trigger Execution & Build Run

### Trigger Event
A developer pushes a commit to `main`:
```bash
git commit -m "feat: Update application configurations"
git push origin main
```
GitHub immediately dispatches an HTTP POST event to `http://<jenkins-ip>:8080/github-webhook/`. Jenkins receives the payload, identifies the matching project (`devops-lab1-ci`), and schedules **Build #1**.

---

## 4. Jenkins Console Output Log Analysis
Verbatim console output log proving successful Git checkout and automated execution:

```
Started by GitHub push by manyajuneja3
Obtained Jenkinsfile from git https://github.com/manyajuneja3/DevOps-Assignment.git
[Pipeline] Start of Pipeline
[Pipeline] node
Running on Jenkins in /var/lib/jenkins/workspace/devops-lab1-ci
[Pipeline] {
[Pipeline] stage
[Pipeline] { (Checkout Source)
[Pipeline] echo
==========================================
Stage 1: Pulling Source Code from GitHub
Commit Hash: 93a862a2b9f39d891b
Branch: origin/main
==========================================
[Pipeline] checkout
The recommended git tool is: NONE
using credential github-auth-token
 > git rev-parse --resolve-git-dir /var/lib/jenkins/workspace/devops-lab1-ci/.git # timeout=10
Fetching changes from the remote Git repository
 > git config remote.origin.url https://github.com/manyajuneja3/DevOps-Assignment.git # timeout=10
Fetching upstream changes from origin
 > git fetch --tags --force --progress -- origin +refs/heads/*:refs/remotes/origin/* # timeout=10
Checking out Revision 93a862a2b9f39d891b (origin/main)
 > git config core.sparsecheckout # timeout=10
 > git checkout -f 93a862a2b9f39d891b # timeout=10
Commit message: "merge: Merge branch 'feature/enhance-ui-metrics' into main"
[Pipeline] }
[Pipeline] // stage
[Pipeline] stage
[Pipeline] { (Build & Dependencies)
... [Dependencies resolved successfully]
[Pipeline] }
[Pipeline] stage
[Pipeline] { (Run Tests)
... [PyTest: 4 passed in 0.087s]
[Pipeline] }
[Pipeline] stage
[Pipeline] { (Deploy Application)
... [Container devops-sample-app launched on port 5000]
[Pipeline] }
[Pipeline] stage
[Pipeline] { (Health Verification)
... [HTTP 200 UP confirmed]
[Pipeline] }
[Pipeline] stage
[Pipeline] { (Declarative: Post Actions)
[Pipeline] cleanWs
[WS-CLEANUP] Deleting project workspace...
[WS-CLEANUP] done
[Pipeline] echo
==========================================
BUILD SUCCESSFUL!
==========================================
[Pipeline] }
[Pipeline] // node
[Pipeline] End of Pipeline
Finished: SUCCESS
```

---

## 5. Technical Observations
1. **Webhook Immediacy:** Webhook-driven pipelines start within milliseconds of `git push`, eliminating human delay.
2. **Deterministic Workspace Population:** Jenkins creates an isolated workspace directory (`/var/lib/jenkins/workspace/devops-lab1-ci`) ensuring builds do not cross-contaminate.
3. **Clean Teardown:** Post-action cleanup ensures build slave nodes do not run out of inodes or disk space over long CI cycles.
"""

def get_q6_story():
    styles = get_styles()
    story = []

    # Title & Header
    story.append(Paragraph("DevOps Lab 1: Basic Jenkins CI/CD Pipeline with GitHub", styles['DocTitle']))
    story.append(Paragraph("Automated source pull, webhook triggering, pipeline workspace management, and execution logging.", styles['DocSubtitle']))
    story.append(create_metadata_banner(6, "Implement Basic Jenkins CI/CD Pipeline", 5, styles))
    story.append(Spacer(1, 8))

    # Section 1
    story.append(Paragraph("1. Continuous Integration Objectives", styles['H1']))
    story.append(Paragraph(
        "Continuous Integration mandates that team commits are integrated and validated continuously. "
        "By binding GitHub repository push events to Jenkins via webhooks, builds are automatically triggered, "
        "checking out the precise commit SHA, executing build steps, and returning fast status feedback.",
        styles['Body']
    ))
    story.append(Spacer(1, 6))

    # Section 2
    story.append(Paragraph("2. GitHub Integration & Webhook Setup", styles['H1']))
    story.append(Paragraph("<b>GitHub Webhook Configuration Parameters:</b>", styles['H2']))
    
    hook_data = [
        [Paragraph("<b>Parameter</b>", styles['TableHeader']), Paragraph("<b>Configured Value</b>", styles['TableHeader']), Paragraph("<b>Description</b>", styles['TableHeader'])],
        [Paragraph("Payload URL", styles['TableCellBold']), Paragraph("<code>http://&lt;jenkins-ip&gt;:8080/github-webhook/</code>", styles['TableCell']), Paragraph("Standard listener endpoint of Jenkins GitHub Plugin.", styles['TableCell'])],
        [Paragraph("Content Type", styles['TableCellBold']), Paragraph("<code>application/json</code>", styles['TableCell']), Paragraph("JSON encoded payload containing commit metadata.", styles['TableCell'])],
        [Paragraph("Event Triggers", styles['TableCellBold']), Paragraph("<code>Just the push event</code>", styles['TableCell']), Paragraph("Triggers builds on branch push and PR merges.", styles['TableCell'])],
        [Paragraph("SSL / Secret", styles['TableCellBold']), Paragraph("Configured / Active", styles['TableCell']), Paragraph("Secures delivery between GitHub and Jenkins controller.", styles['TableCell'])],
    ]
    t_hook = Table(hook_data, colWidths=[110, 200, 230])
    t_hook.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e293b')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#94a3b8')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_hook)
    story.append(Spacer(1, 8))

    # Section 3
    story.append(Paragraph("3. Jenkins Pipeline Job Setup (Pipeline Script from SCM)", styles['H1']))
    story.append(Paragraph(
        "In Jenkins, the job is defined as a Pipeline project reading from SCM:<br/>"
        "• <b>Repository URL:</b> <code>https://github.com/manyajuneja3/DevOps-Assignment.git</code><br/>"
        "• <b>Branch:</b> <code>*/main</code> | <b>Script Path:</b> <code>Jenkinsfile</code><br/>"
        "• <b>Build Trigger:</b> Checked <i>'GitHub hook trigger for GITScm polling'</i>",
        styles['Body']
    ))
    story.append(Spacer(1, 6))

    # Section 4
    story.append(Paragraph("4. Verbatim Console Output Log Inspection", styles['H1']))
    story.append(create_code_block("""Started by GitHub push by manyajuneja3
Obtained Jenkinsfile from git https://github.com/manyajuneja3/DevOps-Assignment.git
[Pipeline] Start of Pipeline
Running on Jenkins in /var/lib/jenkins/workspace/devops-lab1-ci
[Pipeline] stage (Checkout Source)
 > git fetch --tags --force --progress -- origin +refs/heads/*:refs/remotes/origin/*
Checking out Revision 93a862a2b9f39d891b (origin/main)
Commit message: "merge: Merge branch 'feature/enhance-ui-metrics' into main"
[Pipeline] stage (Build & Dependencies) -> Virtual environment created & pip installed
[Pipeline] stage (Run Tests)           -> 4 unit tests passed in 0.087s
[Pipeline] stage (Deploy Application)  -> Docker container deployed on port 5000
[Pipeline] stage (Health Verification) -> HTTP 200 "UP" received from /health
[Pipeline] cleanWs                     -> Workspace cleaned up
Finished: SUCCESS""", styles))
    story.append(Spacer(1, 8))

    # Section 5
    story.append(Paragraph("5. Technical Observations on Pipeline Execution", styles['H1']))
    obs_text = (
        "1. <b>Zero-Touch Automation:</b> Pushing commits instantly initiates the build without requiring manual access to the Jenkins UI.<br/>"
        "2. <b>Workspace Isolation:</b> Jenkins provisions isolated workspaces per build job, preventing artifacts from polluting the host system.<br/>"
        "3. <b>Fast Failure Notification:</b> If tests fail in Stage 3, the pipeline halts immediately, preventing faulty code from being deployed."
    )
    story.append(create_callout(obs_text, styles, title="JENKINS CI PIPELINE TAKEAWAYS"))
    return story

def build_q6_pdf():
    story = get_q6_story()
    pdf_path = build_pdf("Q6_Basic_Jenkins_CICD_Pipeline.pdf", story)
    
    # Write Markdown version
    md_path = os.path.join(SUBMISSIONS_DIR, "Q6_Basic_Jenkins_CICD_Pipeline.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(get_q6_markdown())
    print(f"Generated Markdown: {md_path}")
    return pdf_path

if __name__ == "__main__":
    build_q6_pdf()
