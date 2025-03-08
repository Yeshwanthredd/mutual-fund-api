import pytest
from fastapi.testclient import TestClient
from main import app
from database import Base, engine, SessionLocal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="module")
def test_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    app.dependency_overrides[lambda: next(get_db())] = override_get_db
    return TestClient(app)

@pytest.fixture
def auth_token(client):
    client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpassword123"}
    )
    response = client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "testpassword123"}
    )
    return response.json()["access_token"]

def test_create_portfolio(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post(
        "/portfolio/",
        json={"scheme_code": "120594", "units": 100.0, "purchase_price": 25.50},
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["scheme_code"] == "120594"

def test_get_portfolio(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    client.post(
        "/portfolio/",
        json={"scheme_code": "120594", "units": 100.0, "purchase_price": 25.50},
        headers=headers
    )
    response = client.get("/portfolio/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0