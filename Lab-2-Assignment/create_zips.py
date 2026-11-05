"""
Script to create individual ZIP packages for each question and master ZIP
"""

import os
import zipfile

base_dir = r"d:\Devops Lab 2"
sub_dir = os.path.join(base_dir, "submissions")
zip_dir = os.path.join(base_dir, "zip_submissions")

q_packages = {
    "Q1_Kubernetes_Deployment.zip": [
        ("submissions/Question_1_Kubernetes_Deployment_and_Service.pdf", "Question_1_Kubernetes_Deployment_and_Service.pdf"),
        ("src/k8s/deployment.yaml", "manifests/deployment.yaml"),
        ("src/k8s/service.yaml", "manifests/service.yaml"),
        ("src/k8s/configmap.yaml", "manifests/configmap.yaml")
    ],
    "Q2_Kubernetes_Strategies_Scaling.zip": [
        ("submissions/Question_2_Kubernetes_Rolling_Update_Rollback_Scaling.pdf", "Question_2_Kubernetes_Rolling_Update_Rollback_Scaling.pdf"),
        ("src/k8s/deployment.yaml", "manifests/deployment-v1.yaml"),
        ("src/k8s/deployment-v2.yaml", "manifests/deployment-v2.yaml"),
        ("src/k8s/deployment-broken.yaml", "manifests/deployment-broken.yaml")
    ],
    "Q3_Orchestration_Report.zip": [
        ("submissions/Question_3_Containerization_and_Orchestration_Report.pdf", "Question_3_Containerization_and_Orchestration_Report.pdf"),
        ("src/k8s/deployment.yaml", "k8s/deployment.yaml"),
        ("src/k8s/service.yaml", "k8s/service.yaml"),
        ("src/app/Dockerfile", "docker/Dockerfile")
    ],
    "Q4_Docker_Containerization.zip": [
        ("submissions/Question_4_Containerize_Application_Docker.pdf", "Question_4_Containerize_Application_Docker.pdf"),
        ("src/app/Dockerfile", "Dockerfile"),
        ("src/app/Dockerfile.simple", "Dockerfile.simple"),
        ("src/app/app.py", "app.py"),
        ("src/app/requirements.txt", "requirements.txt")
    ],
    "Q5_Docker_Management_Compose.zip": [
        ("submissions/Question_5_Manage_Docker_Containers_and_Compose.pdf", "Question_5_Manage_Docker_Containers_and_Compose.pdf"),
        ("src/compose/docker-compose.yml", "docker-compose.yml"),
        ("src/app/Dockerfile", "Dockerfile"),
        ("src/app/app.py", "app.py")
    ],
    "Q6_Docker_Storage.zip": [
        ("submissions/Question_6_Docker_Storage_Volumes_BindMounts.pdf", "Question_6_Docker_Storage_Volumes_BindMounts.pdf"),
        ("src/scripts/run_storage_demo.sh", "run_storage_demo.sh")
    ],
    "Q7_Docker_Network.zip": [
        ("submissions/Question_7_Docker_Network_Container_Communication.pdf", "Question_7_Docker_Network_Container_Communication.pdf"),
        ("src/scripts/run_network_demo.sh", "run_network_demo.sh")
    ],
    "Q8_Continuous_Deployment.zip": [
        ("submissions/Question_8_Continuous_Deployment_Kubernetes_CICD.pdf", "Question_8_Continuous_Deployment_Kubernetes_CICD.pdf"),
        ("src/cicd/.github/workflows/deploy.yml", ".github/workflows/deploy.yml"),
        ("src/k8s/kustomization.yaml", "k8s/kustomization.yaml"),
        ("src/k8s/deployment.yaml", "k8s/deployment.yaml"),
        ("src/k8s/service.yaml", "k8s/service.yaml")
    ],
    "Q9_All_Tools_Documentation.zip": [
        ("submissions/Question_9_Master_Tools_Manifests_Record_Book.pdf", "Question_9_Master_Tools_Manifests_Record_Book.pdf"),
        ("src/app/Dockerfile", "src/app/Dockerfile"),
        ("src/app/app.py", "src/app/app.py"),
        ("src/compose/docker-compose.yml", "src/compose/docker-compose.yml"),
        ("src/k8s/deployment.yaml", "src/k8s/deployment.yaml"),
        ("src/k8s/service.yaml", "src/k8s/service.yaml"),
        ("src/k8s/configmap.yaml", "src/k8s/configmap.yaml"),
        ("src/cicd/.github/workflows/deploy.yml", "src/cicd/deploy.yml")
    ]
}

for zip_name, files in q_packages.items():
    zip_path = os.path.join(zip_dir, zip_name)
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for rel_src, arcname in files:
            full_src = os.path.join(base_dir, rel_src.replace('/', os.sep))
            if os.path.exists(full_src):
                zf.write(full_src, arcname)
    print(f"[OK] Created package: {zip_path}")

# Create Master Complete Lab 2 Package
master_zip = os.path.join(zip_dir, "Complete_DevOps_Lab2_Package.zip")
with zipfile.ZipFile(master_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, filenames in os.walk(base_dir):
        # Skip zip_submissions to avoid recursion
        if "zip_submissions" in root:
            continue
        for f in filenames:
            full_path = os.path.join(root, f)
            arcname = os.path.relpath(full_path, base_dir)
            zf.write(full_path, arcname)
print(f"[OK] Created Master Archive: {master_zip}")

