import requests


def test_health_endpoint_returns_healthy(base_url):
    # Send a GET request to the health endpoint
    response = requests.get(f"{base_url}/api/health", timeout=5)

    # Check that the status code is 200
    assert response.status_code == 200

    # Check that the API reports a healthy status
    assert response.json()["status"] == "healthy"