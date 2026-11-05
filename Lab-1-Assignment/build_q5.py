#!/usr/bin/env python3
"""
build_q5.py - Generator for Question 5: Set Up Version Control Using Git (5 Marks)
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

def get_q5_markdown():
    return r"""# Question 5: Version Control Setup, Branching, Merging & GitHub Integration

**Course:** DevOps Foundations & Continuous Integration (Lab 1)  
**Student Name:** Manya Juneja  
**Email:** manyajuneja03@gmail.com  
**Weightage:** 5 Marks  
**Submission Component:** Git Repository Initialization, Staging, Commit History, Branching, Non-Fast-Forward Merge, and Remote GitHub Push  

---

## 1. Overview of Version Control in DevOps
Distributed Version Control Systems (DVCS) like Git provide the single source of truth for all source code, automation scripts, and configuration-as-code manifests. This report demonstrates the complete Git lifecycle executed in Lab 1: repository initialization, file staging, semantic committing, isolated feature branching, non-fast-forward merging, and publishing to a GitHub remote.

---

## 2. Step-by-Step Version Control Execution

### Step 1: Initialize Git Repository
```bash
# Navigate to workspace and initialize repository with root branch named 'main'
cd "d:\Devops lab 1"
git init -b main
# Output: Initialized empty Git repository in D:/Devops lab 1/.git/
```

### Step 2: Author Application Code & Inspect Working Tree
Application assets were created:
- `app.py`: Flask application with `/`, `/health`, and `/api/info` endpoints.
- `test_app.py`: PyTest unit test suite.
- `requirements.txt`: Python package dependencies.
- `Dockerfile`: Multi-stage container packaging definition.
- `deploy.sh`: Automated deployment shell script.
- `Jenkinsfile`: Declarative CI/CD pipeline definition.
- `.gitignore`: Excludes bytecaches, virtual environments, and log files.
- `README.md`: Architecture overview and execution guide.

```bash
git status
# Shows untracked files ready for staging
```

### Step 3: Stage and Commit Initial Codebase
```bash
git add .
git commit -m "feat: Initial commit of DevOps Lab 1 application and CI/CD pipeline"
# Output:
# [main (root-commit) fb5fb47] feat: Initial commit of DevOps Lab 1 application and CI/CD pipeline
#  8 files changed, 551 insertions(+)
#  create mode 100644 .gitignore
#  create mode 100644 Dockerfile
#  create mode 100644 Jenkinsfile
#  create mode 100644 README.md
#  create mode 100644 app.py
#  create mode 100644 deploy.sh
#  create mode 100644 requirements.txt
#  create mode 100644 test_app.py
```

### Step 4: Branching Strategy & Feature Development
To adhere to DevOps best practices, direct commits to `main` are restricted during active feature development. A feature branch was created:
```bash
git checkout -b feature/enhance-ui-metrics
# Output: Switched to a new branch 'feature/enhance-ui-metrics'
```
On this branch, a `/metrics` endpoint was added to `app.py`, and corresponding unit tests were added to `test_app.py`.
```bash
git add app.py test_app.py
git commit -m "feat(metrics): add /metrics monitoring endpoint and test coverage"
# Output:
# [feature/enhance-ui-metrics 1a63744] feat(metrics): add /metrics monitoring endpoint and test coverage
#  2 files changed, 17 insertions(+)
```

### Step 5: Merging Feature Branch into Main
To maintain branch provenance and auditability in CI/CD, the merge was executed using `--no-ff` (no fast-forward):
```bash
git checkout main
git merge --no-ff feature/enhance-ui-metrics -m "merge: Merge branch 'feature/enhance-ui-metrics' into main"
# Output:
# Merge made by the 'ort' strategy.
#  app.py      | 9 +++++++++
#  test_app.py | 8 ++++++++
#  2 files changed, 17 insertions(+)
```

### Step 6: GitHub Remote Configuration & Push
```bash
# Add GitHub remote origin
git remote add origin https://github.com/manyajuneja3/DevOps-Assignment.git

# Push main branch with upstream tracking
git push -u origin main

# Push feature branch for pull request traceability
git push -u origin feature/enhance-ui-metrics
```

---

## 3. Git Commit History & Topological Graph
Execution of `git log --graph --oneline --all --decorate`:

```
*   93a862a (HEAD -> main) merge: Merge branch 'feature/enhance-ui-metrics' into main
|\  
| * 1a63744 (feature/enhance-ui-metrics) feat(metrics): add /metrics monitoring endpoint and test coverage
|/  
* fb5fb47 feat: Initial commit of DevOps Lab 1 application and CI/CD pipeline
```

---

