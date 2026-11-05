"""
Lab 3: Monitoring, Logging & DevSecOps - Locust Load Testing
Student: Manya Juneja | Roll No: 2301730142 | Email: manyajuneja03@gmail.com
"""

from locust import HttpUser, between, task


class DemoUser(HttpUser):
    wait_time = between(0.5, 1.5)

    @task(4)
    def homepage(self):
        self.client.get("/")

    @task(1)
    def status(self):
        self.client.get("/api/status")

    @task(1)
    def emit_log(self):
        self.client.get("/api/log-demo")
