# Lab 3: Monitoring, Logging & DevSecOps - Terraform Provisioning
# Student: Manya Juneja | Roll No: 2301730142 | Email: manyajuneja03@gmail.com

terraform {
  required_version = ">= 1.6.0"
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

resource "docker_network" "lab" {
  name = "lab3-tf-network"
}

resource "docker_image" "app" {
  name = "lab3-demo-app:terraform"
  build { context = "${path.module}/../app" }
}

resource "docker_container" "app" {
  count = var.replicas
  name  = "lab3-demo-app-${count.index + 1}"
  image = docker_image.app.image_id

  networks_advanced { name = docker_network.lab.name }
  env = ["PORT=8080", "FEATURE_GREETING_V2=${var.feature_greeting_v2}"]

  ports {
    internal = 8080
    external = var.base_host_port + count.index
  }
}
