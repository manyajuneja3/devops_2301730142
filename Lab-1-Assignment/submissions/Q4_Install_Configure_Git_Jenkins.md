# Question 4: Install and Configure Git and Jenkins on Ubuntu Linux

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
