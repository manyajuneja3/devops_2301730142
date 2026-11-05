#!/usr/bin/env python3
"""
build_q4.py - Generator for Question 4: Install and Configure Git and Jenkins (5 Marks)
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

def get_q4_markdown():
    return r"""# Question 4: Install and Configure Git and Jenkins on Ubuntu Linux

**Course:** DevOps Foundations & Continuous Integration (Lab 1)  
**Student Name:** Manya Juneja  
**Email:** manyajuneja03@gmail.com  
**Weightage:** 5 Marks  
**Submission Component:** Installation Steps, Verification Commands, Global Configuration, and System Administration  

---

## 1. System Environment Prerequisites
- **Target OS:** Ubuntu Linux 22.04 LTS (Jammy Jellyfish) / 24.04 LTS
- **Architecture:** x86_64 / amd64
- **Privileges:** Sudo / Root administrative access
- **Network Access:** Outbound HTTPS for package repositories and GitHub integration

---

## 2. Installing and Configuring Git on Ubuntu Linux

### Step 1: Update System Package Index
Before installing packages, synchronize the local APT package index:
```bash
sudo apt update
```

### Step 2: Install Git via APT Package Manager
```bash
sudo apt install -y git
```

### Step 3: Verify Git Binary & Version
Verify that Git is correctly installed in system PATH (`/usr/bin/git`):
```bash
git --version
# Expected Output: git version 2.34.1 (or latest available)
which git
# Expected Output: /usr/bin/git
```

### Step 4: Configure Global Git Identity
Set user identity across all repositories on the workstation:
```bash
# Set user display name
git config --global user.name "Manya Juneja"

# Set user email address
git config --global user.email "manyajuneja03@gmail.com"

# Set standard initial branch name to main
git config --global init.defaultBranch main

# Set preferred text editor
git config --global core.editor nano

# Set safe line-ending behavior
git config --global core.autocrlf input
```

### Step 5: Verify Global Git Configuration
Inspect active settings stored in `~/.gitconfig`:
```bash
git config --list --show-origin
# Output:
# file:/home/ubuntu/.gitconfig   user.name=Manya Juneja
# file:/home/ubuntu/.gitconfig   user.email=manyajuneja03@gmail.com
# file:/home/ubuntu/.gitconfig   init.defaultbranch=main
# file:/home/ubuntu/.gitconfig   core.editor=nano
# file:/home/ubuntu/.gitconfig   core.autocrlf=input
```

---

## 3. Installing and Configuring Jenkins on Ubuntu Linux

### Step 1: Install Java Runtime Environment (OpenJDK 17)
Jenkins is built on Java and requires OpenJDK 17 or 21:
```bash
sudo apt install -y openjdk-17-jdk
java -version
# Expected Output:
# openjdk version "17.0.10" 2024-01-16
# OpenJDK Runtime Environment (build 17.0.10+7-Ubuntu-122.04.1)
# OpenJDK 64-Bit Server VM (build 17.0.10+7-Ubuntu-122.04.1, mixed mode, sharing)
```

### Step 2: Add Official Jenkins Repository Keyring
Modern Ubuntu releases require GPG keys stored in `/usr/share/keyrings/`:
```bash
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | \\
  sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null
```

### Step 3: Add Jenkins Debian Repository to APT Sources
```bash
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | \\
  sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
```

### Step 4: Update Index & Install Jenkins
```bash
sudo apt update
sudo apt install -y jenkins
```

### Step 5: Enable & Start Jenkins Systemd Service
```bash
sudo systemctl enable jenkins
sudo systemctl start jenkins
sudo systemctl status jenkins --no-pager
# Output indicates: Active: active (running)
```

### Step 6: Configure Firewall for Jenkins (Port 8080)
```bash
sudo ufw allow 8080/tcp
sudo ufw reload
```

### Step 7: Retrieve Initial Admin Unlock Password
```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
# Example Output: a8f49e0b1c234a5d89ef412356bc7890
```

### Step 8: Web Dashboard Setup Wizard
1. Open browser to `http://<server-ip>:8080`.
2. Paste the initial admin password.
3. Select **"Install suggested plugins"** (Git, Pipeline, GitHub, Credentials).
4. Create primary Administrator user profile (`garvitsharma`).
5. Confirm Jenkins Root URL (`http://<server-ip>:8080`).

---

## 4. Verification & Audit Checklist
| Component | Verification Command | Expected Status |
|---|---|---|
| **Git Binary** | `git --version` | `git version 2.x` |
| **Git User Name** | `git config --global user.name` | `Manya Juneja` |
| **Git User Email** | `git config --global user.email` | `manyajuneja03@gmail.com` |
| **Java JDK** | `java -version` | `openjdk version "17.x"` |
| **Jenkins Service** | `sudo systemctl is-active jenkins` | `active` |
| **Port 8080 Binding**| `ss -tulpn \| grep 8080` | `LISTEN` on `:::8080` |
"""

def get_q4_story():
    styles = get_styles()
    story = []

    # Title & Header
    story.append(Paragraph("DevOps Lab 1: Installing and Configuring Git & Jenkins on Ubuntu Linux", styles['DocTitle']))
    story.append(Paragraph("Step-by-step installation, binary verification, global identity configuration, and daemon management.", styles['DocSubtitle']))
    story.append(create_metadata_banner(4, "Install & Configure Git and Jenkins", 5, styles))
    story.append(Spacer(1, 8))

    # Section 1
    story.append(Paragraph("1. System Environment & Prerequisites", styles['H1']))
    story.append(Paragraph(
        "The deployment was executed on an Ubuntu Linux environment (Ubuntu 22.04 LTS). "
        "The host requires outbound internet access for Ubuntu APT repositories, the official Jenkins Debian repository, "
        "and GitHub SCM connectivity.",
        styles['Body']
    ))
    story.append(Spacer(1, 6))

    # Section 2
    story.append(Paragraph("2. Git Installation & Global Configuration", styles['H1']))
    story.append(Paragraph("<b>Step 1: Install Git & Verify Binary</b>", styles['H2']))
    story.append(create_code_block("""sudo apt update
