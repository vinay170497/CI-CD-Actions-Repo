import requests
import logging
import os
import pytest

# Setup Logging for CI/CD Traceability
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

def call_ollama_api(api_key, base_url, model, prompt):
    # Ensure URL is exactly https://ollama.com
    endpoint = f"{base_url.rstrip('/')}/api/generate"
    
    # SYSTEM FIX: Ensure Bearer prefix is present for Cloud Auth
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model, 
        "prompt": prompt, 
        "stream": False
    }

    logger.info(f"Triggering Cloud Inference: {endpoint} | Model: {model}")
    return requests.post(endpoint, headers=headers, json=payload, timeout=45)

@pytest.fixture
def config():
    # Use environment variable first, fallback to hardcoded for local debug
    key = os.getenv("OLLAMA_API_KEY", "777a9000b48b485d8506faa0b1dbc276.zM3R7cEzYeMtDyFgF_BO6Qz-")
    return {
        "api_key": key,
        "base_url": "https://ollama.com",
        "model": "ministral-3:14b",
        "prompt": "Respond with 'Handshake OK'"
    }

def test_cloud_handshake(config):
    """Tier 1: Connection & Authentication Test"""
    response = call_ollama_api(**config)
    
    # If 401 occurs here, your key MUST be regenerated at ://ollama.com
    assert response.status_code == 200, f"Inference Failed! Status: {response.status_code} | Msg: {response.text}"
    
    data = response.json()
    assert "response" in data, "Cloud returned invalid JSON structure"
    logger.info(f"Cloud Response Verified: {data['response']}")

def test_unauthorized_access(config):
    """Tier 2: Security Validation Test"""
    response = call_ollama_api("invalid_key_test", config["base_url"], config["model"], "hi")
    assert response.status_code == 401
    logger.info("Security Check Passed: System rejected fake key.")
