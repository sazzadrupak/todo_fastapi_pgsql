"""
Test for the Application health check
"""

from fastapi.testclient import TestClient
from fastapi import status

from app.main import app

client = TestClient(app)


def test_return_health_check():
    """Test application health status"""
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'healthy'}
