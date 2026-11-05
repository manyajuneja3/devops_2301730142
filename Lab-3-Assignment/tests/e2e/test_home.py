"""
Lab 3: Monitoring, Logging & DevSecOps - Automated Selenium Tests
Student: Manya Juneja | Roll No: 2301730142 | Email: manyajuneja03@gmail.com
"""

import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def browser():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


def test_health_endpoint(browser):
    base_url = os.getenv("APP_URL", "http://localhost:8080")
    browser.get(f"{base_url}/health")
    assert '"healthy"' in browser.page_source


def test_feature_flag_response(browser):
    base_url = os.getenv("APP_URL", "http://localhost:8080")
    browser.get(base_url)
    assert "greeting_v2" in browser.page_source
