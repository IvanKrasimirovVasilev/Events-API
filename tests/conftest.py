import pytest
from models import User
import uuid


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