import requests
import logging
import sys
import pytest

# Configure logging for full traceability
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("OllamaCloudTest")

def call_ollama_api(api_key, base_url, model, prompt):
    """Execution function that communicates with the cloud."""
    url = f"{base_url.rstrip('/')}/api/generate"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {"model": model, "prompt": prompt, "stream": False}

    logger.info(f"Connecting to: {url} | Model: {model}")
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        logger.info(f"Received status code: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Network request failed: {e}")
        raise

# --- Pytest Infrastructure ---

@pytest.fixture
def valid_config():
    """Fixture containing your verified credentials."""
    return {
        "api_key": "777a9000b48b485d8506faa0b1dbc276.zM3R7cEzYeMtDyFgF_BO6Qz-",
        "base_url": "https://ollama.com/api",
        "model": "ministral-3:14b",  # Using a smaller model for faster CI tests
        "prompt": "Say 'System Online'"
    }

def test_connection_and_auth(valid_config):
    """Verifies that the API key and URL are accepted (200 OK)."""
    response = call_ollama_api(**valid_config)
    
    # Traceability: Log the raw response if failed for easier debugging
    assert response.status_code == 200, f"Auth failed! Status: {response.status_code}, Body: {response.text}"
    logger.info("Assertion Passed: Authentication and connection successful.")

def test_model_response_content(valid_config):
    """Verifies the LLM actually returns a non-empty string."""
    response = call_ollama_api(**valid_config)
    data = response.json()
    
    assert "response" in data, "Malformed JSON: 'response' key missing."
    assert len(data["response"]) > 0, "The model returned an empty string."
    logger.info(f"Assertion Passed: Model returned data: {data['response'][:20]}...")

def test_invalid_auth_handling():
    """Negative test: Ensures system correctly flags unauthorized access (401)."""
    logger.info("Running negative test for invalid API key...")
    response = call_ollama_api("bad_key", "https://ollama.com/api", "ministral-3:14b", "hi")
    
    assert response.status_code == 401, f"Expected 401, but got {response.status_code}"
    logger.info("Assertion Passed: System correctly rejected unauthorized request.")
