from fastapi.testclient import TestClient

from api import app

client = TestClient(app)


def test_main():
    response = client.get('/api/v1/ping')
    assert response.json() == {'msg': 'success', 'code': 200, 'data': 'pong'}