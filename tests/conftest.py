import pytest
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