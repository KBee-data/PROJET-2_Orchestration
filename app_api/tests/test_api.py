from modules import connect   # Override get_engine BEFORE importing app
from main import app
from modules.base import Base
from modules.connect import get_db
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Create a test SQLite DB
SQLALCHEMY_DATABASE_URL = "sqlite:///app_api/data/test.db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_engine():
    return engine

connect.get_engine = override_get_engine


# Create tables in test DB
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


# Override DB dependency session
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

# Test client
# from fastapi.testclient import TestClient
client = TestClient(app)


def test_post_data():
    response = client.post("/data", json={"text": "hello"})
    assert response.status_code == 200


def test_get_data():
    response = client.get("/data")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
