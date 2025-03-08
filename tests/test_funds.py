import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.mark.asyncio
async def test_get_all_funds(client):
    response = client.get("/funds/master")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_schemes_by_fund_house(client):
    response = client.get("/funds/schemes/UTI")
    assert response.status_code == 200
    assert isinstance(response.json(), list)