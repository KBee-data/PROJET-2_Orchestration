"""
Integration and Unit Tests for the FastAPI Service (app_api)
============================================================

This test suite verifies the behavior of the FastAPI application endpoints:
- GET / : Service health check
- POST /data : Ingestion and persistence of text data
- GET /data : Retrieval of all stored text records
- Negative tests : Validation errors on invalid payloads

Testing Architecture & Strategy:
--------------------------------
1. In-Memory SQLite (`sqlite:///:memory:`):
   - Runs strictly in RAM to eliminate disk I/O, speed up test runs, and prevent
     polluting the repository with generated SQLite database files.
2. StaticPool & Thread Safety:
   - By default, an in-memory SQLite database creates a brand-new, empty database
     instance for every new connection. FastAPI's TestClient processes requests across
     multiple threads. We use SQLAlchemy's `StaticPool` and `check_same_thread=False`
     to ensure all threads and database sessions interact with the same in-memory instance.
3. Hermetic Isolation (Setup/Teardown Fixture):
   - The `setup_and_teardown_db` fixture runs automatically around every single test.
     It creates fresh database tables before each test and drops them immediately after,
     preventing state leakage between individual test cases.
4. FastAPI Dependency Overrides:
   - Rather than connecting to PostgreSQL (production DB), FastAPI's `app.dependency_overrides`
     swaps the production `get_db` session provider with `override_get_db`, pointing cleanly
     to our isolated in-memory test engine.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from modules.base import Base
from modules.connect import get_db

# ---------------------------------------------------------------------------
# Test Database Engine & Session Factory Configuration
# ---------------------------------------------------------------------------

# Use an ephemeral in-memory SQLite URI
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Configure the SQLite engine with StaticPool so all connections share the same memory space
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create a scoped sessionmaker bound to our test engine
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ---------------------------------------------------------------------------
# Pytest Fixtures & Dependency Injection Overrides
# ---------------------------------------------------------------------------


@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown_db():
    """Manage database schema lifecycle per test function.

    Guarantees test hermeticity:
    - Pre-test: Creates all tables declared in SQLAlchemy Base metadata.
    - Post-test: Drops all tables so that subsequent tests start with a pristine state.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    """FastAPI dependency override for the database session.

    Yields:
        sqlalchemy.orm.Session: A session bound to the in-memory test database,
        guaranteeing safe closure upon request completion.
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Apply the dependency override on the FastAPI application instance
app.dependency_overrides[get_db] = override_get_db

# Initialize FastAPI's HTTP test client
client = TestClient(app)


# ---------------------------------------------------------------------------
# Test Cases
# ---------------------------------------------------------------------------


def test_health_check():
    """Verify that the root health check endpoint returns HTTP 200 OK.

    Test objective:
        Ensure the API service is operational and can respond to liveness probes.

    Expected:
        - HTTP Status: 200 OK
        - JSON Body: {"status": "ok"}
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_post_data():
    """Verify inserting valid text data via POST /data.

    Test objective:
        Ensure a valid JSON payload is accepted, parsed by Pydantic (TextRequest),
        committed into the database via CRUD helper, and returns a confirmation message.

    Input:
        - JSON: {"text": "hello"}

    Expected:
        - HTTP Status: 200 OK
        - JSON Body: {"message": "Text added"}
    """
    response = client.post("/data", json={"text": "hello"})
    assert response.status_code == 200
    assert response.json() == {"message": "Text added"}


def test_get_data():
    """Verify retrieving all stored text entries via GET /data.

    Test objective:
        Ensure that inserted records can be queried from the database, transformed
        into a DataFrame, serialized to records format, and returned as a JSON list.

    Procedure:
        1. Pre-insert a known record ("sample entry") via POST /data.
        2. Query GET /data.

    Expected:
        - HTTP Status: 200 OK
        - JSON Body: A list containing at least 1 record with id and text "sample entry".
    """
    # Step 1: Pre-populate with a known record
    client.post("/data", json={"text": "sample entry"})

    # Step 2: Fetch all records
    response = client.get("/data")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["text"] == "sample entry"
    assert "id" in data[0]


def test_post_data_invalid_payload():
    """Verify input validation behavior when an invalid payload is sent.

    Test objective:
        Ensure Pydantic's `min_length=1` rule on TextRequest rejects empty strings
        and triggers a 422 Unprocessable Entity HTTP error instead of accepting bad data.

    Input:
        - JSON: {"text": ""}

    Expected:
        - HTTP Status: 422 Unprocessable Entity
    """
    response = client.post("/data", json={"text": ""})
    assert response.status_code == 422


def test_lifespan(monkeypatch):
    """Verify FastAPI lifespan event initializes database tables using get_engine.

    Covers lines 24-26 in main.py.
    """
    monkeypatch.setattr("main.get_engine", lambda: engine)
    with TestClient(app) as test_client:
        response = test_client.get("/")
        assert response.status_code == 200


def test_post_data_database_error(monkeypatch):
    """Verify POST /data returns HTTP 500 when database insertion fails.

    Covers lines 45-46 in main.py.
    """

    def mock_input_data(db, text):
        raise RuntimeError("Database connection lost")

    monkeypatch.setattr("main.input_data", mock_input_data)
    response = client.post("/data", json={"text": "hello"})
    assert response.status_code == 500
    assert response.json()["detail"] == "Database error"


def test_get_data_database_error(monkeypatch):
    """Verify GET /data handles exceptions during read operations.

    Covers lines 58-60 in main.py.
    """

    def mock_read_db(db):
        raise RuntimeError("Failed to query records")

    monkeypatch.setattr("main.read_db", mock_read_db)
    with pytest.raises(RuntimeError):
        client.get("/data")

