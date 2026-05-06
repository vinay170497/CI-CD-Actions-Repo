import playwright
import pytest

@pytest.fixture(scope="function")
def preWork():
    print("Initialization")
    return "pass"

def test_firstCheck(preWork):
    print("First test")
    assert preWork == "pass"

def test_SecondCheck(preSetupWork):
    print("Second Check")
