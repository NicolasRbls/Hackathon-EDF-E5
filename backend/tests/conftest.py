import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, get_db

# Use in-memory SQLite for tests (fast & isolated)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """Override the get_db dependency to use the test database."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

from app import models, security

@pytest.fixture(scope="function")
def admin_token(client, db_session):
    """Create a default admin and return auth headers."""
    # Ensure admin exists
    password = "admin_test_pw"
    hashed = security.get_password_hash(password)
    user = models.User(username="admin_test", password_hash=hashed, role=models.UserRole.ADMIN)
    db_session.add(user)
    db_session.commit()
    
    # Login
    response = client.post("/auth/login", data={"username": "admin_test", "password": password})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
