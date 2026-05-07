import requests
import logging
import os
import pytest
import time

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

def call_ollama_api(base_url, model, prompt):
    endpoint = f"{base_url.rstrip('/')}/api/generate"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": model, 
        "prompt": prompt, 
        "stream": False
    }
    
    logger.info(f"Checking Local Inference: {endpoint} | Model: {model}")
    start_time = time.time()
    response = requests.post(endpoint, headers=headers, json=payload, timeout=30)
    duration = time.time() - start_time
    
    return response, duration

@pytest.fixture
def config():
    return {
        "base_url": "http://localhost:11434",
        "model": "tinyllama:latest", # Lightweight choice for quick tests
        "prompt": "Say 'OK'"
    }

def test_ollama_service_online(config):
    """Check if the Ollama server is actually running"""
    try:
        response = requests.get(config["base_url"], timeout=20)
        assert response.status_code == 200
        logger.info("Ollama server is Online.")
    except requests.exceptions.ConnectionError:
        pytest.fail("Ollama server is not running! Start it with 'ollama serve'")

def test_local_handshake(config):
    """Verify inference works and returns valid JSON"""
    response, duration = call_ollama_api(
        config["base_url"], 
        config["model"], 
        config["prompt"]
    )
    
    # Assertions
    assert response.status_code == 200, f"API Failed with {response.status_code}"
    
    data = response.json()
    assert "response" in data, "Invalid JSON: Missing 'response' field"
    assert len(data["response"]) > 0, "Model returned an empty string"
    
    logger.info(f"Handshake Successful in {duration:.2f}s. Model said: {data['response'].strip()}")

def test_performance_benchmark(config):
    """Ensure the model responds within a reasonable time (under 5 seconds for TinyLlama)"""
    _, duration = call_ollama_api(config["base_url"], config["model"], "Short hello")
    assert duration < 5.0, f"Inference too slow: {duration:.2f}s"
    logger.info(f"Performance Check Passed: {duration:.2f}s")

def test_model_list_verification(config):
    """Check if the requested model is actually installed in Ollama"""
    response = requests.get(f"{config['base_url']}/api/tags")
    models = [m['name'] for m in response.json().get('models', [])]
    print(models)
    assert config["model"] in models, f"Model {config['model']} not found in local Ollama list!"
    logger.info(f"Model Verification Passed: {config['model']} is installed.")
