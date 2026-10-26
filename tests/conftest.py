import pytest
import requests
import uuid

from models import User

@pytest.fixture
def base_url():
    # Return the API base URL
    return "http://localhost:5000"

@pytest.fixture
def user():
    # Create a test user
    return User(username="testuser")

@pytest.fixture
def password():
    # Return a test password
    return "MySecurePassword123"

@pytest.fixture
def registration_user():
    # Generate a unique username for each test
    return {
        "username": f"testuser_{uuid.uuid4().hex[:8]}",
        "password": "MySecurePassword123"
    }

@pytest.fixture
def registered_user(base_url, registration_user):
    # Register a new user through the API
    response = requests.post(
        f"{base_url}/api/auth/register",
        json=registration_user,
        timeout=5
    )

    # Verify successful registration
    assert response.status_code == 201

    # Return the registered user's credentials
    return registration_user