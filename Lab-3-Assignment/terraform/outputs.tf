output "application_urls" {
  value = [for index in range(var.replicas) : "http://localhost:${var.base_host_port + index}"]
}