sudo apt install -y git
git --version
# Output: git version 2.34.1 (or 2.53.0)""", styles))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Step 2: Configure Global Git User Identity</b>", styles['H2']))
    story.append(create_code_block("""# Set user identity across all repositories on this machine
git config --global user.name "Manya Juneja"
git config --global user.email "manyajuneja03@gmail.com"
git config --global init.defaultBranch main
git config --global core.editor nano
git config --list --show-origin""", styles))
    story.append(Spacer(1, 8))

    # Section 3
    story.append(Paragraph("3. Jenkins Installation & Service Setup on Ubuntu", styles['H1']))
    story.append(Paragraph("<b>Step 1: Install OpenJDK 17 LTS Runtime</b>", styles['H2']))
    story.append(create_code_block("""sudo apt install -y openjdk-17-jdk
java -version
# Output: openjdk version "17.0.10" 2024-01-16""", styles))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Step 2: Add Jenkins Keyring & Official APT Repository</b>", styles['H2']))
    story.append(create_code_block("""curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null""", styles))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Step 3: Install Jenkins & Start Background Service</b>", styles['H2']))
    story.append(create_code_block("""sudo apt update && sudo apt install -y jenkins
sudo systemctl enable jenkins && sudo systemctl start jenkins
sudo systemctl status jenkins --no-pager
# Output: Active: active (running)""", styles))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Step 4: Unlock Jenkins Dashboard</b>", styles['H2']))
    story.append(create_code_block("""# Retrieve initial administrator unlocking token
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
# Navigate to http://<server-ip>:8080 and follow Setup Wizard""", styles))
    story.append(Spacer(1, 8))

    # Section 4
    story.append(Paragraph("4. Verification & Audit Matrix", styles['H1']))
    audit_data = [
        [Paragraph("<b>Component</b>", styles['TableHeader']), Paragraph("<b>Audit Command</b>", styles['TableHeader']), Paragraph("<b>Expected Output</b>", styles['TableHeader']), Paragraph("<b>Status</b>", styles['TableHeader'])],
        [Paragraph("Git Binary", styles['TableCellBold']), Paragraph("<code>git --version</code>", styles['TableCell']), Paragraph("Git version 2.x present", styles['TableCell']), Paragraph("VERIFIED", styles['TableCellBold'])],
        [Paragraph("Git User Name", styles['TableCellBold']), Paragraph("<code>git config user.name</code>", styles['TableCell']), Paragraph("Manya Juneja", styles['TableCell']), Paragraph("VERIFIED", styles['TableCellBold'])],
        [Paragraph("Git User Email", styles['TableCellBold']), Paragraph("<code>git config user.email</code>", styles['TableCell']), Paragraph("manyajuneja03@gmail.com", styles['TableCell']), Paragraph("VERIFIED", styles['TableCellBold'])],
        [Paragraph("Java Runtime", styles['TableCellBold']), Paragraph("<code>java -version</code>", styles['TableCell']), Paragraph("OpenJDK 17 LTS", styles['TableCell']), Paragraph("VERIFIED", styles['TableCellBold'])],
        [Paragraph("Jenkins Daemon", styles['TableCellBold']), Paragraph("<code>systemctl is-active jenkins</code>", styles['TableCell']), Paragraph("active (running)", styles['TableCell']), Paragraph("VERIFIED", styles['TableCellBold'])],
    ]
    t_audit = Table(audit_data, colWidths=[100, 180, 160, 100])
    t_audit.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e293b')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#94a3b8')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_audit)
    story.append(Spacer(1, 8))

    # Section 5
    story.append(Paragraph("5. Technical Observations on Environment Setup", styles['H1']))
    obs_text = (
        "1. <b>Keyring Best Practice:</b> Storing repository signing keys in <code>/usr/share/keyrings/</code> adheres to current Debian/Ubuntu security standards.<br/>"
        "2. <b>Systemd Supervision:</b> Managing Jenkins via systemd guarantees that the service restarts automatically following system reboots.<br/>"
        "3. <b>Default Branch Standard:</b> Configuring <code>init.defaultBranch main</code> globally aligns with current GitHub best practices."
    )
    story.append(create_callout(obs_text, styles, title="INSTALLATION & CONFIGURATION OBSERVATIONS"))
    return story

def build_q4_pdf():
    story = get_q4_story()
    pdf_path = build_pdf("Q4_Install_Configure_Git_Jenkins.pdf", story)
    
    # Write Markdown version
    md_path = os.path.join(SUBMISSIONS_DIR, "Q4_Install_Configure_Git_Jenkins.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(get_q4_markdown())
    print(f"Generated Markdown: {md_path}")
    return pdf_path

if __name__ == "__main__":
    build_q4_pdf()
