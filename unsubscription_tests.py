import pytest
import sys
sys.path.append("C:/CodeTru")
from fastapi.testclient import TestClient
from unsubscription_service.main import app
from unsubscription_service.database import Base, get_db
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import asyncio

# Setup Test DB
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Async engine for tests
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

# Sync engine for schema creation
sync_engine = create_engine(
    SQLALCHEMY_DATABASE_URL.replace("aiosqlite", "sqlite"), connect_args={"check_same_thread": False}
)

# Override get_db
async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Create the tables before tests
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=sync_engine)
    yield
    Base.metadata.drop_all(bind=sync_engine)

# Insert a test user
@pytest.fixture(scope="function", autouse=True)
async def insert_test_user():
    async with TestingSessionLocal() as session:
        from unsubscription_service.models import User
        test_user = User(
            username="test_user",
            email="test@example.com",
            reason="Testing",
            comments="Sample comment",
            is_active=True
        )
        session.add(test_user)
        await session.commit()

# Test for Unsubscribe API
def test_unsubscribe_success():
    response = client.post("/unsubscriptions/unsubscribe", json={"username": "test_user"})
    assert response.status_code in [200, 404]
    assert "message" in response.json()

def test_user_already_unsubscribed():
    response = client.post("/unsubscriptions/unsubscribe", json={"username": "test_user"})
    assert response.status_code in [200, 404]
    assert "message" in response.json()

# Test for Subscription API
def test_get_subscriptions():
    response = client.get("/subscriptions/list")
    assert response.status_code == 200
    assert "subscribed_users" in response.json()

def test_get_subscriptions_by_status():
    response = client.get("/subscriptions/list?is_active=true")
    assert response.status_code == 200
    assert "subscribed_users" in response.json()

    response = client.get("/subscriptions/list?is_active=false")
    assert response.status_code == 200
    assert "unsubscribed_users" in response.json()

# Test for Owner's View API
def test_get_unsubscriptions():
    response = client.get("/unsubscriptions/owner_view")
    assert response.status_code == 200
    assert "data" in response.json()

def test_filter_unsubscriptions_by_username():
    response = client.get("/unsubscriptions/owner_view?username=test_user")
    assert response.status_code == 200
    assert "data" in response.json()

def test_filter_unsubscriptions_by_email():
    response = client.get("/unsubscriptions/owner_view?email=test@example.com")
    assert response.status_code == 200
    assert "data" in response.json()

# # Test for Search API
# def test_search_subscriptions():
#     response = client.get("/search/subscriptions?username=test

