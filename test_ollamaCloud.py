import requests
import logging
import os
import pytest

# Setup Logging for CI visibility
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

def call_ollama_api(api_key, base_url, model, prompt):
    # Sanitize URL to prevent the /api/api duplication error
    clean_url = f"{base_url.rstrip('/')}/api/generate"
    if "/api/api" in clean_url:
        clean_url = clean_url.replace("/api/api", "/api")

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"model": model, "prompt": prompt, "stream": False}

    logger.info(f"Connecting to: {clean_url}")
    return requests.post(clean_url, headers=headers, json=payload, timeout=30)

@pytest.fixture
def config():
    """Reads secrets from System Environment Variables (best practice for CI)"""
    return {
        "api_key": os.getenv("OLLAMA_API_KEY", "777a9000b48b485d8506faa0b1dbc276.zM3R7cEzYeMtDyFgF_BO6Qz-"),
        "base_url": "https://ollama.com",
        "model": "ministral-3:14b",
        "prompt": "Test: Respond with 'verified'"
    }

def test_cloud_handshake(config):
    """Verifies connection and auth logic."""
    response = call_ollama_api(**config)
    assert response.status_code == 200, f"Failed: {response.text}"
    assert "response" in response.json()
    logger.info("Assertion Success: Cloud handshake complete.")

def test_unauthorized_access(config):
    """Negative Test: Verifies system security handles bad keys."""
    response = call_ollama_api("invalid_key", config["base_url"], config["model"], "hi")
    assert response.status_code == 401
    logger.info("Assertion Success: Unauthorized access blocked.")
