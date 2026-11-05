import unittest
import json
from app import app

class DevOpsAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page_status(self):
        """Test home page route returns HTTP 200 and expected title."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"DevOps Foundations CI/CD App", response.data)
        self.assertIn(b"Jenkins 2.450+ LTS", response.data)

    def test_health_endpoint(self):
        """Test health check API returns HTTP 200 and healthy status."""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "UP")
        self.assertTrue(data["healthy"])
        self.assertIn("uptime_seconds", data)
        self.assertIn("version", data)

    def test_metrics_endpoint(self):
        """Test metrics endpoint returns valid simulated metrics."""
        response = self.app.get('/metrics')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("cpu_usage_simulated", data)
        self.assertIn("memory_usage_mb", data)

    def test_api_info_endpoint(self):
        """Test project info metadata endpoint."""
        response = self.app.get('/api/info')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["lab"], "Lab 1")
        self.assertEqual(data["vcs"], "Git & GitHub")
        self.assertEqual(data["ci_cd_tool"], "Jenkins Declarative Pipeline")

if __name__ == '__main__':
    unittest.main()
