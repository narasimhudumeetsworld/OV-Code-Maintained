"""Test configuration for pytest."""
import pytest


@pytest.fixture
def sample_python_code():
    """Sample Python code for testing."""
    return '''
def greet(name: str) -> str:
    """Greet a user by name."""
    return f"Hello, {name}!"

def process_data(data):
    password = "secret123"  # Bad practice
    return data
'''


@pytest.fixture
def sample_javascript_code():
    """Sample JavaScript code for testing."""
    return '''
function greet(name) {
    return `Hello, ${name}!`;
}

// Bad practice - innerHTML
element.innerHTML = userInput;
'''