## 4. Technical Observations
1. **Branch Protection:** Developing on `feature/*` branches isolates unstable experimental code from breaking the CI/CD pipeline monitoring `main`.
2. **Explicit Merge Commits (`--no-ff`):** Fast-forward merges collapse branch history into a single linear timeline. Using `--no-ff` records the exact merge commit and enables one-command rollbacks (`git revert -m 1 <merge-commit-hash>`).
3. **Semantic Commit Messages:** Following the conventional commit specification (`feat:`, `fix:`, `merge:`) enables automated changelog generation and automated semantic version bumping.
"""

def get_q5_story():
    styles = get_styles()
    story = []

    # Title & Header
    story.append(Paragraph("DevOps Lab 1: Version Control Setup, Branching & GitHub Integration", styles['DocTitle']))
    story.append(Paragraph("Repository initialization, staging, committing, branch management, merging, and remote synchronization.", styles['DocSubtitle']))
    story.append(create_metadata_banner(5, "Set Up Version Control Using Git", 5, styles))
    story.append(Spacer(1, 8))

    # Section 1
    story.append(Paragraph("1. Version Control Fundamentals in DevOps", styles['H1']))
    story.append(Paragraph(
        "Version control represents the single source of truth in modern DevOps workflows. "
        "Every change to application code, Dockerfiles, and Jenkinsfiles must be versioned, reviewed, "
        "and merged through controlled branch workflows before triggering automated CI/CD builds.",
        styles['Body']
    ))
    story.append(Spacer(1, 6))

    # Section 2
    story.append(Paragraph("2. Step-by-Step Git Operations", styles['H1']))
    story.append(Paragraph("<b>Step 1: Initialize Repository & Initial Commit</b>", styles['H2']))
    story.append(create_code_block("""git init -b main
git add .
git commit -m "feat: Initial commit of DevOps Lab 1 application and CI/CD pipeline"
# Commit fb5fb47 created with 8 files and 551 insertions""", styles))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Step 2: Feature Branching & Development</b>", styles['H2']))
    story.append(create_code_block("""# Create and switch to isolated feature branch
git checkout -b feature/enhance-ui-metrics
# Added /metrics monitoring endpoint and unit tests
git add app.py test_app.py
git commit -m "feat(metrics): add /metrics monitoring endpoint and test coverage"
# Commit 1a63744 created on branch feature/enhance-ui-metrics""", styles))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Step 3: Non-Fast-Forward Merge into Main</b>", styles['H2']))
    story.append(create_code_block("""git checkout main
git merge --no-ff feature/enhance-ui-metrics -m "merge: Merge branch 'feature/enhance-ui-metrics' into main"
# Commit 93a862a generated uniting branches via 'ort' merge strategy""", styles))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Step 4: Push to Remote GitHub Repository</b>", styles['H2']))
    story.append(create_code_block("""git remote add origin https://github.com/manyajuneja3/DevOps-Assignment.git
git push -u origin main
git push -u origin feature/enhance-ui-metrics""", styles))
    story.append(Spacer(1, 8))

    # Section 3
    story.append(Paragraph("3. Verified Commit Topology Graph", styles['H1']))
    story.append(Paragraph("The exact commit tree structure confirmed via <code>git log --graph --oneline --all --decorate</code>:", styles['Body']))
    story.append(create_code_block("""*   93a862a (HEAD -> main) merge: Merge branch 'feature/enhance-ui-metrics' into main
|\\  
| * 1a63744 (feature/enhance-ui-metrics) feat(metrics): add /metrics monitoring endpoint and test coverage
|/  
* fb5fb47 feat: Initial commit of DevOps Lab 1 application and CI/CD pipeline""", styles))
    story.append(Spacer(1, 8))

    # Section 4
    story.append(Paragraph("4. Technical Observations on Git Workflows", styles['H1']))
    obs_text = (
        "1. <b>Preserving Branch History:</b> The `--no-ff` flag prevents fast-forward collapsing, preserving evidence of feature work and code reviews.<br/>"
        "2. <b>Atomic Commits:</b> Commits are segregated into distinct logical changes (`feat`, `feat(metrics)`, `merge`), simplifying debugging.<br/>"
        "3. <b>Multi-Branch Traceability:</b> Publishing feature branches to GitHub enables team collaboration and automated pull-request validation."
    )
    story.append(create_callout(obs_text, styles, title="GIT VERSION CONTROL TAKEAWAYS"))
    return story

def build_q5_pdf():
    story = get_q5_story()
    pdf_path = build_pdf("Q5_Git_Version_Control_Setup.pdf", story)
    
    # Write Markdown version
    md_path = os.path.join(SUBMISSIONS_DIR, "Q5_Git_Version_Control_Setup.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(get_q5_markdown())
    print(f"Generated Markdown: {md_path}")
    return pdf_path

if __name__ == "__main__":
    build_q5_pdf()
